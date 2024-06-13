+++
title = "Generating a Kubernetes Secret manifest from 1Password"
draft = false
date = 2024-06-12

[taxonomies]
tags = ["kubernetes", "1password", "rust", "cli"]
categories = ["kubernetes", "devops"]
+++

When you manage your own Kubernetes cluster you will inevitably have to manage
some secrets, and if you manage it using GitOps practices you should know that
it's not a good idea to store your secrets in a git repository.

There are many different solutions to solve this problem, but a lot of them rely
on using some kind of third-party secrets management platform, which can come
with unexpected costs.

A simpler alternative is to use Bitnami's Sealed Secrets controller, which lets
you encrypt the secret in the git repository, and then the controller will
decrypt the secret inside the cluster.

This simplicity comes with a cost, as it becomes quite cumbersome to manage many
secrets since you need to store copies of the original unencrypted secrets
somewhere safe, and then you need to re-encrypt it every time you update a
value.

In this article I will introduce a small CLI tool to that alleviates some of
this by reading the secrets from 1Password.

<!-- more -->

## Introduction

I've made a new CLI tool called [`op2secret`][op2secret]. It's a simple CLI that
wraps the official 1Password CLI to read the fields of a secret and generate a
Kubernetes Secret manifest from them.

Since it generates a Secret manifest, it's possible to pipe it directly to
`kubeseal` which can then be redirected to a file.

## Requirements

The tool relies on the official [1Password CLI] to read from your vault, so that
will have to be installed and avilable in your `PATH`.

If the 1Password CLI executable is called something other than `op`, you can
tell `op2secret` which one to use with the `--op-bin` argument or the `OP_BIN`
environment variable.

[1Password CLI]: https://developer.1password.com/docs/cli/get-started/

## Installation

The simplest way to install it is to download the executable for your platform
to a location that is in your `$PATH`:

```sh
% sudo curl -L https://github.com/mkroman/op2secret/releases/download/v0.1.0-rc1/op2secret-x86_64-unknown-linux-musl \
    -o /usr/local/bin/op2secret
% sudo chmod a+x /usr/local/bin/op2secret
```
## Usage

### Generate a basic auth secret

To read an item from 1Password with the name `some-namespace/some-secret`, with
a username and password, and generate a secret with the type
`kubernetes.io/basic-auth`:

```sh
op2secret -t kubernetes.io/basic-auth some-namespace/some-secret
```

This will generate the following manifest:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: some-secret
  namespace: some-namespace
stringData:
  password: bar
  username: foo
type: kubernetes.io/basic-auth
```

### Generate a sealed secret

To generate a bitnami sealed secret manifest instead of a regular secret, we can
pipe the manifest directly to `kubeseal`:

```sh
op2secret -t kubernetes.io/basic-auth some-namespace/some-secret | kubeseal -o yaml
```

This will result in something similar to:

```
---
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  creationTimestamp: null
  name: some-secret
  namespace: some-namespace
spec:
  encryptedData:
    password: AgBVXNveLww8ZSL72V9Iwe3T8mDwERWRD/3fpKbhsyiBVMjqtqz3DGlGu6y1gE8KOObwXQ/xD6nfhs/Gc3sRtwftIjwkwOjV39WE0ACIBsGPpXrmGDqsCDpGl4WM/LxiXT1N7E/CZqcc5jrSBoto70bxkaeuSm8h+rYPSjkt4s6oHEJoESUsnBj1eewU5s0Lw2WfPGA6nciXA6SUp4hhqbFW0vQNLg/Apu47rxcR4Xqzn+1E2jgFK77adGvaOoU9SzYEmdunMH1gE9r4f/AqzzfSe4NpPRpKFlwKvLbv7u+7uOHQgV9zErME2OdHt031lwSWE8wkZEOT0Xke5E3wOCDtC8RfrspVtKRMik5i17oz2YvNpVzX8uqXT/PBv4G3pkPFMw+uOP9epxyLBobbC99A8Keq/Rhe4Spa9d6/gpHJe07g1rZSRqSb1v3+Ro75x1n/0rfxDfOcg1+sc1BWm5b15d9NsCqWWN4gxPBgas80dQndmqroPKZO4PgEKyxsmfdedA+WGZsy9ynAqMmyJi5MIhQb9a3vkNQoQ6/ttzMKc1aNjzdciJifzeYunhK29/eL1E9g0K56rOl2gzWenH25joTmKmC13UdiX9mlV38SmFScT4GMYBLR960WcM5Oys5aF6Ej1E18XEuUOXxwNJF5hCqysWxgKomNyg4DYwrZIEGScsj50R4GR3hwuBCjnwPs+2k=
    username: AgCGTB18VTunR67fyrtZAySnIgf0SXvd2qiWEXRHCEcSl91E1dZdiC820/GySlmHOV+JHNTRf5SrVVpXtp0IHdoIvo9tzV1zVnfdMwJCOmy3oC9PeJVmdFD7/bRa6+YBTyq0JYXarqLsc24AMOSuVbKbidvmbyAH/VNlOUvrQK1fdgYKS+CRbbhTjnHbhhTXAxVy6DJ4lZHXo6qbt//Iu19qz5NtmFWuuvxTB+lpRZJfjriljq9sCf/gAiLyhre/YC7IvBAIWfMzRosbTgbpqStxQSURkW/3Z+kH4UG9mqXMA8ubjTwN3t0H6iie2OOhPyWBl7YNX03PQX/XOh+aIA625hJPsOvTWoS/Vhw0bWpZiAiyA0djBnGjl7zGmLEllvuXguvxCY1Ebcof41eSNJz6AlbbpwNotQ/oD/omz3YdP9Fx3hgXRLZvSVwNV1UMFOJLm08oGWNFAa5Tl7/ZtYhqSNDldlPqO/aw41Rwm7ifr7JEdq7RO4ViFtqt1X6b73T/qfvuOj7NMEkDaVx16iuWapelGG5jmREXu/PT43ewxCt7l1JcZfUeaJ6cYvnk0CZNVNawYtbT9p9kInxCcjC3KtXNhaGZPfcG+PGHrnqIQcabKmNBNUsps5vWJeWCMZPp/HVwrU95I71pUlwL+R1xcQnemOS2zdgcf/7IbqBlcnMaqaVgY77aIvswekvHXP5bjDo=
  template:
    metadata:
      creationTimestamp: null
      name: some-secret
      namespace: some-namespace
    type: kubernetes.io/basic-auth
```

[op2secret]: https://github.com/mkroman/op2secret

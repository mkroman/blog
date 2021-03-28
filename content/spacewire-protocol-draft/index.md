+++
title = "Spacewire protocol draft"
date = 2021-03-18
draft = true

[taxonomies]
tags = ["spacewire", "protocol"]
categories = ["cryptography", "privacy"]
+++

This is an initial draft version of the protocol specification for [spacewire],
an end-to-end encrypted file-sharing library and CLI utillity, that utilizes
trustless relays to transfer data, inspired by [croc].

[croc]: https://github.com/schollz/croc
[spacewire]: https://github.com/mkroman/spacewire

<!-- more -->

# Introduction

Spacewire is a library-first, CLI-second end-to-end encrypted communication
protocol that attempts to make it easy to establish multiple communication
channels between two parties, using a single connection to an untrusted relay.

When Alice wants to send some arbitrary data to Bob, several problems can arise
when attempting to establish a direct connection between the two - including,
but not limited to: blocking firewalls, nat traversal, user is behind cgnat

Spacewire attempts to solve this by using a user-specified and untrusted
third-party relay, to which both Alice and Bob can connect and open multiple
communication channels, each secured by deriving shared ephemeral keys from a
session key that Alice shares with Bob out of bounds.

## Primitives

Spacewire only uses eliptic curve cryptography for the more efficient key size
and key generation. The chosen curve is `Curve25519`.

Key agreement is done using a slightly modified version of Signals [X3DH] key
agreement protocol, with the SHA-256 hash function and the `Curve25519` curve.

Once shared keys have been established, the two parties will create a channel on
the relay server and share messages encrypted and authenticated using
`AEAD_CHACHA20_POLY1305`.

[X3DH]: https://signal.org/docs/specifications/x3dh/

## Roles

## Encoding

For simplicity and efficiency, the protocol is binary-encoded using
network-endian data types.

### Packets

#### Encapsulation

Each packet is prefixed by a header that determines the type as well as the
length of the packet.

# Acknowledgements

This project is heavily inspired by the `wormhole` projects (webwormhole,
magic-wormhole, etc.) and [croc].

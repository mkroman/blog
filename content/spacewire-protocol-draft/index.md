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

## Packets

### Encapsulation

Each packet is prefixed by a header that determines the type as well as the
length of the packet.

### Format

#### SERVER_HELLO

The servers response to `CLIENT_HELLO`.

###### Fields

| Offset | Size (bytes) | Field            | Description                                       |
| ------ | ------------ | ---------------- | ------------------------------------------------- |
| 0x00   | 0x02         | protocol_version | The current protocol version                      |
| 0x02   | 0x100        | server_pk        | The servers public key                            |
| 0x102  | 0x20         | challenge        | A random 256-bit challenge for the client to sign |

#### CLIENT_HELLO

The first message that the client sends to the server upon connection, which includes the
protocol version.

#### Fields

| Offset   | Size (bytes) | Field            | Description                  |
| -------- | ------------ | ---------------- | ---------------------------- |
| 0x00     | 0x100        | client_pkey      | The clients public key       |
| 0x100    | 0x140?       | signed_prekey    | The clients signed prekey    |
| 0x240    | TBD          | prekey_signature | The clients prekey signature |

#### LINK_CREATE

##### Fields

No fields.

#### LINK_OPEN

The client wants the server to open a link between the current client and the client with
the given `client_key`

This is forwarded to the target client.

##### Fields

| Offset | Size (bytes) | Field       | Description                            |
| ------ | ------------ | ----------- | -------------------------------------- |
| 0x00   | 0x100        | target_pkey | The target clients public identity key |
| 0x100  | 0x20         | challenge   | Challenge for target_pkey to sign      |

#### LINK_CHALLENGE

The relay wants the client to authenticate a challenge with its public key.

##### Fields

| Offset | Size (bytes) | Field     | Description               |
| ------ | ------------ | --------- | ------------------------- |
| 0x00   | 0x20         | challenge | Challenge to authenticate |

#### LINK_CHALLENGE_RESPONSE

The signed response to a LINK_CHALLENGE.

##### Fields

| Offset | Size (bytes) | Field     | Description               |
| ------ | ------------ | --------- | ------------------------- |
| 0x00   | 0x20         | challenge | Challenge to authenticate |

#### LINK_ACK

The client acknowledges and agrees to open an encrypted channel

This is forwarded to the target client.

##### Fields

| Offset | Size (bytes) | Field               | Description                                                |
| ------ | ------------ | ------------------- | ---------------------------------------------------------- |
| 0x00   | 0x100        | target_pub_identity | The target clients public identity key                     |
| 0x100  | 0x110        | cipher_pub_key      | Authenticated ciphertext of the requesting clients pub key |

#### LINK_NACK

The client disagrees to open a link.

This is forwarded to the target client.

###### Fields

| Offset | Size (bytes) | Field               | Description                                                |
| ------ | ------------ | ------------------- | ---------------------------------------------------------- |
| 0x00   | 0x100        | target_pub_identity | The target clients public identity key                     |
| 0x100  | 0x110        | cipher_pub_key      | Authenticated ciphertext of the requesting clients pub key |

#### ALERT

# Acknowledgements

This project is heavily inspired by the `wormhole` projects (webwormhole,
magic-wormhole, etc.) and [croc].

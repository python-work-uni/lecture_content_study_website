# INFO3616 Week 8: Network Security Protocols — Exam Quick-Teach

> **Target Reading Time:** 7–9 minutes  
> **Source Material:** Week 8 Lecture Slides & Lecture Notes combined  
> **Course:** INFO3616 Cybersecurity Engineering, The University of Sydney  
> **Core Topics:** IPv4 Subnetting Mechanics, OAuth 2.0 vs OpenID Connect (OIDC), Transport Layer Security (TLS 1.2 vs TLS 1.3, Handshake flows, 0-RTT), IPsec Architecture (AH vs ESP, Transport Mode vs Tunnel Mode, SA, SAD, SPD, IKEv2).

---

## 1. Network Layer Foundations & Subnetting Mechanics

### IPv4 Address Classes (Rapid Recognition):
* **Class A:** `1.0.0.0` to `126.255.255.255` (Prefix bit `0`, default mask `/8`)
* **Class B:** `128.0.0.0` to `191.255.255.255` (Prefix bits `10`, default mask `/16`)
* **Class C:** `192.0.0.0` to `223.255.255.255` (Prefix bits `110`, default mask `/24`)

### Subnet Calculation Steps (Exam Favorite):
1. **Identify Network vs Host Bits:**
   * A subnet mask (e.g., `255.255.255.128`) has 25 network bits (`/25`) and $32 - 25 = 7$ host bits.
2. **Calculate Subnet Size:** Size $= 2^{\text{host bits}} = 2^7 = 128$ addresses per subnet.
3. **Determine Subnet Range:** Subnets increment by 128 in the final octet:
   * Subnet 1: `172.16.13.0` – `172.16.13.127`
   * Subnet 2: `172.16.13.128` – `172.16.13.255`
4. **Identify Addresses:**
   * **Subnet Address:** First address in range (all host bits 0) $\to$ `172.16.13.0`
   * **Broadcast Address:** Last address in range (all host bits 1) $\to$ `172.16.13.127`
   * **Usable Host Addresses:** $2^{\text{host bits}} - 2 = 128 - 2 = 126$ usable hosts.

---

## 2. Application Layer: OAuth 2.0 vs OpenID Connect (OIDC)

A classic exam conceptual trap is confusing OAuth with OpenID Connect:

| Feature | OAuth 2.0 | OpenID Connect (OIDC) |
| :--- | :--- | :--- |
| **Primary Purpose** | **AUTHORIZATION** (Delegated Access) | **AUTHENTICATION** (Identity Verification) |
| **Question Answered**| *"What resources is this client permitted to access?"* | *"Who is the user currently logged in?"* |
| **Core Artifact** | **`access_token`** (Opaque string or JWT for API endpoints) | **`id_token`** (Signed JWT containing user profile claims) |
| **Analogy** | A hotel keycard granting access to room 402 | A passport or driver's license proving your identity |
| **Relationship** | The underlying authorization framework | An identity layer built **on top of** OAuth 2.0 |

---

## 3. Transport Layer Security (TLS)

TLS sits between the Application Layer (HTTP) and Transport Layer (TCP) to provide end-to-end security.

### Architecture: The Four TLS Subprotocols:
1. **TLS Handshake Protocol:** Authenticates server (and optionally client), negotiates cipher suites, and establishes session keys.
2. **TLS Record Protocol:** Performs fragmentation, AEAD encryption, integrity check, and transmission of application data.
3. **TLS Alert Protocol:** Communicates session errors, closures, and security warnings.
4. **ChangeCipherSpec Protocol:** Signal to switch to negotiated cipher suites (deprecated/removed in TLS 1.3).

---

## 4. TLS 1.2 vs TLS 1.3: The Crucial Exam Comparison

TLS 1.3 represents a massive overhaul to eliminate latency and deprecated cryptographic flaws:

```
TLS 1.2 Handshake (2 Round Trips / 2-RTT):
Client                          Server
  | ------ ClientHello ----------> |  (Round Trip 1: Agree on ciphers)
  | <----- ServerHello, Cert ----- |
  | ------ Key Exchange ---------> |  (Round Trip 2: Exchange keys)
  | <----- Finished -------------- |
  | ====== Encrypted Data =======> |

TLS 1.3 Handshake (1 Round Trip / 1-RTT):
Client                          Server
  | -- ClientHello + Key Share --> |  (Round Trip 1: Combines cipher + key share!)
  | <-- ServerHello + Cert + Fin - |
  | ====== Encrypted Data =======> |
```

| Dimension | TLS 1.2 | TLS 1.3 |
| :--- | :--- | :--- |
| **Handshake Latency** | **2-RTT** (Two full round-trip times) | **1-RTT** (Client guesses curve and sends DH key share upfront) |
| **Session Resumption** | Session IDs / Session Tickets | **0-RTT Early Data** (Sends encrypted data on first flight using PSK) |
| **0-RTT Security Caveat** | N/A | **Vulnerable to Replay Attacks!** (Attacker can duplicate non-idempotent HTTP requests) |
| **Key Exchange** | RSA key transport OR static DH OR (EC)DHE | **(EC)DHE only** (Mandates **Perfect Forward Secrecy**) |
| **Static RSA Key Exchange**| Supported (leaked private key decrypts past traffic) | **Completely Removed** |
| **Symmetric Ciphers** | CBC mode, RC4, 3DES, standalone MACs | **AEAD only** (AES-GCM, AES-CCM, ChaCha20-Poly1305) |

---

## 5. Internet Layer Security: IPsec

IPsec operates at Layer 3 (Network Layer). It secures all IP traffic transparently without modifying user applications.

### A. The Two Core Protocols: AH vs ESP
1. **Authentication Header (AH - Protocol 51):**
   * Provides: **Data Integrity, Origin Authentication, Anti-Replay**.
   * **Does NOT provide confidentiality (No encryption)!** All data is in plain view.
   * Authenticates the **entire IP packet**, including the outer IP header (excluding mutable fields like TTL and header checksum).
2. **Encapsulating Security Payload (ESP - Protocol 50):**
   * Provides: **Confidentiality (Encryption)** + optional Data Integrity, Origin Authentication, and Anti-Replay.
   * Does **not** protect the outer IP header (outer IP header must remain readable by intermediate routers).

---

### B. Transport Mode vs Tunnel Mode

```
Original IP Packet:  [ IP Header ] [ TCP Header ] [ Payload ]

IPsec Transport Mode (Host-to-Host):
  AH:   [ IP Header ] [ AH Header ] [ TCP Header ] [ Payload ]
  ESP:  [ IP Header ] [ ESP Header ] [ TCP Header ] [ Payload (Encrypted) ] [ ESP Trailer/Auth ]

IPsec Tunnel Mode (Gateway-to-Gateway / VPN):
  AH:   [ NEW IP Header ] [ AH Header ] [ Original IP Header ] [ TCP Header ] [ Payload ]
  ESP:  [ NEW IP Header ] [ ESP Header ] [ Original IP Header | TCP Header | Payload (All Encrypted) ] [ ESP Trailer/Auth ]
```

* **Transport Mode:**
  * Protects only the transport-layer payload (TCP/UDP + data).
  * Original IP header remains visible.
  * Used for end-to-end communication between two cooperating end hosts.
* **Tunnel Mode:**
  * Encapsulates the **entire original IP packet** inside a brand-new IP packet with a new IP header.
  * Hides the original source and destination IP addresses (protects against traffic analysis).
  * Standard mode used for **Site-to-Site VPNs** and firewall/router gateways.

---

### C. IPsec Architecture & Core Databases

1. **Security Association (SA):**
   * A one-way (simplex) logical connection that specifies cryptographic algorithms, keys, and parameters.
   * **Exam Rule:** Because an SA is simplex, bidirectional communication between two hosts requires **at least two SAs**!
   * Uniquely identified by a **3-tuple:**
     $$\big(\text{SPI [Security Parameter Index]}, \;\text{Destination IP Address}, \;\text{Protocol [AH or ESP]}\big)$$
2. **Security Policy Database (SPD):**
   * A policy table inspected for every inbound and outbound packet. Specifies the action:
     * **DISCARD:** Drop the packet.
     * **BYPASS:** Allow the packet to travel in plaintext (no IPsec).
     * **PROTECT:** Enforce IPsec processing via an SA.
3. **Security Association Database (SAD):**
   * Stores the operational parameters for each active SA (encryption keys, authentication keys, sequence numbers, lifetime).
4. **IKEv2 (Internet Key Exchange v2):**
   * The automated control plane protocol that authenticates peers, runs Diffie-Hellman, and dynamically negotiates SAs and keys.

---

## 6. Exam Self-Check (Test Yourself)

1. **Given IP `172.16.13.5` with mask `255.255.255.128`, what is the broadcast address?**  
   *`172.16.13.127` (since the subnet range spans from `.0` to `.127`).*
2. **Why does TLS 1.3 completely remove RSA key exchange?**  
   *Because RSA key exchange lacks Perfect Forward Secrecy (PFS). If the server's private key is compromised years later, an attacker can decrypt all previously recorded sessions.*
3. **What is the security risk of TLS 1.3 0-RTT early data?**  
   *Early data is not protected against replay attacks. An eavesdropper can intercept and re-send the first flight to repeat an action (e.g., duplicate financial transactions).*
4. **Can IPsec AH operate through a NAT (Network Address Translation) router?**  
   *No. NAT modifies the IP header (changing the IP address and checksum), which breaks AH's integrity check because AH authenticates the outer IP header.*
5. **How many SAs are needed for secure bidirectional communication between two endpoints using ESP?**  
   *Two SAs (one for inbound traffic, one for outbound traffic).*

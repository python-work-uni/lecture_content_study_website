# INFO3616 Week 6: Hashes, MACs, & Digital Signatures — Exam Quick-Teach

> **Target Reading Time:** 6–8 minutes  
> **Source Material:** Week 6 Lecture Slides & Lecture Notes combined  
> **Course:** INFO3616 Cybersecurity Engineering, The University of Sydney  
> **Core Topics:** Cryptographic Hash Functions & 3 Security Properties, The Birthday Attack / Paradox, SHA-2 vs SHA-3, Message Authentication Codes (MACs & HMAC), Authenticated Encryption (AE & AEAD), Digital Signatures (RSA vs DSA).

---

## 1. Security Properties Cheat Sheet (Memorise for True/False & MCQs)

| Primitive | Confidentiality | Integrity | Origin Authentication | Non-Repudiation | Shared vs Asymmetric Key |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Hash Function** | ❌ | ✅ | ❌ | ❌ | None (Public mathematical function) |
| **MAC / HMAC** | ❌ | ✅ | ✅ | ❌ | Shared Symmetric Secret Key |
| **Digital Signature** | ❌ | ✅ | ✅ | ✅ | Asymmetric Key Pair (Sign with $SK$, Verify with $PK$) |
| **AEAD (e.g. AES-GCM)**| ✅ | ✅ | ✅ | ❌ | Shared Symmetric Secret Key |

* **Crucial Exam Rule:** A raw hash function provides **integrity only**. If an attacker alters the message in transit, they can simply recompute and replace the hash unless the hash is keyed (MAC) or digitally signed!

---

## 2. Cryptographic Hash Functions & The 3 Core Properties

A cryptographic hash function $h = H(M)$ maps arbitrary-length inputs $M$ to a fixed-size $n$-bit digest.

```
Arbitrary Length Message M ---> [ Hash Function H ] ---> Fixed Length Digest h (n bits)
```

### The Three Fundamental Security Requirements:
1. **Preimage Resistance (One-Way Property):**
   * *Definition:* Given an output hash value $h$, it is computationally infeasible to find *any* input $x$ such that $H(x) = h$.
   * *Brute-force cost:* **$2^n$** evaluations.
   * *Application:* Password storage (storing $H(\text{password})$ so the password cannot be reversed).
2. **Second Preimage Resistance (Weak Collision Resistance):**
   * *Definition:* Given a *specific input* $x$, it is computationally infeasible to find a *different input* $y \neq x$ such that $H(y) = H(x)$.
   * *Brute-force cost:* **$2^n$** evaluations.
   * *Application:* Document integrity (prevents an attacker from substituting an altered document for an existing one with the same hash).
3. **Collision Resistance (Strong Collision Resistance):**
   * *Definition:* It is computationally infeasible to find *any two arbitrary distinct inputs* $x \neq y$ such that $H(x) = H(y)$.
   * *Brute-force cost:* **$2^{n/2}$** evaluations (NOT $2^n$, due to the **Birthday Attack**!).

> **Hierarchy of Properties:**
> Collision Resistance implies Second Preimage Resistance. (If an attacker cannot find *any* collision, they certainly cannot find a collision matching a specific target $x$).

---

## 3. The Birthday Attack & The Birthday Paradox

Why is the cost of finding a collision only $2^{n/2}$ instead of $2^n$?
* **The Birthday Paradox:** In a room of just **23 people**, the probability that at least two people share the same birthday exceeds **50%**, even though there are 365 possible days in a year!
* **Generalised Mathematical Principle:** If we select $k$ random items from a space of size $N$, the probability of at least one collision reaches $\approx 50\%$ when:
  $$k \approx 1.177 \sqrt{N} \approx \sqrt{N} = \sqrt{2^n} = 2^{n/2}$$
* **Exam Implication:**
  * For an $n$-bit hash function, finding *any* collision requires only **$2^{n/2}$ attempts**.
  * A 128-bit hash function (like MD5) provides only $2^{64}$ operations of collision resistance — well within reach of modern compute!
  * **Rule:** To achieve an $m$-bit security level against collision attacks, the hash output length $n$ must be at least **$2m$ bits** (e.g., a 256-bit hash like SHA-256 provides 128-bit collision security).

---

## 4. Hash Architectures: SHA-2 vs SHA-3

* **SHA-2 (SHA-256, SHA-512):**
  * Built on the **Merkle-Damgård construction** (splits message into 512-bit or 1024-bit blocks and iterates a compression function).
  * *Vulnerability:* Susceptible to **Length Extension Attacks** (given $H(M)$ and the length of $M$, an attacker can compute $H(M \parallel \text{extension})$ without knowing $M$).
* **SHA-3 (Keccak):**
  * Built on the **Sponge Construction** (uses state permutations with two phases: **Absorbing** message blocks into state, then **Squeezing** output bits out).
  * Fundamentally different design; **immune to length-extension attacks**.

---

## 5. Message Authentication Codes (MAC) & HMAC

* **What is a MAC?** A keyed cryptographic checksum: $T = \text{MAC}(K, M)$.
  * Alice and Bob share a secret key $K$.
  * Alice sends $(M, T)$. Bob computes $\text{MAC}(K, M)$ and verifies it matches $T$.
  * Ensures **Integrity** (message not altered) and **Authenticity** (only someone with $K$ could generate $T$).
  * Does **NOT** provide Non-Repudiation: Bob could fabricate $T$ because Bob also knows key $K$.

### HMAC (Hash-Based MAC)
Why not simply calculate $H(K \parallel M)$? Because Merkle-Damgård hashes are vulnerable to length extension!
HMAC solves this with a **nested double-hash structure**:
$$\text{HMAC}(K, M) = H\Big((K^+ \oplus \text{opad}) \;\parallel\; H((K^+ \oplus \text{ipad}) \;\parallel\; M)\Big)$$

* $K^+$ is key $K$ padded with zeros to match the hash block size (e.g., 512 bits).
* $\text{ipad} = 0x36$ repeated (inner pad).
* $\text{opad} = 0x5C$ repeated (outer pad).
* **Why it works:** The inner hash digests the secret key and the message; the outer hash digests the outer key and the inner hash result. This nested construction mathematically prevents length-extension attacks.

---

## 6. Authenticated Encryption (AE) & AEAD

To achieve both **Confidentiality** (encryption $E$) and **Integrity/Authenticity** (MAC), three composition paradigms exist:

1. **Encrypt-then-MAC (EtM):**
   $$C = E_{K_1}(M), \quad T = \text{MAC}_{K_2}(C)$$
   * Compute ciphertext first, then compute MAC over the ciphertext.
   * **The Gold Standard (Most Secure):** Adopted in TLS 1.3 and IPsec. The receiver verifies $T$ before decrypting, completely eliminating decryption/padding oracle attacks!
2. **MAC-then-Encrypt (MtE):**
   $$T = \text{MAC}_{K_2}(M), \quad C = E_{K_1}(M \parallel T)$$
   * Legacy approach used in SSL / TLS $\le 1.2$.
   * Vulnerable to padding oracle attacks (e.g., POODLE, Lucky 13) because the recipient must decrypt before verifying the MAC.
3. **Encrypt-and-MAC (E&M):**
   $$C = E_{K_1}(M), \quad T = \text{MAC}_{K_2}(M)$$
   * Used in SSH. The MAC is computed directly over plaintext, which can leak information about the message if the MAC is deterministic.

### AEAD (Authenticated Encryption with Associated Data)
Modern protocols require sending unencrypted metadata (e.g., packet headers, sequence numbers, IP addresses) alongside encrypted payloads.
* AEAD encrypts the plaintext payload while generating a single tag $T$ that authenticates **both** the ciphertext and the cleartext associated data (AD).
* **Industry Standard:** **AES-GCM (Galois/Counter Mode)** — highly efficient, parallelizable block cipher mode combining CTR encryption with Galois field polynomial authentication.

---

## 7. Digital Signatures: RSA vs DSA

A digital signature provides **Authenticity, Integrity, and Non-Repudiation** using asymmetric cryptography.

### The General Scheme:
1. Sender digests message: $h = H(M)$.
2. Sender encrypts/signs $h$ using their **Private Key ($SK$)**: $S = \text{Sign}_{SK}(h)$.
3. Sender transmits $(M, S)$.
4. Anyone verifies by computing $H(M)$ and checking it against $\text{Verify}_{PK}(S)$ using sender's **Public Key ($PK$)**.

### Two Core Implementations:
1. **RSA Signatures:**
   * Signature generation: $S \equiv (H(M))^d \pmod n$.
   * Signature verification: Verify that $S^e \equiv H(M) \pmod n$.
   * RSA can do both encryption and signing.
2. **DSA (Digital Signature Algorithm / DSS):**
   * Based on the **Discrete Logarithm Problem** (and Schnorr signatures).
   * Generates a signature pair $(r, s)$ using an ephemeral per-signature random value $k$.
   * **Crucial Distinction:** DSA is strictly designed for **signatures only** — it *cannot* be used for message encryption!

---

## 8. Exam Self-Check (Test Yourself)

1. **Why does an attacker looking for *any* collision need only $\approx 2^{128}$ attempts for SHA-256?**  
   *Because of the Birthday Paradox: finding any two messages with matching hashes requires $\mathcal{O}(2^{n/2}) = 2^{256/2} = 2^{128}$ evaluations.*
2. **Can a MAC provide non-repudiation? Why or why not?**  
   *No. A MAC relies on a shared symmetric secret key known to both sender and receiver. The receiver could have forged the tag themselves.*
3. **Why is Encrypt-then-MAC (EtM) superior to MAC-then-Encrypt (MtE)?**  
   *EtM allows the recipient to authenticate the ciphertext before decrypting, preventing padding oracle attacks and processing of malicious ciphertexts.*
4. **Why is signing $H(M)$ preferable to signing $M$ directly?**  
   *Efficiency (hashes are small and fixed-length) and security (prevents mathematical/homomorphic manipulation of plaintext blocks).*

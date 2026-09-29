# INFO3616 Week 5: Asymmetric Cryptography — Exam Quick-Teach

> **Target Reading Time:** 6–8 minutes  
> **Source Material:** Week 5 Lecture Slides & Lecture Notes combined  
> **Course:** INFO3616 Cybersecurity Engineering, The University of Sydney  
> **Core Topics:** Public-Key Cryptosystems, RSA Key Derivation & Mathematics, Attacks on RSA & Padding (OAEP), Diffie-Hellman Key Exchange, Person-in-the-Middle Attacks, Hybrid Encryption. *(Note: Elliptic Curve arithmetic is non-examinable).*

---

## 1. Why Asymmetric Cryptography? (The Motivation)

In **symmetric cryptography**, $N$ users who wish to communicate securely pairwise require $\frac{N(N-1)}{2}$ shared secret keys. Moreover, symmetric crypto requires a secure out-of-band channel to distribute the secret key before communication begins.

**Asymmetric (Public-Key) Cryptography** solves this:
* Each entity creates a **key pair**:
  * **Public Key ($PK$):** Distributed openly to anyone.
  * **Private Key ($SK$):** Kept strictly confidential by the owner.
* For $N$ users, only **$2N$ keys** are needed in total.
* **Encryption use case:** Anyone encrypts with the recipient's $PK$; only the recipient can decrypt with their $SK$.
* **Signature use case:** Sender signs with their $SK$; anyone can verify with the sender's $PK$.

---

## 2. One-Way Functions & Trapdoors

At the heart of asymmetric cryptography is the **Trapdoor One-Way Function**:
* **One-Way Function $y = f(x)$:** Easy to compute in the forward direction for any $x$, but computationally infeasible to invert ($x = f^{-1}(y)$) given only $y$.
* **Trapdoor:** A special piece of secret information $K$. Without $K$, inverting $f(y)$ is computationally infeasible. With $K$, inverting $f(y)$ becomes fast and trivial:
  $$x = g(y, K)$$

### The Two Classic Mathematical Trapdoors:
1. **Integer Factorisation / RSA Problem:**
   * Multiplying two large prime numbers $p \times q = n$ is computationally trivial ($\mathcal{O}(\text{bits}^2)$).
   * Finding $p$ and $q$ given only the composite modulus $n$ is computationally intractable for sufficiently large keys ($\ge 2048$ bits).
2. **Discrete Logarithm Problem (DLP):**
   * Given base $g$, prime $p$, and exponent $x$, calculating $y \equiv g^x \pmod p$ via modular exponentiation is fast ($\mathcal{O}(\log x)$).
   * Given $g, p$, and $y$, finding the exponent $x$ such that $y \equiv g^x \pmod p$ is computationally infeasible for large $p$.

---

## 3. Mathematical Foundations: Totient & Euler's Theorem

* **Coprime:** Integers $a$ and $b$ are coprime if their greatest common divisor $\gcd(a, b) = 1$.
* **Euler's Totient Function $\phi(n)$:** The number of positive integers less than $n$ that are coprime to $n$.
  * If $p$ is prime: $\phi(p) = p - 1$.
  * Since $\phi$ is multiplicative for coprime factors: for $n = p \cdot q$ (where $p$ and $q$ are distinct primes):
    $$\phi(n) = (p - 1)(q - 1)$$
* **Euler's Theorem:** If $\gcd(a, n) = 1$, then:
  $$a^{\phi(n)} \equiv 1 \pmod n$$
  * *Corollary:* $a^{k \cdot \phi(n) + 1} \equiv a \pmod n$. This corollary is the exact mathematical reason why RSA decryption works!

---

## 4. RSA Algorithm: Step-by-Step Mechanics

### A. Key Generation (Must Know for Calculation Questions)
1. **Select two large distinct primes:** $p$ and $q$.
2. **Compute modulus:** $n = p \cdot q$.
3. **Compute totient:** $\phi(n) = (p - 1)(q - 1)$.
4. **Choose public exponent $e$:** Select $e$ such that $1 < e < \phi(n)$ and $\gcd(e, \phi(n)) = 1$. *(In practice, $e = 65537 = 2^{16} + 1$ is standard).*
5. **Compute private exponent $d$:** Solve the modular multiplicative inverse:
   $$e \cdot d \equiv 1 \pmod{\phi(n)} \iff d \equiv e^{-1} \pmod{\phi(n)}$$
   *(Computed using the Extended Euclidean Algorithm).*
6. **Output Keys:**
   * **Public Key:** $(e, n)$
   * **Private Key:** $(d, n)$ *(or $(d, p, q)$)*

### B. Encryption and Decryption
* **Plaintext Message:** Represented as an integer $M$ where $0 \le M < n$.
* **Encryption (Sender uses recipient's Public Key):**
  $$C \equiv M^e \pmod n$$
* **Decryption (Recipient uses their Private Key):**
  $$M \equiv C^d \pmod n$$

### C. Worked Mini-Example (Toy Numbers)
* Pick $p = 11$, $q = 17$.
* Modulus: $n = 11 \times 17 = 187$.
* Totient: $\phi(n) = (11 - 1)(17 - 1) = 10 \times 16 = 160$.
* Choose $e = 7$ (check: $\gcd(7, 160) = 1$).
* Find $d$: $7d \equiv 1 \pmod{160} \implies 7 \times 23 = 161 = 1 \times 160 + 1 \implies d = 23$.
* Encrypt $M = 88$:
  $$C \equiv 88^7 \pmod{187} = 11$$
* Decrypt $C = 11$:
  $$M \equiv 11^{23} \pmod{187} = 88$$

---

## 5. Critical Vulnerabilities of "Textbook" RSA & Why Padding is Mandatory

"Textbook" (unpadded) RSA is mathematically elegant but **completely insecure in practice**:

1. **Deterministic Encryption (No Semantic Security / IND-CPA):**
   * If an attacker knows the plaintext is either "YES" or "NO", they encrypt both with the public key $e$ and compare the result to ciphertext $C$.
2. **Malleability (Homomorphic Property):**
   * Multiplying two ciphertexts multiplies the underlying plaintexts:
     $$C_1 \cdot C_2 \equiv (M_1)^e \cdot (M_2)^e \equiv (M_1 \cdot M_2)^e \pmod n$$
   * An active attacker can manipulate ciphertext without decrypting it.
3. **Small Message / Small Exponent Attacks:**
   * If $M^e < n$ (e.g., $e=3$ and $M$ is small), $C = M^3$ over standard integers, so $M = \sqrt[3]{C}$ without using modulo arithmetic at all!
4. **Poor Prime Selection Pitfalls:**
   * If $p$ and $q$ are chosen too close to each other ($p \approx q \approx \sqrt{n}$), Fermat's factorisation method can factor $n$ in a few iterations.
   * If private exponent $d$ is too small ($d < \frac{1}{3}n^{1/4}$), Wiener's attack factors $n$.
   * Modern requirement: Key size must be $\ge 2048$ bits.

### The Fix: OAEP (Optimal Asymmetric Encryption Padding)
To achieve **semantic security** (indistinguishability under chosen-ciphertext attack, IND-CCA2), RSA is never used raw. It must use **OAEP**:
* Injects random padding bytes into the plaintext block prior to exponentiation.
* Ensures that encrypting the exact same message twice produces completely different ciphertexts.
* Destroys the algebraic multiplicative structure, stopping malleability.

---

## 6. Diffie-Hellman (DH) Key Exchange

Diffie-Hellman allows two parties to establish a **shared symmetric secret key** over an unencrypted, public channel without transmitting the secret itself.

### The Protocol Flow:
1. **Public Setup:** A large prime $p$ and a primitive root (generator) $g$ modulo $p$.
2. **Alice's Move:**
   * Picks a secret random integer $a$ ($1 < a < p$).
   * Computes public value $A = g^a \pmod p$.
   * Sends $A$ across the network to Bob.
3. **Bob's Move:**
   * Picks a secret random integer $b$ ($1 < b < p$).
   * Computes public value $B = g^b \pmod p$.
   * Sends $B$ across the network to Alice.
4. **Key Derivation:**
   * Alice computes: $K = B^a \pmod p = (g^b)^a \pmod p = g^{ab} \pmod p$.
   * Bob computes: $K = A^b \pmod p = (g^a)^b \pmod p = g^{ab} \pmod p$.
   * Both now share $K = g^{ab} \pmod p$.

### The Fatal Flaw: Person-in-the-Middle (PitM) Attack
* Vanilla Diffie-Hellman provides **no authentication of the endpoints**.
* An attacker (Mallory) intercepts Alice's public value $A$ and sends her $g^m$; intercepts Bob's public value $B$ and sends him $g^m$.
* Mallory establishes shared secret $K_1 = g^{am}$ with Alice and $K_2 = g^{bm}$ with Bob.
* Mallory decrypts, reads, alters, and re-encrypts all communications transparently.
* **The Defense:** Authenticate the public values using **Digital Signatures / Public-Key Certificates (PKI)**.

---

## 7. Hybrid Encryption (Putting It Together)

* **Problem:** Asymmetric operations (modular exponentiation of 2048-bit numbers) are ~1000× slower than symmetric algorithms (like AES).
* **Practical Architecture:**
  1. Generate a temporary, random symmetric **session key** $K_{\text{session}}$ (e.g., 256-bit AES key).
  2. Encrypt the large message payload using $K_{\text{session}}$ with AES-GCM (fast bulk encryption).
  3. Encrypt $K_{\text{session}}$ using the recipient's asymmetric public key (RSA-OAEP) or derive it via Diffie-Hellman (ECDHE).
  4. Transmit both the encrypted session key and the ciphertext payload.

---

## 8. Exam Self-Check (Test Yourself)

1. **Why does Euler's theorem guarantee $M^{ed} \equiv M \pmod n$?**  
   *Because $ed = 1 + k\phi(n)$, so $M^{ed} = M \cdot (M^{\phi(n)})^k \equiv M \cdot (1)^k = M \pmod n$.*
2. **Can RSA encrypt a message $M$ where $M \ge n$?**  
   *No. Plaintext values must strictly lie in the interval $0 \le M < n$. Larger messages must be chunked or handled via hybrid encryption.*
3. **What is the primary difference between Diffie-Hellman and RSA?**  
   *Diffie-Hellman is strictly a key exchange/agreement protocol (cannot directly encrypt arbitrary data); RSA can perform both encryption and digital signatures.*
4. **Why is padding (OAEP) required for RSA?**  
   *To provide semantic security (preventing dictionary/guessing attacks on deterministic ciphertexts) and prevent homomorphic malleability.*

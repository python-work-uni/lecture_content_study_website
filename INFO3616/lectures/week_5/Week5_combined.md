# Week 5 — Asymmetric Cryptography

**INFO3616 Cybersecurity Engineering — Lecture Notes & Slides**

Recommended Reading: *Cryptography and Network Security* (7th Edition — William Stallings)
- **Chapter 9** – Public-key Cryptography and RSA
- **Chapter 10** – Other Public-key Cryptosystems

These notes are provided to assist with understanding the lecture content. This material is prepared based on the above book chapters. You are not allowed to upload this material to any internet source or share it with anyone else.

## Agenda

- Asymmetric/Public-key cryptography
- Key exchange
- Elliptic curve arithmetic and elliptic curve cryptography (ECC) — *Non-Examinable (for information only)*

---

# 1 Asymmetric / Public-key Cryptography

Symmetric cryptography uses the same shared key for both encryption and decryption, relying on substitution (confusion) and permutation (diffusion) to scramble messages and secure data. In contrast, public-key cryptography is a change of paradigm in two respects:

- Each participant has a **public key** (publicly distributed) and a **private key** (kept secret). Anyone may use the receiver's public key to encrypt a message, but only the receiver (owner of the private key) can decrypt it. Hence it is also known as **asymmetric cryptography**.
- It utilizes two distinct keys for encryption and decryption, relying on mathematical functions with specific properties beyond substitution and permutation.

Asymmetric algorithms have the following important characteristics:

- It is computationally infeasible to determine the decryption key given only knowledge of the cryptographic algorithm and the encryption key.
- In some algorithms like RSA, from a mathematical point of view, either of the two related keys can be used for encryption while the other can be used for decryption.
- This form of cryptography is based on mathematical problems with certain properties. A number of mathematical problems are *believed* to have the desired properties — **but there is no proof yet!**

## 1.1 Public-key Cryptosystems

The essential steps of using public-key cryptography are as follows:

1. Each user gets a pair of keys (private key and public key).
2. Each user places one key (public key) as a publicly accessible file. The companion key (private key) is kept confidential.
3. **Confidentiality** — If Bob wishes to send a confidential message to Alice, Bob encrypts the message with Alice's public key before sending it, and upon receiving the message, Alice decrypts it using her private key (Figure 1a). Since only Alice has access to her private key, only Alice can decrypt this message; therefore, confidentiality is achieved.
4. **Origin Authentication** — If Bob wants to send a message to Alice guaranteeing that the message was sent by him, Bob encrypts the message with his own private key (Figure 1b). Upon receiving the message, Alice can decrypt it using Bob's public key. **Digital signatures**, a key application of public-key cryptography, follow this approach. In this case, not only Alice but anyone who has access to Bob's public key can verify the origin of the message.

> **Summary**
> - **Confidentiality** — Encrypt by the public key and decrypt by the private key. Anyone can encrypt, but only the receiver can decrypt, because only they have the private key.
> - **Origin Authentication** — Encrypt by the private key and decrypt by the public key. Anyone can decrypt, but only the receiver could have encrypted it, because only they have the private key.

It is important to note that we refer to the conceptual usage of keys here in the confidentiality and origin authentication settings. In practice, we don't simultaneously use the same key pair for both purposes.

Overall, in public key cryptography, all participants in the system have access to all other participants' public keys, while each participant keeps the private keys confidential. Table 1 summarizes the applications of public-key cryptosystems.

|**Algorithm**|**Encryption/Decryption**|**Digital Signature**|**Key Exchange**|
|---|---|---|---|
|RSA|Yes|Yes|Yes|
|Elliptic Curve|Yes|Yes|Yes|
|Diffie-Hellman|No|No|Yes|
|DSS|No|Yes|No|

*Table 1: Applications for Public-key Cryptosystems*

We will discuss RSA, Diffie-Hellman, Elliptic Curve and Digital Signature Schemes (DSS).

## 1.2 Requirements for Public-key Cryptography

Following conditions that should be met by algorithms that can be used in public-key cryptography:

1. It is computationally easy for a party **B** to generate a key pair (public key *PUb*, private key *PRb*).
2. It is computationally easy for a sender **A**, knowing the public key and the message to be encrypted *M*, to generate the corresponding ciphertext:
   - *C* = *E*(*PUb*, *M*)
3. It is computationally easy for the receiver **B** to decrypt the resulting ciphertext using the private key to recover the original message:
   - *M* = *D*(*PRb*, *C*) = *D*[*PRb*, *E*(*PUb*, *M*)]
4. It is computationally infeasible for an adversary who knows the public key, *PUb*, to determine the private key, *PRb*.
5. It is computationally infeasible for an adversary who knows the public key, *PUb*, and a ciphertext, *C*, to recover the original message *M*, without knowing the private key *PRb*.

We may introduce a sixth requirement, which, while beneficial, may not be essential for all public-key applications:

6. The two keys can be applied in either order.

The above requirements can be aggregated to the requirement of a **trap-door one-way function**.

## 1.3 Trapdoor Properties

We are looking for a function with the following properties:

- **Computationally fast** to compute the function value *f(x) = y*
- **Computationally infeasible** to compute the inverse function *f⁻¹(y) = x*
- **Unless** we are in possession of a piece of information (the "trapdoor") that allows us to speed it up dramatically — hence the name "*trapdoor function*".

> **Corollary:** It must be **computationally infeasible** to compute the private key from the public key (without the trapdoor information).

**One-way function**: A function that maps a domain into a range such that every function value has a unique inverse, with the condition that the calculation of the function is easy, whereas the calculation of the inverse is infeasible:

- *Y* = *f*(*X*) → Easy

**Trap-door one-way function**: A function that is relatively easy to compute in one direction but computationally difficult to invert without the knowledge of additional information called the "*trapdoor*".

- *Y* = *fk*(*X*) → Easy if *k* and *X* are known
- *X* = *fk⁻¹*(*Y*) → Easy if *k* and *Y* are known
- *X* = *fk⁻¹*(*Y*) → Infeasible if *k* is unknown

## 1.4 Classic Trapdoor Candidate Problems

### 1.4.1 Discrete Logarithms in Modular Arithmetic

It is computationally infeasible to compute the discrete logarithm modulo *p* for certain *p*. (Diffie and Hellman, 1976)

**Discrete Logarithm Problem (DLP):** Given *y*, *p*, *g* satisfying the equation *y* = *g*ˣ mod *p*, where *p* is a prime number and *g* is a primitive root of *p*, how can we find *x*?

### 1.4.2 RSA Problem

It is computationally impossible to compute the *eᵗʰ* root of an integer modulo *n*, for certain *n*.

**RSA Problem:** When *c* = *mᵉ* mod *n* and *c*, *e*, and *n* are known, can you find *m*?

Both the Discrete Logarithm problem and the RSA problem have the property that 'computationally infeasible' becomes 'easy to compute' with additional information (i.e., the private key).

## 1.5 Recap: Coprime Numbers & Euler's Phi Function

- We say two numbers are **coprime** if they share only one divisor, and that divisor is 1.
  - Example: 8 and 27 are coprime: 8 = 2·2·2, and 27 = 3·3·3.
- We define **ℤ\*ₙ** as all non-negative integers < *n* that are coprime to the integer *n*.
  - Example: *n* = 12. Then, ℤ\*₁₂ = {1, 5, 7, 11}.
- ℤ\*ₙ is useful: it is an Abelian group under multiplication. **Euler's Phi Function** (also called the totient function) defines the number of elements in ℤ\*ₙ.
  - For example, ɸ(12) = 4.
- When *n* is a product of two primes *p* and *q* where *p* ≠ *q*, there is an easier way to calculate ɸ(*n*):
  - In that case ɸ(*n*) = (*p* − 1)(*q* − 1).

---

# 2 RSA Algorithm

The Rivest-Shamir-Adleman (RSA) scheme was developed by Ron Rivest, Adi Shamir, and Len Adleman at MIT in 1977 and is the most widely accepted and implemented general-purpose approach to public-key encryption. RSA is defined for a particular class of functions and allows us to build a trapdoor function. RSA encrypts plaintext in blocks, with each block having a binary value less than some number *n*.

## 2.1 RSA Key Derivation and Encryption/Decryption

RSA algorithm generates keys (values of *e*, *d*, and *n*) as follows. In practice, we use **very** large numbers.

1. Let *p* and *q*, *p* ≠ *q*, be prime.
2. Define *n* = *p* · *q* (we call *n* the modulus).
3. Use Euler's totient function to calculate ɸ(*n*) = (*p* − 1)(*q* − 1).
4. Choose 1 < *e* < ɸ(*n*), gcd(*e*, ɸ(*n*)) = 1 — i.e., *e* is coprime with ɸ(*n*). One way: choose *e* > max(*p*, *q*) to be prime. Testing primality of an integer is fast.
5. Calculate *d* such that *d* ≡ *e*⁻¹ mod ɸ(*n*) — i.e., *d* is the modular inverse of *e*.
6. Now we have the keys:
   - (*e*, *n*) is the **public key**
   - (*d*, *n*) is the **private key**
   - At this point we delete *p*, *q*, and ɸ(*n*) permanently.
7. **Encryption:** *c* = *mᵉ* mod *n*
8. **Decryption:** *m* = *cᵈ* mod *n*

*Note: in the above key generation process, ɸ(x) denotes Euler's phi function that counts elements in ℤ\*ₙ.*

## 2.2 Why RSA Works over ℤ/nℤ

RSA encryption is defined as a function from ℤ/nℤ to ℤ/nℤ:

- RSA : ℤ/nℤ → ℤ/nℤ [Recall ℤ/nℤ is a commutative ring]
- Note: *n* is not prime, but a product of two primes.

We had a very good reason to choose RSA to work over ℤ/nℤ:

- Exponentiation in ℤ/nℤ is fast to compute [Recall exponentiation by squaring]. In other words, computing *c* = *mᵉ* mod *n* is very efficient.
- But getting the **eᵗʰ** root of *c* to get the original *m* is believed to be **infeasible**.

> Note that RSA cannot uniquely encrypt values greater than *n*; such values are reduced modulo *n*, so decryption returns a value less than *n*, not the original input.

By its mathematical nature, RSA can encrypt only numbers — more specifically, only numbers in ℤ/nℤ. That means the sender and receiver must use a mapping of numbers to characters to make this useful: a ⇒ 1, b ⇒ 2, etc.

## 2.3 RSA — Toy Example

- 1) Let *p* = 7 and *q* = 11
- 2) *n* = *p* · *q* ⇒ *n* = 77
- 3) ɸ(*n*) = (*p* − 1)(*q* − 1) = (7 − 1)(11 − 1) = 6 × 10 = 60
- 4) Let's select *e* as 13 — note that 13 is less than 60 and is coprime with 60
- 5) Calculate *d* such that 13*d* mod 60 = 1 — i.e., *d* is the modular inverse of *e*. We get *d* = 37
- 6) Now we have the keys:
  - (13, 77) is the public key
  - (37, 77) is the private key
- 7) **Encryption:** *c* = 3¹³ mod 77 = 38
- 8) **Decryption:** *m* = 38³⁷ mod 77 = 3

## 2.4 RSA Algorithm — Worked Example (Notes)

**Key generation:** Select two prime numbers as *p* = 17 and *q* = 11.
- Obtain *n* = *pq* = 17 ∗ 11 = 187
- Calculate ɸ(*n*) = (*p* − 1)(*q* − 1) = 16 ∗ 10 = 160
- Select *e* such that *e* is coprime to ɸ(*n*) = 160 and *e* < ɸ(*n*) → *e* = 7
- Determine *d* such that *d* ∗ 7 ≡ 1 mod 160 and *d* < 160.
  - 23 ∗ 7 = 161 = (1 ∗ 160) + 1 → *d* = 23
- *PU* = {7, 187}, *PR* = {23, 187}

**Encryption:** Encrypt plaintext *M* = 88. *C* = 88⁷ mod 187 = 11

**Decryption:** *M* = 11²³ mod 187 = 88

It should be noted that while encrypting numerical values with RSA is straightforward, non-numerical characters must be mapped to numerical values before encryption.

## 2.5 Security of RSA

The security of RSA rests on:

- Obtaining the *eᵗʰ* root of a number in ℤ/nℤ is computationally infeasible unless you know *d*.
- Factoring *n* = *pq*, for very large *p* and *q*, is computationally infeasible. Otherwise, *d* can be easily calculated.
- This is for now though — quantum risks later. Australia plans to get rid of RSA by 2030.

The defense against brute forcing *d* is to use a large key space for *d*. The larger the number of bits in *d*, the more secure the system becomes. However, increasing the key size can also slow down the system due to the more complex calculations required for key generation, encryption, and decryption.

To make factoring *n* = *pq* computationally infeasible:

- *p* and *q* must be **very large**.
- Encoding *n* needs thousands of bits (RSA key lengths: 2048-bit and more).
- *p* and *q* must **not be too close together** (allows forms of fast factoring).

In practice, there are many more limiting factors — not every key is a good key. Consequently, it is **not recommended to implement RSA yourself** for use in production environments.

## 2.6 Attacks on RSA

Five possible approaches to attacking RSA:

- **Brute force**: This involves trying all possible private keys — feasible only against smaller keys.
- **Mathematical attacks**: There are several approaches, all equivalent in effort to factoring the product of two primes.
- **Timing attacks**: These depend on the running time of the decryption algorithm.
- **Hardware fault-based attack**: This involves inducing hardware faults in the processor that is generating digital signatures.
- **Chosen ciphertext attacks**: This type of attack exploits properties of the RSA algorithm (e.g., malleability).

## 2.7 Never Use RSA Without Padding

### Malleability

Malleability in RSA means that an attacker can modify a ciphertext in a predictable way so that the decrypted plaintext is also changed in a related, predictable way, without knowing the private key.

**Example:**

- Attacker intercepts ciphertext *c*.
- Attacker computes a modified ciphertext and sends it to the receiver:
  - *c'* ≡ *c* · *rᵉ* mod *n* (e.g., using *r* = 2, *c'* ≡ *c* · 2ᵉ mod *n*)
- Receiver decrypts *c'* and obtains *r·m* (e.g., 2*m*):
  - (*c'*)ᵈ mod *n* ≡ (*c* · *rᵉ* mod *n*)ᵈ mod *n* ≡ *r·m*
- Result looks valid, not random. The receiver cannot detect that the message was altered.
- **Key idea:** Vanilla RSA preserves structure → tampering yields a predictable, manipulated plaintext (not garbage).
- This is a generic result; the scalar multiplication can be any number, not just 2.
- Recall, this is a **Chosen Ciphertext Attack (CCA)**.

**Detailed derivation (notes):** First, Eve listens for a ciphertext that she wants to crack. Next, she takes this ciphertext, multiplies it by a random value raised to the power of Bob's *e* value, and gets Bob to decrypt it. If Eve can determine the decrypted value for this ciphertext, she can determine the original message as:

- (*c'*)ᵈ = (*c* × *rᵉ*)ᵈ = (*mᵉ* × *rᵉ*)ᵈ = *m^(e×d)* × *r^(e×d)* = *m* × *r*, since (*mᵉ*)ᵈ mod *n* must equal *m*¹ mod *n*.

Eve obtains the original plaintext by dividing the resulting plaintext by *r*. **Note** the CCA assumption here: we assume the attacker has the ability to get *c'* decrypted.

### No 'Semantic Security'

- An attacker can forward-compute (likely) messages and see if they match a given ciphertext.
- Deterministic encryption with a public key → **Chosen Plaintext Attacks (CPA)**.
- Lack of randomness.

The vanilla form of RSA is not secure. It is vulnerable to CCA because of malleability, and basic RSA encryption does not provide semantic security due to its lack of randomness. Since RSA is deterministic — the same plaintext encrypted with the same public key will always produce the same ciphertext — it is vulnerable to attacks like CPA. In such attacks, an adversary can encrypt likely messages and compare the results to a given ciphertext to infer the original plaintext.

### Solution: Padding

- Sophisticated **padding**, which adds randomness on encryption and removes it on decryption.
- To achieve semantic security, modern RSA implementations incorporate padding schemes that introduce randomness, ensuring that the same plaintext encrypted multiple times results in different ciphertexts.
- Padding is crucial, but non-trivial! Today, we use **OAEP (Optimal Asymmetric Encryption Padding)**.

## 2.8 Hybrid Encryption

**RSA has two key problems:**

- **Problem 1:** Public-key cryptography is slow — long keys! RSA is 100–1000 times slower than AES.
- **Problem 2:** It requires a mechanism to map characters to numbers for practical use.

**Solution: Hybrid Encryption**

To address these limitations, most applications employ hybrid encryption. In this approach, public-key encryption like RSA is used to quickly establish a symmetric key, and subsequent communications are secured using symmetric key encryption. Almost all public-key encryption uses hybrid encryption in practice:

- Generate a random symmetric key *k*.
- Encrypt the actual message as *cₘ* = Encₖ(*m*).
- Encrypt *k* as *cₖ* = Encₚₖ(*k*) using the receiver's public key.
- Send (*cₖ*, *cₘ*).

---

# 3 Key Exchange — Diffie-Hellman

There are many public-key cryptosystems besides RSA. One of the best-known ones is **not used for encryption**, but for key exchange. The question to solve: *Can Alice and Bob establish a shared symmetric key without a purely listening attacker being able to obtain the key?* Finite fields come to our aid.

Diffie–Hellman is the first published algorithm that implemented the public-key (trapdoor) principle, published by Diffie and Hellman in 1976. Its best-known application is secure key exchange, which can subsequently be used for symmetric-key encryption. Other applications of the Diffie–Hellman algorithm include:

- Diffie-Hellman Key Exchange
- *ElGamal encryption/decryption*
- *Digital Signature Standard (DSA/DSS)*

Diffie-Hellman is based on finite fields. The security of the Diffie–Hellman algorithm relies on the difficulty of computing discrete logarithms. Specifically, it is considered **computationally infeasible to compute a discrete logarithm over a finite field**, provided the prime number used to define the field is sufficiently large. However, if additional information, such as the private key, is available, this computation becomes computationally feasible.

**Recap — Discrete Logarithm Problem (DLP):** Given *y*, *p*, *g* satisfying the equation *y* = *g*ˣ mod *p*, where *p* is a prime number and *g* is a primitive root of *p*, how can we find *x*?

## 3.1 Finite Fields Revisited: Primitive Roots

- Let *p* be prime. We know ℤ/pℤ is a finite field.
- Elements of ℤ/pℤ are {0, 1, ..., *p* − 1}.
- You can define a new group over the numbers: **ℤ\*ₚ = {1, ..., p − 1}** (with multiplication operation).
- There is a special element *g* ∈ ℤₚ such that every number *a* ∈ ℤ\*ₚ is a power of *g*.
- So, actually, ℤ\*ₚ = {*g*⁰ = 1, *g*¹ = ..., *g^(p−2)* = ...}.
- *g* is called a **primitive root** (or generator) of ℤₚ.

## 3.2 Diffie-Hellman Key Exchange

The following summarizes the Diffie-Hellman algorithm for exchanging a shared key between two users *A* and *B* who have already shared two publicly known values *p* (a prime number) and *g* (a primitive root of *p*).

- **Alice**:
  - Choose random value *a* < *p*
  - Compute *X* = *gᵃ* mod *p*
  - Send *X* to Bob
  - Compute *k* = *Yᵃ* mod *p*
- **Bob**:
  - Choose random value *b* < *p*
  - Compute *Y* = *gᵇ* mod *p*
  - Send *Y* to Alice
  - Compute *k* = *Xᵇ* mod *p*
- Both sides obtain the same *k* value:
  - *Yᵃ* mod *p* = (*gᵇ*)ᵃ = *g^(ab)* = (*gᵃ*)ᵇ = *Xᵇ* mod *p*

Each user selects a random integer *a* and *b* such that they are less than *p*, and computes *X* = *gᵃ* mod *p* and *Y* = *gᵇ* mod *p*, respectively. The *a* and *b* are kept private (i.e., private keys of A and B), and the *X* and *Y* values are publicly exchanged by the two users (i.e., *X* and *Y* are the public keys of the two users).

After the exchange, each user can separately and independently calculate the same key: A computes *Yᵃ* mod *p*, and B computes *Xᵇ* mod *p*. Both of these values will be equal and that will be the shared key; *K* = *Yᵃ* mod *p* = *Xᵇ* mod *p*.

Through this process, the two parties have exchanged a secret value *K* which is typically used as a shared key. DH key exchange allows key establishment over an insecure channel, **under a passive attacker**.

An adversary who can only passively observe the key exchange will only know the values *p*, *g*, *X*, and *Y* and will be forced to take a discrete logarithm to determine one of the private keys *a* or *b* to calculate the shared key *K*. For instance, if calculating *b*, the adversary needs to compute *b* such that *Y* = *gᵇ* mod *p*, which is solving the DLP. For large primes, this task is computationally infeasible. Hence, the shared secret key *K* is considered secure from a passive observer.

## 3.3 Person-in-the-Middle Attack

While the Diffie-Hellman algorithm is secure against passive eavesdroppers, it is vulnerable to person-in-the-middle attacks. When the attacker is active, the standard DH key exchange is not secure.

The adversary first observes the publicly shared values of *p* and *g*, and then generates two separate sets of private and public key pairs. The attacker then positions themselves between the two communicating users, Alice and Bob, intercepting and replacing the messages transmitted during the key exchange:

- **Attacker**: Choose random values *c*, *d* < *p*; compute *X'* = *g^c* mod *p*, *Y'* = *g^d* mod *p*; send *X'* to Alice and *Y'* to Bob.
- Alice: chooses random *a* < *p*, computes *X* = *gᵃ* mod *p*, sends *X*; computes *k₁* = *X'ᵃ* mod *p*.
- Bob: chooses random *b* < *p*, computes *Y* = *gᵇ* mod *p*, sends *Y*; computes *k₂* = *Y'ᵇ* mod *p*.
- Attacker: computes *k₁* = *X^c* mod *p*, *k₂* = *Y^d* mod *p*.

By doing this, the attacker performs two independent key exchanges: one with Alice and another with Bob. At the end of this process, the attacker establishes separate secret keys *K₂* and *K₁* with Alice and Bob respectively, and can use these keys to perform a person-in-the-middle attack (intercept and replace original messages) on future communications between Alice and Bob.

The key exchange protocol is vulnerable to such an attack because it **does not authenticate the participants**.

**Solution:** Digital signatures and public-key certificates. Person-in-the-middle attacks in Diffie-Hellman key exchange can be overcome by using digital signatures, where each party signs their public key with their private key, allowing the other party to verify the authenticity of the key using the corresponding public key, ensuring that the exchanged keys have not been tampered with by an attacker. These topics are discussed in the next lecture.

---

# 4 Elliptic Curve Cryptography (ECC) — Non-Examinable

The following is a very brief introduction.

- Our schemes so far are defined for rings and fields constructed with the help of the mod operation — i.e., we use modular arithmetic.
- Elliptic curves *E*(*a*,*b*) are defined by equations of the form *y*² = *x*³ + *ax* + *b*.
- When defined over a finite field, they produce a finite set of points.
- A group can be defined over these points using point addition.
- This allows us to define a Discrete Logarithm Problem (ECDLP).
  - ECDLP is harder per bit than classical DLP.
- Therefore, elliptic curve cryptography achieves the same security with much shorter keys.
  - Typical ECC keys: 256 bits (very common), 384 bits (high security).

## 4.1 Same Idea, Different Group

**Diffie-Hellman (classical setting)**

- Group: ℤ\*ₚ
- Operation: multiplication mod *p*
- Computation: *aᵏ* mod *p* (repeated multiplication)
- Key idea: Security comes from the Discrete Logarithm Problem (DLP)

**Key transition:** So far, we have used groups derived from modular arithmetic. We now construct a different Abelian group with the same goal.

**Elliptic Curve Cryptography (ECC): same idea, different group**

- Elements: points on a curve over a finite field ℤₚ
- Operation: point addition, i.e., *kP* = *P* + *P* + ⋯ + *P*
- Given *P* and *Q* = *kP*, it is computationally infeasible to recover *k*.
- **Note:** All arithmetic is performed modulo *p* (implicitly).

## 4.2 Elliptic Curves — Geometric Intuition

**Geometric Intuition**

- Consider *E*(1,1), which is *y*² = *x*³ + *x* + 1.
- We define *O*: the point at infinity (identity element). This is an imaginary point to complete the math.

**Point addition**

- Take two points *P* and *Q* on the curve.
- Draw the line through *P* and *Q*.
- The line intersects the curve at a third point.
- Reflect this point across the x-axis: this gives *P* + *Q*.

**Key Properties**

- The negative of a point: −*P* = (*x*, −*y*), i.e., reflection across the x-axis.
- Three points on a line sum to zero: *P* + *Q* + *R* = 0.

**Special Case related to ECC**

- What if *P* = *Q*? Use the tangent line at *P*.
- The tangent intersects the curve at another point. Reflect it across the x-axis. This gives 2*P*.

## 4.3 Elliptic Curves over a Finite Field ℤₚ

- We now define elliptic curves over a finite field ℤₚ.
- Now the curve equation becomes *Eₚ*(*a*,*b*): *y*² = *x*³ + *ax* + *b* (mod *p*).

**Example curve over ℤ₂₃:** Let's consider *E₂₃*(1,1): *y*² = *x*³ + *x* + 1 (mod 23).

- Check if point (*x*,*y*) = (9,7) lies on the curve:
  - 7² ≡ 9³ + 1·9 + 1 (mod 23)
  - 49 ≡ 739 (mod 23)
  - 3 ≡ 3 ✓

**Points on the curve E₂₃(1,1):**

- The curve consists of all pairs of (*x*,*y*) satisfying the above equation, plus *O*, the point at infinity.
- This forms a finite set of points.

## 4.4 Elliptic Curves over a Binary Field GF(2ᵐ)

**Transition from Prime Fields**

- Previously, we used prime fields ℤₚ over an elliptic curve.
- Now, we define curves over binary fields GF(2ᵐ) [recall — we did something similar in AES].
- Elements are polynomials with coefficients in GF(2) (bit strings).
- Arithmetic is done modulo an irreducible polynomial.

**Curve Equation:** *y*² + *xy* = *x*³ + *ax*² + *b*, with addition/multiplication in GF(2ᵐ).

**Field Generator:** Let *g* be a primitive element (generator) of GF(2⁴). Every non-zero field element can be expressed as a power of *g*: GF(2⁴)\* = {*g*⁰, *g*¹, *g*², …, *g*¹⁴}.

### 4.4.1 Example Curve and Point over GF(2⁴)

Let's consider the curve *y*² + *xy* = *x*³ + *ax*² + *b* where *a* = *g*⁴ and *b* = 1. Let's consider the test point (*x*,*y*) = (*g*⁵, *g*³) and verify whether it is on the curve.

**Verification:**
*y*² + *xy* = *x*³ + *ax*² + *b*
(*g*³)² + *g*⁵*g*³ = (*g*⁵)³ + *g*⁴(*g*⁵)² + 1
*g*⁶ + *g*⁸ = *g*¹⁵ + *g*¹⁴ + 1
1100 + 0101 = 0001 + 1001 + 001
1001 = 1001 ⇒ Point (*x*,*y*) = (*g*⁵, *g*³) is on the curve ✓

**Properties of GF(2⁴):**

- We select *f*(x) = *x*⁴ + *x* + 1 as the irreducible polynomial and *g* as 0010 (i.e., *g* = *x*).
- Now we can develop powers of *g*.
- Let's calculate *g*⁴ which is *x*⁴. *x*⁴ is greater than the largest degree polynomial that can be supported by 4 bits (which is *x*³). So we need to calculate: *x*⁴ = *x*⁴ mod (*x*⁴ + *x* + 1).
  - *x*⁴ − (*x*⁴ + *x* + 1) = *x*⁴ + (*x*⁴ + *x* + 1) = *x* + 1 = 0011.
  - Note: 1) In GF, addition and subtraction are the same, done through XOR. 2) Adding the same element twice results in zero.

## 4.5 Elliptic Curve Cryptography (ECC) — Discrete Log

Consider the equation *Q* = *kP* where *Q*, *P* ∈ *Eₚ*(*a*, *b*) and *k* < *p*. It is hard to determine *k* given *P*, *Q* → the discrete logarithm problem for elliptic curves.

**Example:** Consider the group *E₂₃*(9,17):

- Defined by: *y*² mod 23 = (*x*³ + 9*x* + 17) mod 23
- Find discrete logarithm *k* of *Q* = (4, 5) to base *P* = (16, 5).
- The only way to do this is brute force:
  - *P* = (16,5) ⇒ 2*P* = (20,20) ⇒ 3*P* = (14,14) ⇒ 4*P* = (19,20) ⇒ 5*P* = (13,10) ⇒ 6*P* = (7,3) ⇒ 7*P* = (8,7) ⇒ 8*P* = (12, 17) ⇒ 9*P* = (4,5) ⇒ *k* is 9.
- In practice, *k* would be very large, thus the brute-force approach is infeasible.

## 4.6 Elliptic Curve Diffie-Hellman Key Exchange (ECDH)

- Both users A and B (and any attacker) know *a*, *b*, *q*, *G*, *n*.
- These are system-wide public parameters.
- *G* is a base point (generator) on the curve.
- *n* is the order of *G*, i.e., *nG* = *O*. Usually *n* is chosen to be a large prime.
- Public keys are computed as: *P_A* = *n_A* × *G*, *P_B* = *n_B* × *G*.
  - This scalar multiplication is efficient.
- Private keys *n_A* and *n_B* are kept secret.
- Even with *P_A* and *G*, an attacker cannot compute *n_A*.
- Security relies on the hardness of the Elliptic Curve Discrete Logarithm Problem.
- Both parties compute the same key: *n_A* ∗ *P_B* = *n_A* ∗ (*n_B* ∗ *G*) = *n_B* ∗ (*n_A* ∗ *G*) = *n_B* ∗ *P_A*.

## 4.7 EC ElGamal Encryption

- **Public parameters:** Elliptic curve *E_q*(*a*,*b*), generator point *G* with large order *n*, message encoded as curve point *P_m*.

| Alice (sender) | Bob (receiver) |
|---|---|
| 1. Select private key *n_A* where *n_A* < *n* | 1. Select private key *n_B* where *n_B* < *n* |
| 2. Compute public key *P_A* = *n_A* × *G* | 2. Compute public key *P_B* = *n_B* × *G* (shared publicly) |
| 3. Choose random integer *k* (new for each message) | 3. Receive *C_m* = {*kG*, *P_m* + *kP_B*} |
| 4. Send ciphertext: *C_m* = {*kG*, *P_m* + *kP_B*} | 4. Recover: *P_m* = (*P_m* + *kP_B*) − *n_B* × (*kG*) |

- *kP_B* acts as a one-time mask on *P_m*. This is the embedded ECDH shared secret. *P_B* is B's public key.
- Works because *n_B* × (*kG*) = *k* × (*n_BG*) = *kP_B*, i.e., the mask cancels out.
- **Why is *k* random and chosen fresh each time?** Reusing *k* for two different messages leaks information. An attacker can XOR the two ciphertexts and eliminate the mask, exposing the relationship between messages. A fresh *k* per message prevents this.

**Example:** Consider the global (system-level) parameters: *E₂₅₇*(0, −4): *y*² = *x*³ – 4, *G*(2, 2).

- **Encryption:**
  - Bob's private key *n_B* = 101, Bob's public key *P_B* = *n_BG* = 101(2, 2) = (197, 167).
  - Alice wants to send *P_m* = (112, 26) and chooses *k* = 41. Compute *kG* = 41(2,2) = (136, 128).
  - Alice encrypts: *kP_B* = 41(197, 167) = (68, 84) and *P_m* + *kP_B* = (112, 26) + (68, 84) = (246, 174).
  - Alice sends: *C_m* = {*C₁*, *C₂*} = {(136, 128), (246, 174)} to Bob.
- **Decryption:** Bob computes *C₂* − *n_B C₁* = (246, 174) − 101(136, 128) = (246, 174) − (68, 84) = (112, 26).

## 4.8 Security of ECC

- The security of ECC depends on how difficult it is to determine *k* given *kP* and *P* — the elliptic curve logarithm problem.
- Comparable key sizes in terms of computational effort for cryptanalysis are compared in a table; pay attention to the key length of RSA versus ECC.

---

# 5 Post-Quantum Cryptography (PQC)

PQC focuses on developing algorithms that remain secure even in the presence of quantum computational power.

**Breaking Asymmetric Cryptography**

- **Shor's algorithm** can efficiently factor large numbers and compute discrete logarithms.
- RSA, Diffie-Hellman Key Exchange, and ECC will be vulnerable.

**Symmetric Cryptography is More Resilient**

- **Grover's algorithm** provides a quadratic speedup for brute-forcing the keys of symmetric ciphers.
- A symmetric key's effective security level is halved.
- A 256-bit key would offer security comparable to a 128-bit key against a quantum adversary.
- Doubling key sizes is a solution.

**Post Quantum Cryptography (PQC)**

Some of the key concepts of PQC include:

- **Lattice-Based Cryptography** is based on the hardness of problems related to lattice structures in high-dimensional spaces.
- **Code-Based Cryptography** relies on the hardness of decoding random linear codes.
- **Hash-Based Cryptography** leverages the security properties of hash functions for cryptographic tasks.

---

# 6 Recap

- Public-key cryptosystem and its applications
- RSA algorithm and attacks on RSA
- Hybrid encryption
- Diffie-Hellman key exchange and person-in-the-middle attack
- An overview of elliptic curves and elliptic curve cryptography
- ECC Diffie-Hellman key exchange
- The security of ECC
- Post Quantum Cryptography (PQC)

---

# 7 Practice Quiz

**Question 1:** Select all that is TRUE for the RSA algorithm.

- **a)** One factor that makes RSA secure is the difficulty in prime number factorisation.
- **b)** RSA is still considered secure irrespective of the key size.
- **c)** Padding is required to make RSA secure.
- **d)** RSA is a symmetric key encryption algorithm.
- **e)** You can choose any two prime numbers to construct an RSA scheme.

**Explanation:** The security of RSA lies on two factors. The first is the difficulty of prime factorization. The second is the difficulty of finding the *eᵗʰ* root of a number under modulo *n*. Therefore **a)** is TRUE.

**b)** is FALSE. These days we consider only key sizes above 2048 bits as secure for RSA.

**c)** is TRUE. A semantically secure cryptosystem is one in which only a small amount of information about the plaintext can be extracted from the ciphertext. Textbook RSA doesn't have any randomness. Therefore, it doesn't have any semantic security. As a result, we add padding.

**d)** is FALSE. RSA is an asymmetric cryptosystem.

**e)** is FALSE. We can't select any two prime numbers. For starters, we can't select two small prime numbers. Even for large prime numbers, there are restrictions. We can't select prime numbers that are close to each other. Then the factorization problem becomes easier.

**Question 2:** For *p* = 11 and *q* = 17 and choose *e* = 7. Apply the RSA algorithm to find the ciphertext when the plaintext message is 88.

- a) 23 b) 64 c) 11 d) 54

**Explanation:** In the RSA notation, we have been given *p* = 11, *q* = 17 and *e* = 7. We can find,

- *n* = *pq* = 187
- ɸ(*n*) = (*p* − 1)(*q* − 1) = 160 (as *e* is given we don't need it; but note that *e* is less than ɸ(*n*)).
- *C* = *Mᵉ* mod *n* = 88⁷ mod 187 = **11**

**Question 3:** In an RSA system the public key of a given user is *e* = 31, *n* = 3599. What is the private key of this user?

- a) 3031 b) 2412 c) 2432 d) 1023

**Explanation:** In the RSA notation, we have been given *e* = 31 and *n* = 3599. We can find:

- *p* = 59 and *q* = 61 (by finding the prime factors of 3599) and *n* = *pq* = 3599
- ɸ(*n*) = (*p* − 1)(*q* − 1) = 58 × 60 = 3480

We know the private and the public key have the property *ed* ≡ 1 mod (ɸ(*n*)), i.e., 31*d* ≡ 1 mod (3480). Check them one by one:

- 31 × 3031 mod (3480) = 1. Therefore, **3031** is the correct answer. You can verify the rest.
- E.g., 31 × 2412 mod (3480) = 1692.

**Question 4:** The ............. protocol enables two users to establish a secret key using a public-key scheme based on discrete logarithms.

- a) Micali-Schnorr b) Elgamal-Fraiser c) Diffie-Hellman d) Miller-Rabin

**Explanation:** We learned only one public key cryptography-based key exchange scheme in the class. That is the Diffie-Hellman key exchange. The rest are either made up or not related. For example, Micali-Schnorr is a random number generator algorithm, and Miller-Rabin is a primality test.

**Question 5:** The basic Diffie-Hellman key exchange protocol is vulnerable to a ............. attack because it does not authenticate the participants.

- a) one-way function b) time complexity c) chosen ciphertext d) person-in-the-middle

**Explanation:** An attacker can store and replay messages in the Diffie-Hellman key exchange and conduct an active person-in-the-middle attack. Diffie-Hellman key exchange is secure only against a passive attacker. For protection against active attackers, a modified version of the process is required, called the signed Diffie-Hellman key exchange.

**Question 6:** The Diffie-Hellman algorithm depends on the difficulty of computing discrete logarithms for its effectiveness. TRUE or FALSE.

- a) TRUE b) FALSE

**Explanation:** There are two key mathematical problems that have trapdoor properties: the discrete logarithm problem and the RSA problem. DH key exchange relies on the discrete logarithm problem.

**Question 7:** Read this article on how the advances in quantum computing can affect symmetric and asymmetric cryptography differently: https://builtin.com/cybersecurity/post-quantum-cryptography

Based on your reading, which cryptographic scheme will become more vulnerable when quantum computing becomes feasible?

- a) Symmetric cryptography b) Asymmetric cryptography

**Explanation:** Once quantum cryptography becomes available, some of the previously infeasible problems become feasible. As a result, asymmetric cryptography becomes vulnerable.

**Question 8:** Asymmetric and symmetric encryption have their own advantages and disadvantages. For example, asymmetric cryptography is slower and not suitable for real-time communications. On the other hand, symmetric cryptography is faster and more suitable for real-time data encryption and bulk data encryption. However, key distribution is an issue with symmetric encryption. As a result, most applications, especially in communications settings, use hybrid cryptography. Watch the following video on hybrid cryptography: https://www.youtube.com/watch?v=VPvZbMXfv_0

"Hybrid cryptography uses asymmetric cryptography to establish a symmetric key between two parties that can be used for subsequent communications." TRUE or FALSE

- a) TRUE b) FALSE

**Explanation:** The answer is TRUE. Hybrid cryptography assumes the receiver's public key is already shared with the sender. The sender generates a session key (a symmetric key), encrypts it with the receiver's public key, and sends it to the receiver. The receiver can decrypt the message using their private key and recover the session key. Now, both parties have access to the shared session key, which can be used for any subsequent communication.

**Question 9:** A considerably larger key size can be used for ECC compared to RSA. TRUE or FALSE.

- a) TRUE b) FALSE

**Explanation:** The statement is FALSE. In general, ECC key sizes are much shorter than RSA, which is an advantage of ECC. This is because the elliptic curve logarithm problem is more difficult than the RSA problem.

**Question 10:** Consider the elliptic curve *E₇*(2,1); that is, the curve is defined by *y*² = *x*³ + 2*x* + 1 with a modulus of *p* = 7. Which of the following is NOT a point in *E₇*(2,1)? *Not examined — for information only.*

- a) (0,1) b) (1,5) c) (3,4) d) (1,2)

**Explanation:** The equation we are after is *y*² mod 7 = *x*³ + 2*x* + 1 mod 7. We check each answer separately (Figure 4: Points on an Elliptic Curve). Only **(3,4)** is not satisfying the equation.

---

# References

- [1] W. Diffie and M. E. Hellman, "Multiuser cryptographic techniques," in *Proceedings of the June 7-10, 1976, national computer conference and exposition*, 1976, pp. 109–112.
- [2] R. L. Rivest, A. Shamir, and L. Adleman, "A method for obtaining digital signatures and public-key cryptosystems," *Communications of the ACM*, vol. 21, no. 2, pp. 120–126, 1978.

*Source slides: Dr. Thilini Dahanayaka, School of Computer Science, The University of Sydney. Original notes: Dr Suranga Seneviratne, Senior Lecturer — Security.*

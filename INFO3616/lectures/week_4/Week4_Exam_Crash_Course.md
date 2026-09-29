# Week 4 Exam Cram Sheet: Symmetric Cryptography

---

## 1. Fundamentals & Core Principles

* **Symmetric vs. Asymmetric:**
  * **Symmetric (Shared-Key):** Encryption key equals decryption key ($k_e = k_d$, or $k_d$ is easily derived from $k_e$). Shuffles and substitutes bits/symbols.
  * **Asymmetric (Public-Key):** $k_e \neq k_d$ and computationally infeasible to deduce $k_d$ from $k_e$. Based on hard math problems.
* **Kerckhoffs’ Principle (Critical Exam Concept):**
  * *Rule:* The security of a cryptographic system must depend **only on the secrecy of the key**, never on the secrecy of the algorithm/mechanism.
  * *Why?* Open algorithms allow global public scrutiny ("many eyes" find flaws early).
  * *Historical failures:* **GSM A5/1** and **DVD CSS** relied on proprietary/secret algorithms and were quickly reverse-engineered and broken.
* **Attack Models (Weakest to Strongest Adversary):**
  1. **Ciphertext-Only:** Intercepts ciphertext $c$ only (e.g., historical eavesdropping).
  2. **Known-Plaintext:** Knows some $(p_i, c_i)$ pairs (e.g., cribs/weather reports in WWII Enigma).
  3. **Chosen-Plaintext:** Attacker chooses $p$ and obtains corresponding $c = E_k(p)$ (Standard model for public-key ciphers; e.g., BEAST attack).
  4. **Chosen-Ciphertext:** Attacker submits crafted $c$ to an oracle and receives decrypted $p$ (e.g., Bleichenbacher attack).

---

## 2. Shannon’s Core Design Goals

Modern ciphers combine two properties to thwart statistical cryptanalysis:
* **Confusion:** Blurs the relationship between the **ciphertext and the key**.
  * Each ciphertext bit must depend on multiple key bits.
  * Achieved primarily via non-linear **Substitution (S-boxes)**.
* **Diffusion:** Spreads the statistical properties of the **plaintext across the ciphertext**.
  * Flipping 1 bit in the plaintext should flip $\approx 50\%$ of the ciphertext bits (Strict Avalanche Criterion - SAC).
  * Achieved primarily via **Permutation / Transposition (P-boxes)**.

---

## 3. Historical Ciphers & Stream Primitives

### Caesar & Vigenère
* **Caesar (Monoalphabetic):** $c_i = (p_i + k) \pmod{26}$. Insecure due to letter frequency analysis (e.g., 'E' is the most frequent letter in English).
* **Vigenère (Polyalphabetic):** $c_i = (p_i + k_{i \pmod{|k|}}) \pmod{26}$.
* **Kasiski Examination (Exam Problem):**
  * Used to find key length $|k|$ without knowing the key.
  * Find repeated ciphertext blocks. Calculate the distances (intervals) between repetitions.
  * The key length is a **common factor (or GCD)** of the observed distances.
  * *Once key length $d$ is found:* Group every $d$-th letter and solve using monoalphabetic frequency analysis.

### One-Time Pad (OTP)
* **Encryption/Decryption:** $c = p \oplus k \iff p = c \oplus k$.
* **Information-Theoretic / Perfect Secrecy:** Holds **if and only if**:
  1. Key is **truly random** (entropy matches message).
  2. Key length is $\ge$ plaintext length ($|k| \ge |p|$).
  3. The key is **NEVER reused** (not even partially).
* **Why Impractical?** Key distribution problem and generating massive volumes of true entropy.
* **Key Reuse Vulnerability (Two-Time Pad / Crib Dragging):**
  $$c_1 \oplus c_2 = (p_1 \oplus k) \oplus (p_2 \oplus k) = p_1 \oplus p_2$$
  The key cancels out! An attacker guesses common words (cribs like `" the "`) and drags them across $c_1 \oplus c_2$ to recover readable text.

---

## 4. DES vs. 3DES vs. AES (Comparison Table)

| Feature | DES | 3DES (Triple DES) | AES (Rijndael) |
| :--- | :--- | :--- | :--- |
| **Structure** | **Feistel Network** | **Feistel Network** | **Substitution-Permutation Network (SPN)** (NOT Feistel!) |
| **Block Size** | 64 bits | 64 bits | **128 bits** (Fixed) |
| **Key Size** | 56 bits (64-bit key with 8 parity bits discarded) | 112 bits (2-key) or 168 bits (3-key) | **128, 192, or 256 bits** |
| **Number of Rounds** | 16 rounds | $16 \times 3 = 48$ rounds | 10 rounds (128-bit key)<br>12 rounds (192-bit key)<br>14 rounds (256-bit key) |
| **Current Status** | **Broken / Insecure** (Key space $2^{56}$ too small; brute-forceable in hours) | Deprecated (too slow, small 64-bit block size) | **Current de facto standard** |

### Key Mechanics of DES:
* **Feistel Round Operation:**
  $$L_n = R_{n-1}$$
  $$R_n = L_{n-1} \oplus F(R_{n-1}, K_n)$$
  * Feistel property: Decryption is structurally identical to encryption—just apply the round keys in reverse order ($K_{16} \to K_1$). Individual round functions $F$ do **not** need to be invertible.
* **S-Box Table Lookup (Guaranteed Exam Question):**
  * Input: 6 bits $(b_0, b_1, b_2, b_3, b_4, b_5)$.
  * **Row selector:** Outer bits $(b_0 b_5)_2$ (values 0–3).
  * **Column selector:** Middle 4 bits $(b_1 b_2 b_3 b_4)_2$ (values 0–15).
  * Output: 4-bit binary representation of the decimal value at $(\text{Row}, \text{Column})$.
  * *Worked Example:* Input `010000` $\to$ Row: `00` = 0; Column: `1000` = 8. Look up Row 0, Col 8 in table $\to 3 \to \mathbf{0011}_2$.

### 3DES Sequence:
* **Encrypt-Decrypt-Encrypt (EDE):**
  * $C = E_{K_3}(D_{K_2}(E_{K_1}(P)))$
  * *Why EDE instead of EEE?* **Backward compatibility.** If $K_1 = K_2 = K_3$, $E_{K_1}(D_{K_1}(E_{K_1}(P))) = E_{K_1}(P)$ (reverts to single DES).

### AES Inner Round Structure (4 Steps):
1. **SubBytes:** Byte substitution using an invertible S-box over $GF(2^8)$ (provides **confusion**).
2. **ShiftRows:** Cyclic byte shifting per row (provides **diffusion** / permutation).
3. **MixColumns:** Matrix multiplication in the finite field $GF(2^8)$ modulo irreducible polynomial $m(x) = x^8 + x^4 + x^3 + x + 1$ (diffuses bytes across each column). *Note: Omitted in the final round.*
4. **AddRoundKey:** Bitwise XOR of the state array with the 128-bit round key derived from the key expansion schedule.

---

## 5. Cipher Block Modes of Operation

| Mode | Formula | Pros / Cons | Vulnerability / Exam Note |
| :--- | :--- | :--- | :--- |
| **ECB** *(Electronic Codebook)* | $C_i = E_k(P_i)$ | Each block encrypted independently. | **NEVER USE.** Preserves plaintext patterns (the famous "Tux penguin / USYD logo" outline remains clearly visible). |
| **CBC** *(Cipher Block Chaining)* | $C_i = E_k(P_i \oplus C_{i-1})$<br>$C_0 = IV$ | Masks patterns; ciphertext depends on all prior blocks. | **Sequential:** Cannot parallelize encryption. Requires unique, unpredictable **IV**. |
| **CTR** *(Counter Mode)* | $C_i = P_i \oplus E_k(\text{Nonce} \parallel i)$ | **Fully parallelizable**, random access, turns block cipher into a stream cipher. | Reusing $(\text{Nonce}, \text{Key})$ pair produces identical keystream $\to$ total compromise (Two-Time Pad attack). |

### Rules for Initialization Vectors (IV) & Nonces:
* **IVs / Nonces do NOT need to be kept secret** (they are transmitted in plaintext alongside $C$).
* **IVs / Nonces must NEVER be repeated with the same key.**
  * WEP (Wired Equivalent Privacy) failed because its IV was only 24 bits long, causing frequent IV reuse and allowing key recovery under RC4.

---

## 6. PRNGs & Stream Ciphers

* **CSPRNG (Cryptographically Secure Pseudo-Random Number Generator):**
  * Deterministic algorithm expanding a short true-random **seed** into a long bitstream.
  * *Criteria:* (1) Computationally infeasible to predict future bits even knowing past bits; (2) Infeasible to reconstruct the seed; (3) Output is computationally indistinguishable from true random bits.
* **Modern Stream Ciphers:**
  * **ChaCha20** and **Salsa20** are modern, fast, secure standards (designed by Daniel J. Bernstein).
  * **RC4** is **broken/insecure** (used in older SSL/TLS and WEP; do not use).

---

## 7. Math & Brute-Force Rapid Reference

* **Average Brute-Force Search Time:**
  * For a key space of size $2^k$, an attacker on average tests half the keys: $2^{k-1}$.
  * For DES ($k = 56$ bits): Keys to test $= 2^{55} \approx 3.6 \times 10^{16}$.
  * At $10^9\text{ keys/sec}$: $\frac{2^{55}}{10^9} \approx 3.6 \times 10^7\text{ sec} \approx 1.14\text{ years}$.
  * At $10^{13}\text{ keys/sec}$: $\frac{2^{55}}{10^{13}} \approx 3600\text{ sec} \approx 1\text{ hour}$.
* **Finite Fields $\mathbb{Z}_n$ / $GF(p)$ Rule:**
  * $\mathbb{Z}_n = \{0, 1, \dots, n-1\}$ forms a finite field under addition/multiplication modulo $n$ **if and only if $n$ is prime**.
  * If $n$ is composite (e.g., $n = 6$), non-coprime elements (like 2, 3, 4) lack multiplicative inverses ($2 \cdot x \not\equiv 1 \pmod 6$ for any integer $x$), so it is **not** a field.
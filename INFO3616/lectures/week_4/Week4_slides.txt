# Week 4 Symmetric Cryptography 



Dr. Thilini Dahanayaka 

School of Computer Science, The University of Sydney 

## Agenda 

- Cryptography - Definitions 

- Historical Ciphers 

- Stream and Block Ciphers 

- DES and 3DES 

- Advanced Encryption Standard (AES) 

- Cipher Block Modes 

- Pseudorandom Number Generation 

## Math to Know 

- Hopefully you have read the lecture notes provided on the require math background. Following are the key ideas you need to know. 

   - XOR function 

   - Modular Arithmetic 

   - Extended Euclidean Algorithm 

   - Primitive Roots under modulo 

   - Discrete Logarithm Problem 

   - Groups/Rings/Fields and their variants 

   - Different types of finite fields and operations within those. 

   - Broader applicability of those math concepts in different aspects of cryptography. 



Even if you haven’t done it today, please ensure that you follow the given notes on math. Those are assessable. You will also need them throughout this unit. 

## Recommended Reading 

- Cryptography & Network Security - 7th Edition by William Stallings 

   - **Chapter 1** – Computer network and security concepts 

   - **Chapter 2** – Introduction to Number Theory 

   - **Chapter 3** – Classical Encryption Techniques 

   - **Chapter 4** – Block Ciphers and Data Encryption Standards 

   - **Chapter 5** – Finite Fields 

   - **Chapter 6** – Advanced Encryption Standards 

   - **Chapter 7** – Block Cipher Operation 

   - **Chapter 8** – Random bit Generation and Stream Ciphers 



Now that’s a lot of chapters !! All you need to know are in the lectures and we are not using all the content of those chapters. However, reading those will help you to better understand the concepts. 





1. Cryptography - Definitions 

## Cryptography 

- An indispensable tool 

   - Secure protocols and systems use cryptography for: 

      - Data confidentiality (encryption) 

      - Data integrity (signatures, message authentication codes) 



   - Authentication & data origin verification (signatures, message authentication codes) 

   - ■ Non-repudiation (signatures) 

- Fundamental understanding of the principles of cryptography is required for many careers in Computing. 

- In this unit, we introduce it more from a functional point of view, rather than mathematical/formal. 

## Cryptography 

- A double-edged sword: complex and many subtleties 

- Inconsiderate application of cryptography: likely insecure system 

   - Worse, an insecure system that seems secure to its developers and users 



   - The attacker doesn’t know it is supposed to be secure and will take it apart 

   - ○ Historical example GSM A5/1 algorithm 

- Implementing cryptography requires tremendous experience and knowledge      of the peculiarities of hardware and programming languages 

   - Do not cook (implement) your own crypto and use it for real 

   - Recognized way to become proficient is to practice, find a mentor, and discuss with other implementers → long career path with no shortcuts! 

## Cryptography 



**Cryptography:** The science of securely transmitting data, spatially and temporally. 

      - **Spatially:** Over a physical distance 

      - **Temporally:** Data stays secure a long time into the future 

- In this unit, we are commonly concerned with: 

   - Confidentiality 

   - Integrity 

   - Authentication 

- There are other applications of cryptography: 

   - Non-repudiation 

   - Privacy 

   - Anonymity 

## Means to Achieve These 

- **Confidentiality:** Encryption 

   - Symmetric encryption 

   - Asymmetric (public-key) encryption 

- **Integrity:** 

   - Symmetric and asymmetric ways to achieve this 

   - Message Authentication Codes and Signatures 

   - Hash functions 

- **Authentication:** Protocols 

## Two Forms of Cryptography 



**Symmetric Cryptography:** The key for encryption and decryption is the same (ke = kd), or at least kd ← ke  (i.e., can derive kd from ke) 

- Also known as **shared-key cryptography** 

- Based on algorithms to shuffle symbols around and map them to others 



**Asymmetric Cryptography:** The keys for encryption and decryption are different (ke ≠ kd), and it is infeasible to compute kd from ke 

- Also known as **public key cryptography** 

- Based on the hardness of some mathematical problems 

## Kerkhoff’s Principle 



**Kerkhoff’s Principle:** The security of a given cryptographic mechanism must depend only on the security of the cryptographic keys used, but never on the mechanism or anything else, except the keys, being a secret 

- Cryptographic mechanisms are usually publicly disclosed - often products of public competitions. 

- ● Many eyes argument: the weaknesses of a mechanism are found faster if many experts analyze it. 

- This principle has proved valuable time and again. 

- There is a sad history of cryptographic designers abandoning the principle 

   - Famous case: A5/1 and A5/2 for GSM. Initially secret, later found weak. 

   - CSS encryption for DVDs (found weak) 

## Symmetric Cipher Model 



Source: Cryptography and Network Security (Seventh Edition - William Stallings) 





2. Historical Ciphers 

## Traditional Concepts 

- Transposition and substitution 

   - Transposition shifts the positions of symbols according to a rule 

   - Substitution replaces symbols with others, according to a rule 

   - Rule usually parameterized by key 

   - Transposition and substitution can both be part of the same cipher 





## Substitution Techniques - Caesar Cipher 

- Special case of monoalphabetic substitution – The simplest form of substitution cipher. A symbol from the plaintext alphabet is always mapped to the same symbol of the ciphertext alphabet 

|r1 →s5|
|---|
|r2 →s2|
|r3 →s9|
|…→…|
|rn →s17|



## Substitution Techniques - Caesar Cipher 

- Every letter is simply shifted by n positions, e.g., n = 3: a → d, b → e, c → f, … 

- Roman historian Suetonius claimed this cipher was used by Gaius Iulius Caesar, but others used similar methods before 

- Security by today’s standards is very low, but the level of education thousands of years ago may have made it effective enough. 

## Problem - Frequency Analysis 



- Every natural language has an associated characteristic frequency at which letters occur. 

- This is preserved in the ciphertext. Makes it easy to deduce the mapping 

Source: Cryptography and Network Security (Seventh Edition - William Stallings) 

## Substitution Techniques - Vigenère Cipher 

- Consider the plaintext "HELLO" and the keyword "KEY". 

- For simplicity, we'll use an alphabet _A_ of 26 letters ( _N_ =26) with numerical values assigned as _A_ =0, _B_ =1, ..., _Z_ =25. 

- **Given:** 

   - Plaintext _P_ = "HELLO" → _Pi_ ={7,4,11,11,14} 

   - Keyword _K_ = "KEY" → _Kj_ ={10,4,24}, where ∣ _K_ ∣=3 

- **Encryption Process:** 

   - To encrypt each letter _Pi_ using the formula _Ci=(Pi+Kimod_ ∣ _K_ ∣ _) mod 26_ 

- **Decryption Process:** 

   - To decrypt each letter _Ci_ using the formula _Pi=(Ci−Kimod_ ∣ _K_ ∣ _+26) mod 26_ 





Substitution Techniques - Vigenère Cipher 



Substitution Techniques - Vigenère Cipher 

## Breaking Vigenère Cipher 

- The Vigenère cipher encrypts plaintext by applying a series of Caesar ciphers based on the letters of a keyword. For each letter of the keyword, it uses a different shift value (i.e., a different Caesar cipher). 

- When analyzed separately, each monoalphabetic substitution (each Caesar cipher) used in the Vigenère cipher is relatively easy to break due to its simplicity. 

- Several statistical tests exist to estimate d, e.g., Friedman test or Kasiski test 

## Breaking Vigenère Cipher 

- Kasiski test is intuitive: 

   - When the plaintext contains the same sequences of symbols at intervals of length k,  then these are mapped to the same sequences of symbols in the ciphertext. 

   - Search for such repetitions in ciphertext, note the intervals. 

   - Greatest common divisor of all intervals is likely the key length 

   - Example: 

<u>https://crypto.interactive-maths.com/kasiski-analysis-breaking-the-code.html</u> 

## Breaking Vigenère Cipher 

- Assume our key is “KEY” 

- And our plain text is “THE BELOW IS AN EXAMPLE FOR KASISKI TEST. THE TEXT IS ENCRYPTED UTILISING THE VIGENERE CIPHER.” 

   - The distance between the 1st and 2nd repetition is 33. Therefore the key size must be one of 1, 3, 11 and 33, which are factors of 33. 



- The distance between the 2nd and 3rd repetition is 27. Therefore the key size must be one of 1, 3, 9 and 27. 

- The common factors are 1 and 3. We can ignore 1 as it is a very weak key that can be brute-forced. 

- So the possible key size is 3. 

## Transposition Techniques: Rail Fence Cipher 

- The plaintext is written down as a sequence of diagonals and then read off as a sequence of rows 

● Example: “MEET ME AFTER THE TOGA PARTY” with a rail fence of depth 2 



The encrypted message is: MEMATRHTGPRYETEFETEOAAT 

## From Classic to Modern 

- Polyalphabetic ciphers addressed an observed shortcoming: frequency analyses (in many forms) can yield the key 

- Shannon identified two design goals for modern ciphers: 

   - **Diffusion:** must blur statistically significant characteristics in plaintext ■ Every ciphertext symbol must depend on many plaintext symbols 

   - ■ On average, a bit flip in plaintext should change half the ciphertext bits 

   - **Confusion:** must blur dependency between ciphertext and key ■ Each symbol in ciphertext must depend on several symbols in key 

## One Time Pad (OTP) 



This is a symmetric cryptographic scheme. Not be confused with the OTP (One Time Password) that is used in Multi-Factor-Authentication (MFA). 

**Perfect security:** given a ciphertext, any possible plaintext is equally likely the correct one 

- One-Time Pad o: random sequence of bits with |o| ≥ |p|, i.e., at least as long as the plaintext 

- Ciphertext: c = o ⊕ p (XOR) 

- OTP is perfectly secure if, and only if: 

   - o is truly random (more later!) 

   - |o| ≥ p 

   - Never used twice, not even in part 

- OTPs have been used on occasion, but only in extremely high-value situations (e.g., red telephone). Why? Conditions on o are usually **much too hard** to achieve - OTP is impractical 

## One Time Pad (OTP) Example 

● OTP is not secure if the key is repeated. 





<u>http://travisdazell.blogspot.com/2012/11/many-time-pad-attack-crib-drag.html</u> 

## Attacks on Cryptography 

- A cryptographic system is **compromised** 

   - If an adversary can obtain plaintexts for certain ciphertexts, or 

   - An adversary can obtain decryption key kd when given ke 

- **Cryptanalysis** : decrypting without knowledge of key 

- Several forms of attacks define the strength of the adversary: 

   - **Ciphertext-only** - Attacker may only see ciphertexts 

   - **Known plaintext** - Attacker may see some plaintexts and corresponding ciphertexts 

   - **Chosen plaintext** - Attacker may choose a plaintext and see the corresponding ciphertext 

   - **Chosen ciphertext** - Attacker may choose ciphertext and decrypted plaintext 



3. Stream vs. Block Ciphers 

## Stream Ciphers 

- Pseudo-random functions to generate keystream from seed 

**Idea: generate a key stream from the secret key** 

- Apply some f (k) to obtain a stream b = b0 b1 b2  . . . bn  of bits 

- ● Apply a combination function on plaintext p = p0 p1 p2  . . . pn  and b0 b1 b2  . . . bn - commonly ⊕ (XOR) 

- Ciphertext is then simply: c = b ⊕ p 

- Challenge: keystream must be as ‘unpredictable’ as possible without knowledge of k 

**Rephrasing this:** it must be infeasible to determine whether the key stream is random or deterministic - the latter would imply there is a pattern! 

## Stream Ciphers 



Source: Cryptography and Network Security (Seventh Edition - William Stallings) 

## Block Ciphers 



Source: Cryptography and Network Security (Seventh Edition - William Stallings) 

## Block Ciphers 

● Substitution implemented via Substitution box **(S-boxes)** 

- Permutation implemented via Permutation box **(P-boxes)** 

   - → We will discuss S-boxes and P-boxes in DES 

- Multiple rounds of executing the algorithm to improve **diffusion and confusion** 

● Rounds arranged in so-called ‘networks’ 

## Example 1: Feistel Cipher 

- Define the steps of a block cipher 

- Multiple rounds 

- All rounds in the Feistel cipher have the same structure: 

   - **Substitution:** is performed on the left half of the data 

   - **Permutation:** is performed that consists of the interchange of the two halves of the data 

- Used in many block ciphers: DES, Blowfish, Twofish, RC6 



Source: Cryptography and Network Security (Seventh Edition - William Stallings) 

## Feistel Cipher: Encryption and Decryption 



Source: Cryptography and Network Security (Seventh Edition - William Stallings) 

## Example 2: Substitution-Permutation Network (SPN) 

##### ● Alternative network structure. 





4. DES and 3DES 

## Data Encryption Standard (DES) 

- Published in 1977, standardized in 1979 

- Key in each round: **subkey** derived from the actual key 

- Total of 8 S-boxes 

- Outputs from **S-boxes** are sent through one **P-box** to achieve good spread over S-boxes **in the next round** (and a bit more that is not important for our purposes) 

- ● It can be shown that the number of rounds, 16, is indeed necessary to achieve security 

## S-Boxes 

- Look-up tables: map of block of bits to and output block of bits 

   - Mapping is carefully chosen and vetted 

- How to make sure that decryption is possible? 

   - Either S-boxes themselves are invertible, or 

   - Their arrangement in a cipher is invertible as a whole 

- Changing one bit in input of S-box will map to an output block where, on average, half of all bits are flipped (diffusion) 

- We give an example from one of the most famous standards: Data Encryption Standard (DES) 

   - Note: DES was secure in its day; today the key length is too short 

   - State-of-the-art: Advanced Encryption Standard (AES) 

   - Also uses S-boxes, but differently 

## S-Box S[0] from DES 



- **Used like this:** 

   - **Example:** 

- Input string = (b0, b1, b2, b3, b4, b5) 

- b0 and b5 give row; (b1, b2, b3, b4)  give column 

- ○ Interpret the number in that cell as binary 

- Input = (1, 1, 0, 1, 1, 1) → (110111)2 

- ○ Row: (11)2  = (3)10 ; Column: (1011)2  = (11)10 ○ Output: (14)10  = (1110)2 → **1110** 

## P-Boxes 

- Transposition is defined in P-boxes 

- These are simple index permutations: re-orderings 

- Often, P-boxes are used together with S-boxes 

   - Create chain: S-boxes → P-box → S-boxes, etc. 

   - P-box takes the output from S-boxes 

   - P-box distributes bits of **one** S-box on to as many of the following S-boxes as possible 

## DES Encryption and Decryption 



https://www.tutorialspoint.com/cryptography/data_encryption_standard.htm 



Source: Wikipedia 

## The Strength of DES vs. 3DES vs. AES 

- 56-bit keys: 

   - 2<sup>56</sup> possible keys = 7.2 x 10<sup>16</sup> keys 

   - However, a rate of 1 billion = 10<sup>9</sup> keys combinations per second is reasonable for today’s multicore computers 

   - Supercomputer technology can run a rate of 10<sup>13</sup> encryptions per second 



Source: Cryptography and Network Security (Seventh Edition - William Stallings) 

## 3DES Encryption and Decryption 



- Purpose: DES replacement 

- 168-bit key, no brute-force attack 

- Has 2 or 3 keys 

## Block Cipher Design Principles 

- **Number of rounds:** The greater the number of rounds, the more difficult it is to perform cryptanalysis, even with a weak **function F** - provides the element of confusion in a Feistel cipher 

- **Design of function F:** 

   - Nonlinear 

   - Good avalanche properties algorithm (strict avalanche criterion (SAC)) 

   - Bit independence criterion (BIC) 

   - SAC and BIC appear to strengthen the effectiveness of the **confusion function.** 

- **Key Schedule Algorithm:** Should guarantee key/ciphertext SAC and BIC 



5. Advanced Encryption Standard (AES) 

## Finite Field Arithmetic 

- AES uses arithmetic in the finite field GF(2<sup>8</sup> ) with the irreducible polynomial m(x) = x<sup>8</sup> + x<sup>4</sup> + x<sup>3</sup> + x + 1 

- Multiplication of two bytes is defined as multiplication in the finite field GF(2<sup>8</sup> ) 

- Addition of two bytes is defined as the bitwise XOR operation. 

- Example: A = (a7 a6…a1 a0) and B = (b7 b6…b1 b0). ○ The sum A + B = (c7 c6…c1 c0), where ci=ai XOR bi 

## AES 

- Current de-facto block cipher on the Internet 

- Chosen in an open competition to be the successor of DES 

- Operates at key lengths of 128, 192, and 256 bit 

- Uses S-Boxes and P-Boxes 

- The S-Boxes actually describe a mathematical function that is believed to achieve excellent diffusion and confusion 

- Cryptanalysis attempts aimed to describe this function in easier terms, but so far have all failed 

- ● **Fun fact:** AES is not a cipher. The **Rijndael cipher** has been selected as the Advanced Encryption Standard (AES). 

## AES Structure 

Source: Cryptography and Network Security (Seventh Edition - William Stallings) 



## AES Encryption 

- The key is expanded into an array of 44, 32-bit words **w** [i] using the **key expansion algorithm** – takes 16-byte key (4 words) and produces a linear array of 176-byte (44 words) 

- Round key is 4 distinct words for AES-128, 6 words for AES-192, and 8 words for AES-256 

- Four different stages are used, one of permutation and three of substitution: ○ **Substitute bytes** : Uses an S-box to perform a byte-by-byte substitution of the block. ○ **ShiftRows** : A simple permutation. 

   - **MixColumns** : A substitution that makes use of arithmetic over GF(2<sup>8</sup> ). 

   - **AddRoundKey** : A simple bitwise XOR of the current block with a portion of the expanded key. 

### AES Encryption and Decryption 

Source: Cryptography and Network Security (Seventh Edition - William Stallings) 



## AES Encryption Round 



Source: Cryptography and Network Security (Seventh Edition - William Stallings) 

## Watch this Later 

<u>https://www.youtube.com/watch?v=gP4PqVGudtg</u> 



6. Block Modes 

## Block Modes for 3DES and AES 

- Ciphers must handle messages of arbitrary length 

- Solution: split messages in block and process them according to a **cipher block mode** . 

- These modes of operation can introduce new security problems if not designed and **used** properly. 

- **Classic block modes** only encrypt data 

   - E.g., Electronic Codebook (ECB), Cipher Block Chaining (CBC), Counter (CTR), … 

- Modern modes provide **authenticated encryption (AE, AEAD)** 

   - Combine encryption and integrity protection 

   - E.g., Galois Counter Mode (GCM), Counter-with-CBC-MAC (CCM) mode, … 

## Electronic Code Book Mode - ECB 

● Block-wise: ci = Enck(mi) 



Source: Cryptography and Network Security (Seventh Edition - William Stallings) 

## The Problem with ECB 





Simple message: good for teaching. Beyond that, do not use it 

## Cipher Block Chaining (CBC) 

● CBC encrypt: ci = Enck(ci-1⊕ mi) 

● CBC decrypt: mi = Deck(ci) ⊕ ci-1 



Source: Cryptography and Network Security (Seventh Edition - William Stallings) 





After using CBC 

## Other Block Modes 



Cipher Feedback Mode (CFB) 

Counter Mode (CTR) 



Output Feedback Mode (OFB) 



7. Pseudorandom Number Generation 

## The Use of Random Numbers 

- Key distribution and reciprocal authentication schemes 

- Session key generation 

- Generation of keys for the RSA public-key encryption algorithm (next week’s lecture) 

- Generation of a bit stream for symmetric stream encryption (mentioned above) 

## CSPRNG 

Cryptographically Secure Pseudo-Random Number Generator 

- A Pseudorandom Number Generator **(PRNG)** outputs a **deterministic** sequence of numbers 

   - Takes a seed value as the start value 

   - Output sequence depends on the seed 

- A PRNG is cryptographically secure, i.e., a **CSPRNG** , if: 

   - It is computationally infeasible to brute-force the seed value (try all possible values) to correctly predict the output, and 

   - It is computationally infeasible to distinguish the output sequence from true randomness 

- Only option for the attacker is, in other words, to know the **seed** 

## PRNG 



So, how to generate “Seed”? 

Source: Cryptography and Network Security (Seventh Edition - William Stallings) 

## PRNG 





Source: Cryptography and Network Security (Seventh Edition - William Stallings) 

## The use of PRNG in Stream Ciphers 

##### **ChaCha20 and Salsa20** 

- Family of related ciphers by DJ Bernstein 

- ● Current de-facto standard for stream ciphers on the Internet 

- Basis of CSPRNG in OpenBSD and Linux 

**RC4** 



- Used to be de-facto standard for TLS/SSL 

- ● Feasible breakage in 2013 

- **● Avoid today** 

## Recap 



#### **We discussed:** 

- Basic terminology: Plaintext, Ciphertext and Key 

- ● Kerckhoffs’ Principle 

- Historical ciphers 

- Traditional ideas of symmetric encryption - substitution and transposition 

- Information theoretic view - confusion and diffusion 

- One Time Pad 

- Block Ciphers and Stream Ciphers 

- S-Boxes, P-boxes, and Feistel Networks 

- DES and AES 

- Cipher Block Modes 

- Pseudorandom number generator 




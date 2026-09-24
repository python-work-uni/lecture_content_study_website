# Week 5 Asymmetric Cryptography 



Dr. Thilini Dahanayaka 

School of Computer Science, The University of Sydney 

## Announcements 

- Student representative 

- Assignment 1 - Any questions? 

- Assignment 1 Submission Instructions - Please read the assignment description carefully. 

- A break between tutorials and assignments 

## Agenda 

- Asymmetric/Public-key cryptography 

- Key exchange 

- Elliptic curve arithmetic and elliptic curve cryptography (ECC) 

   - Non-Examinable (for information only) 

## Recommended Reading 

- Cryptography & Network Security - 7th Edition by William Stallings 

   - **Chapter 9** – Public-key Cryptography and RSA 

   - **Chapter 10** – Other Public-key Cryptosystems 



1. Asymmetric/Public Key Cryptography 

## Public-key Cryptography 

- Symmetric cryptography is based on shared keys and scrambling of messages to achieve confusion and diffusion. 

- Public-key cryptography is a change of paradigm in two respects: 

   - Each participant has a public key (publicly distributed) and a private key (secret) 

   - Anyone may use the receiver’s public key to encrypt a message 

   - Only the receiver (owner of the private key) can decrypt it 

   - Hence also known as asymmetric cryptography 

- This form of cryptography is based on mathematical problems with certain properties 

- A number of mathematical problems are believed to have the desired properties. ○ But no proof yet! 

## Public-key Cryptography 



**Confidentiality** - Encrypt by the public key and decrypt by the private key. Anyone can encrypt. But only the receiver can decrypt, because only they have the private key. 



**Origin Authentication** - Encrypt by private key and decrypt by public key. Anyone can decrypt. But only the receiver could have encrypted it because only they have the private key. 

## Public-key Cryptography - Applications 

- Encryption/Decryption, Digital Signatures, and Key Exchange 

- We will discuss RSA, Diffie-Hellman, Elliptic Curve and Digital Signature Schemes (DSS) 



## Trapdoor Properties 

- We are looking for a function with the following properties: 

   - **Computationally fast** to compute the function value **_f(x) = y_** 

   - **Computationally infeasible** to compute the inverse function **_f_**<sup>**_-1_**</sup> **_(y)= x_** 

   - **Unless** we are in possession of a piece of information that allows to speed it up dramatically. 

   - Hence the name “ _trapdoor function_ ”. 

   - ○ **Corollary:** It must be **computationally infeasible** to compute the private key from the public key (without the trapdoor information) 

## Classic Trapdoor Candidate Problems 

● **Discrete Logarithms in Modular Arithmetic:** It is computationally infeasible to compute the discrete logarithm modulo p, for certain p. (Diffie and Hellman, 1976) **Discrete Logarithm Problem (DLP):** Given **_y, p, g_** satisfying the equation **_y = g_**<sup>**_x_**</sup> **_mod p_** where **_p_** is a prime number and **_g_** is primitive root of **_p_** , how can we find **_x_** ? 

- **RSA Problem:** It is computationally infeasible to compute the e<sup>th</sup> root of an integer modulo n, for certain n. 

When **_c = m_**<sup>**_e_**</sup> **_mod n_** and **_c, e,_** and **_n_** are known can you find **_m_** ? 

Both the Discrete Logarithm and the RSA problem have the property ‘computationally infeasible’. However they become ‘easy to compute’ with additional information (i.e., private key). 

## Recap: Coprime Numbers & Euler’s Phi function 

- We say two numbers are coprime if they share only one divisor, and that divisor is 1 

   - Example: 8 and 27 are coprime: 

      - 8 = 2 · 2 · 2, and 27 = 3 · 3 · 3 

- We define ℤ*n  as all non-negative integers < n that are coprime to the integer n ○ Example: n = 12. Then, ℤ*12= {1, 5, 7, 11} 

- ℤ*n is useful: it is an Abelian group under multiplication. Euler’s Phi Function (also called at the totient function) defines the number of elements in ℤ*n. 

   - For example, ɸ (12) = 4. 

- When n is a product of two primes p and q where p ≠ q, there is an easier way to calculate ɸ (n) 

   - In that case ɸ (n) = (p-1)(q-1) 

## The RSA Problem 

- RSA is developed in 1977 by Ron Rivest, Adi Shamir, and Len Adleman at MIT 

- The RSA problem allows us to build a trapdoor function. It is defined for a particular class of functions. 

## RSA Key Derivation and Encryption/Decryption 

- 1) Let p and q, p  ≠ q be prime 

   - 6) Now we have the keys 

- In practice: **very** large numbers 

   - (e,n) is the public key 

   - (d,n) is the private key 

- 2) Define n = p · q, (we call n as the modulus) 

      - At this point we delete p, q, and ϕ(n) permanently 

- 3) Use Euler’s totient function to calculate                 ϕ(n) = (p - 1)(q - 1) 

- 4) Choose 1 < e < ϕ(n),  gcd(e, ϕ(n)) = 1 

   - i.e., e is coprime with ϕ(n) 

   - ○ One way: choose e > max(p, q) to be prime ○ Testing primality of an integer is fast 

   - Let m be the plaintext and c be the cipher text 

   - 7) Encryption: c = m<sup>e</sup> mod n 

- 5) Calculate d such that d ≡ e<sup>-1</sup> mod ϕ(n) 

   - 8) Decryption: m = c<sup>d</sup> mod n 

- i.e., d is the modular inverse of e 

## RSA - Toy Example 

- 1) Let p=7 and q=11 

   - 6) Now we have the keys 

- 2) n = p · q ⇒ n = 77 

         - (13,77) is the public key 

         - (37,77) is the private key 

- 3) ϕ(n) = (p - 1)(q - 1) = (7-1)(11-1)= 6 x 10 = 60 

      - Let 3 be the plaintext and c be the cipher text 

- 4) Let’s select e as 13 

   - Note that 13 is less than 60 and is coprime with 60 

- 5) Calculate d such that 13d mod 60 = 1 

   - 7) Encryption: c = 3<sup>13</sup> mod 77 = 38 

- i.e., d is the modular inverse of e 

- ○ We get d = 37 

- 8) Decryption: m = 38<sup>37</sup> mod 77 = 3 

## The RSA Problem 

- RSA encryption is defined as a function from ℤ/nℤ to ℤ/nℤ : 

   - RSA : ℤ/nℤ → ℤ/nℤ [Recall ℤ/nℤ is a commutative ring] 

   - Note: n is not prime, but product of two primes. 

- We had a very good reason to choose RSA to work over ℤ/nℤ 

   - Exponentiation in ℤ/nℤ is fast to compute [Recall exponentiation by squaring] 

   - In other words, computing c = m<sup>e</sup> mod n is very efficient 

- But getting the **e**<sup>**th**</sup> root of **√c** to get the original **m** is believed to be infeasible 

- Note that RSA cannot uniquely encrypt values greater than n; such values are reduced modulo n, so decryption returns a value less than n, not the original input. 

## The RSA Problem 

- By now it is clear that due to its mathematical nature, RSA can encrypt only numbers. More specifically only the number in ℤ/nℤ. 

- That means sender and receiver must use a mapping of numbers to characters to make this useful: a ⇒ 1, b ⇒ 2. 

## The RSA Problem - Full example 



Source: Cryptography and Network Security 

(Seventh Edition - William Stallings) 

## Security of RSA 

- The security of RSA rests on 

   - Obtaining the e<sup>th</sup> root of a number in ℤ/nℤ is computationally infeasible unless you know d 

   - ○ Factoring n = pq, for very large p and q, is computationally infeasible 

   - This is for now though - quantum risks later. Australia plans to get rid of RSA by 2030 

- p and q, p  ≠ q, must be very large. 

- Encoding n needs thousands of bits (RSA key lengths: 2048 bit and more) 

- p and q, p≠ q, must not be too close together (allows forms of fast factoring) 

   - In practice, there are many more limiting factors 

   - Not every key is a good key 

- Never implement RSA yourself and use in production 

## Attacks on RSA 

- Five possible approaches: 

   - **Brute force:** This involves trying all possible private keys. 

   - **Mathematical attacks:** There are several approaches, all equivalent in effort to factoring the product of two primes. 

   - **Timing attacks:** These depend on the running time of the decryption algorithm. 

   - **Hardware fault-based attack:** This involves inducing hardware faults in the processor that is generating digital signatures. 

   - **Chosen ciphertext attacks:** This type of attack exploits properties of the RSA algorithm (e.g. Malleability) 

## Never use RSA without Padding 

- RSA is not secure to use without padding: 



**Malleability:** Malleability in RSA means that an attacker can modify a ciphertext in a predictable way so that the decrypted plaintext is also changed in a related, predictable way, without knowing the private key. 

**Example** 

- Attacker intercepts ciphertext c 

- Attacker computes modified ciphertext and send to the receiver: 

   - **c'≡c** ⋅ **2**<sup>**e**</sup> **mod n** 

- Receiver c' and obtains 2m 

   - **(c')**<sup>**d**</sup> **mod n ≡ (c** ⋅ **2**<sup>**e**</sup> **mod n)**<sup>**d**</sup> **mod n ≡ 2m** 

   - A slightly hand-wavy proof is available in lecture notes 

- Result is valid-looking, not random 

- Receiver cannot detect that the message was altered 

- ● **Key idea:** Vanilla RSA preserves structure → tampering yields a predictable, manipulated plaintext (not garbage) 

- This is a generic result, the scalar multiplication can be any number, not just 2. 

- Recall, this is a Chosen Ciphertext Attack (CCA) 

## Never use RSA without Padding 

#### **No ‘semantic security** ’ 

- An attacker can forward-compute (likely) messages and see if they match a given ciphertext. 

- ● Deterministic encryption and public key is out -> Chosen Plain Text Attacks (CPA) 

- Lack of randomness 

#### **Solution** 

- Sophisticated padding, which adds randomness on encryption and removes it on decryption. 

- Padding is crucial, but non-trivial! Today, we use OAEP (Optimal Asymmetric Encryption Padding). 

## Hybrid Encryption 

**RSA has two key problems** 

- **Problem 1:** Public-key cryptography is slow - long keys! 

   - RSA is 100-1000 times slower than AES 

- **Problem 2:** Needs a mapping from characters to numbers to be useful 

**Solution: Hybrid Encryption** 

- Therefore, in general we don’t use RSA continuously. Rather we use hybrid cryptography using RSA to quickly establish a symmetric key. 

## Hybrid Encryption 

### **Almost all public-key encryption uses hybrid encryption in practice.** 

- Generate random symmetric key k 

- Encrypt actual message as cm = Enck(m) 

- Encrypt k as ck  = EncPK(k)  using receiver’s public key 

- ● Send (ck , cm) 



2. Key Exchange 

## Key Exchange 

- There are many public-key cryptosystems besides RSA. 

- One of the best-known ones is **not used for encryption** , but for key exchange. 

- Question to solve: ‘Can Alice and Bob want to establish a shared symmetric key without a **purely listening attacker** being able to obtain the key?’ 

- How do they do that? 

- Finite fields come to our aid. 

## Diffie-Hellman 

- First published algorithm that implemented public-key (trap-door) principle 

- Became the basis for: 

   - Diffie-Hellman Key Exchange 

   - ElGamal encryption/decryption 

   - Digital Signature Standard (DSA/DSS) 

- Diffie-Hellman is based on finite fields 

## Discrete Logarithm Problem 

- Just as with factorization and the e<sup>th</sup> root before over our special ring, there is another trapdoor problem. 

- It is computationally infeasible to compute a logarithm over a finite field, if the prime number used to construct the field is large enough. 

**Discrete Logarithm Problem (DLP):** Given **_y, p, g_** satisfying the equation **_y = g_**<sup>**_x_**</sup> **_mod p_** where **_p_** is a prime number and **_g_** is primitive root of **_p_** , how can we find **_x_** ? 

● But if you have one extra piece of information (‘private key’), then it suddenly becomes ‘easy’. How do we make use of it? 

## Finite Fields Revisited: Primitive Roots 

- Let p be prime. We know ℤ/pℤ is a finite field. 

- Elements of ℤ/pℤ are {0, 1, ... , p - 1} 

- You can define a new group over the numbers ○ ℤp*  = {1, ... , p - 1} (with multiplication operation) 

- 

- ● You can also show: there is a special element g ∈ ℤp 

- Every number a ∈ ℤp*  is a power of g 

- So, actually, ℤp*  = {g0 = 1, g1  =  ... , gp-2 = ...} 

- 

- ● g is called a primitive root (or generator) of ℤp 

## Diffie-Hellman Key Exchange 



<!-- Start of picture text -->
Let p be prime, and g, a generator for ℤp*<br>Alice<br>Bob<br>● Choose random value a < p<br>● Choose random value b < p<br>● Compute X = g a   mod p<br>●<br>Compute Y = g b   mod p<br>● Send X to Bob<br>● Send Y to Alice<br>● Compute k = Y a   mod p<br>●<br>Compute k = X b   mod p<br>Y a  mod p = (g b ) a  = g ab  = (g a ) b   = X b  mod p<br> Both sides obtain the same k value<br><!-- End of picture text -->

DH Key exchange allows key establishment over an insecure channel, under a passive 

attacker 

## Person-in-the-Middle Attack 

   - When the attacker is active, the standard DH key exchange is not secure 

      - **Attacker** 

      - **Alice Bob** ● Choose random values c,d < p 

      - Choose random value a < p ● Compute ● Choose random value b < p 

      - <sup>a</sup> mod p ○ X’ = g<sup>c</sup> mod p ● Compute Y = g<sup>b</sup> mod p 

      - ○ Y’ = g<sup>d</sup> mod p ● Send Y 

      - ● Send X’ to Alice and Y’ to Bob 

- Choose random value a < p 

- ● Compute X = g<sup>a</sup> mod p ● Send X 



<!-- Start of picture text -->
Compute k1 = X’ a   mod p<br>Compute k2 = Y’ b   mod p<br>Compute k1 = X c   mod p<br>Compute k2 = Y d   mod p<br><!-- End of picture text -->

## Person-in-the-Middle-Attack 

- The key exchange protocol is vulnerable to such an attack because it does not authenticate the participants. 

● **Solution:** Digital signatures and public-key certificates (more on this later) 

- We will discuss those topics in the next lecture 



3. Elliptic Curve Cryptography (Non-Examinable) 

## Elliptic Curve Cryptography (ECC) 

The following is a very brief introduction. 

- Our schemes so far are defined for rings and fields constructed with the help of the mod operation - i.e., we use modular arithmetic 

- Elliptic curves E(a,b) are defined by equations of the form y<sup>2</sup> =x<sup>3</sup> +ax+b 

- When defined over a finite field, they produce a finite set of points 

- A group can be defined over these points using point addition 

- This allows us to define a Discrete Logarithm Problem (ECDLP) ○ ECDLP is harder per bit than classical DLP 

- Therefore, elliptic curve cryptography achieves the same security with much shorter keys ○ Typical ECC keys: 256 bits (very common)384 bits (high security) 

## Elliptic Curve Cryptography 

##### **Diffie-Hellman (classical setting)** 

* 

- Group: ℤp 

- Operation: multiplication mod p 

- Computation: a<sup>k</sup> mod p (repeated multiplication) 

- Key idea: Security comes from the Discrete Logarithm Problem (DLP) 

- **Key Transition** 

- So far, we have used groups derived from modular arithmetic 

- We now construct a different Abelian group with the same goal 

**Elliptic Curve Cryptography (ECC): same idea, different group** 

- Elements: points on a curve over a finite field ℤp 

- Operation: point addition i.e., kP=P + P + ⋯ + P 

- Given P and Q=kP, it is computationally infeasible to recover k. 

- **Note:** All arithmetic is performed modulo p (implicitly) 

## Elliptic Curves - Geometric Intuition 

##### **Geometric Intuition** 

- Consider E(1,1) which is y<sup>2</sup> =x<sup>3</sup> +x+1 

- We define O: the point at infinity (identity element) 

- This is an imaginary point to complete the math 

##### **Point addition** 

- Take two points P and Q on the curve 

- Draw the line through P and Q 

- The line intersects the curve at a third point 

- Reflect this point across the x-axis: This gives P+Q 

##### **Key Properties** 

- The negative of a point: -P = (x,-y). i.e., reflection across x-axis 

- Three points on a line sum to zero: P+Q+R = 0 



##### **Special Case related to ECC** 

- What if P=Q? Use the tangent line at P 

- The tangent intersects the curve at another point. Reflect it across the x-axis. This gives 2P 

## Elliptic Curves over a Finite Field 

##### **Elliptic Curves over** ℤ **p** 

- We now define elliptic curves over a finite field ℤp 

- Now the curve equation becomes Ep(a,b) 

   - y<sup>2</sup> =x<sup>3</sup> +ax+b (mod p) 

##### **Example curve over** ℤ **23** 

- Let’s consider E23(1,1): y<sup>2</sup> =x<sup>3</sup> +x+1 (mod 23) 

- Check if point (x,y)=(9,7) lies on the curve: 

   - 7<sup>2</sup> ≣ 9<sup>3</sup> +1.9+1 (mod 23) 

   - 49 ≣ 739 (mod 23) 



- 3 ≣ 3 

##### **Points on the curve E23(1,1)** 

- The curve consists of 

   - All pairs of (x,y) satisfying the above equation 

   - Plus O, the point at the infinity 

- This forms a finite set of points 



Points (other than O) on the curve E23(1,1) 

## Elliptic Curves over a Finite Field 



Points (other than O) on the curve E23(1,1) 

## Elliptic Curves over a Binary Field GF(2<sup>m</sup> ) 

##### **Transition from Prime Fields** 

- Previously, we used prime fields ℤp over an Elliptic Curve 

- Now, we define curves over binary fields GF(2<sup>m</sup> ) [Recall - We did something similar in AES] 

- Elements are polynomials with coefficients in GF(2) (bit strings) 

- Arithmetic is done modulo an irreducible polynomial 

##### **Curve Equation** 

- y<sup>2</sup> + xy = x<sup>3</sup> + ax<sup>2</sup> + b 

- Addition/multiplication is in GF(2<sup>m</sup> ) 

##### **Field Generator** 

- Let g be a primitive element (generator) of GF(2<sup>4</sup> ) 

- Every non-zero field element can be expressed as a power of g: 

   - GF(2<sup>4</sup> )∗={g<sup>0</sup> ,g<sup>1</sup> ,g<sup>2</sup> ,…,g<sup>14</sup> } 

## Elliptic Curves over a Binary Field GF(2<sup>4</sup> ) 

##### **Example Curve and point** 

- Let’s consider the curve y<sup>2</sup> + xy = x<sup>3</sup> + ax<sup>2</sup> + b where a= g<sup>4</sup> and b=1 



- We can denote this curve as 

- Let’s consider the test point (x,y) = (g<sup>5</sup> , g<sup>3</sup> ) and verify  whether it is on the curve 

##### **Verification** 

y<sup>2</sup> + xy = x<sup>3</sup> + ax<sup>2</sup> + b (g<sup>3</sup> )<sup>2</sup> + g<sup>5</sup> g<sup>3</sup> = (g<sup>5</sup> )<sup>3</sup> + g<sup>4</sup> (g<sup>5</sup> )<sup>2</sup> + 1 g<sup>6</sup> + g<sup>8</sup> = g<sup>15</sup> + g<sup>14</sup> + 1 

##### 1100+0101 = 0001+1001+001 

1001 = 1001 ⇒ Point (x,y) = (g<sup>5</sup> , g<sup>3</sup> )  is on the curve 

##### **Properties of GF(2**<sup>**4**</sup> **)** 

- We select f(x) = x<sup>4</sup> +x+1 as the irreducible polynomial and g as 0010 (i.e., g=x). 

- Now we can develop powers of g as below 



- Let’s calculator g4 which is x<sup>4</sup> . x<sup>4</sup> is greater than the largest degree polynomial that can be supported by 4 bits (which is x<sup>3</sup> ). So we need to calculate. x<sup>4</sup> = x<sup>4</sup> mod (x<sup>4</sup> +x+1) 

x<sup>4</sup> = x<sup>4</sup> mod (x<sup>4</sup> +x+1) 1) In GF addition and subtraction is = x<sup>4</sup> - (x<sup>4</sup> +x+1) the same done through XOR. = x<sup>4</sup> + (x<sup>4</sup> +x+1) = x+1 2) Adding the same element twice = 0011 results in zero. 

## Elliptic Curves over a Binary Field 





The Elliptic Curve 

## Elliptic Curve Cryptography (ECC) 

- Consider the equation Q = kP where Q, P ∈ Ep(a, b) and k< p ○ It is hard to determine k  given P, Q → discrete logarithm problem for elliptic curves 

- Example: consider the group E23(9,17) 

   - Defined by: y<sup>2</sup> mod 23 = (x<sup>3</sup> + 9x + 17) mod 23 

   - Find discrete logarithm k of Q = (4, 5) to base P = (16, 5) 

   - The only way to do this is brute force 

      - P = (16,5) ⇒ 2P = (20,20) ⇒ 3P = (14,14) ⇒ 4P = (19,20) ⇒5P = (13,10) ⇒ 6P = (7,3) ⇒ 7P = (8,7) ⇒ 8P = (12, 17) ⇒ 9P = (4,5) ⇒ k is 9 

- In practice, k would be very large, thus the brute-force approach infeasible 

## Elliptic Curve Diffie-Hellman Key Exchange (ECDH) 



- Both users A and B (and any attacker) know a,b,q,G,n 

- These are system-wide public parameters 

- G is a base point (generator) on the curve 

- n is the order of G. That is nG=O.  Usually n is chosen to be a large prime 

- Public keys are computed as: PA= nA x G, PB= nB x G 

- This scalar multiplication is efficient 

- Private keys nA and nB are kept secret 

- Even with PA and G, attacker cannot compute nA 

- ● Security relies on the hardness of the Elliptic Curve Discrete Logarithm Problem 

- Both parties compute the same key 

nA ∗ PB  = nA ∗ (nB ∗ G) = nB ∗ (nA ∗ G) = nB ∗ PA 

## EC El-Gamal Encryption 

● Public parameters: Elliptic curve Eq(a,b), generator point G with large order n, message encoded as curve point Pm 

Alice (sender) 

Bob (receiver) 

1. Select private key _nA_ where nA < n 

2. Compute public key _PA_ = nA × G 

3. Choose random integer _k_ (new for each message) 

4. Send ciphertext: Cm = {kG, Pm + kPB} 

1. Select private key _nB_ where nB < n 

2. Compute public key _PB_ = nB × G (shared publicly) 

3. Receive Cm = { kG, Pm + kPB } 

4. Recover: Pm = (Pm + kPB) − nB × (kG) 

kPB acts as a one-time mask on Pm . This is the embedded ECDH shared secret. PB is B’s public key 

Works because nB × (kG) = k × (nBG) = kPB  i.e., The mask cancels out 

**Why is k random and chosen fresh each time?** Reusing k for two different messages leaks information. An attacker can XOR the two ciphertexts and eliminate the mask, exposing the relationship between messages. A fresh k per message prevents this. 

## EC El-Gamal Encryption - Example 

- Consider the global (system-level) parameters: E257(0, -4): y<sup>2</sup> = x<sup>3</sup> – 4,  G(2, 2) 

- Encryption 

   - Bob’s private key nB  = 101, Bob’s public key PB  = nBG = 101(2, 2)=(197, 167) 

   - ● Alice wants to send Pm  = (112, 26) and choose k = 41. Compute kG = 41(2,2) = (136, 128) ● Alice encrypts: kPB  = 41(197, 167) = (68, 84) and Pm  + kPB  = (112, 26) + (68, 84) = (246, 174). ● Alice sends: Cm  = {C1, C2} =  {(136, 128), (246, 174)} to Bob 

- Decryption 

   - Bob computes: C2 - nBC1  = (246, 174) - 101(136, 128) = (246, 174) - (68, 84) = (112, 26) 

## Security of ECC 

- The security of ECC depends on how difficult it is to determine k given kP and ○ Elliptic curve logarithm problem 

- The table compares various algorithms by showing comparable key sizes in terms of computational effort for cryptanalysis 

- Pay attention to key length of RSA and ECC 



## Post Quantum Cryptography (PQC) 

- **Breaking Asymmetric Cryptography** 

   - Shor's algorithm, can efficiently factor large numbers and compute discrete logarithms 

   - ○ RSA, Diffie-Hellman Key Exchange, ECC will be vulnerable 

- **Symmetric Cryptography is More Resilient** 

   - Grover's algorithm, provides a quadratic speedup for brute-forcing the keys of symmetric ciphers 

   - Symmetric key's effective security level is halved 

   - A 256-bit key would offer security comparable to a 128-bit key against a quantum adversary 

   - Doubling Key Sizes  as a solution. 

- **Post Quantum Cryptography (PQC)** 

   - Lattice-based, Code-based, Hash-based cryptography 

## Recap 

- **We discussed:** 

   - Public-key cryptosystem and its applications 

   - RSA algorithm and attacks on RSA 

   - Hybrid encryption 

   - Diffie-Hellman key exchange and person-in-the-middle attack 

   - An overview of the elliptic curves and Elliptic curve cryptography 



- ECC Diffie-Hellman key exchange 

- The security of ECC 

- Post Quantum Cryptography (PQC) 


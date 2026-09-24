,,,, The University of Sydney School of Computer Science Dr Suranga Seneviratne Senior Lecturer - Security 



## **Asymmetric Cryptography** 

Recommended Reading 

**Cryptography and Network Security (** 7<sup>_th_</sup> **Edition - William Stallings) Chapter 9** – Public-key Cryptography and RSA **Chapter 10** - Other Public-key Cryptosystems. 

These lecture notes are given to you to assist with understanding the lecture content better. This content is prepared based on the above book chapters. You are not allowed to upload this material to any internet source or share it with anyone else. 

# **1 Asymmetric/Public-key cryptography** 

Symmetric cryptography uses the same shared key for both encryption and decryption relying on the principles of substitution (confusion) and permutation (diffusion) to secure data. In contrast, public-key cryptography utilizes two distinct keys for encryption and decryption (hence also known as asymmetric cryptography), relying on mathematical functions with specific properties beyond substitution and permutation. Asymmetric algorithms have the following important characteristics. 

- It is computationally infeasible to determine the decryption key given only knowledge of the cryptographic algorithm and the encryption key. 

- In some algorithms like RSA, from a mathematical point of view, either of the two related keys can be used for encryption while the other can be used for decryption. 

## **1.1 Public-key Cryptosystems** 

The essential steps of using public-key cryptography are as follows. 

1. Each user gets a pair of keys (private key and public key) 

2. Each user places one key (public key) as a publicly accessible file. The companion key (private key) is kept confidential. 

3. If Bob wishes to send a **confidential message** to Alice, Bob encrypts the message with Alice’s public key before sending it, and upon receiving the message, Alice decrypts it using her private key as shown in Figure 1a. Since only Alice has access to her private key, only Alice can decrypt this message; therefore, confidentiality is achieved. 

4. If Bob wants to send a message to Alice guaranteeing that the message was sent by him ( **origin authentication** ), Bob encrypts the message with his own private key as shown 

August 26, 2026 

Cybersecurity Engineering - Lecture Notes 







<!-- Start of picture text -->
(a) Confidentiality (b) Origin Authentication<br><!-- End of picture text -->

Figure 1: Public-key Cryptography 

Source: Cryptography and Network Security (Seventh Edition - William Stallings) 

in Figure 1b. Upon receiving the message Alice can decrypt it using Bob’s public key. **Digital signatures** ; a key application of public-key cryptography follows this approach. In this case, not only Alcie but anyone who has access to Bob’s public key can verify the origin of the message. 

It is important to note that we refer to the conceptual usage of keys here in the confidentiality and origin authentication settings. In practice, we don’t simultaneously use the same key pair for both purposes. 

Overall, in public key cryptography, all participants in the system have access to all other participants’ public keys, while each participant keeps the private keys confidential. Table 1 summarizes the applications of public-key cryptosystems. 

|**Algorithm**|**Encryption/Decryption**|**Digital Signature**|**Key Exchange**|
|---|---|---|---|
|RSA|Yes|Yes|Yes|
|Elliptic Curve|Yes|Yes|Yes|
|Diffie-Hellman|No|No|Yes|
|DSS|No|Yes|No|



Table 1: Applications for Public-key Cryptosystems 

## **1.2 Requirements for Public-key Cryptography** 

Following conditions that should be met by algorithms that can be used in public-key cryptography. 

1. It is computationally easy for a party _B_ to generate a key pair (public key _PUb_ , private key _PRb_ ). 

2. It is computationally easy for a sender _A_ , knowing the public key and the message to be encrypted, _M_ , to generate the corresponding ciphertext: 

      - _C_ = _E_ ( _PUb, M_ ) 

3. It is computationally easy for the receiver _B_ to decrypt the resulting ciphertext using the private key to recover the original message: 

   - _M_ = _D_ ( _PRb, C_ ) = _D_ [ _PRb, E_ ( _PUb, M_ )] 

August 26, 2026 

Cybersecurity Engineering - Lecture Notes 

4. It is computationally infeasible for an adversary who knows the public key, _PUb_ , to determine the private key, _PRb_ . 

5. It is computationally infeasible for an adversary who knows the public key, _PUb_ , and a ciphertext, _C_ , to recover the original message _M_ , without knowing the private key _PRb_ . 

We may introduce a sixth requirement, which, while beneficial, may not be essential for all public-key applications. 

6. The two keys can be applied in either order: 



The above requirements can be aggregated to the requirement of a **trap-door one-way function** . 

**One-way function** : A function that maps a domain into a range such that every function value has a unique inverse, with the condition that the calculation of the function is easy, whereas the calculation of the inverse is infeasible: 

_Y_ = _f_ ( _X_ ) –> Easy 



**Trap-door one-way function** : A function that is relatively easy to compute in one direction but computationally difficult to invert without the knowledge of additional information called the " _trapdoor_ ". 

_Y_ = _fk_ ( _X_ ) –> Easy if _k_ and _X_ are known 

_X_ = _fk_<sup>_−_1(</sup><sup>_Y_)–>Easyif</sup><sup>_k_and</sup><sup>_Y_areknown</sup> _X_ = _fk_<sup>_−_1(</sup><sup>_Y_)–>Infeasibleif</sup><sup>_k_isunknown</sup> 

**Classic trap-door candidate problems** : 

1. **Discrete logarithms in modular arithmetic** 

It is computationally infeasible to compute the discrete logarithm modulo _p_ for certain _p_ . (Diffie and Hellman, 1976) 

**Discrete Logarithm Problem (DLP)** : Find _x_ , given _p_ (a prime number), _g_ (a primitive root of _p_ ), and _y_ satisfying the equation, 

_y_ = _g_<sup>_x_</sup> mod _p_ 

2. **RSA problem** 

   - It is computationally impossible to compute the _e_<sup>_th_</sup> root of an integer modulo _n_ , for certain _n_ . 

August 26, 2026 

Cybersecurity Engineering - Lecture Notes 

**RSA Problem** : Find _m_ , given known values _c_ , _e_ , and _n_ satisfying the equation, 



Both the Discrete Logarithm problem and the RSA problem have the property that ‘computationally infeasible’ becomes ‘easy to compute’ with additional information. 

## **1.3 RSA Algorithm** 

The Rivest-Shamir-Adleman (RSA) [2] scheme was developed by Ron Rivest, Adi Shamir, and Len Adleman at MIT in 1977 and is the most widely accepted and implemented general-purpose approach to public-key encryption. RSA algorithm encrypts plaintext in blocks with each block having a binary value less than some number _n_ . 

RSA algorithm generates keys (values of _e_ , _d_ , and _n_ ) as follows. 

**Key Generation by Sender** Select _p_ , _q p_ and _q_ both prime, _p̸_ = _q_ Calculate _n_ = _p_ x _q_ Calculate _ϕ_ ( _n_ ) = ( _p −_ 1)( _q −_ 1) Select integer _e_ gcd( _ϕ_ ( _n_ ) _, e_ ) = 1; 1 _< e < ϕ_ ( _n_ ) Calculate _d d ≡ e_<sup>_−_1</sup> ( mod _ϕ_ ( _n_ )) Public Key: _PU_ = _{e, n}_ Private Key: _PR_ = _{d, n}_ 

Note that in the above key generation process, _ϕ_ ( _x_ ) denotes _Euler’s phi function_ that counts elements in Z<sup>_∗_</sup> _n_<sup>.</sup> 

**Encryption by Sender** 

Plaintext: _M < n_ Ciphertext: _C_ = _M_<sup>_e_</sup> mod _n_ 

Note that RSA encryption is defined as a function from Z _/n_ Z to Z _/n_ Z. The intuition behind this choice is that, as exponentiation in Z _/n_ Z is fast to compute, computing _C_ = _M_<sup>_e_</sup> mod _n_ is very easy (satisfies the second requirement above for public-key encryption). However, getting<sup>_√_</sup> _e C_ to get the original _M_ (decryption without knowing _d_ ) is believed to be **infeasibly hard** . 

August 26, 2026 

Cybersecurity Engineering - Lecture Notes 

## **Decryption by Receiver** 

Ciphertext: _C_ Plaintext: _M_ = _C_<sup>_d_</sup> mod _n_ 

RSA Algorithm - Example 

**Key generation** : Select two prime numbers as _p_ = 17 and _q_ = 11. Obtain _n_ = _pq_ = 17 _∗_ 11 = 187 Calculate _ϕ_ ( _n_ ) = ( _p −_ 1)( _q −_ 1) = 16 _∗_ 10 = 160 Select _e_ such that e is coprime to _ϕ_ ( _n_ ) = 160 and _e < ϕ_ ( _n_ ) _→ e_ = 7 Determine _d_ such that _d ∗_ 7 _≡_ 1 mod 160 and _d <_ 160. 23 _∗_ 7 = 161 = (1 _∗_ 160) + 1 _→ d_ = 23 _PU_ = _{_ 7 _,_ 187 _}_ , _PR_ = _{_ 23 _,_ 187 _}_ **Encryption** : Encrypt plaintext _M_ = 88. _C_ = 88<sup>7</sup> mod 187 = 11 **Decryption** _M_ = 11<sup>23</sup> mod 187 = 88 

It should be noted that while encrypting numerical values with RSA is straightforward, non-numerical characters must be mapped to numerical values before encryption. 

### **1.3.1 Security of RSA** 

The security of RSA depends on the following: 

- Getting<sup>_√_</sup> _e C_ to get the original _M_ is believed to be **infeasibly hard** unless _d_ is known. 

- Factoring _n_ = _pq_ , for very large _p_ and _q_ , is computationally infeasible. Otherwise, _d_ can be easily calculated. 

The defense against brute forcing _d_ is to use a large key space for _d_ . The larger the number of bits in _d_ , the more secure the system becomes. However, it is important to recognize that increasing the key size can also slow down the system due to the more complex calculations required for key generation, encryption, and decryption. 

To make factoring _n_ = _pq_ computationally infeasible, 

- _p_ and _q_ , _p_ must be **very large** . 

- _p_ and _q_ , _p_ must not be too close together 

There are many other factors that contribute to the security of a key. Consequently, it is not recommended to implement RSA yourself for use in production environments. 

Five possible approaches to attacking RSA are, 

August 26, 2026 

Cybersecurity Engineering - Lecture Notes 

- **Brute force** : This involves trying all possible private keys – feasible only against smaller keys. 

- **Mathematical attacks** : There are several approaches, all equivalent in effort to factoring the product of two primes. 

- **Timing attacks** : These depend on the running time of the decryption algorithm. 

- **Hardware fault-based attack** : This involves inducing hardware faults in the processor that is generating digital signatures. 

- **Chosen ciphertext attacks** : This type of attack exploits properties of the RSA algorithm (e.g. Malleability). 

Malleability of RSA 

First, Eve listens for a ciphertext that she wants to crack: 



Next, she takes this ciphertext, multiply it by a random value raised to the power of Bob’s _e_ value) and get Bob to decrypt it: 



If Eve can determine the decrypted value for this ciphertext, she can determine the original message as: 

( _c_<sup>_′_</sup> )<sup>_d_</sup> = ( _c × r_<sup>_e_</sup> )<sup>_d_</sup> = ( _m_<sup>_e_</sup> _× r_<sup>_e_</sup> )<sup>_d_</sup> = _m_<sup>_e×d_</sup> _× r_<sup>_e×d_</sup> = _m × r_ since ( _m_<sup>_e_</sup> )<sup>_d_</sup> mod _n_ must equal _m_<sup>1</sup> mod _n_ . 

Eve obtains the original plaintext by dividing the resulting plaintext by _r_ . 

**Note** the Chosen-Ciphertext-Attack (CCA) assumption here. We assume that the attacker has the ability to get _c_<sup>_′_</sup> decrypted. 

**RSA and Padding** : The vanilla form of RSA is not secure. For example, it is vulnerable to CCA because of malleability. Basic RSA encryption does not provide semantic security due to its lack of randomness. Since RSA is deterministic—meaning the same plaintext encrypted with the same public key will always produce the same ciphertext—it is vulnerable to attacks like Chosen Plaintext Attacks (CPA). In such attacks, an adversary can encrypt likely messages and compare the results to a given ciphertext to infer the original plaintext. To achieve semantic security, modern RSA implementations incorporate padding schemes that introduce randomness, ensuring that the same plaintext encrypted multiple times results in different ciphertexts. Today, we use OAEP (Optimal Asymmetric Encryption Padding) for this. 

## **1.4 Hybrid Encryption** 

Public-key cryptography has the following limitations. 

- Public-key cryptography is slow, particularly when long keys are used to enhance security 

August 26, 2026 

Cybersecurity Engineering - Lecture Notes 

• It requires a mechanism to map numbers to characters for practical use 

To address these limitations, most applications employ hybrid encryption. In this approach, public-key encryption like RSA is used to quickly establish a symmetric key, and subsequent communications are secured using symmetric key encryption. 

# **2 Diffie-Hellman Key Exchange** 

Diffie–Hellman algorithm is the first published public-key algorithm published by Diffie and Hellman [1] in 1976 and its best-known application is secure key exchange which can subsequently be used for symmetric-key encryption. Other applications of the Diffie–Hellman algorithm include _ElGamal encryption/decryption_ and _Digital Signature Standard (DSA/DSS)_ . 

The security of the Diffie–Hellman algorithm relies on the difficulty of computing discrete logarithms. Specifically, it is considered **computationally infeasible to compute a discrete logarithm over a finite field** , provided the prime number used to define the field is sufficiently large. However, if additional information, such as the private key, is available, this computation becomes computationally feasible. 

**Recap: Discrete Logarithm Problem (DLP)** : Can we find _x_ , given _p_ (a prime number), _g_ (a primitive root of _p_ ) and _y_ satisfying the equation, 



## **2.1 Diffie-Hellman Algorithm** 

Figure 2 summarizes the Diffie-Hellman algorithm for exchanging a shared key between two users _A_ and _B_ who have already shared two publicly known values _p_ (a prime number) and _g_ (a primitive root of _q_ ). Accordingly, each user selects a random integer _a_ and _b_ such that they are less than _p_ and computes _X_ = _g_<sup>_a_</sup> mod _p_ and _Y_ = _g_<sup>_b_</sup> mod _p_ , respectively. The _a_ and _b_ are kept private (i.e., private keys of A and B), and the _X_ and _Y_ values are publicly exchanged by the two users(i.e., X and Y are the public keys of the two users). 

After the exchange, each user can separately and independently calculate the same key; i.e., A will compute _Y_<sup>_a_</sup> mod _p_ , and B will compute _X_<sup>_b_</sup> mod _p_ . Both of these values will be equal and that will be the shared key; _K_ = _Y_<sup>_a_</sup> mod _p_ = _X_<sup>_b_</sup> mod _p_ . 



Through this process, the two parties have exchanged a secret value _K_ which is typically used as a shared key. 

An adversary who can only passively observe the key exchange will only know the values _p_ , _g_ , _X_ , and _Y_ and will be forced to take a discrete logarithm to determine one of the private keys 

August 26, 2026 

Cybersecurity Engineering - Lecture Notes 



Figure 2: Diffie-Hellman Algorithm Source: Cryptography and Network Security (Seventh Edition - William Stallings) 

_a_ or _b_ to calculate the shared key _K_ . 

For instance, if calculating _b_ , the adversary needs to compute _b_ such that _Y_ = _g_<sup>_b_</sup> mod _p_ , which is solving the DLP. For large primes, this task is computationally infeasible. Hence, the shared secret key _K_ is considered secure from a passive observer. 

## **2.2 Person-in-the-middle-attack** 

While the Diffie-Hellman algorithm in Figure 2 is secure against passive eavesdroppers, it is vulnerable to person-in-the-middle-attacks as shown in Figure 3. Accordingly, the adversary first observes the publicly shared values of _p_ and _g_ , and then generates two separate sets of private and public key pairs. The attacker then positions themselves between the two communicating users, _Alice_ and _Bob_ , intercepting and replacing the messages transmitted during the key exchange. By doing this, the attacker performs two independent key exchanges: one with _Alice_ and another with _Bob_ . At the end of this process, the attacker establishes separate secret keys _K_ 2 and _K_ 1 with _Alice_ and _Bob_ respectively and can use these keys to perform a person-in-the-middle-attack (intercept and replace original messages) on future communications between Alice and Bob. 

Person-in-the-middle attacks in Diffie-Hellman key exchange can be overcome by using digital signatures, where each party signs their public key with their private key, allowing the other party to verify the authenticity of the key using the corresponding public key, ensuring that the exchanged keys have not been tampered with by an attacker. 

August 26, 2026 

Cybersecurity Engineering - Lecture Notes 



Figure 3: Person-in-the-middle-attack on Diffie-Hellman key exchange 

## **2.3 Post-Quantum Cryptography (PQC)** 

PQC focuses on developing algorithms that remain secure even in the presence of quantum computational power. Some of the key concepts of PQC include, 

- **Lattice-Based Cryptography** is based on the hardness of problems related to lattice structures in high-dimensional spaces. 

- **Code-Based Cryptography** relies on the hardness of decoding random linear codes. 

- **Hash-Based Cryptography** leverages the security properties of hash functions for cryptographic tasks. 

# **3 Practice Quiz** 

**Question 1:** Select all that is TRUE for the RSA algorithm. 

**a)** One factor that makes RSA secure is the difficulty in prime number factorisation. 

- **b)** RSA is still considered secure irrespective of the key size. 

- **c)** Padding is required to make RSA secure. 

**d)** RSA is a symmetric key encryption algorithm 

**e)** You can choose any two prime numbers to construct an RSA scheme 

August 26, 2026 

Cybersecurity Engineering - Lecture Notes 

**_Explanation_** _:_ The security of RSA lies on two factors. The first is the difficulty of prime factorization. The second is the difficulty of finding the _eth_ root of a number under modulo n. Therefore **a)** is TRUE. 

**b)** is FALSE. These days we consider only key sizes above 2048 bits as secure for RSA. 

**c)** is TRUE. A semantically secure cryptosystem is one in which only a small amount of information about the plaintext can be extracted from the ciphertext. Textbook RSA doesn’t have any randomness. Therefore, it doesn’t have any semantic security. As a result, we add padding. 

**d)** in FALSE. RSA is an asymmetric cryptosystem. 

**e)** in FALSE. We can’t select any two prime numbers. For starters, we can’t select two small prime numbers. Even for large prime numbers, there are restrictions. We can’t select prime numbers that are close to each other. Then the factorization problem becomes easier. 

**Question 2:** For _p_ = 11 and _q_ = 17 and choose _e_ = 7. Apply the RSA algorithm to find the ciphertext when the plaintext message is 88. 

**a)** 23 **b)** 64 

**c)** 11 **d)** 54 

In the RSA notation, we have been given p=11, q=17 and e=7. We can find, 

_n_ = _pq_ = 187 

_ϕ_ ( _n_ ) = ( _p −_ 1)( _q −_ 1) = 160 (As _e_ is given we don’t need it. But note that _e_ is less than _ϕ_ ( _n_ ).) 

_C_ = _M_<sup>_e_</sup> mod _n_ = 88<sup>7</sup> mod 187 = 11 

**Question 3:** In an RSA system the public key of a given user is e = 31, n = 3599. What is the private key of this user? 

**a)** 3031 

**b)** 2412 **c)** 2432 

**d)** 1023 

**_Explanation_** _:_ In the RSA notation, we have been given e=131 and n=3599. We can find 

p= 59 and q = 61 (By finding the prime factors of 3599) and n = pq = 3599 

_ϕ_ ( _n_ ) = ( _p −_ 1)( _q −_ 1) = 58 _×_ 60 = 3480 

We know the private and the public key have the property. 

August 26, 2026 

Cybersecurity Engineering - Lecture Notes 

_ed ≡_ 1 mod ( _ϕ_ ( _n_ )) i.e. 31 _d ≡_ 1 mod (3480) 

Check them one by one. 

31 x 3031 mod (3480) = 1. Therefore, 3031 is the correct answer. You can verify the rest. 

E.g. 31 x 2412 mod (3480) = 1692. 

**Question 4:** The ............. protocol enables two users to establish a secret key using a public-key scheme based on discrete logarithms. 

**a)** Micali-Schnorr **b)** Elgamal-Fraiser **c)** Diffie-Hellman 

**d)** Miller-Rabin 

**_Explanation_** _:_ We learned only one public key cryptography-based key exchange scheme in the class. That is the Diffe-hellman key exchange. The rest are either made up or not related. For example, Micali-Schnorr is a random number generator algorithm, and Miller-Rabin is a primality test. 

**Question 5:** The basic Diffe-Hellamn key exchange protocol is vulnerable to a ............. attack because it does not authenticate the participants. 

**a)** one-way function 

**b)** time complexit 

**c)** chosen ciphertext 

**d)** person-in-the-middle 

**_Explanation_** _:_ An attacker can store and replay messages in the Diffe-Hellman key exchange and conduct an active person-in-the-middle attack. Diffe-Hellman key exchange is secure only against a passive attacker. For protection against active attackers, a modified version of the process is required, called as the signed Diffe-Hellman key exchange. 

**Question 6:** The Diffie-Hellman algorithm depends on the difficulty of computing discrete logarithms for its effectiveness. TRUE or FALSE. **a)** TRUE 

**b)** FALSE 

**_Explanation_** _:_ There are two key mathematical problems that have trapdoor properties. The discrete logarithm problem and the RSA problem. DH key exchange relies on the discrete logarithm problem. 

**Question 7:** Read this article on how the advances in quantum computing can affect symmetric and asymmetric cryptography differently. 

```
https://builtin.com/cybersecurity/post-quantum-cryptography
```

August 26, 2026 

Cybersecurity Engineering - Lecture Notes 

Based on your reading, which cryptographic scheme will become more vulnerable when quantum computing becomes feasible? 

**a)** Symmetric cryptography 

**b)** Asymmetric cryptography 

**_Explanation_** _:_ Once quantum cryptography becomes available, some of the previously infeasible problems become feasible. As a result, asymmetric cryptography becomes vulnerable. 

**Question 8:** Asymmetric and symmetric encryption have their own advantages and disadvantages. For example, asymmetric cryptography is slower and not suitable for real-time communications. On the other hand, symmetric cryptography is faster and more suitable for real-time data encryption and bulk data encryption. However, key distribution is an issue with symmetric encryption. As a result, most of the applications, especially in communications settings, use hybrid cryptography. Watch the following video on hybrid cryptography and decide whether the following statement is TRUE or FALSE. 

```
https://www.youtube.com/watch?v=VPvZbMXfv_0
```

“Hybrid cryptography uses asymmetric cryptography to establish a symmetric key between two parties that can be used for subsequent communications.” TRUE or FALSE 

**a)** TRUE 

**b)** FALSE 

**_Explanation_** _:_ The answer is TRUE. Hybrid cryptography assumes the receiver’s public key is already shared with the sender. The sender generates a session key (a symmetric key), encrypts it with the receiver’s public key, and sends it to the receiver. The receiver can decrypt the message using their private key and recover the session key. Now, both parties have access to the shared session key, which can be used for any subsequent communication. 

**Question 9:** A considerably larger key size can be used for ECC compared to RSA. TRUE or FALSE. 

**a)** TRUE **b)** FALSE 

**_Explanation_** _:_ The statement is False. In general, ECC key sizes are much shorter than RSA, which is an advantage of ECC. This is because the elliptic curve logarithm problem is more difficult than the RSA problem. 

**Question 10:** Consider the elliptic curve _E_ 7(2 _,_ 1); that is, the curve is defined by _y_<sup>2</sup> = _x_<sup>3</sup> +2 _x_ +1 with a modulus of _p_ = 7. Which of the following is NOT a point in _E_ 7(2 _,_ 1)? Not examined - for information only 

**a)** (0,1) **b)** (1,5) **c)** (3,4) 

August 26, 2026 

Cybersecurity Engineering - Lecture Notes 

## **d)** (1,2) 

The equation we are after is _y_<sup>2</sup> mod 7 = _x_<sup>3</sup> + 2 _x_ + 1 mod 7. We check each answer separately as shown in the following table. 



Figure 4: Points on an Elliptic Curve 

Only (3,4) is not satisfying the equation. 

August 26, 2026 

Cybersecurity Engineering - Lecture Notes 

# **References** 

- [1] W. Diffie and M. E. Hellman, “Multiuser cryptographic techniques,” in _Proceedings of the June 7-10, 1976, national computer conference and exposition_ , 1976, pp. 109–112. 

- [2] R. L. Rivest, A. Shamir, and L. Adleman, “A method for obtaining digital signatures and public-key cryptosystems,” _Communications of the ACM_ , vol. 21, no. 2, pp. 120–126, 1978. 

August 26, 2026 

Cybersecurity Engineering - Lecture Notes 


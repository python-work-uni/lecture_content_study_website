The University of Sydney School of Computer Science Dr Suranga Seneviratne Senior Lecturer - Security 



## **Symmetric Cryptography** 

Recommended Reading 

**Cryptography and Network Security (** 7<sup>_th_</sup> **Edition - William Stallings)** 

- **Chapter 2** – Introduction to Number Theory 

- **Chapter 3** – Classical Encryption Techniques 

- **Chapter 4** – Block Ciphers and Data Encryption Standards 

- **Chapter 5** – Finite Fields 

- **Chapter 6** – Advanced Encryption Standards 

- **Chapter 7** – Block Cipher Operation 

- **Chapter 8** – Random bit Generation and Stream Ciphers 

Also, please read the separate handouts given for cryptography-related math concepts. 

These lecture notes are given to you to assist with understanding the lecture content better. This content is prepared based on the above book chapters. You are not allowed to upload this material to any internet source or share it with anyone else. 

# **1 Introduction** 

Cryptography is an indispensable tool in the design of secure protocols and systems. It is used to ensure: 

- **Data Confidentiality:** Achieved through encryption. 

- **Data Integrity:** Ensured by signatures and Message Authentication Codes (MACs). 

- **Authentication and Data Origin Verification:** Accomplished using signatures and Message Authentication Codes (MACs). 

- **Non-repudiation:** Implemented with signatures. 

A fundamental understanding of cryptography principles is crucial for many careers in computing. 

In this unit, we introduce cryptography from a functional point of view with less emphasis on mathematical or formal perspectives (i.e., proofs). However, we cover a significant amount of basic math you need to know to understand foundational cryptographic concepts. Before you read this, please make sure that you read and understand the introduction to number theory and abstract algebra lecture notes. 

August 20, 2026 

Cybersecurity Engineering - Lecture Notes 

## **1.1 Challenges in Cryptography** 

Cryptography is a double-edged sword, complex and full of subtleties. Inconsiderate application of cryptographic techniques can lead to insecure systems. Worse, these systems may appear secure to developers and users while being vulnerable to attackers. An example is the historical GSM A5/1 algorithm. 

## GSM A5/1 algorithm 

The GSM-based second-generation cellular systems in 90’s used the secret and proprietary A5 stream cipher design. This algorithm uses a 64-bit secret key and has two main variants. The A5 ciphers are responsible for encryption of the data transmitted between the mobile device and the Base Transceiver Station (BTS). 

Historical records show that there were some serious cryptographic weaknesses found in 1994. By the late 90s, multiple works showed that combinations of cryptanalytic and hardware attacks could be used to conduct practical attacks against the A5/1 algorithm. The specific internal structure of the GSM communication protocol allowed the possibility of conducting the most powerful cryptographic attack, a **ciphertext-only attack** . Here, an adversary that eavesdrops a communication and gathers a sequence of consecutive encrypted frames can recover the secret key with moderate computational power. 

**Source:** The (in)security of proprietary cryptography by Roel Verdult [ **?** ]. 

### **1.1.1 Implementation Challenges** 

Implementing cryptography requires extensive experience and knowledge of hardware and programming languages. Therefore, it is advised: 

- Do not implement your own cryptography for real-world applications. Always use known and standardised methods. 

- To become proficient, practice, find a mentor, and engage in discussions with other implementers. It is a long career path with no shortcuts. 

## **1.2 Definition of Cryptography** 

Cryptography is the science of securely transmitting data over space and time. 

- **Spatially:** Ensuring data security over physical distances. For example, this means securing communication between one of your browser tabs and a remote web server such as `www.google.com` . 

- **Temporally:** Keeping data secure for a long duration into the future. For example, this might involve encrypting sensitive archival data today in a way that it remains secure and unreadable even decades from now, despite advancements in computing power and cryptographic techniques. 

## **1.3 Core Topics in This Unit** 

In this unit, we focus on the following core aspects of cryptography: 

August 20, 2026 

Cybersecurity Engineering - Lecture Notes 

- **Confidentiality:** Achieved through encryption methods. 

   - Symmetric encryption 

   - Asymmetric (public-key) encryption 

- **Integrity:** Ensured through both symmetric and asymmetric methods. 

   - Message Authentication Codes (MACs) 

   - Signatures 

   - Hash functions 

- **Authentication:** Implemented through various protocols. 

While there are other applications of cryptography such as for achieving Non-repudiation, Privacy, Anonymity, those are not covered in this unit. 

# **2 Cryptography - Definitions** 

Basic Definitions and Notations 

We can define the following components of a crypto-system. 

**Plaintext:** Plain-text _p_ is the non-encrypted, unprotected data. It is built from the symbols from the alphabet _R_ = _{r_ 1 _, r_ 2 _, ..., rn}_ . For example, common English comes from the alphabet {[A-Z],[a-z],[0-9]}. 

**Encryption:** The encryption process encodes plaintext using the cipher function, _Enc_ and a key _ke_ and produces the ciphertext _c_ . That is _Encke_ ( _p_ ) = _c_ . 

**Ciphertext:** Ciphertext _c_ may not necessarily come from the same alphabet as the plain text. It may not even be of the same size as the plaintext alphabet. We denote the ciphertext alphabet as _S_ = _{s_ 1 _, s_ 2 _, ..., sm}_ . 

**Decryption:** The decryption process decodes ciphertext using the decipher function, _Dec_ and a key _kd_ and produces back the plaintext _p_ . That is _Deckd_ ( _c_ ) = _p_ . 

**Symmetric cryptography** - In symmetric cryptography, the encryption key is the same as the decryption key, i.e., _ke_ = _kd_ , or _kd_ can be derived from _ke_ . This is also known as **shared key cryptography** . Symmetric cryptography algorithms usually shuffle symbols around and map them to others. 

**Asymmetric cryptography** - In asymmetric cryptography, the encryption key is different from the decryption key, i.e., _ke̸_ = _kd_ or it is infeasible to derive _kd_ from _ke_ . This is also known as **public key cryptography** . Asymmetric cryptography algorithms are based on the hardness of some mathematical problems. 

August 20, 2026 

Cybersecurity Engineering - Lecture Notes 

# **3 Kerkhoff’s Principle** 

We have discussed the Kerkhoff’s Principle several times by now in our discussions on why open design is important in cybersecurity. Formally Kerkhoff’s Principle can be defined as follows. 

## Kerkhoff’s Principle 

The security of a given cryptographic mechanism must depend only on the security of the cryptographic keys used, but never on the mechanism or anything else, except the keys, being a secret. 

In fact, almost all the mainstream cryptographic algorithms that are used in practice are publicly disclosed. For example, we know exactly how AES (Advanced Encryption Standard) or RSA (Rivest–Shamir–Adleman) work. Their security is purely dependent on the secrecy of the used keys. Why this is important is because when the design is disclosed, many researchers and engineers can look into the algorithm and find possible flaws. In fact, when NIST (National Institute of Standards and Technology) runs competitions to establish new cryptographic standards, they invite the global cryptographic community to submit algorithms for public review and scrutiny. This process ensures that the winning algorithms have undergone rigorous analysis and testing by experts worldwide. The transparency of these competitions, like the one that led to the selection of AES, helps to ensure that the chosen standards are robust, secure, and free from hidden vulnerabilities. 

There have been many historical examples of not following the Kerkhoff’s principle end in disasters. We already discussed the GSM A5/1 algorithm earlier. Another example is what happened with the Content Scrambling System of DVDs. 

## DVD Content Scrambling System (CSS) 

The CSS was put in place to prevent DVDs made for one region of the world being played in another region. It also prevented copying of DVD content, whether legal or illegal, from the DVD to any other media. It also prevented (due to the non-disclosure of the algorithm to the public) viewing of movies and other content on the DVDs on software or hardware DVD players not approved by the Copy Control Association (CCA) [ **?** ]. 

CSS relied on the secrecy of its algorithm for security. The DVD Consortium assumed that by keeping the algorithm secret, the system would remain secure. However, once the algorithm was reverse-engineered and made public, the entire copyright system was compromised. 

# **4 Symmetric Cipher Model** 

Figure 1 shows the schematic overview of the symmetric cipher model, which is the focus of this lecture. Note here that the Encryption and the Decryption keys are the same. 

August 20, 2026 

Cybersecurity Engineering - Lecture Notes 



Figure 1: Basic operation of symmetric key cryptography [1]) 

# **5 Historical Ciphers** 

## **5.1 Traditional Concepts** 

**Transposition** and **substitution** are two fundamental techniques used in historical symmetric ciphers. **Transposition** involves shifting the positions of symbols in a message according to a specific rule, thereby altering the order of the symbols without changing the symbols themselves. **Substitution** , on the other hand, replaces symbols with other symbols based on a predetermined rule. Both transposition and substitution are typically governed by a key that parameterizes the rule, ensuring that only those with the correct key can correctly decipher the message (e.g., the shift). It’s also common for transposition and substitution to be combined within the same cipher, enhancing the complexity and security of the encryption. Figure 2 shows two basic examples of substitution and transposition. 



Figure 2: Examples for substitution and transposition 

## **5.2 Breaking the Substitution/Caesar cipher** 

The substitution cipher is by no means secure today. First, due to its monoalphabetic nature, it still preserves the patterns of natural language. For example, in English, the most common letter is ‘E’. An attacker could easily identify that the most frequent symbol after substitution is likely to be ‘E’ and then start guessing other letters, possibly using a dictionary lookup to assist. This idea is called _frequency analysis_ . Moreover, brute-forcing a substitution cipher would take only a few seconds on a modern computer. 

We can extend the idea of the Caesar cipher to build a polyalphabetic cipher. 

August 20, 2026 

Cybersecurity Engineering - Lecture Notes 

# **6 Vigenère Cipher** 

The Vigenère Cipher is a _poly-alphabetic cipher_ where each plain text character is encrypted with a different Caesar cipher. Which Caeser cipher to use is determined by the corresponding letter of the key. Here is an example. Consider our key is the word `CRYPTO` and our plaintext is `THISISAGREATDAY` . Encryption and decryption happen as below. 



<!-- Start of picture text -->
C R Y P T O C R Y P T O C R Y<br>T H I S I S A G R E A T D A Y<br>C=2, T=19 C=2, A=0 C=2, D=3<br>Encryption = C+T mod 26 = 21 Encryption = C+A mod 26 = 2  Encryption = C+D mod 26 = 5<br>V Y G H B G C X P T T H F R W<br>C R Y P T O C R Y P T O C R Y<br>V=21, C=2 C=2, C=2 F=5, C=2<br>Decryption = V-C mod 26 = 19  Decryption = C-C mod 26 = 0  Decryption = F-C mod 26 = 3<br>T H I S I S A G R E A T D A Y<br>Encryption<br>Decryption<br><!-- End of picture text -->

Figure 3: Vigenère Cipher - Encryption and Decryption Process 

## **6.1 Breaking the Vigenère Cipher** 

**If you know the key length** - The key idea to note in Vigenère Cipher is that there will be positions where the plain text will be encrypted by the same character in the key. For example, in the figure, the plain text characters “T”, “A”, and “D” are encrypted by the key character “C”. Now if you assume you have enough encrypted text, then you can use frequency analysis to guess what might be the cipher character for the letter “E”. 

Say you find that among all the cipher characters that were encrypted by the first character of the key is character “G”. Now you can use this information to recover the first character of the key. `6-c mod 26 = 4` , where `c` is the first character in the key. This results in c = 2, meaning the first character of the key is “C”. Next, you can do the same for the cipher characters that were encrypted from the second character of the key can recover it, and so on. 

**If you don’t know the key length** - You assume different key lengths and repeat the process until you get sense descriptions. However, with natural language, you can make your life easier by doing the Kasiski Examination. 

## **6.2 Kasiski Examination** 

Kasiski allows us to find the key length in some circumstances. The idea is to find repeated patterns in cipher text with the hope that some will correspond to situations where the same plain text is encrypted by the same parts of the key. This is not, in particular, coincidental because the natural language has a number of repetitive patterns (e.g., the word ‘the’ will be repeated quite a lot in English language text) and given the short key sizes of the Vigenère Cipher, there will be occasions where the same plain text was encrypted by the same part of the key. See the below example. For simplicity, we ignore the space and period characters. We assume our key is “ `KEY` ” and our plain text is “ `THE BELOW IS AN EXAMPLE FOR KASISKI TEST. THE TEXT IS ENCRYPTED UTILISING THE VIGENERE CIPHER.` ”. 

August 20, 2026 

Cybersecurity Engineering - Lecture Notes 



<!-- Start of picture text -->
1<br>Plaintext  T H E B E L O W I S A N E X A M P L E F O R K A S I S K I T E S T<br>Key  K E Y K E Y K E Y K E Y K E Y K E Y K E Y K E Y K E Y K E Y K E Y<br>Encryption  D L C L I J Y A G C E L O B Y W T J O J M B O Y C M Q U M R O W R<br>1st<br>34  61<br>Plaintext  T H E T E X T I S E N C R Y P T E D U T I L I S I N G T H E V I G<br>Key  K E Y K E Y K E Y K E Y K E Y K E Y K E Y K E Y K E Y K E Y K E Y<br>Encryption  D L C D I V D M Q O R A B C N D I B E X G V M Q S R E D L C F M E<br>2nd 3rd<br>67<br>Plaintext  E N E R E C I P H E R<br>Key  K E Y K E Y K E Y K E<br>Encryption  O R C B I A S T F O V<br><!-- End of picture text -->

Figure 4: Kasiski Examination 

The observation here is that the number of characters between the two repeated patterns is a multiple of the key length. Therefore, we can conclude the following. 

- The distance between the 1st and 2nd repetition is 33. Therefore the key size must be one of 1, 3, 11 and 33, which are factors of 33. 

- The distance between the 2nd and 3rd repetition is 27. Therefore the key size must be one of 1, 3, 9 and 27. 

- The common factors are 1 and 3. We can ignore 1 as it is a very weak key that can be brute-forced. 

- So the possible key size is 3. 

Once you know the key size, you identify the cipher text characters that were encrypted by the same key character and conduct frequency analysis to infer each character of the key. _This step will still include some guesswork and trial and error similar to any other case of cryptanalysis._ 

# **7 Ideas Behind Modern Ciphers** 

In Vigenère Cipher, we saw how polyalphabetic ciphers addressed an observed shortcoming of monoalphabetic ciphers: that frequency analyses (in many forms) can yield the key. Modern ciphers extend these ideas further. 

Claude Shannon identified two design goals for modern ciphers. 

August 20, 2026 

Cybersecurity Engineering - Lecture Notes 

## Confusion and Diffusion 

**Confusion:** This principle ensures that the relationship between the ciphertext and the key is as complex and unpredictable as possible, i.e. _each symbol in ciphertext must depend on several symbols in key_ . The goal is to make it difficult for an attacker to determine the key even if they have access to the ciphertext. Substitution techniques, where one piece of data (e.g., a letter or bit) is replaced with another, are commonly used to achieve confusion. By substituting elements in a complex way, modern ciphers introduce confusion. 

**Diffusion:** This principle spreads the influence of each plaintext bit across multiple ciphertext bits, making it difficult to discern any patterns, _i.e., every ciphertext symbol must depend on many plaintext symbols_ . Diffusion is often achieved through transposition, where the positions of bits or characters are shifted around according to a specific pattern, thus spreading the plaintext information throughout the ciphertext. 

# **8 Attacks on Cryptographic Systems** 

A cryptographic system is compromised if an adversary can obtain plaintexts for certain ciphertexts or the adversary can obtain the decryption key _kd_ when given _ke_ . **Cryptanalysis** is the science of decrypting without knowledge of the key. Depending on the attacker’s capabilities. 

- **Ciphertext-only** - The attacker may only see ciphertexts. 

   - _Example_ - During World War II, many military communications were encrypted. If an attacker intercepted these encrypted messages (ciphertext) without knowing the corresponding plaintext or having any additional information, they would be in a ciphertext-only attack scenario. The challenge would be to decrypt the intercepted messages purely by analyzing the ciphertext. 

- **Known plaintext** - The attacker may see some plaintexts and corresponding ciphertexts. _Example:_ During World War II, the Allies, particularly the British cryptanalysts at Bletchley Park, were able to break the Enigma cipher used by Nazi Germany because they knew certain plaintext phrases (such as weather reports or common military terms) and the corresponding ciphertexts. This known plaintext information helped them in analyzing the patterns in the Enigma’s encrypted messages, leading to the decryption of other messages. 

- **Chosen plaintext** - The attacker may choose a plaintext and see the corresponding ciphertext (standard model for asymmetric cryptography!). 

   - _Example_ - In the BEAST attack on SSL/TLS, the attackers are choosing plaintext blocks and studying the corresponding ciphertext blocks generated by the server’s encryption algorithm to uncover vulnerabilities and deduce the secret key. 

- **Chosen ciphertext** - The attacker may choose ciphertext and decrypted plaintext (so-called oracle attacks). 

   - _Example_ - In Bleichenbacher’s attack on PKCS1 v1.5, the attackers are exploiting a decryption oracle, submitting various ciphertexts, and studying the decrypted outputs to infer details about the decryption process and ultimately to uncover the secret key. 

August 20, 2026 

Cybersecurity Engineering - Lecture Notes 

# **9 Stream Ciphers vs. Block Ciphers** 

Symmetric ciphers can be categorised into two based on their operation. 

Stream Ciphers vs. Block Ciphers 

**Stream Ciphers:** A stream cipher encrypts data one bit or byte at a time. It takes a single bit or byte of plaintext and combines it with a corresponding bit or byte of a keystream (a sequence of bits derived from a secret key) to produce a bit or byte of ciphertext. This process continues in a stream, hence the name. E.g., RC4 (now considered insecure) and Salsa20 

**Block Ciphers:** A block cipher encrypts data in fixed-size blocks (typically 64 or 128 bits). It takes a block of plaintext, processes it with the secret key, and outputs a block of ciphertext of the same size. If the plaintext is smaller than the block size, padding is added to fill the block. E.g. DES (now considered insecure) and AES. 

# **10 Stream Ciphers** 

In stream cipher design, pseudo-random functions are employed to generate a keystream from a seed, which is typically derived from a secret key. The fundamental idea is to generate a keystream _b_ = _b_ 0 _, b_ 1 _, b_ 2 _, . . . , bn_ from the secret key _k_ by applying a cryptographic function _f_ ( _k_ ). This keystream is then combined with the plaintext _p_ = _p_ 0 _, p_ 1 _, p_ 2 _, . . . , pn_ using a bitwise operation, most commonly the XOR operation (denoted as _⊕_ ). The resulting ciphertext is obtained as _c_ = _p ⊕ b_ , where each bit of the plaintext is XORed with the corresponding bit of the keystream. 

One of the primary challenges in this process is ensuring that the keystream is as unpredictable as possible without knowledge of the secret key _k_ . Specifically, it should be computationally infeasible for an attacker to distinguish between a truly random keystream and one generated deterministically from the key _k_ . If an attacker could identify patterns or predict the keystream, the security of the encryption would be compromised. Therefore, the design of the pseudo-random function used to generate the keystream is crucial, as it must ensure that the keystream appears random and lacks any discernible patterns that could be exploited. 

Figure 5 illustrates a schematic overview of a stream cipher system. 



Figure 5: Basic operation of stream ciphers [1]) 

One-Time Pad is an example of a stream cipher. However, it is important to note that its key 

August 20, 2026 

Cybersecurity Engineering - Lecture Notes 

stream is completely random, as opposed to the pseudo-random key streams used in other stream ciphers. 

# **11 One-Time Pad** 

One-Time Pad (not to get confused with the One-Time Passwords) is a simple cipher that assumes a random key for each message you encrypt, and the key size is greater than the message itself. The encryption process is simply XORing the plain text with the key and the decryption process is vice versa. Here using XORing is not mandatory; you can also use modular arithmetic like `mod 26` . 

Figure 6 shows two instances where the same plain text is encrypted at two different instances. Note the two assumptions at work; i) key length is as long as the plain text, ii) the key is random and never repeated/reused. As a result, the cipher texts in the two instances are very different - which leads to the fundamental property of One-Time Pad - the resulting cipher text doesn’t show any relationship with the plain text. 



<!-- Start of picture text -->
Plain text  1 0 1 1 1 1 0 1 Plain Text  1 0 1 1 1 1 0 1<br>0 1 1 0 0 0 1 1 1 1 0 1 0 1 1 0<br>Key  Key<br>Cipher  1 1 0 1 1 1 1 0 Cipher  0 1 1 0 1 0 1 1<br>Text  Text<br>Cipher Text = Plain Text ⊕ Key Cipher Text = Plain Text ⊕ Key<br>(a) Encryption of the same cipher text at two different instances<br>Cipher  1 1 0 1 1 1 1 0 Cipher  0 1 1 0 1 0 1 1<br>Text  Text<br>0 1 1 0 0 0 1 1 1 1 0 1 0 1 1 0<br>Key  Key<br>Plain text  1 0 1 1 1 1 0 1 Plain text  1 0 1 1 1 1 0 1<br>Plain Text = Cipher Text ⊕ Key Plain Text = Cipher Text ⊕ Key<br>(b) Decryption of the received cipher text<br>Encryption<br>Decryption<br><!-- End of picture text -->

Figure 6: Operation of One-Time Pad 

We call this property as _“perfect secrecy”_ . That is, the cipher text does not convey any information about the content of the plain text. Essentially, this means no matter how much cipher text you have, it does not convey anything about what the plain text and the key were. This is why there is an emphasis in One Time Pad that the key can not be repeated. In fact, it can be proved that any _“perfect secrecy”_ scheme must use at least as much key material as there is plain text to encrypt. In terms of probabilities, it means that the probability distribution of the possible plain texts is independent of the cipher text. 

Nonetheless, the One-Time Pad is not that practical due to two reasons. 

- The key distribution is an issue - How can Alice and Bob securely exchange the key? If 

August 20, 2026 

Cybersecurity Engineering - Lecture Notes 

they already have the means to do that, the One-Time Pad is no longer required. 

- Related to that is the generation of that much of a volume of truly random keys. OneTime Passwords will not be able to handle the requirements of common applications that require frequent communications. 

## **11.1 Repeating the key in One-Time Pad** 

When the key is repeated (i.e., many time pads or looping one-time pads), the One-Time Pad can be broken similarly to how we broke the Vigenère Cipher earlier. However, there are other methods as well. An example of such a method is called “crib dragging”. 

- Let’s consider a One-Time Pad that uses XOR. 

- And consider two plain texts _P_ 1 and _P_ 2 encrypted by the same key _K_ 

- So we get _C_ 1 = _P_ 1 _⊕ K_ and _C_ 2 = _P_ 2 _⊕ K_ 

- Now assume the attacker gets hold of the two cipher texts, _C_ 1 and _C_ 2. The attacker can build a new string _P_ where _P_ = _C_ 1 _⊕ C_ 2, which can be simplified. _P_ = _C_ 1 _⊕ C_ 2 

_P_ = ( _P_ 1 _⊕ K_ ) _⊕_ ( _P_ 2 _⊕ K_ ) 

_P_ = _P_ 1 _⊕ P_ 2 (because _K ⊕ K_ is all zeros) 

This also means that _P_ 1 = _P ⊕ P_ 2 and _P_ 2 = _P ⊕ P_ 1 

- Using this information, the attacker can try “crib dragging”. The idea is to guess a word that can appear in one of the plan texts. For example, if it is English, and the text is sufficiently large, it is reasonable to assume the word “the” will be there somewhere in the plain text. So the idea is to try “the” in all possible positions in one of the plain texts, XOR them with _P_ and see whether some readable can be obtained. The process continues like this. 

- A worked example of the idea can be found here - `http://travisdazell.blogspot. com/2012/11/many-time-pad-attack-crib-drag.html` 

# **12 Block Ciphers** 

As mentioned before, block cyphers encrypt data in fixed-size blocks (typically 64 or 128 bits) as shown in Figure 7. It takes a block of plaintext, processes it with the secret key, and outputs a block of ciphertext of the same size. If the plaintext is smaller than the block size, padding is added to fill the block. 

August 20, 2026 

Cybersecurity Engineering - Lecture Notes 



Figure 7: Basic operation of block ciphers [1] 

In block ciphers, substitution is implemented through **Substitution boxes (S-boxes)** , while permutation (transposition) is carried out using **Permutation boxes (P-boxes)** . These components are executed across multiple rounds of the algorithm, which helps to enhance the diffusion and confusion properties. The rounds are structured in specific arrangements, often referred to as **‘networks’** , to ensure the effective mixing of the plaintext into ciphertext. 

# **13 Feistel Cipher** 

The Feistel cipher is a common structure used in block ciphers like DES, Blowfish, Twofish, and others. It divides the data block into two halves and processes them in multiple rounds. Each round follows the same basic structure as illustrated in Figure 8: 

1. **Splitting the Data:** 

Given a block of data _X,_ split it into two halves: _Ln_ and _Rn_ 



2. **Round Operations (for each round** _n_ **) :** The right-hand side half goes through a keyed function _F_ , and the output is XORed with the left-hand side, i.e. _Rn_ +1. The direct output of the function _F_ becomes _Ln_ +1. This process happens multiple times. We will learn what exactly happens inside _F_ under DES - basically, it consists of an arrangement with S and P boxes. 

August 20, 2026 

Cybersecurity Engineering - Lecture Notes 



Figure 8: Example Feistel Network [1] 

Beyond Feistel networks, there are other ways of arranging S-boxs and P-boxes, such as the Substitution Permutation Network (SPN) used in AES. 

# **14 Data Encryption Standards (DES)** 

DES encryption algorithm, originally published in 1977 and standardized in 1979, uses a key that, in each round, is transformed into a subkey derived from the actual key (round key). The algorithm includes a total of eight S-boxes, with the outputs from these S-boxes being sent through one P-box to ensure good diffusion across the S-boxes in the subsequent round. It is important to note that the 16 rounds utilized in this process are necessary to achieve the desired level of security. The algorithm employs a Feistel structure between rounds. As we discuss later, DES no longer considered secure. 

## **14.1 S-Boxes** 

S-boxes are basically look-up tables. They map a block of bits and output a block of bits. The mapping functions are carefully chosen. Usually, changing one bit in the input of the S-box will map to an output block where, on average, half of all bits are flipped (diffusion). There are two options to make the decryption possible. 

**Invertible S-Boxes:** If an S-box is invertible, it means that for every possible output of the S-box, there is a unique input that could have produced it. This property allows the decryption process to reverse the transformation applied during encryption. 

August 20, 2026 

Cybersecurity Engineering - Lecture Notes 

**Invertible Arrangement:** Even if the individual S-boxes aren’t invertible, the way they are combined and used in the overall encryption algorithm (such as in combination with other transformations) can still allow the entire encryption process to be reversed. This means the cipher as a whole is designed in such a way that decryption is possible, even if some components (like S-boxes) are not individually invertible. This is what DES uses. 

### **14.1.1 Example S-box - S[0] from DES** 



Figure 9: S[0] in DES 

Use like this: 

input string = ( _b_ 0 _, b_ 1 _, b_ 2 _, b_ 3 _, b_ 4 _, b_ 5) 

_b_ 0 and _b_ 5 give the row; ( _b_ 1 _, b_ 2 _, b_ 3 _, b_ 4) give the column. 

Interpret the number in that cell as binary. 

Example: 



Row: (11)2 = (3)10; Column: (1011)2 = (11)10 

Output: (14)10 = (1110)2 _→_ **1110** 

DES has eight S-boxes like this one. 

## **14.2 P-Boxes** 

Transposition in encryption is handled by P-boxes, which are simple index permutations or re-orderings of bits. P-boxes are often used in conjunction with S-boxes to create a chain where the output from S-boxes is passed through a P-box before being fed into subsequent S-boxes. The P-box redistributes the bits from one S-box across as many of the following S-boxes as possible, ensuring effective diffusion throughout the encryption process. 

August 20, 2026 

Cybersecurity Engineering - Lecture Notes 

## **14.3 Operation of DES** 



Figure 10: Building blocks of DES 

- DES accepts data blocks of 64-bits, and its key size is 56-bits. The round-key generator generates 16 48-bit round keys to use in the 16 rounds. 

- Inside each round is the Feistel arrangement where the function _F_ looks like the figure on the right. 

- Inside one round, the 64-bit input is split into two halves, left hand and right hand, 32 bits each. The right-hand side goes through the function F. The First 32 bits are expanded to 48 bits using the expansion box so that it is the same size as the round key. Next, the expanded output is XORed with the round key and resulting 48 bits intermediate output is sent to 8 S-Boxes. Note from the previous example that each S-box accepts 6-bit input, so the 48-bit output is split evenly among the 8 s-boxes. Recall also that the S-box output is 4 bits each, so the the 8 S-boxes result in 32 bits, making that output suitable for the next round. This process repeats 16 times. 

## **14.4 Security of DES** 

As it was mentioned earlier, DES is no longer considered secure. The major limitation of DES comes from its shorter key length. In DES there are 2<sup>56</sup> possible keys. That means the key space is _∼_ 7 _._ 2 _×_ 10<sup>16</sup> . At a rate of 10<sup>9</sup> keys per second (a multicore computer) or 10<sup>13</sup> keys per second (a supercomputer), DES can be broken in _≈_ 1 year or _≈_ 1 hour, respectively. As a result, we use AES that has larger key sizes of 128, 192, and 256 these days. The table in Figure 11 below provides a summary of the times taken to break each crypto scheme. 

August 20, 2026 

Cybersecurity Engineering - Lecture Notes 



Figure 11: Strength of DES and AES [1] 

## Example Calculation 

DES key space = 2<sup>56</sup> = 7 _._ 2 _×_ 10<sup>16</sup> 

If you are brute forcing the key, trying all possible combinations of the keys is the worst case. Usually, you will find the key much earlier than that. **So we assume that** **_on average_ once we tried half the amount of keys, we will get a hit.** 

This means we have to only try 2<sup>55</sup> keys. 

At 10<sup>9</sup> keys per second we need 2<sup>55</sup> _/_ 10<sup>9</sup> seconds. 

This is equal to _≈_ 36 _,_ 028 _,_ 797 seconds, and that is _≈_ 1 _._ 2 years. 

At 10<sup>13</sup> keys per second we need 2<sup>55</sup> _/_ 10<sup>13</sup> seconds. Which is _≈_ 3,600 seconds, which is only an hour. 

**The last row of the table has a typo. I hope you can figure it out !!** 

## **14.5 3DES** 

As an intermediate solution to the risks of DES, 3DES was introduced. It is basically applying DES three times, with a slight difference as illustrated in Figure 12. 



Figure 12: Encryption and Decryption in 3DES [1] 

August 20, 2026 

Cybersecurity Engineering - Lecture Notes 

3DES uses two keys ( _K_ 1 _, K_ 2) or three keys ( _K_ 1 _, K_ 2 _, K_ 3), giving effective key sizes of 112 bits (56 x 2) or 168 bits (56 x 3). The two options are there to balance between performance and security. 

Let’s follow the operation of the three key options. First, we take the plain text, _p_ and encrypt it using _K_ 1, i.e., we get _EK_ 1( _p_ ). Next, we use the decryption function of DES with _K_ 2 on this output. i.e., we get _DK_ 2( _EK_ 1( _p_ )). Note that we use the decryption function but with a different key, so we will not get the original plaintext back. Next, we do another round of encryption using _K_ 3 to obtain _C_ = _EK_ 3( _DK_ 2( _EK_ 1( _p_ ))). 

Why do we use the Encryption, Decryption, and Encryption sequence? Why not simply Encryption, Encryption, and Encryption? There are several reasons. One is backward compatibility. When using the same key in three steps, 3DES will again become DES. 

# **15 Block Cipher Design Principles** 

**Number of Rounds:** In block cipher design, the number of rounds plays a crucial role in determining the cipher’s resistance to cryptanalysis. A higher number of rounds increases the difficulty of breaking the cipher, even if the underlying function F is not particularly strong. This added complexity enhances the element of confusion, especially in Feistel ciphers, making it harder for attackers to deduce the relationship between the plaintext and ciphertext. 

**Design of Function F:** The function F within a block cipher should be nonlinear and exhibit strong avalanche properties, such as those defined by the strict avalanche criterion (SAC). Also, it is recommended for F to satisfy Bit Independence Criterion (BIC). 

Desired properties of F 

**Strict Avalanche Criterion (SAC):** Whenever a single input bit is complemented, each of the output bits changes with a 50% probability. 

**Bit Independence Criterion (BIC):** Output bits j and k should change independently when any single input bit i is inverted, for all i, j and k. 

**Key Schedule Algorithm:** The Key Schedule Algorithm generates one subkey for each round from the main key. In general, we would like to select subkeys to maximize the difficulty of deducing individual subkeys and the difficulty of working back to the main key. No general principles for this have yet been defined; SAC and BIC are desired here. 

# **16 Advanced Encryption Standards (AES)** 

Advanced Encryption Standards (AES) is the current de-facto block cipher on the Internet. It is the successor of DES. It operates in three key sizes: 128, 192, and 256. Its block size is 128 bits. AES also uses S-boxes and P-boxes. However, in contrast to DES, AES doesn’t use the Feistel Network. Rather, it is based on a substitution-permutation network (SPN). 

August 20, 2026 

Cybersecurity Engineering - Lecture Notes 

## **16.1 Finite Field Arithmetic** 

AES uses arithmetic in the finite field _GF_ (2<sup>8</sup> ) with the irreducible polynomial _m_ ( _x_ ) = _x_<sup>8</sup> + _x_<sup>4</sup> + _x_<sup>3</sup> + _x_ + 1. That means addition and multiplication are done differently. Please refer to the math background handouts to understand this further. 

## **16.2 AES Encryption and Decryption** 

The high-level flow of AES is shown in Figure 13. Overall, it takes 128-bit blocks and an M-bit key (128, 192, or 256) and has 10, 12, or 14 rounds, depending on the key size. For clarity for the rest of the discussion, let’s focus on 128-bit key size. 



Figure 13: Encryption in AES [1] 

**Key Expansion Algorithm** The key expansion process generates 11 round keys, each 128 bits in size, resulting in a total of 176 bytes (11 × 16 bytes). 

**Inside each round** four steps are happening. 

August 20, 2026 

Cybersecurity Engineering - Lecture Notes 

- **Substitute bytes:** Uses an S-box to perform a byte-by-byte substitution of the block. 

- **ShiftRows:** A simple permutation. 

- **MixColumns:** A substitution that makes use of arithmetic over _GF_ (2<sup>8</sup> ). 

- **AddRoundKey:** A simple bitwise XOR of the current block with a portion of the expanded key. 

# **17 Cipher Block Modes** 

Ciphers are designed to handle messages of arbitrary length by splitting them into blocks and processing these blocks according to a cipher block mode. However, if these modes of operation are not carefully designed and used, they can introduce new security vulnerabilities. Traditional block modes, such as Electronic Codebook (ECB), Cipher Block Chaining (CBC), and Counter (CTR), focus solely on data encryption. In contrast, modern modes offer authenticated encryption (AE, AEAD), which combines encryption with integrity protection. Examples of these advanced modes include Galois Counter Mode (GCM) and Counter-with-CBC-MAC (CCM). 

## **17.1 Electronic Code Book Mode – ECB** 

In ECB, each plaintext block is encrypted independently, as shown in Figure 14. That is _Ci_ = _Ei_ ( _Pi_ ) 



Figure 14: ECB [1] 

ECB has a major limitation, and as a result, it is not used at all these days. Most of the time, plaintext will have patterns that repeat (e.g. white background of an image). In ECB, the same plain text will generate the same cipher text. As a result, some patterns in the plaintext will be visible in ciphertext as well, as shown in the example in Figure 15. 

August 20, 2026 

Cybersecurity Engineering - Lecture Notes 



Figure 15: ECB Encryption Example 

## **17.2 Cipher Block Chaining – CBC** 

In CBC, each plaintext block is XORed with the previous ciphertext block before being encrypted. The first block is XORed with an initialization vector (IV) to ensure that even identical plaintext blocks result in different ciphertexts. 

This approach avoids the problem in Electronic Codebook (ECB), where identical plaintext blocks are encrypted into identical ciphertext blocks, making patterns in the plaintext easily detectable. By chaining the blocks together, CBC ensures that the encryption of each block depends on the previous one, effectively masking patterns and providing better security. The operation of CBC is shown in Figure 16. Now, the problem of the same plaintext being mapped to the same cypher text is no longer there, as shown in Figure 17. 



Figure 16: CBC [1] 



Figure 17: CBC Encryption Example 

**Initialization Vector (IV):** The IV is a random or pseudo-random value that is used as the first input in the encryption process. Its primary purpose is to introduce randomness into the encryption, ensuring that even if the same plaintext is encrypted multiple times with the same 

August 20, 2026 

Cybersecurity Engineering - Lecture Notes 

key, the resulting ciphertext will be different each time. 

The IV does not need to be kept secret. It is often transmitted along with the ciphertext to allow the decryption process to correctly reconstruct the original plaintext. Since the IV is not a secret, its role is not to provide security through secrecy but through the introduction of unpredictability. 

It is critical that the IV is never repeated when using the same encryption key. If the same IV is used with the same key for encrypting identical plaintext blocks, the resulting ciphertext blocks will also be identical. This can reveal patterns in the plaintext and compromise security, similar to the vulnerabilities seen in the ECB mode. 

Wired Equivalent Privacy (WEP) 

WEP, an early security protocol for wireless networks, uses the RC4 stream cipher, which relies on a combination of a secret key and an Initialization Vector (IV) to encrypt data. 

In WEP, the IV is only 24 bits long, which is relatively small. This small size means that after a certain amount of data is transmitted, the same IV is likely to be reused. In busy networks, IVs can start repeating very quickly. 

When the same IV is reused with the same secret key, RC4 generates the same key stream. If an attacker can capture multiple packets with the same IV, they can observe how the key stream interacts with different plaintexts. 

Plaintext Recovery: By analyzing these repeated key streams, especially if parts of the plaintext are known or predictable (like certain headers or protocol-specific information), an attacker can start to recover the plaintexts of other packets. Once enough packets are captured, the attacker can deduce the key stream and, eventually, the secret key itself. 

## **17.3 Counter Mode - CTR** 

Though CBC overcomes the limitations of ECB, it is inefficient. The encryption process is sequential, and each step is dependent on the output of the previous step. As a result, CBC can’t be parallelised. Counter mode provides an easy solution for this. 

In CTR mode, a counter is incremented for each block, and this counter, combined with a nonce, is encrypted to produce a keystream that is then XORed with the plaintext, ensuring both efficiency and security. The operation of CTR mode is shown in Figure 18. 

August 20, 2026 

Cybersecurity Engineering - Lecture Notes 



Figure 18: CTR 

The nonce in CTR mode serves a similar role to the Initialization Vector (IV) in CBC. Like an IV, the nonce does not need to be kept secret, but it is crucial that it is never reused with the same key. Reusing a nonce with the same key would result in the same keystream being generated, which could allow an attacker to recover the plaintext by analyzing the repeated patterns in the ciphertext. 

# **18 Pseudo Random Number Generators** 

Random numbers are essential in cryptography because they introduce unpredictability and ensure the security of various cryptographic operations. In encryption, random numbers are used to generate keys, Initialization Vectors (IVs), and nonces, all of which prevent patterns from emerging in encrypted data. This unpredictability is critical because if an attacker could predict or reproduce these random values, they could potentially decrypt messages or forge digital signatures. Random numbers also play a vital role in secure communication protocols, where they are used in generating session keys and ensuring that each session remains unique and secure. Without strong randomness, cryptographic systems would be vulnerable to attacks that exploit predictable patterns, ultimately compromising the confidentiality and integrity of sensitive data. 

A Cryptographically Secure Pseudo-Random Number Generator (CSPRNG) is a type of Pseudorandom Number Generator (PRNG) that produces a deterministic sequence of numbers based on an initial seed value. The output sequence of a PRNG is entirely dependent on this seed, making the seed crucial to the generator’s operation. For a PRNG to be considered cryptographically secure, it must be computationally infeasible for an attacker to brute-force the seed value or predict the output sequence. Additionally, the output must be indistinguishable from true randomness, ensuring that the only viable option for an attacker is to somehow know or discover the seed. 

# **19 Practice Quiz** 

**Question 1:** Consider the following in a simple cryptosystem where c is the cipher text, p is the plain text and k is the key, and c = p XOR k. 

August 20, 2026 

Cybersecurity Engineering - Lecture Notes 

Assume: 

p (plaintext) = 10111011 

k (key) = 00111101 

Which one(s) of the following is true about basic cryptographic operations? Select all that apply. 

**a)** c = 10000110 

**b)** c XOR p = k 

**c)** p = c XOR k 

**d)** The attacker only needs one plain text and cipher text pair to derive the key. 

**_Explanation_** _: We know that c = p XOR k. So c = 10111011 XOR 00111101, which is 10000110. Therefore c =10000110. => a) is correct._ 

_b) is correct. This is a property of XOR. You can verify this: c = 10000110 and p=10111011. c XOR p = 00111101, which is equal to k._ 

_c) is also correct. Again this is a property of XOR. You can verify this._ 

_Above b) shows that if the attacker can get hold of a cipher text and its corresponding plaintext, they can derive the key._ 

**Question 2:** As mentioned in the lecture, use the below link to read about using the Kasiski analysis for breaking the Vigenère Cipher (A polyalphabetic cipher). 

```
https://crypto.interactive-maths.com/kasiski-analysis-breaking-the-code.html
```

Now answer the following. 

’BWGWBHQSJBBKNF’ is a ciphertext generated from the Vigenère Cipher using a two-letter key. You also, know that the second letter of the plaintext is "I". 

What is the correct plain text? 

**a)** AIMISTHEANSWER 

**b)** SIXISTHEANSWER **c)** AIDISTHEANSWER 

**d)** HITISTHEANSWER 

**_Explanation_** _: The key idea is that “same key” and “same plain text” will result in the same cipher text. Therefore we can build something like this, where the two-character key is repeated (See Figure 19)._ 

August 20, 2026 

Cybersecurity Engineering - Lecture Notes 



Figure 19: Key alignment in Vigenère Cipher 

_Given the second letter of the plaintext is I, we can conclude that the fourth letter is also I - because the cipher text is W and it is encrypted by the same key._ 

_We can also conclude that the first, fifth, and eleventh characters in the plain text have to be the same - because they have encrypted with the same character in the key and have produced the same cipher text B (See Figure 20)._ 



Figure 20: Same cipher text 

_Now we can eliminate answers_ 

_AIMISTHEANSWER SIXISTHEANSWER AIDISTHEANSWER HITISTHEANSWER_ 

_Only “SIXISTHEANSWER” has the first, fifth, and eleventh characters the same._ 

**Question 3:** Which of the following statement is NOT TRUE about one-time pad (OTP)? Select all that apply. 

**a)** Once generated OTPs can be reused. 

**b)** OTP length has to be at least as long as the plaintext. 

**c)** Practical use of OTP is difficult. 

**d)** OTP gives perfect security. 

**_Explanation_** _: The key idea of OPT is that once generated, it can be used only once. Why? “if you re-use the same key, and someone has access to one message you encrypted in both plaintext and encrypted form, they can use that to find your key (i.e., known plaintext attack)_ 

_Therefore “Once generated OTPs can be reused” is NOT true => The correct answer._ 

_To avoid repetition, the OTP length must be greater than the plaintext. Therefore “OTP length has to be at least as long as the plaintext” is TRUE._ 

August 20, 2026 

Cybersecurity Engineering - Lecture Notes 

_OTP have issues distributing the key. Therefore “Practical use of OTP is difficult” is TRUE._ 

_OTP gives the maximum randomness in the ciphertext. The key is not repeated and the ciphertext does not provide any additional information about the plaintext._ 

**Question 4:** What is TRUE about the IV (Initialization Vector) used in symmetric cryptography? 

**a)** IV must be kept as a secret. 

**b)** IVs can be repeated. 

**c)** IV ensures that the same pain text block does not generate the same cipher text. **d)** IV are used in ECB (Electronic Code Block) block mode. 

**_Explanation_** _: In general, the requirement IVs is that they must not be repeated, but they do not have to be a secret. Usually, they are generated at the transmitter communication and sent in plaintext to the receiver. If IVs are repeated, the same issues as OTP repetition can happen. Therefore 1) and 2) are not true. 3) explain the exact idea of IV - therefore, it is TRUE. We use ECB as the motivation to use IV. Therefore 4) is not true._ 

**Question 5:** Which of the following are TRUE about Congrunet modulo n? Select all that apply. 

**a)** 26 _≡_ 11 mod (5) 

**b)** 74 _≡_ 30 mod (11) 

**c)** If _a ≡ b_ mod ( _n_ ) _and b ≡ c_ mod ( _n_ ) then _a ≡ c_ mod ( _n_ ) 

**d)** If _a ≡ b_ mod ( _n_ ) and _b ≡ c_ mod ( _n_ ) then _a_ = _c_ 

## **_Explanation_** _:_ 

**a)** 26 mod (5) = 1 and 11 mod (5) = 1 = _⇒_ 26 _≡_ 11 mod (5) = _⇒_ TRUE **b)** 74 mod (11) = 8 and 30 mod (11) = 8 = _⇒_ 74 _≡_ 30 mod (11) = _⇒_ TRUE 

## **c)** 

_a ≡ b_ mod ( _n_ ) = _⇒_ 

_a_ = _k_ 1 _n_ + _p_ 1 (where _p_ 1 _< n_ ) _b_ = _k_ 2 _n_ + _p_ 1 (where _p_ 1 _< n_ ) 

Similarly, 

_b_ = _k_ 3 _n_ + _p_ 2 (where _p_ 2 _< n_ ) _c_ = _k_ 4 _n_ + _p_ 2 (where _p_ 2 _< n_ ) 

_k_ 2 _n_ + _p_ 1 = _k_ 3 _n_ + _p_ 2 ( _k_ 2 _− k_ 3) _n_ + _p_ 1 = _p_ 2 

August 20, 2026 

Cybersecurity Engineering - Lecture Notes 

_c_ = _k_ 4 _n_ + ( _k_ 2 _− k_ 3) _n_ + _p_ 1 _c_ = ( _k_ 4 + _k_ 2 _− k_ 3) _n_ + _p_ 1 = _⇒ a ≡ c_ mod ( _n_ ) = _⇒_ TRUE 

d) This is not true. Giving a counter-example will be enough. 

Let a = 26, b = 11, c = 16, and n = 5. 

26 _≡_ 11 mod (5) 11 _≡_ 16 mod (5), And a is not equal to c. = _⇒_ NOT TRUE 

**Question 6:** Which of the following is NOT a finite filed under the given modulus? 

**a)** 0,1 modulus = 2 **b)** 0,1,2,3,4,5 modulus = 6 **c)** 0,1,2,3,4,5,6 modulus = 7 **d)** 0,1,2,3,4,........,30 modulus = 31 

**_Explanation:_** _The key here is that we know what are prime finite fields. That is 0,1,2,3,....p-1 is a field when p is a prime. That means a), c), and d) are all finite fields._ 

_b) is not a field. The first observation is that the modulus is not prime. Here it can be proved that some elements in 0,1,2,3,4,5 don’t have a multiplicative inverse under modulo 6._ 

_For example, let’s take 2._ 

_2.0 mod 6 = 0 2.1 mod 6 = 2 2.2 mod 6 = 4 2.3 mod 6 = 0 2.4 mod 6 = 2 2.5 mod 6 = 4_ 

_That is, there is no such element in 0,1,2,3,4,5 such that 2.x mod 6 =1 (lacking the inverse multiplicative property). Therefore 0,1,2,3,4,5 is not a finite field._ 

**Question 7:** DES (Data Encryption Standards) is still considered secure. TRUE or FALSE.? **a)** TRUE **b)** FALSE 

**_Explanation:_** _FALSE - DES is insecure because of the shorter key length._ 

**Question 8:** AES uses a ............... bit block size and a key size of ............... bits. 

**a)** 128; 128 or 256 **b)** 64; 128 or 192 **c)** 256; 128, 192, or 256 

August 20, 2026 

Cybersecurity Engineering - Lecture Notes 

**d)** 128; 128, 192, or 256 

**_Explanation:_** _AES is a block cipher that supports 128-bit blocks and three key sizes: 128, 192, or 256._ 

**Question 9:** Like DES, AES also uses Feistel Structure. TRUE or FALSE. 

**a)** TRUE 

**b)** FALSE 

**_Explanation:_** _AES does not use a Feistel structure. Instead, each full round consists of four separate functions:_ 

- _Byte substitution_ 

- _Permutation_ 

- _Arithmetic operations over a finite field_ 

- _XOR with a key_ 

**Question 10:** Compute the output of the following S-Box (as shown in the lecture). Your input is 010000. 



Figure 21: Given S-Box 

**a)** 0011 **b)** 0001 **c)** 0000 **d)** 1010 

**_Explaination:_** _The input string is 010000._ 

_b_ 0 _and b_ 5 _gives the row - that means_ 002 _->_ 010 _is the row._ 

_b_ 1 _b_ 2 _b_ 3 _b_ 4 _gives the column - that means_ 10002 _->_ 810 _is the column._ 

_At the 0th row and 8th column, the table reads 3. So the output is 0011._ 

# **References** 

- [1] William Stallings. _Cryptography and Network Security: Principles and Practice, Global Edition_ . Pearson, Upper Saddle River, NJ, 8th edition, 2022. 

August 20, 2026 

Cybersecurity Engineering - Lecture Notes 


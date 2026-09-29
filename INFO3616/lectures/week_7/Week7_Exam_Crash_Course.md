# INFO3616 Week 7: Authentication & Key Distribution — Exam Quick-Teach

> **Target Reading Time:** 7–9 minutes  
> **Source Material:** Week 7 Lecture Slides & Lecture Notes combined  
> **Course:** INFO3616 Cybersecurity Engineering, The University of Sydney  
> **Core Topics:** Dolev-Yao Model & Boyd's Theorem, Perfect Forward Secrecy (PFS), Symmetric Key Distribution (KDC, Needham-Schroeder flaw, Kerberos 3-step ticket flow), Public Key Infrastructure (PKI, X.509 Certificates, Chain of Trust), Certificate Revocation (CRL, OCSP, OCSP Stapling), Multi-Factor Authentication & Replay Prevention.

---

## 1. Foundational Security Theorems & Models

### The Dolev-Yao Threat Model
In modern protocol analysis, the network is modeled as completely controlled by the adversary:
* The attacker can **intercept, read, modify, replay, delay, and inject** any message at will.
* All security must be guaranteed cryptographically through the messages themselves.

### Boyd's Theorem (The Key Distribution Dilemma)
> *"Assuming the absence of a secure channel, two entities cannot establish an authenticated shared secret without an existing trust relationship."*

* **Exam Takeaway:** You cannot bootstrap secure, authenticated communication out of thin air. You either need:
  1. A pre-shared secret (master key), or
  2. A **Trusted Third Party (TTP)** — such as a Key Distribution Center (KDC) or a Certificate Authority (CA).

### Forward Secrecy / Perfect Forward Secrecy (PFS)
* **Definition:** A protocol guarantees PFS if the compromise of long-term private keys does **not** compromise past session keys.
* **Mechanism:** Achieved by using **ephemeral Diffie-Hellman** (DHE or ECDHE), where a fresh temporary key pair is generated for each session and immediately discarded after use.
* *Contrast:* If an attacker records encrypted traffic and later steals a static RSA private key, they can decrypt all historical recorded sessions (No PFS!).

---

## 2. Symmetric Key Distribution & Key Hierarchy

* **Key Hierarchy:**
  * **Master Key:** Long-term symmetric secret shared between a principal and a trusted KDC.
  * **Session Key:** Temporary symmetric key generated dynamically for a single session between two communicating parties.
* **The Needham-Schroeder Symmetric Protocol & Its Fatal Flaw:**
  * Alice contacts KDC to talk to Bob. KDC sends Alice a session key $K_{AB}$ and an encrypted ticket for Bob: $E_{K_B}(K_{AB}, A)$.
  * **The Denning-Sacco Attack:** The ticket contains no timestamp! If an attacker ever learns an old compromised session key $K_{AB}$, they can replay the old ticket to Bob indefinitely. Bob will accept it, believing it is a fresh session.

---

## 3. Kerberos: The Complete 3-Step Protocol Flow

Kerberos solves the Needham-Schroeder replay vulnerability by introducing **Timestamps** and **Authenticators**.

```
[ Alice (Client) ] ──(1) Get TGT──> [ Authentication Server (AS) ]
        │
        ├──(2) Get Service Ticket──> [ Ticket Granting Server (TGS) ]
        │
        └──(3) Access Service─────> [ Application Server (SS) ]
```

### Step 1: Authentication Service Exchange (User Login)
1. **Alice $\to$ AS:** Alice sends her identity $A$ and requests access to the TGS.
2. **AS $\to$ Alice:** AS generates session key $K_{A,\text{TGS}}$ and returns:
   * **Ticket Granting Ticket (TGT):** Encrypted with the TGS's secret key:
     $$\text{TGT} = E_{K_{\text{TGS}}}(A, \text{TGS}, K_{A,\text{TGS}}, \text{Lifetime}, \text{Timestamp})$$
   * **Client Payload:** Encrypted with Alice's password-derived master key $K_A$:
     $$E_{K_A}(K_{A,\text{TGS}}, \text{TGS}, \text{Lifetime}, \text{Timestamp})$$
* *Result:* Alice enters her password once to decrypt $K_{A,\text{TGS}}$. The TGT cannot be tampered with by Alice because it is encrypted with $K_{\text{TGS}}$.

### Step 2: Ticket-Granting Service Exchange (Requesting a Service)
1. **Alice $\to$ TGS:** Alice sends:
   * The $\text{TGT}$,
   * An **Authenticator** encrypted with $K_{A,\text{TGS}}$: $E_{K_{A,\text{TGS}}}(A, \text{Timestamp})$,
   * The identity of the requested service $V$.
2. **TGS Actions:**
   * Decrypts the $\text{TGT}$ using its secret key $K_{\text{TGS}}$ to extract $K_{A,\text{TGS}}$ and verify ticket expiration.
   * Decrypts the Authenticator using $K_{A,\text{TGS}}$ and verifies the timestamp against its replay cache (within a 5-minute window).
3. **TGS $\to$ Alice:** Returns:
   * **Service Ticket:** Encrypted with Server $V$'s secret key $K_V$:
     $$\text{Ticket}_V = E_{K_V}(A, V, K_{A,V}, \text{Lifetime}, \text{Timestamp})$$
   * Service Session Key $K_{A,V}$ encrypted with $K_{A,\text{TGS}}$:
     $$E_{K_{A,\text{TGS}}}(K_{A,V})$$

### Step 3: Client/Server Exchange (Accessing Application Server)
1. **Alice $\to$ Server $V$:** Alice sends $\text{Ticket}_V$ and a fresh Authenticator $E_{K_{A,V}}(A, \text{Timestamp})$.
2. **Server $V$ Actions:** Decrypts $\text{Ticket}_V$ with $K_V$, extracts $K_{A,V}$, decrypts the Authenticator, verifies identity and freshness.
3. **Server $V \to$ Alice (Mutual Authentication):** Server responds with $E_{K_{A,V}}(\text{Timestamp} + 1)$ to prove it also knows $K_{A,V}$.

---

## 4. Public-Key Infrastructure (PKI) & X.509 Certificates

### Why Certificates?
If Alice sends Bob her public key $PK_A$ over a network, an attacker (Mallory) can substitute their own public key $PK_M$ (PitM attack). A **Digital Certificate** cryptographically binds an identity to a public key.

### Structure of an X.509 Certificate:
$$\text{Cert} = \big[ \text{Subject Name, Subject } PK, \text{Issuer (CA) Name, Validity Period, Serial No} \big] \parallel \text{Sig}_{SK_{\text{CA}}}\big(H(\text{Data})\big)$$

### The Chain of Trust:
```
[ End-Entity (Website) Cert ] ──signed by──> [ Intermediate CA ] ──signed by──> [ Root CA (Self-Signed) ]
                                                                                         │
                                                                                (Pre-installed in OS /
                                                                                  Browser Root Store)
```
* **Why use Intermediate CAs?**
  * The Root CA private key is kept strictly **offline in a secure vault** (air-gapped).
  * Intermediate CAs issue day-to-day certificates. If an Intermediate CA is compromised, only its subtree is revoked—the Root CA remains trusted.

---

## 5. Certificate Revocation: CRL vs OCSP vs OCSP Stapling

When a private key is leaked or an employee leaves, a certificate must be revoked before its expiration date.

| Mechanism | How It Works | Strengths | Critical Flaws (Exam Traps) |
| :--- | :--- | :--- | :--- |
| **CRL (Certificate Revocation List)** | CA periodically publishes a signed list of revoked serial numbers. | Simple, offline verification once downloaded. | Lists become massive (megabytes); high latency; replay vulnerability between updates. |
| **OCSP (Online Certificate Status Protocol)** | Client sends real-time HTTP request to CA's OCSP responder for a specific cert status. | Lightweight query; real-time status. | **Privacy leak:** CA tracks every website the user visits; **Latency:** extra DNS/HTTP lookup; **Soft-fail:** browsers ignore if responder is down. |
| **OCSP Stapling (Best Practice)** | The **web server** queries the OCSP responder periodically, caches the signed/timestamped status, and **staples** it into the TLS handshake. | **Zero privacy leak** (CA doesn't see users); **No client latency**; Tamper-proof (signed by CA). | Server must actively support and refresh stapled tokens. |

---

## 6. Authentication Protocols & Replay Prevention

### Corroborative Evidence (The 3 Factors):
1. **Something you know:** Password, PIN.
2. **Something you have:** Smartcard, hardware token, phone (SMS/App).
3. **Something you are:** Biometrics (fingerprint, iris, voice).
* **Multi-Factor Authentication (MFA):** Requires $\ge 2$ **different categories** (e.g., password + SMS token is MFA; password + security question is NOT MFA because both are "something you know").

### Defeating Replay Attacks: Nonces vs Timestamps
* **Nonces (Number Used Once):**
  * Random challenge sent by the verifier: Bob sends $N_B \to$ Alice responds with $\text{MAC}_K(N_B)$.
  * *Advantage:* Does not require clock synchronization.
  * *Disadvantage:* Requires a 2-way or 3-way handshake (challenge-response).
* **Timestamps:**
  * Sender includes current time $t$: Alice sends $E_K(M, t)$.
  * *Advantage:* Supports single-message unilateral authentication.
  * *Disadvantage:* Requires tightly synchronized clocks (e.g., NTP) and a server-side replay cache to reject duplicate timestamps within the tolerance window.

---

## 7. Exam Self-Check (Test Yourself)

1. **According to Boyd's theorem, why can't two strangers establish an authenticated key over the Internet without a CA or KDC?**  
   *Because an active attacker (Dolev-Yao model) can execute a Person-in-the-Middle attack by substituting keys without detection.*
2. **In Kerberos, why can't a user alter the contents of their own Ticket Granting Ticket (TGT)?**  
   *Because the TGT is encrypted using the secret master key of the TGS ($K_{\text{TGS}}$), which the user does not possess.*
3. **What is the fatal security flaw in the Needham-Schroeder symmetric protocol?**  
   *Bob cannot verify the freshness of the ticket sent by Alice (lack of timestamp), allowing replay of an old, compromised session key (Denning-Sacco attack).*
4. **How does OCSP Stapling protect user privacy compared to traditional OCSP?**  
   *In traditional OCSP, the client queries the CA directly (revealing every site visited). In OCSP Stapling, the web server fetches the signed status and sends it to the client, keeping the user invisible to the CA.*

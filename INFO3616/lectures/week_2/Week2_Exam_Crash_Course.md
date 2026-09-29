# Week 2 Exam Cram Guide: Usability and Security

**Read Time:** ~7–10 minutes  
**Core Goal:** Master the key definitions, biases, password calculations, passkey mechanics, and UX concepts tested in Dr. Seneviratne & Dr. Dahanayaka's course.

---

## 1. Core Usability Foundations

* **People as the Weakest Link:** 80%–90% of security breaches stem from human error (e.g., 2020 Twitter Bitcoin scam where administrative credentials were found on a Slack channel).
* **Theoretical vs. Effective Security:**
  * *Theoretical Security:* Cryptographically sound on paper (e.g., Smart cards with high-entropy keys).
  * *Effective Security:* Usable and operationally viable in practice. If a mechanism imposes too much friction (lost cards, broken readers, no cross-platform support), users bypass or resist it.
* **Principle of Psychological Acceptability (Saltzer & Schroeder / Bishop):**
  * *Formal Definition:* Security mechanisms must be designed for ease of use so users routinely and automatically apply protection mechanisms correctly. Mistakes occur when users must translate their mental model into a foreign specification language.
  * *Simplified Axiom:* **"A security mechanism should not make a resource more difficult to access than if the mechanism were not present."**
* **The Three Categories of Human Error:**
  1. **Manual Skill Fails (Slips/Lapses):** Failure in executing an automated physical skill (e.g., mistyping a URL $\rightarrow$ exploited by **typosquatting** such as `glthub.com` or `amozon.com`).
  2. **Following the Wrong Rule (Mistakes at Rule Level):** Operating on a flawed mental guideline (e.g., believing *"Always trust HTTPS because it has a padlock"*—attackers obtain valid SSL certificates easily).
  3. **Cognitive Reasons:** Misunderstanding the risk, lacking mental capacity, or intentionally ignoring advice to finish work tasks (e.g., deferring disruptive patches).

---

## 2. Cognitive Biases & Decision-Making

### A. Prospect Theory & Risk Misperception (Kahneman & Tversky)
* **Prospect Theory & Loss Aversion:** **Losses are felt significantly more intensely than equivalent gains.**
  * *Security exploitation:* Phishing lures leverage loss avoidance: *"Your PayPal account has been frozen; click here immediately to restore access"* is much more effective than promising a reward.
* **Risk Misperception:** If users enjoy or prefer an activity, they perceive **high benefit and low risk**; if they dislike it, they perceive **low benefit and high risk** (e.g., driving vs. flying fear).
* **Anchoring Effect:** Users disproportionately rely on the first piece of information received.
  * *Example:* Fake antivirus alerts quoting "$1,000 value, now only $50!" or lottery scam processing fees seeming tiny relative to the advertised jackpot anchor.
* **Availability Heuristic:** Estimating likelihood based on how easily examples come to mind.
  * *Example:* ATO tax refund SMS scams sent during tax return season when tax documents are top-of-mind.

### B. Behavioural Economics & Paradigms
* **Present Bias & Hyperbolic Discounting:** Heavily prioritizing immediate payoffs over future, larger consequences.
  * *Security impact:* Users postpone system updates and reboot requests because immediate task completion outweighs the abstract future risk of a zero-day exploit.
* **Privacy Paradox:** The measurable contradiction where individuals express deep concern about personal privacy, yet willingly trade data for immediate gratification (e.g., clicking "Accept All Cookies" blindly).
* **Control Paradox:** Giving users more fine-grained privacy settings often gives them a false sense of security, paradoxically causing them to share *more* private data.
* **Clustering Illusion:** Seeing patterns and structure in purely random data (e.g., the "hot hands" fallacy in basketball, or trusting a phishing email simply because it copied familiar formatting and logos).
* **Confirmation Bias:** Interpreting information selectively to reinforce preexisting beliefs while ignoring contradicting evidence (e.g., once a user believes an email is genuinely from PayPal, they overlook subtle typos in the domain name).
* **Zero-Risk Bias:** Preferring options that eliminate a single risk completely (reducing it to 0%) rather than alternative solutions that reduce total risk far more across the whole system.

---

## 3. Techniques to Influence & Deceive

### Robert Cialdini’s 6 Levers of Influence
| Lever | Mechanism | Social Engineering / Attack Example |
| :--- | :--- | :--- |
| **Reciprocity** | Urge to return favors | Attacker posing as IT helps fix a minor printer issue, then asks the victim to test a malicious executable tool. |
| **Commitment & Consistency** | Need to align with past public choices | Attacker gets an employee to commit verbally to strict policy compliance, then asks for their password "to audit compliance". |
| **Social Proof / Validation** | Looking to others to dictate behavior | Attacker mentions that everyone else in the finance department already completed the verification survey. |
| **Liking** | Complying with people we like/find charming | Attacker connects over shared hobbies or flattery before asking for system access. |
| **Respect to Authority** | Deference to perceived hierarchy | Attacker poses as the CEO, an ATO official, or a hospital doctor (e.g., Cialdini's hospital nurse study where 95% complied). |
| **Scarcity** | Fear of missing out (FOMO) | "Only 2 software license keys remaining at this discount; click to register." |

### User Conditioning & Education
* **User Conditioning ("Click-Whirr"):** Habituation caused by repetitive, benign alerts (warning dialogue fatigue, Windows Recycle Bin confirmation, generic SSL certificate warnings). Users develop automatic dismissal reflexes without reading.
* **User Education Realities:**
  * Distributing passive policy documents fails.
  * Interactive training with continuous feedback is better, but **education alone is insufficient**.
  * Security language conflicts with everyday user language; engineering must eliminate friction via **good defaults and gentle nudges** rather than blaming the user.

---

## 4. Usability and Security of Passwords

### The Three Fundamental Password Concerns
1. **Entry:** Will the user type it accurately on mobile and desktop without high error rates?
2. **Memorability:** Will the user remember it, write it down, or pick a trivial pattern?
3. **Disclosure:** Will the user leak it via phishing, shoulder surfing, or social engineering?

### Debunking Outdated Password Advice
* **Myth 1: "Change passwords every 30/60/90 days"**
  * *Reality:* **Harmful advice.** Stored correctly (salted and hashed), strong passwords do not expire. Frequent forced changes cause users to adopt predictable transformations (e.g., `Spring2025!` $\rightarrow$ `Summer2025!`).
  * *Modern Policy:* Do not expire passwords unless a breach is suspected (UK NCSC since 2015, Australia since 2017).
* **Myth 2: "Enforce strict character composition rules" (e.g., 1 uppercase, 1 symbol, 1 digit)**
  * *Reality:* Rejects strong, long passphrases while approving weak, predictable passwords (e.g., accepts `Password123!`, rejects `geyps5aykj0q71c637n9gf4ycg`).
  * *Modern Practice:* Check candidate passwords against common dictionaries, breached credential lists, and leetspeak substitutions.

### Secure & Memorable Creation Strategies
* **Diceware / Dice Method:**
  * Roll 5 standard six-sided dice $\rightarrow$ generates a 5-digit index from $11111$ to $66666$ ($6^5 = 7,776$ unique words on the EFF list).
  * Stringing 6 random words creates a high-entropy passphrase with a memorable mental story.
* **Letters-from-a-Sentence:** Extracting the first 1–2 letters of words in a personal mnemonic sentence (e.g., *"Wow! 62 students, all in this memorable class of 2026!"* $\rightarrow$ `W!62s,aitmc02026!`).
* **Person-Action-Object (PAO):** Creating vivid mental imagery (e.g., *"Darth Vader riding a pony on Mt Everest"* $\rightarrow$ `DVr4poMt3!`).
* **Writing Passwords Down:** Not always bad! Writing a password down and storing it in a locked private bedroom is safer against remote cyberattacks than picking an easily guessable password. (Never in open public or shared office environments).

---

## 5. Password Calculations & Entropy Formulas

### Combinatorics (Search Space $N$)
* **With Replacement (Standard):**
  $$N = C^L$$
  * $C =$ size of character pool
  * $L =$ length of password
* **Without Character Repetition (Permutation $P$):**
  $$P(C, L) = \frac{C!}{(C - L)!}$$

### Information Entropy ($H$, measured in bits)
$$H = \log_2(N) = L \cdot \log_2(C)$$

#### Exam Numerical Benchmarks to Remember:
* **6 lowercase letters:** $N = 26^6 \approx 308.9 \times 10^6 \implies H \approx 28.2\text{ bits}$.
* **8 mixed characters (72-char set):** $N = 72^8 \approx 7.2 \times 10^{14} \implies H \approx 49.36\text{ bits}$.
* **6-word Diceware Passphrase:**
  * Word list size: $6^5 = 7,776$ words.
  * Combinations: $N = 7,776^6 \approx 2.21 \times 10^{23}$.
  * Entropy: $H = \log_2(7,776^6) = 6 \cdot \log_2(7,776) \approx \mathbf{77.55\text{ bits}}$.

---

## 6. Passkeys (FIDO2 / WebAuthn)

Passkeys replace passwords with public-key asymmetric cryptography and local device biometrics (FaceID/TouchID/PIN).

### Architecture & Workflows
```
[User Device / Authenticator]                     [Relying Party (Server / Website)]
        |                                                        |
        |------------------ 1. Registration Request ------------>|
        |<----------------- 2. Server Challenge -----------------|
        |                                                        |
  [Local Biometric Prompt]                                       |
  [Generate Asymmetric Key Pair]                                 |
  [Store Private Key in TPM / Enclave]                           |
        |                                                        |
        |-------- 3. Public Key + Signed Challenge Response ---->|
        |                                           [Store Public Key]
        |                                                        |
        |=================== Later: Login =======================|
        |                                                        |
        |------------------ 1. Login Request ------------------->|
        |<----------------- 2. Fresh Challenge ------------------|
  [Local Biometric Verification]                                 |
  [Private Key Signs Challenge]                                  |
        |                                                        |
        |------------------ 3. Signed Response ----------------->|
        |                                           [Verify with Stored Public Key]
        |<----------------- 4. Authentication OK ----------------|
```

* **Key Takeaway:** The **private key never leaves the user's hardware secure enclave**. The server only ever holds the public key. Eliminates phishing, credential stuffing, and server database password leaks.

---

## 7. UX/UI Security Design Principles

* **Mental Models:** Internal cognitive representations users hold about how a system works. Interfaces should match users' existing mental models rather than forcing them to think like developers.
* **Affordance:** Visual or functional properties of an interface that show how it can be used (e.g., a button looks pushable, turns green when active, or greyed out when input is incomplete).
* **Constraints:** Structural boundaries that prevent the user from making incorrect or hazardous choices (e.g., restricting invalid characters, bounding permission toggles).
* **Conventions:** Standardized symbols and patterns users recognize from past experiences (e.g., padlock icon for encryption, gear icon for settings).

---

## 8. Quick Exam Traps & Flash Facts

* **Saltzer & Schroeder Definition:** The principle of psychological acceptability requires that the human interface be easy to use and that the user's mental model aligns with the protection mechanism.
* **Typo Squatting is:** A failure of **manual skill**, not a cognitive error or wrong rule.
* **"HTTPS is safe" is:** An error of **following the wrong rule**.
* **Do we expire passwords?** No, periodic mandatory expiry is an outdated, harmful practice.
* **Is writing passwords down always wrong?** False; writing down complex passwords in physically secure private home spaces is acceptable compared to choosing weak, memorizable passwords.
* **Defaults:** Setting secure defaults (e.g., automatic night patching while charging on Wi-Fi, minimal privileges) is the single most effective way to counter user present bias.
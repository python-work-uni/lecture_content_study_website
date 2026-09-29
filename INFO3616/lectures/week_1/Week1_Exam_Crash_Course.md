# Week 1: Introduction to Security Engineering — Exam Cram Sheet
*Read time: ~6–8 minutes*

---

## 1. What is Security Engineering?

* **Engineering Definition:** Applying science and maths to solve real-world problems.
* **Security Engineering Definition:** Conceiving, designing, and implementing hardware and software that produces *only the expected answers*, even when confronted with **malice, error, or mischance**.
* **"Programming Satan's Computer" (Anderson & Needham, 1995):** The key challenge that sets security engineering apart is the presence of an **intelligent, hostile opponent** who actively tries to manipulate inputs and alter messages at the most inconvenient moment.
* **Crucial Exam Distinction:**
  * **Safety Engineering:** Prevents accidental harm to humans, property, or the environment (e.g., toxic gas release valves, machine guards). *No hostile opponent.*
  * **Reliability Engineering:** Ensures components perform without failure over time to minimize downtime (e.g., RAID disks, backup generators, predictive sensor maintenance). *No hostile opponent.*
  * **Security Engineering:** Defends against an **intelligent adversary with malicious intent** (e.g., firewalls, MFA, encryption).
* **Mantra:** *"Security is a process, not a product."* (Static products cannot counter evolving attacker incentives, system complexity, and dynamic environments).

---

## 2. Anderson’s Security Framework (The 4 Pillars)

Any system evaluation or post-incident review (e.g., the 2013 Target breach) traces back to these four elements:

```
          [ Policy ]
         /          \
  [ Incentives ]  [ Mechanisms ]
         \          /
         [ Assurance ]
```

1. **Policy (The "What"):** High-level rules defining what it means to keep the system secure (e.g., "Customer data must stay in local data centres", retention limits). *Does NOT specify how to implement it.*
2. **Mechanisms (The "How"):** The technical/procedural machinery used to enforce policy (e.g., AES encryption, access control lists, cryptographic hashes, 4-eyes principle).
3. **Assurance (The "Confidence"):** How much reliance you can realistically place on a mechanism and how well mechanisms work together (e.g., RSA-2048 takes trillions of years classically, but ~10 seconds on a quantum computer; FireEye alerts are reliable, but human follow-up may fail).
4. **Incentives (The "Why"):** The motivations driving both **defenders** (workload, negligence, insider rogue gains) and **attackers** (financial profit, espionage, vandalism). Guides *Threat Modelling*.

---

## 3. Security Goals & Critical Exam Nuances

| Goal | Definition & Exam Trap |
| :--- | :--- |
| **Confidentiality / Secrecy** | Limiting plain-text data access exclusively to authorised entities. Access control and encryption are mechanisms to achieve this. |
| **Integrity** | Detecting unauthorized modification of data in transit or storage. **Exam note:** Integrity means **tamper-evident** (detecting changes), **NOT** tamper-resistant (physically preventing changes). |
| **Authenticity** | Verifying the genuine origin/source of data. In cryptographic protocols, authenticity **requires both Integrity + Freshness** (proof it's not a replay attack). |
| **Authorisation** | Determining if an entity has permission to perform an action. **Exam note:** Authorisation does **not** imply Authentication (e.g., possessing a movie ticket proves authorization without revealing identity). |
| **Accountability** | Tracing actions back to a specific responsible entity. Requires auditable, protected, non-forgeable logs. |
| **Non-Repudiation** | Ensuring an entity cannot successfully deny responsibility for an action (a legal concept). Cryptographically requires **authenticity + integrity + secure timestamping**. |
| **Deniability** | The deliberate capability to reject responsibility (the functional opposite of non-repudiation; useful in confidential communications). |
| **Availability** | Ensuring systems and resources are accessible to authorised users when needed. Attacked by DoS/DDoS. *May sometimes be traded off for confidentiality (e.g., battlefield comms prioritize availability).* |
| **Privacy vs Anonymity** | **Privacy:** Control over what information about yourself you disclose (identity may be known to the host).<br>**Anonymity:** Complete lack of identity/traceability within a context (pseudonym, no IPs logged). |

---

## 4. Fundamental Security Design Principles (Saltzer & Schroeder)

*Memorize the name, meaning, and classic scenario:*

1. **Economy of Mechanism:** Keep security designs as simple and small as possible (easier to verify, smaller codebase = fewer vulnerabilities; Unix modular design vs. bloated OS).
2. **Fail-Safe Defaults:** Base access on explicit **permission**, not exclusion. Default state is **DENY**. (e.g., firewall drop-by-default; POODLE attacked insecure fallbacks).
3. **Complete Mediation:** Check **every single access request**, every time. Do not rely on unvalidated cached decisions (e.g., Zero Trust Architecture).
4. **Open Design (Kerckhoffs's Principle):** Design must be public, not secret; only the **key** is secret. Never rely on *security through obscurity* (e.g., DVD CSS cipher failed because secrecy was broken).
5. **Separation of Privilege:** Require **multiple distinct attributes/conditions** to gain access (e.g., Multi-Factor Authentication; Unix requiring both root password AND membership in `wheel` group).
6. **Least Privilege:** Entities operate using the absolute minimum set of privileges needed for the minimum time (e.g., running Apache as `www-data` rather than `root`).
7. **Least Common Mechanism:** Minimize shared functions/paths between different users to prevent cross-contamination (e.g., never reuse passwords across services; isolate user workspaces).
8. **Psychological Acceptability:** Security must not unduly burden user workflow, or users will bypass it (e.g., biometric Touch ID/Face ID integrates security seamlessly).
9. **Isolation:** Keep critical resources completely segregated from public networks (e.g., Apple Secure Enclave coprocessor isolating biometrics and keys from the main OS).
10. **Encapsulation:** Object-oriented isolation where internal structures are modified only via specific designated access points (e.g., database stored procedures and views).
11. **Modularity:** Reusable, protected security modules designed so sub-components can be upgraded without breaking the system (e.g., AWS KMS for centralized crypto).
12. **Layering (Defense in Depth):** Overlapping defensive barriers spanning technology, people, and operations (e.g., MFA + firewalls + patch management + user phishing training).
13. **Least Astonishment:** The interface should behave in a way that matches the user's intuitive mental model (e.g., avoid odd parsing quirks like legacy JS interpreting leading zeros as octal).

---

## 5. Attacks, Vectors, Surfaces & Opponents

### A. Passive vs. Active Attacks (ITU-T X.800)
* **Passive Attacks:** Goal is solely to observe or obtain transmitted information. System resources are **not** altered.
  * *Examples:* Eavesdropping, release of message content, traffic analysis (analyzing flow/patterns without decrypting), side-channel analysis (measuring CPU power consumption or acoustic keyboard typing).
* **Active Attacks:** Goal is to alter data, impersonate, or disrupt system operation.
  * *Categories:* **Masquerade** (pretending to be someone else), **Replay** (re-sending captured valid packets), **Modification** (tampering with messages), **Denial of Service (DoS)**.

### B. Vectors vs. Surfaces vs. Trees
* **Attack Vector:** A specific method/pathway used by an attacker to gain unauthorized access (e.g., phishing, SQL injection, Person-in-the-Middle, malware).
* **Attack Surface:** The **sum total** of all reachable and exploitable vulnerability points in a system.
  * Categories: *Network* (open ports), *Software* (web app forms, parsers), *Human* (social engineering).
* **Attack Tree:** A hierarchical tree diagram mapping attack techniques. Root node = attacker goal (e.g., "Compromise Bank Account"); Leaves = atomic attack methods.

### C. Standard Cryptographic Personas
* **Alice & Bob:** Legitimate communicating parties.
* **Eve:** Passive eavesdropper (listens without modifying).
* **Mallory:** Malicious active adversary (modifies, replays, intercepts).
* **Trent:** Trusted third party (e.g., Certificate Authority).

---

## 6. Rapid-Fire Exam Traps & Multiple-Choice Logic

* **Is Access Control a security goal?** In this course syllabus, **no**. Access control is a **mechanism** used to achieve confidentiality and integrity.
* **Does Authorisation require Authentication?** **No.** You can be authorized anonymously via a token, ticket, or capability key.
* **Ransomware encrypts your disk — what goal is lost?** **Availability** (files are locked; operational capacity is denied).
* **Two employees must sign off on a wire transfer — what principle?** **Separation of privilege** (also known as the "four-eyes principle").
* **Measuring electromagnetic radiation or power fluctuations:** This is a **passive attack** (information leakage observation), not active modification.
* **Target Breach Failure Analysis:**
  * *Policy:* Allowed 3rd-party vendor (HVAC) unsegmented access without verifying vendor security.
  * *Mechanism:* Malware detector (FireEye) alerted, but human/incident response procedures were absent.
  * *Incentive:* High holiday sales volume prioritized over investigating alerts.
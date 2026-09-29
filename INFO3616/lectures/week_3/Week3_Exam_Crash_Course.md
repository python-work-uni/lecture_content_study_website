# Access Control: 5–10 Min High-Yield Exam Cram Guide

---

## 1. Fundamentals: The Core Triad
* **Authentication**: Proving **identity** ("Who are you?"). E.g., password, biometric.
* **Authorization**: Granting **privileges** ("What are you permitted to do?").
* **Access Control**: Enforcing the policy that connects authenticated principals to authorized operations on objects.
* **Security Engineering Framework**:
  $$\text{Policy} \longrightarrow \text{Mechanisms} \longrightarrow \text{Assurance}$$
  *(Attacker incentives are countered by policy, implemented via mechanisms, yielding a measurable level of assurance).*

---

## 2. DAC vs. MAC

| Feature | Discretionary Access Control (DAC) | Mandatory Access Control (MAC) |
| :--- | :--- | :--- |
| **Control Owner** | **Resource Owner** (subject who created the object). | **Central Authority** / Security Policy Administrator. |
| **Flexibility** | High (owner can share, edit, delegate). | Low/Rigid (strict system-wide enforcement). |
| **User Override**| Yes, owner grants/revokes permissions freely. | **No**, users/supervisors cannot override rules. |
| **Real-World** | Standard Unix/Windows file sharing, OneDrive Personal. | Military MLS, SELinux, OneDrive Enterprise DLP. |

---

## 3. Security Policy Models (MLS)

Exam questions heavily target **Bell-LaPadula** and **Biba**. Remember their primary focus!

### Bell-LaPadula (BLP) — Focus: **Confidentiality**
*Information cannot flow downwards.*
1. **Simple Security Property**: **No Read Up**
   * A subject cannot read an object of higher clearance ($\text{Clearance}(S) \ge \text{Classification}(O)$).
2. **$\star$ (Star) Property**: **No Write Down**
   * A subject cannot write to an object of lower classification ($\text{Clearance}(S) \le \text{Classification}(O)$).
   * *Why?* Prevents high-level users or Trojan horses from leaking classified secrets to lower unclassified files.
3. **Discretionary Property**: Employs an access control matrix for discretionary rules.

> **BLP Exam Traps & Criticisms:**
> * **Zero Integrity**: Low-clearance users **can write up** (e.g., an unclassified user can overwrite Top Secret files!).
> * **Covert Channels**: Does not protect against covert channels (e.g., signaling 1s and 0s via CPU load variations).

---

### Biba Model — Focus: **Integrity**
*Opposite/Dual of Bell-LaPadula. Untrusted data cannot corrupt trusted objects.*
1. **Simple Integrity Property**: **No Read Down**
   * Subject can only read data at its own level or higher (prevents consuming dirty/untrusted data).
2. **$\star$ (Star) Integrity Property**: **No Write Up**
   * Subject can only write to its own level or lower (prevents a low-integrity subject from tampering with high-integrity data).
3. **Invocation Property**: A lower-integrity process **cannot invoke** or call a higher-integrity process.

* **Real-world Examples**:
  * Avionics vs. In-flight entertainment (entertainment can read airspeed, but cannot write to avionics controls).
  * Windows Integrity Levels (Vista/10/11), SELinux.

---

### Model Quick-Comparison Matrix

| Model | Primary Goal | Read Rule | Write Rule |
| :--- | :--- | :--- | :--- |
| **Bell-LaPadula** | **Confidentiality** | **No Read Up** (Read $\le$) | **No Write Down** (Write $\ge$) |
| **Biba** | **Integrity** | **No Read Down** (Read $\ge$) | **No Write Up** (Write $\le$) |

---

## 4. Linux / OS Access Control

### Standard Permission Triads
* Permissions: `r` (Read = 4), `w` (Write = 2), `x` (Execute = 1).
* Triads: `[User/Owner] [Group] [Others]` (e.g., `chmod 755 file` $\to$ `rwxr-xr-x`).
* **Directories**: The `x` bit is required to **traverse/enter** the directory.

### The 3 Special Bits
1. **SUID (Set User ID)**:
   * File runs with the **privileges of the file owner**, not the user executing it.
   * *Example*: `/usr/bin/passwd` (owned by root, allows normal users to update `/etc/shadow`).
2. **SGID (Set Group ID)**:
   * On executable: runs with privileges of the file's group.
   * On directory: newly created files automatically inherit the parent directory's group.
3. **Sticky Bit**:
   * On a directory (e.g., `/tmp`), **only the file owner or root can delete or rename** the file, even if others have write access to the directory.

### Process Identities
* **Real UID/GID**: The user who actually launched the process.
* **Effective UID/GID (eUID/eGID)**: Evaluated by the kernel for permission checks (changed by SUID/SGID).
* **Saved UID/GID**: Allows a process to drop privileges and switch back safely.
* **Root**: UID = 0 (bypasses standard DAC checks).

---

## 5. Other Platforms: Mobile & Windows

* **Windows**:
  * Enforced by the **Security Reference Monitor (SRM)**.
  * Uses 13–16 fine-grained permissions (not just RWX). Greater flexibility, but high complexity can lead to misconfigurations.
* **Apple iOS**:
  * Sandboxing: Each app runs isolated. Read-only OS file system.
  * APIs grant capabilities upon explicit user consent. Sensor values are read-only (reflecting Biba).
* **Android**:
  * Built on Linux: **each app runs as its own unique Linux UID**.
  * Permissions are capabilities. "Dangerous" permissions approved at runtime (Trust On First Use since Android 6).
  * *Known Flaw*: Shared/public storage (`/sdcard`) is globally readable/writable; apps often misuse it instead of internal private storage.

---

## 6. Middleware & Web Access Control

### Browsers & Web Security
* **Same-Origin Policy (SOP)**: Scripts from origin A (protocol + host + port) cannot access or modify resources from origin B.
* **Confused Deputy Problem**:
  * A privileged entity (the "deputy", e.g., the browser or a proxy) is tricked by an attacker into misusing its authority to perform unauthorized actions on the user's behalf.
  * *Examples*: Cross-Site Scripting (XSS), Cross-Site Request Forgery (CSRF).

### Virtualization & Containers
* **Hypervisor (Ring -1)**: Runs VMs (Full vs. Para-virtualization).
  * *Note*: Malware can detect VM artifacts (timing, CPU IDs) and alter its behavior.
* **Docker / Containers**:
  * Uses Linux namespaces/cgroups (lightweight isolation).
  * **Security risk**: The Docker daemon runs as **root**. Anyone who can run Docker commands can gain root control of the host.

---

## 7. Hardware Access Control

### Privilege Rings
* **Ring 0**: Kernel / Most Privileged (full hardware access).
* **Rings 1 & 2**: Device drivers (rarely used in modern consumer OSes).
* **Ring 3**: User Applications / Least Privileged.
* **Ring -1 (VMX root mode)**: Hypervisor.
* **SMM (System Management Mode)**: Underneath Ring 0 / BIOS level.
* **Rule**: Lower numbered rings can inspect/control higher numbered rings, never vice-versa (**Principle of Least Privilege**).

### Hardware Memory & Key Protection
* **Segment / Page Addressing**: Triggers a **Segmentation Fault (`SIGSEGV`)** if a process attempts unauthorized cross-boundary reads/writes.
* **TPM (Trusted Platform Module)**: Hardware-isolated cryptographic chip for key generation, storage, and attestation.
* **ARM CHERI**: Hardware-enforced capabilities to guarantee spatial memory safety and prevent memory-corruption zero-days.

---

## 8. Critical Practice Questions & Common Traps

| Question Scenario | Correct Answer | Key Reason / Trap |
| :--- | :--- | :--- |
| *Can a user with Low clearance write to a Top-Secret file in Bell-LaPadula?* | **YES** | BLP only enforces **No Write Down**. Writing **UP** is allowed because it doesn't leak secrets downward (confidentiality maintained, though integrity is broken!). |
| *Can a user with High clearance write to a Low-clearance file in Bell-LaPadula?* | **NO** | Violates the **$\star$-property (No Write Down)**. |
| *What is the difference between a Covert Channel and a Side Channel?* | **Intent of communication path** | **Covert channel**: Using a channel *not intended for communication* (e.g., modulating CPU load) to deliberately pass secret data. **Side channel**: Passive leakage/inference (observing timing, power, heat). |
| *Who can delete a file in a directory with the Sticky Bit set?* | **Only the file owner or root** | Having write access to the directory is not enough to delete someone else's file. |
| *Why does Docker expand the attack surface if used for access control?* | **Docker daemon runs as root** | Any user granted access to interact with the Docker daemon effectively has root privileges. |
A3 Technical Interview | ELEC3609/9609 

https://pages.github.sydney.edu.au/2026S2-INTERNET-SOFTWAR... 

Week 13 

A3 Technical Interview 

# **ELEC3609/9609 - Week 13 Lab** 

## **A3 Technical Interview** 

Each group will participate in a technical interview conducted by the tutors, focusing on your **deployment setup** and **security configurations** for Assignment 3. 

## **Task Description** 

This lab session is a **technical interview** to assess your group’s understanding of your **deployment** and **security setup** in A3. Tutors will ask questions about: 

- Your **AWS deployment environment** and configuration decisions. 

- Web server and backend setup (e.g., Nginx, uWSGI, HTTPS). 

- Your implementation of key **security requirements** (authentication, permissions, firewall, HTTPS, etc.). 

- Technical challenges or decisions encountered during deployment and hardening. 

Be prepared to **explain, justify, and demonstrate** your deployment and security setup using a **live instance** and related configuration files. 

## **Presentation Order and Time Allocation** 

To efficiently manage lab time, interviews and deployment checks will run **in parallel** . 

### **Interview Flow** 

- Groups will be interviewed in **ascending group number order** _(e.g., Group 1 → Group 2 → Group 3 …)_ 

8/6/2026, 8:11 PM 

1 of 3 

A3 Technical Interview | ELEC3609/9609 

https://pages.github.sydney.edu.au/2026S2-INTERNET-SOFTWAR... 

- When your group number is called, **bring your laptop** to the tutor’s desk. 

- Each group will have **10 minutes total** , answer questions on deployment & security 

### **Parallel Deployment Check** 

- One tutor will conduct interviews at the tutor desk in ascending group order. 

- At the same time, the **second tutor will move around the room** to test deployments. 

- The second tutor will verify that your website is successfully deployed and functioning by interacting with it on your machine. 

#### **INFO** 



Please have your laptop ready and your deployed website accessible before your turn. 

### **Special Requests** 

If your group requires an earlier interview due to urgent circumstances, please inform tutors **before the lab begins.** 

## **During Interview** 

- Ensure your group has: 

   - A **deployed website running in one group member’s AWS Learner Lab EC2 instance** . 

   - Access to your **EC2 instance via terminal** (SSH). 

   - Access to key configuration files such as nginx.conf , uwsgi.ini <mark>,</mark> and your Django settings. 

- Be prepared to **demonstrate live** the deployment setup and security measures. 

- Be respectful and quiet while other groups are being interviewed. 

- All group members must attend and be prepared to answer. 

## **Reminder** 

8/6/2026, 8:11 PM 

2 of 3 

A3 Technical Interview | ELEC3609/9609 

https://pages.github.sydney.edu.au/2026S2-INTERNET-SOFTWAR... 

This interview is part of your final project mark and focuses on your **technical understanding of deployment and security** . 

To prepare: 

- **Practice accessing your EC2 instance** via command line. 

- Make sure you can **locate and explain configuration files quickly** (many groups waste time here). 

- If possible, **deploy your website on more than one member’s AWS Learner Lab environment** as a backup in case your primary instance is down. 

- Be familiar with how you implemented: 

   - HTTPS, reverse proxy, uWSGI 

   - SSH configuration and file permissions 

   - Django production settings 

   - Security hardening (e.g., limited DB permissions, disabled debug mode, cookie/JWT protection) 

## **Credit** 

This lab content was authored and maintained by **Jiawen Wen** , with materials adapted from prior offerings and updated to align with 2026 delivery. All standards used in this lab (IEEE, ISO/IEC) are referenced for educational purposes under fair use and are available to enrolled students via the university's licensed repository. 

8/6/2026, 8:11 PM 

3 of 3 


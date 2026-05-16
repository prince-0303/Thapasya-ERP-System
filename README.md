# Thapasya ERP: Institutional Management System

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Razorpay](https://img.shields.io/badge/Razorpay-02042B?style=for-the-badge&logo=razorpay)

## 📌 Overview
Thapasya ERP is a full-stack Enterprise Resource Planning solution designed to digitize administrative and academic workflows for a multi-branch arts institution. The system streamlines student lifecycles, from initial enquiry and course booking to automated fee management and real-time attendance tracking.

## 🚀 Key Features

### 💳 Secure Payment Engineering
* **End-to-End Integration:** Implemented the Razorpay API for seamless digital fee collection.
* **Cryptographic Security:** Enforced **HMAC-SHA256 signature verification** on both client-side verify endpoints and server-side webhooks to ensure transaction integrity.
* **Automated Reconciliation:** Built a background webhook listener to handle asynchronous events (`order.paid`, `payment.failed`), automatically updating student ledgers in Supabase.

### 🎓 Student & Academic Management
* **Dynamic Dashboards:** Developed a student-facing portal for viewing schedules, course logs, and personal attendance history.
* **Smart Attendance:** Integrated a tracking system that calculates "Total Present" counts and provides visual history calendars.
* **Multi-Branch Logic:** Designed the backend to support multiple physical branches under a single unified database schema.

### 🛠 Tech Stack
* **Backend:** FastAPI (Python), SQLAlchemy ORM, Pydantic.
* **Database:** PostgreSQL (Supabase), Alembic for database migrations.
* **Infrastructure:** Deployed on **AWS EC2** with **Nginx** reverse proxy and **AWS S3** for media storage.
* **Frontend:** React.js (Public Site) and Flutter (Mobile Application).
* **Communication:** WebSockets for real-time data transfers and Firebase for push notifications.

## 🏗 System Architecture
The backend follows a **Repository Pattern** to decouple business logic from data access, ensuring the system remains maintainable and testable as the institution scales.

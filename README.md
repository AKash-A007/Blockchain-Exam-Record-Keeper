# Blockchain Exam Record Keeper

**Tamper-Proof Student Marks using Blockchain and Docker**

This project is a Flask-based API that stores student exam results on a custom-built blockchain instead of a traditional database. Each student record is stored as a block containing:

- Hash of the previous block  
- Timestamp  
- Student roll number, subject, and marks  

This ensures exam records are immutable, auditable, and transparent.

Docker is used to containerize the application for ease of deployment and portability. An optional Redis setup is available for caching or pub/sub features.

---

## Features

- Add student marks as new blocks to the blockchain
- Retrieve the full blockchain ledger of results
- Verify blockchain integrity to detect tampering
- Optional Redis integration for faster queries or messaging
- Fully containerized with Docker and Docker Compose support

---

## Project Structure

├── app.py # Flask API and blockchain logic
├── requirements.txt # Python dependencies
├── Dockerfile # Docker image configuration
├── docker-compose.yml # Optional setup for Flask + Redis
├── chain.json # Stores persistent blockchain data
└── README.md # Project documentation

---

## API Endpoints

| Endpoint     | Method | Description                                |
|--------------|--------|--------------------------------------------|
| `/add_mark`  | POST   | Add a new student mark (requires JSON body)|
| `/chain`     | GET    | Retrieve the full blockchain               |
| `/verify`    | GET    | Check if the blockchain is valid           |

### Example JSON Payload for `/add_mark`

```json
{
  "roll_no": "101",
  "subject": "Math",
  "marks": 87
}

Running the Application with Docker
Option 1: Build and Run (Flask Only)
docker build -t exam-blockchain .
docker run -p 5000:5000 exam-blockchain


Application will be available at: http://localhost:5000

Option 2: Run with Docker Compose (Flask + Redis)
docker-compose up --build

Demo Usage
Add a Student Mark
curl -X POST http://localhost:5000/add_mark \
     -H "Content-Type: application/json" \
     -d '{"roll_no": "101", "subject": "Math", "marks": 87}'

Get the Blockchain
curl http://localhost:5000/chain

Verify Blockchain Integrity
curl http://localhost:5000/verify
```

##Why Blockchain?

Traditional databases allow updates and deletes, making them vulnerable to tampering.
Blockchain enforces immutability by linking each block to the previous one using cryptographic hashes.
Any unauthorized modification breaks the chain's integrity.

This makes blockchain an ideal solution for securely storing exam results.

Why Docker?

Packages the application and all its dependencies in a single container

Ensures consistent execution across environments

Simplifies deployment and scaling

Easily shareable through platforms like Docker Hub

Demonstrates practical DevOps and containerization skills

Key Learning Outcomes

Understanding blockchain fundamentals: hashing, immutability, linking blocks

Building REST APIs using Flask

Using Docker for containerization

Multi-container orchestration using Docker Compose

Integrating Redis for caching and messaging (optional)

Future Improvements

Implement authentication using JWT (for teacher access control)

Develop a web-based dashboard for students to view their marks

Simulate blockchain consensus across multiple nodes

Add role-based access and logging for audit trails

Author

Akash A

Tech Stack

Python

Flask

Docker

(Optional) Redis


Let me know if you'd like this saved as a downloadable `.md` file or need help publishing it to GitHub.

# Blockchain-Exam-Record-Keeper
🔒 Tamper-Proof Student Marks using Blockchain + Docker

This project is a Flask-based API that stores exam results on a mini blockchain instead of a traditional database.
Each student mark is stored as a block with:

Hash of previous block

Timestamp

Roll number + Marks

This ensures the exam records are immutable, auditable, and transparent.

Docker is used to containerize the application, making it easy to build, run, and share.

✨ Features

Add student marks as new blockchain blocks.

View the full blockchain ledger of results.

Verify chain integrity (detect tampering).

(Optional) Redis cache for faster blockchain queries or pub/sub notifications.

Fully containerized with Docker.

📂 Project Structure
├── app.py                # Flask API (Blockchain logic)
├── requirements.txt      # Dependencies
├── Dockerfile            # Docker build file
├── docker-compose.yml    # Optional: Flask + Redis multi-container setup
├── chain.json            # Stores blockchain data
└── README.md             # Project documentation

⚡ API Endpoints
Endpoint	Method	Description
/add_mark	POST	Add a new mark (JSON: roll_no, subject, marks)
/chain	GET	Get the full blockchain
/verify	GET	Check if the blockchain is valid
🐳 Running with Docker
1️⃣ Build and Run (Flask only)
docker build -t exam-blockchain .
docker run -p 5000:5000 exam-blockchain


App will be available at: http://localhost:5000

2️⃣ Run with Docker Compose (Flask + Redis)
docker-compose up --build

📊 Demo Usage
Add a student mark
curl -X POST http://localhost:5000/add_mark \
     -H "Content-Type: application/json" \
     -d '{"roll_no": "101", "subject": "Math", "marks": 87}'

Get the blockchain
curl http://localhost:5000/chain

Verify blockchain integrity
curl http://localhost:5000/verify

🎯 Why Blockchain?

Traditional databases allow updates/deletes → tampering possible.

Blockchain enforces immutability: each block references the previous block’s hash.

Any unauthorized change → chain becomes invalid.

Perfect fit for secure exam result storage.

🚀 Why Docker?

Package app + dependencies into one container.

Run anywhere without setup issues.

Push to Docker Hub → anyone can pull and run instantly.

Demonstrates modern DevOps deployment skills.

🏆 Key Learning Outcomes

Blockchain basics (immutability, hash linking).

REST API development with Flask.

Containerization with Docker.

Multi-container orchestration with Docker Compose.

Redis integration for caching / pub-sub.

📌 Future Improvements

Add authentication (JWT for teachers).

Web dashboard for students to view marks.

Blockchain consensus simulation with multiple nodes.

🔗 Author: Your Name
📅 Tech Stack: Python, Flask, Docker, (Optional Redis)

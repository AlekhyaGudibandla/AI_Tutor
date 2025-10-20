<!-- TITLE & HEADER ANIMATION -->
<h1 align="center">
  ✨ AI Tutor & Quiz App ✨  
</h1>

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Nunito&weight=600&size=24&pause=1000&color=00C853&center=true&vCenter=true&width=600&lines=Your+Personalised+AI+Tutor+%26+Quiz+Companion;Powered+by+Groq's+Llama+3.3+70B+Model;Built+with+FastAPI+%2B+Streamlit+%2B+Docker;Learn+Smarter%2C+Not+Harder+💫" alt="Typing SVG" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-success?logo=fastapi" />
  <img src="https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?logo=streamlit" />
  <img src="https://img.shields.io/badge/Containerized-Docker-blue?logo=docker" />
  <img src="https://img.shields.io/badge/Deployed%20on-AWS%20EC2-orange?logo=amazon-aws" />
  <img src="https://img.shields.io/badge/License-MIT-green" />
</p>

---

## 🌟 Overview

**AI Tutor & Quiz App** is your *intelligent study buddy*, personalizing education to match your learning style, knowledge level, and preferred language.

Whether you’re revising for exams or exploring a new subject, it adapts to **how you learn best** — and makes studying feel *effortless*.

💡 Powered by **Groq’s Llama 3.3 70B** model, it delivers natural explanations and generates dynamic quizzes tailored just for you.

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| 🧠 **AI Tutor** | Personalized explanations based on subject, learning style (hands-on, text-based, visual), and language (English, Hindi, Spanish, French, German). |
| 📝 **Quiz Generator** | Auto-generates quizzes. Pick subject, difficulty level, and number of questions (5–10). |
| 💬 **Simple UI** | Clean Streamlit interface — distraction-free and easy to use. |
| 🐳 **Dockerized Setup** | Run both FastAPI & Streamlit seamlessly with Docker Compose. |
| ☁️ **Deployed on AWS EC2** | Fully deployed — accessible globally via your EC2 public IP. |

---

## 🧩 Tech Stack

| Layer        | Technology              |
|--------------|--------------------------|
| **Frontend** | Streamlit                |
| **Backend**  | FastAPI                  |
| **AI Model** | Groq Llama 3.3 70B       |
| **Container**| Docker & Docker Compose  |
| **Deployment** | AWS EC2 + ECR         |
| **Language** | Python 3.10+             |

---

## ⚙️ Setup Instructions

### 🛠 1. Clone the Repository
```bash
git clone https://github.com/your-username/AI_Tutor.git
cd AI_Tutor
````

### 🔑 2. Configure Environment Variables

In both `backend/` and `frontend/`, create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

### 🧱 3. Run with Docker Compose

Make sure Docker is installed and running:

```bash
docker compose up --build
```

* Frontend → [http://localhost:8501](http://localhost:8501)
* Backend → [http://localhost:8000](http://localhost:8000)

---

## 🚀 AWS EC2 Deployment

1. Push Docker images to **Amazon ECR**.
2. SSH into your **EC2 instance**, pull the images.
3. Run:

```bash
docker run -d -p 8501:8501 your-frontend-image
docker run -d -p 8000:8000 your-backend-image
```

4. Open your EC2 public IP:

```
http://<your-ec2-ip>:8501
```

---

## 🗂 Folder Structure

```
AI_Tutor/
├── backend/
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
└── README.md
```

---

## 🌈 Future Enhancements

* 📊 Track learning progress
* 📈 Quiz performance analytics
* 💡 Smart topic recommendations
* 🌍 Multilingual voice interaction

---

## 💡 Why This Project?

Let’s face it — studying can feel *boring and repetitive*.
This app fixes that with **AI-powered personalization** that makes learning feel natural, effective, and a little magical.
Think of it as your own *AI-powered study coach* — but way cooler.

---

## 🧑‍💻 Author

**👩‍💻 Alekhya Gudibandla**
🎓 B.Tech in Mathematics and Computing
💬 Passionate about AI, ML & creative EdTech innovation

<p align="center">
  <a href="https://github.com/AlekhyaGudibandla"><img src="https://img.shields.io/badge/GitHub-Profile-black?logo=github" /></a>
  <a href="https://www.linkedin.com/in/alekhya-gudibandla-3571b5256/"><img src="https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin" /></a>
  <a href="mailto:alekhyagudibandla2005@gmail.com"><img src="https://img.shields.io/badge/Email-Contact-red?logo=gmail" /></a>
</p>

---

## 🪪 License

Licensed under the **MIT License** — free for personal and commercial use.

---

<h3 align="center">
  💡 “Learn smarter, not harder — with a little help from AI.” 💫
</h3>

<p align="center">
  <img src="https://raw.githubusercontent.com/saadeghi/saadeghi/master/dino.gif" width="500" />
</p>

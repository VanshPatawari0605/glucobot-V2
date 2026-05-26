# 🩺 GlucoBot v2 — AI Diabetes Risk Assessment

<div align="center">

### Predict. Prevent. Protect.

An AI-powered diabetes risk screening platform built using Machine Learning, FastAPI, and Gemini AI.

🌐 **Live Demo:** https://glucobot-v2.vercel.app/

</div>

---

# 📌 About The Project

GlucoBot v2 is a modern full-stack healthcare web application designed to help users quickly assess their diabetes risk using clinically relevant health parameters.

The application combines:
- 🧠 Machine Learning prediction
- 💬 AI health assistant
- 📄 PDF report generation
- 📎 Medical report parsing
- ⚡ FastAPI backend
- 🎨 Responsive medical-grade frontend

This project is a complete upgrade from the original Streamlit prototype into a scalable production-style architecture using FastAPI + Vanilla JS frontend.

---

# ✨ Features

## 🔬 AI Diabetes Risk Scan
- 8 health input fields
- Real-time prediction
- Animated risk gauge
- Risk classification:
  - Low Risk
  - Moderate Risk
  - High Risk

---

## 📄 Downloadable Health Report
Generate a professional PDF report containing:
- Risk score
- Prediction summary
- User health inputs
- Donut chart visualization
- Personalized recommendations

---

## 💬 Gemini AI Health Assistant
Integrated with Google Gemini 2.5 Flash:
- Diabetes-related Q&A
- Lifestyle suggestions
- General healthcare guidance

---

## 📎 Smart Medical PDF Upload
Upload medical reports and auto-extract:
- Glucose
- BMI
- Blood Pressure
- Age
- Insulin

---

## 🤖 Animated UI Experience
- Robot doctor splash screen
- Smooth animations
- Medical-style interface
- Fully responsive design

---

# 🧠 Machine Learning Pipeline

| Component | Details |
|---|---|
| Dataset | Pima Indians Diabetes Dataset |
| Samples | 768 |
| Features | 9 |
| Preprocessing | Median Imputation + StandardScaler |
| Balancing | SMOTE |
| Feature Engineering | BMI×Age, Glucose×BMI, Glucose×Insulin |
| Algorithms | LR, KNN, SVM, RF, Gradient Boosting, XGBoost |
| Final Model | Soft Voting Ensemble |

---

# 📊 Model Accuracy Comparison

| Model | Accuracy |
|---|---|
| KNN | 74% |
| Logistic Regression | 76% |
| SVM | 78% |
| Gradient Boosting | 81% |
| Random Forest | 82% |
| XGBoost | 83% |
| ⭐ Voting Ensemble | **87%** |

---

# 🏗️ Project Architecture

```bash
glucobot-v2/
│
├── backend/
│   ├── main.py
│   ├── utils/
│   │   ├── predict.py
│   │   ├── chat.py
│   │   ├── pdf_gen.py
│   │   └── pdf_reader.py
│   │
│   ├── model/
│   │   ├── diabetes_model.pkl
│   │   └── scaler.pkl
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── scan.html
│   ├── chat.html
│   └── css/style.css
│
└── README.md
```

---

# 🛠️ Tech Stack

## Backend
- Python
- FastAPI
- Uvicorn
- Scikit-learn
- XGBoost
- ReportLab
- Google Gemini API

## Frontend
- HTML5
- CSS3
- Vanilla JavaScript
- Responsive UI Design

## Machine Learning
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- SMOTE

---

# 🚀 Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/VanshPatawari0605/glucobot-v2.git
cd glucobot-v2
```

---

## 2️⃣ Backend Setup

```bash
cd backend

python -m venv venv
```

### Activate Environment

### Windows
```bash
venv\Scripts\activate
```

### Mac/Linux
```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Add Gemini API Key

Create a `.env` file inside the backend folder:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## 5️⃣ Run Backend Server

```bash
uvicorn main:app --reload
```

Backend will run on:

```bash
http://127.0.0.1:8000
```

Swagger Docs:

```bash
http://127.0.0.1:8000/docs
```

---

## 6️⃣ Run Frontend

Open:

```bash
frontend/index.html
```

OR use Live Server extension in VS Code.

---

# 🌐 Deployment

| Layer | Platform |
|---|---|
| Frontend | Vercel |
| Backend | Render |

### Live Website
https://glucobot-v2.vercel.app/

---

# 📷 Screenshots

## 🏠 Landing Page
(Add Screenshot Here)

## 🔬 Risk Scan
(Add Screenshot Here)

## 💬 AI Chat Assistant
(Add Screenshot Here)

## 📄 PDF Report
(Add Screenshot Here)

---

# 🔮 Future Improvements

- User authentication
- Medical history tracking
- Multi-language support
- Doctor dashboard
- Cloud database integration
- Advanced analytics

---

# ⚠️ Disclaimer

GlucoBot is an educational and screening tool only.

It is NOT a substitute for:
- Professional medical advice
- Diagnosis
- Clinical treatment

Always consult qualified healthcare professionals.

---

# 👨‍💻 Author

## Vansh Patawari
B.Tech Information Technology  
KIIT University

### GitHub
https://github.com/VanshPatawari0605

### LinkedIn
https://linkedin.com/in/vansh-patawari-8ab0432a8

---

# ⭐ Support

If you liked this project:

- ⭐ Star the repository
- 🍴 Fork the project
- 📢 Share it with others

---

<div align="center">

### Built with ❤️ by Vansh Patawari

</div>

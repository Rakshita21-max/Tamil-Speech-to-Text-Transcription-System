# 🎙️ Tamil Speech-to-Text Transcription System (Whisper)

## 📌 Overview

This project is a **Tamil Speech-to-Text Transcription System** built using OpenAI’s Whisper model.
It allows users to upload or record Tamil audio and receive accurate text output.

The system is designed with a modular architecture for **training, preprocessing, and deployment**, making it suitable for research and real-world applications.

---

## 🚀 Features

* 🎧 Convert Tamil speech to text
* 🤖 Powered by Whisper (Deep Learning model)
* 🌐 Simple UI using Gradio
* 📂 Support for local dataset training
* ⚡ Easy deployment and execution

---

## 🏗️ Project Structure

```
tamil-speech-to-text/
│
├── app/
│   ├── main.py          # Entry point
│   ├── ui.py            # UI using Gradio
│
├── model/
│   ├── train.py         # Model training
│   ├── inference.py     # Speech-to-text logic
│
├── data/
│   ├── dataset/         # Audio dataset
│
├── utils/
│   ├── preprocess.py    # Data preprocessing
│
├── requirements.txt
├── start_app.bat
├── .gitignore
```

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone <your-repo-link>
cd tamil-speech-to-text
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### 3️⃣ Activate Environment

```bash
venv\Scripts\activate
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
python app/main.py
```

OR (Windows):

```bash
start_app.bat
```

---

## 🧠 How It Works

1. User uploads Tamil audio via UI
2. Audio is passed to Whisper model
3. Model processes and converts speech → text
4. Output is displayed instantly

---

## 👥 Team Responsibilities

| Role        | Responsibility                  |
| ----------- | ------------------------------- |
| Frontend    | UI development using Gradio     |
| Model       | Training Whisper model          |
| Dataset     | Data collection & preprocessing |
| Integration | Deployment & system integration |

---

## 🔧 Technologies Used

* Python
* OpenAI Whisper
* PyTorch
* Gradio
* Hugging Face (optional for fine-tuning)

---

## 📊 Future Enhancements

* Fine-tuning Whisper for better Tamil accuracy
* Real-time speech recognition
* Emotion-aware transcription
* Multi-language support

---

## 🚫 .gitignore Includes

```
venv/
__pycache__/
*.pyc
data/
last_ui_error.txt
```

---

## 📜 License

This project is for academic and research purposes.

---

## 🙌 Acknowledgements

* OpenAI Whisper
* Hugging Face
* Gradio

---
---
Dark & Light Mode Theme Toggle

This project demonstrates how to implement a Dark Mode and Light Mode toggle using HTML, CSS. It allows users to switch between themes and saves their preference for future visits.

---
Then Based on Error Reduse For Overfitting 
* because Training data is accacuy good but testing low fit

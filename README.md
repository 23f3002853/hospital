# 📞 Hospital Call App

## 🔗 Deployed Link
http://localhost:5500  


---

## 📌 Project Description
The Hospital Call App is a voice-enabled appointment booking system that simulates a real-time phone call experience.  
Users can interact using voice or text to book appointments with hospital departments and doctors.

---

## 🚀 Features
- 📞 Call simulation interface  
- 🎤 Voice input using Speech Recognition  
- 🔊 Voice output using Text-to-Speech  
- 🤖 Rasa chatbot integration  
- 🏥 Appointment booking flow (Department → Doctor)  
- ⚠️ Error handling (no response, server offline, empty input)  

---

## 🛠️ Technologies Used
- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Rasa (Python)  
- **Voice:** Web Speech API  
- **Database:** SQLite (for logging/appointments)  

---

## ▶️ How to Run the Project

### 1. Start Rasa Server
```bash
rasa run --enable-api --cors "*"

### 2. Start Action Server
```bash
rasa run actions
3. Run Frontend

Open index.html in browser
OR run:
```bash
python -m http.server 5500

Then open:
```bash
http://localhost:5500
### 📂 Project Structure
hospital/
│── index.html
│── domain.yml
│── nlu.yml
│── stories.yml
│── rules.yml
│── credentials.yml
│── endpoints.yml
│── README.md
### 🧪 Testing

The system was tested for:

Greeting recognition
Appointment booking flow
Voice input/output
Database storage
Server offline handling

All test cases passed successfully ✅

### 🐞 Defect Fixes
Fixed no response issue by retraining Rasa
Fixed "None" values in responses
Fixed voice playback issues
Fixed API connection errors

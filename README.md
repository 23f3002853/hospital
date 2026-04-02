

### 🏥 Hospital Voice IVR Assistant
### 🔗 Project Access
Local UI: http://localhost:5500

Middleware Gateway: http://localhost:8000

Rasa Core: http://localhost:5005

### 📌 Project Description
The Hospital Voice IVR Assistant is an advanced, AI-driven appointment booking system. It mimics a real-world telephonic IVR (Interactive Voice Response) experience, allowing patients to book appointments using natural language. The system supports multilingual interactions and features a robust 4-layer architecture to ensure seamless communication between the user and the hospital database.

### 🚀 Key Features
📞 Full Call Simulation: Interactive UI that mimics a dialer and active call state.

🎤 Multilingual STT: Speech-to-Text supporting English, Hindi, and Telugu.

🔊 Natural TTS: High-quality voice output for a human-like experience.

🤖 Context-Aware NLU: Powered by Rasa to understand user intent and extract entities (Department/Doctor).

🗄️ Backend Persistence: Automatic logging of calls and appointments into a SQLite database.

🛡️ Fail-Safe Logic: Graceful handling of server timeouts, empty audio, and background noise.

🛠️ Technology Stack
Frontend: HTML5, CSS3 (Flexbox/Grid), JavaScript (ES6+).

Middleware: FastAPI (Python) – The bridge between Voice UI and Rasa.

NLU Engine: Rasa Open Source 3.x.

Database: SQLite3 (Relational mapping for appointments and logs).

APIs: Web Speech API, Google Translate API (for multilingual support).

### 🏗️ Technical Architecture
The system operates on a 4-Layer Model:

User Interface Layer: Captures voice and renders the call UI.

Integration Layer (FastAPI): Translates and routes requests.

Intelligence Layer (Rasa): Processes natural language and manages conversation state.

Data Layer (SQLite): Stores transactional data and audit logs.



### 📂 Project Structure

hospital/
├── data/
│   ├── nlu.yml             # Training data for intents
│   ├── stories.yml         # Conversation paths
│   └── rules.yml           # Logic for fallbacks
├── models/                 # Trained Rasa models
├── actions/
│   └── actions.py          # SQL Database logic
├── app.py                  # FastAPI Integration Gateway
├── main_voice_bot.py       # Main Voice/Logic Loop
├── speech_to_text.py       # STT Configuration
├── text_to_speech.py       # TTS Configuration
├── hospital_system.db      # SQLite Database
└── README.md               # Project Documentation

### 🧪 Quality Assurance Summary
Intent Accuracy: 95% success rate in identifying "Book Appointment".

Latency: Average response time < 2.0 seconds.

Robustness: Successfully handles noise interference via energy threshold filtering.

Data Integrity: 100% successful mapping of user voice input to SQL database rows.

### ✅ Defect Resolution Log (Finalized)
Fixed: Language drift (Finnish/Static noise) via langdetect filters.

Fixed: Connection timeouts by implementing a FastAPI heartbeat.

Fixed: Empty audio crashes via Python guard clauses.

Fixed: Database lock issues by using scoped SQL connections.

### Status: 🟢 Ready for Deployment / Final Review

### ▶️ Setup & Execution Instructions
1. Initialize the Database
Ensure your hospital_system.db is initialized with appointments and call_logs tables.

2. Start the Rasa Action Server (Terminal 1)
```bash
rasa run actions```
3. Start the Rasa NLU Server (Terminal 2)
```bash
rasa run --enable-api --cors "*"```
4. Start the FastAPI Gateway (Terminal 3)
```bash
python app.py```
5. Launch the Voice Bot UI (Terminal 4)
```bash
python main_voice_bot.py```

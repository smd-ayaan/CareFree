# CarePass — AI Health-Screening Access System

**One-liner:** A contactless access-control system that verifies identity via ArcFace facial recognition and screens real-time health vitals (SpO2, heart rate, ECG, blood pressure, respiratory rate) before granting entry.

---

## Overview

CarePass extends a reference IoT access-control paper (Hiremani et al., 2022) by replacing its conventional Dlib-based face recognition with **ArcFace** deep embeddings for significantly higher accuracy, and by adding genuine **multimodal health screening** — a capability the base paper claimed but never implemented.

Access is granted only when a person is **recognized AND physiologically normal**. If recognized but showing abnormal vitals, the system flags the entry for review instead of outright denial.

## Features

- Contactless facial recognition using ArcFace (512-D embeddings, cosine similarity matching)
- Real-time vitals: SpO2, Heart Rate, ECG, Blood Pressure (derived), Respiratory Rate (derived)
- Web-based frontend with live scan flow
- Local Flask backend — no cloud dependency
- SQLite-based enrollment and access logging
- Low-cost hardware (~₹1,000–1,500): Arduino Nano, MAX30102, AD8232

## Tech Stack

| Layer | Tools |
|---|---|
| Face Recognition | Python, `insightface` (ArcFace), OpenCV |
| Backend | Flask, SQLite |
| Frontend | HTML, CSS, vanilla JS |
| Hardware | Arduino Nano, MAX30102 (PPG), AD8232 (ECG) |
| Firmware | Arduino C++ |

## Project Structure

```
├── app.py              # Flask server — serves frontend, exposes /api/scan
├── face_service.py      # ArcFace-based face capture + matching logic
├── database.py           # SQLite: enrolled users + access logs
├── enroll.py              # CLI script to enroll a new face
├── recognize.py           # Standalone live-recognition test script
├── carepass.html          # Frontend — scan flow + result screens
└── arduino_firmware/
    └── sensor_reader.ino   # Reads MAX30102 + AD8232, sends over Serial
```

## Setup

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install flask insightface onnxruntime opencv-python numpy pyserial scipy
```

## Usage

**1. Enroll a user:**
```bash
python enroll.py
```

**2. Run the app:**
```bash
python app.py
```

**3. Open in browser:**
```
http://127.0.0.1:5000
```

## Reference

Hiremani, N. et al. "Artificial Intelligence-Powered Contactless Face Recognition Technique for Internet of Things Access for Smart Mobility." *Wireless Communications and Mobile Computing*, 2022.

## Status

🚧 In development — Embedded System Architecture course project.

- [x] Face recognition (ArcFace) — enrollment + live matching
- [x] Frontend-backend bridge (Flask)
- [ ] Vitals processing (MAX30102 + AD8232 integration)
- [ ] Decision engine (identity + vitals fusion)
- [ ] Hardware integration (servo, LED, buzzer feedback)

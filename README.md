<h1 align="center">🚀 Ensemble Deep Learning Framework for</h1>

<h3 align="center">Multi-Object Detection & Human Attribute Analysis using AI</h3>

<p align="center">
  <b>A powerful AI-based web application for detecting objects, identifying people, and analyzing human attributes like gender & emotion.</b>
</p>

---

<h2>✨ Features</h2>

<ul>
  <li>🧠 <b>Multi-Object Detection</b> using YOLO</li>
  <li>👤 <b>Person Identification</b> (P1, P2, P3...)</li>
  <li>😊 <b>Emotion Detection</b> (Happy, Sad, Angry, Neutral)</li>
  <li>🚻 <b>Gender Classification</b> (Male / Female)</li>
</ul>

<h3>🎥 Supports</h3>
<ul>
  <li>📷 Image Upload</li>
  <li>🎬 Video Upload</li>
  <li>📹 Live Camera Recording</li>
</ul>

<h3>📊 Displays</h3>
<ul>
  <li>Total Persons Count</li>
  <li>Male / Female Count</li>
  <li>Person-wise Details</li>
  <li>Object Class-wise Counts</li>
</ul>

---

<h2>🏗️ Architecture</h2>

<pre>
Frontend (React.js)
        ↓
Backend API (Flask)
        ↓
Core ML Pipeline (core_pipeline.py)
        ↓
Models:
   - YOLO (Object Detection)
   - MTCNN (Face Detection)
   - EfficientNetV2-L (Gender + Emotion)
</pre>

---

<h2>📁 Project Structure</h2>

<pre>
Major Project Testing/
│
├── backend/
│   ├── app.py
│   ├── core_pipeline.py
│   ├── uploads/
│
├── frontend/
│   ├── src/
│   ├── package.json
│
├── models/ (Not included in repo)
│
├── test_combined.py
├── requirements.txt
└── README.md
</pre>

---

<h2>⚙️ Installation & Setup</h2>

<h3>1️⃣ Clone Repository</h3>

<pre>
git clone https://github.com/Govardhan2302/Essemble-DeepLearning-Framework-for-Multi-Object-Detection-and-Human-Attribute-Analysis.git
cd Essemble-DeepLearning-Framework-for-Multi-Object-Detection-and-Human-Attribute-Analysis
</pre>

<h3>2️⃣ Backend Setup (Flask)</h3>

<pre>
cd backend
pip install -r requirements.txt
python app.py
</pre>

<p>Backend runs at: <b>http://127.0.0.1:5000</b></p>

<h3>3️⃣ Frontend Setup (React)</h3>

<pre>
cd frontend
npm install
npm start
</pre>

<p>Frontend runs at: <b>http://localhost:3000</b></p>

---

<h2>📸 Usage</h2>

<h3>🔹 Image</h3>
<ul>
  <li>Upload image → Click Analyze</li>
</ul>

<h3>🔹 Video</h3>
<ul>
  <li>Upload video → Click Analyze</li>
</ul>

<h3>🔹 Live Camera</h3>
<ul>
  <li>Open Camera → Start → Stop → Analyze</li>
</ul>

---

<h2>📊 Output</h2>

<h3>🧾 Console Output</h3>

<pre>
===== FINAL COUNTS =====
Persons: 11
Male: 7
Female: 4

P1 | male | angry
P2 | female | surprise

chair: 4
</pre>

<h3>🌐 Web Output</h3>

<ul>
  <li>Bounding Boxes with Labels</li>
  <li>Summary Counts</li>
  <li>Person Details Table</li>
</ul>

---

<h2>🧠 Models Used</h2>

<table border="1" cellpadding="8">
<tr>
<th>Task</th>
<th>Model</th>
</tr>
<tr>
<td>Object Detection</td>
<td>YOLO</td>
</tr>
<tr>
<td>Face Detection</td>
<td>MTCNN</td>
</tr>
<tr>
<td>Gender Detection</td>
<td>EfficientNetV2-L</td>
</tr>
<tr>
<td>Emotion Detection</td>
<td>EfficientNetV2-L</td>
</tr>
</table>

---

<h2>⚠️ Known Issues</h2>

<ul>
  <li>Webcam may not work without HTTPS</li>
  <li>Large videos take time</li>
  <li>GPU recommended</li>
</ul>

---

<h2>🚀 Future Improvements</h2>

<ul>
  <li>Real-time streaming</li>
  <li>Face tracking</li>
  <li>Age detection</li>
  <li>Cloud deployment</li>
</ul>

---

<h2>📦 Requirements</h2>

<pre>
flask
flask-cors
opencv-python
torch
torchvision
ultralytics
mtcnn
numpy
Pillow
</pre>

---

<h2>👨‍💻 Author</h2>

<p><b>Bharath Reddy Kadiveti</b></p>

---

<h2>📜 License</h2>

<p>Academic and research purposes only.</p>

---

<h2 align="center">⭐ If you like this project, give it a star!</h2>

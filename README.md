# 🚀 Social Ads Predictor: End-to-End MLOps Pipeline

This project demonstrates a **production-ready Machine Learning deployment pipeline**. It trains a classification model to predict whether a user will purchase a product based on **Gender, Age, and Estimated Salary**, and serves it as a **scalable, containerized API** using **BentoML** and **Docker**.

---

## 🏗 Architecture Overview

The application follows a **decoupled Client–Server architecture**, simulating a real-world production environment.

### 🔧 Backend (The Brain)

* **Tech Stack:** BentoML, ONNX Runtime, Scikit-Learn
* **Deployment:** Wrapped in a Docker Container (Linux/Debian)
* **Role:** Exposes a REST API on port **3000** to handle inference requests

### 🎨 Frontend (The Face)

* **Tech Stack:** Streamlit (Python)
* **Deployment:** Runs locally on the host machine
* **Role:** Captures user input (Gender, Age, Salary) and sends HTTP requests to the Backend

---

## 📂 Project Structure

```text
social-ads-bento/
├── service.py              # BentoML Service logic (API endpoints)
├── bentofile.yaml          # Configuration for building the Bento (Dependencies, Docker rules)
├── train.py                # Training script (Scikit-Learn -> ONNX conversion)
├── frontend.py             # Streamlit User Interface code
├── Social_Network_Ads.csv  # Dataset used for training
├── requirements.txt        # Python dependencies for the Frontend
└── README.md               # Project documentation
```

---

## 🛠 Prerequisites

* **Docker Desktop** (Must be installed and running)
* **Python 3.10+** (For local development)

---

## 🚀 How to Run the Project

### Phase 1: Setup & Training

#### 1️⃣ Installation

Clone the repository and set up your Python environment:

```bash
# 1. Create a virtual environment
python -m venv venv

# 2. Activate the environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```


#### 2️⃣ Train the Model

Run the training script to train the classifier and convert it to ONNX. This saves the model to your local BentoML store:

```bash
python train.py
```

**Output:** You should see a message confirming the model `social_ads_onnx:latest` has been saved.

---

### 🔍 Optional: Test the Service Locally (Without Docker)

Before building the Bento and containerizing the service, you can run the backend
locally to validate that the model and API work correctly.

```bash
bentoml serve service.py --reload

### Phase 2: Build & Run Backend (Docker)

In this phase, we package the model into a **Bento** and run it as a Docker container.

#### 1️⃣ Build the Bento

This packs the model, code, and dependencies defined in `bentofile.yaml`.

```bash
bentoml build
```

> **Important:** Take note of the TAG generated in the output (e.g., `onnx_ads_service:hyrfaa6ykkjyhigt`).

#### 2️⃣ Containerize (Create Docker Image)

Convert the Bento into a standard OCI-compliant Docker image:

```bash
# Replace 'TAG' with the actual tag from the previous step
bentoml containerize onnx_ads_service:TAG
```

#### 3️⃣ Run the Docker Container

Start the inference server inside an isolated Linux container:

```bash
# -p 3000:3000 maps the container's port to your machine
# --rm automatically deletes the container when you stop it
docker run --rm -p 3000:3000 onnx_ads_service:TAG
```

✅ **Verify:** Open [http://localhost:3000](http://localhost:3000) to see the Swagger UI. The backend is now live!

---

### Phase 3: Run the Frontend (Streamlit)

Leave the Docker terminal open. Open a new terminal window to run the user interface.

#### 1️⃣ Activate Environment

Ensure you are inside your virtual environment:

```bash
# Windows:
venv\Scripts\activate
```

#### 2️⃣ Launch the Streamlit App

```bash
streamlit run frontend.py
```

🌐 **Access:** The app will open automatically in your browser (usually at [http://localhost:8501](http://localhost:8501)).

---

## 🧪 Usage

1. **Input Data:** Select Gender, Age, and Salary in the web interface
2. **Predict:** Click the **Predict Purchase** button
3. **Result:** The frontend sends a request to the Docker container (`http://localhost:3000/predict`) and displays whether the user is likely to purchase

---

## 💡 Key MLOps Concepts Demonstrated

* **Reproducibility**
  Using `bentoml containerize`, the model ships with its own OS and libraries, eliminating the *“it works on my machine”* problem.

* **Model Portability**
  The Docker image is cloud-agnostic and can be deployed to **AWS, Kubernetes, or Azure** without changing any code.

* **Interoperability**
  ONNX Runtime enables high-performance inference, fully decoupled from the original training framework.

---

🔥 *This project is a clean, real-world example of how ML models should be trained, packaged, and served in production.*

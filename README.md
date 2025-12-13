🚀 Social Ads Predictor: End-to-End MLOps PipelineThis project demonstrates a production-ready Machine Learning deployment pipeline. It trains a classification model to predict if a user will purchase a product based on their Gender, Age, and Estimated Salary, and serves it as a scalable, containerized API using BentoML and Docker.🏗 Architecture OverviewThe application follows a decoupled Client-Server architecture, simulating a real-world production environment:Backend (The Brain):Tech Stack: BentoML, ONNX Runtime, Scikit-Learn.Deployment: Wrapped in a Docker Container (Linux/Debian).Role: Exposes a REST API on port 3000 to handle inference requests.Frontend (The Face):Tech Stack: Streamlit (Python).Deployment: Runs locally on the host machine.Role: Captures user input (Gender, Age, Salary) and sends HTTP requests to the Backend.📂 Project Structuresocial-ads-bento/
├── service.py              # BentoML Service logic (API endpoints)
├── bentofile.yaml          # Configuration for building the Bento (Dependencies, Docker rules)
├── train.py                # Training script (Scikit-Learn -> ONNX conversion)
├── frontend.py             # Streamlit User Interface code
├── Social_Network_Ads.csv  # Dataset used for training
├── requirements.txt        # Python dependencies for the Frontend
└── README.md               # Project documentation
🛠 PrerequisitesDocker Desktop (Must be installed and running).Python 3.10+ (For local development).🚀 How to Run the ProjectFollow these steps to set up the environment, train the model, and run the application.Phase 1: Setup & Training1. InstallationClone the repository and set up your Python environment.# 1. Create a virtual environment
python -m venv venv

# 2. Activate the environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
2. Train the ModelRun the training script to train the classifier and convert it to ONNX. This saves the model to your local BentoML store.python train.py
Output: You should see a message confirming the model social_ads_onnx:latest has been saved.Phase 2: Build & Run Backend (Docker)In this phase, we package the model into a "Bento" and run it as a Docker container.1. Build the BentoThis packs the model, code, and dependencies defined in bentofile.yaml.bentoml build
Important: Take note of the TAG generated in the output (e.g., onnx_ads_service:hyrfaa6ykkjyhigt).2. Containerize (Create Docker Image)Convert the Bento into a standard OCI-compliant Docker image.# Replace 'TAG' with the actual tag from the previous step
bentoml containerize onnx_ads_service:TAG
3. Run the Docker ContainerStart the inference server inside an isolated Linux container.# -p 3000:3000 maps the container's port to your machine
# --rm automatically deletes the container when you stop it
docker run --rm -p 3000:3000 onnx_ads_service:TAG
Verify: Open http://localhost:3000 to see the Swagger UI. The backend is now live!Phase 3: Run the Frontend (Streamlit)Leave the Docker terminal open. Open a new terminal window to run the user interface.1. Activate EnvironmentEnsure you are inside your virtual environment.# Windows:
venv\Scripts\activate
2. Launch the Streamlit Appstreamlit run frontend.py
Access: The app will open automatically in your browser (usually at http://localhost:8501).🧪 UsageInput Data: Select Gender, Age, and Salary in the web interface.Predict: Click the "Predict Purchase" button.Result: The frontend sends a request to the Docker container (http://localhost:3000/predict) and displays whether the user is likely to purchase.💡 Key MLOps Concepts DemonstratedReproducibility: By using bentoml containerize, we solve the "It works on my machine" problem. The model ships with its own OS and libraries, guaranteed to run anywhere.Model Portability: The Docker image produced here is cloud-agnostic and can be deployed to AWS, Kubernetes, or Azure without changing code.Interoperability: Uses ONNX Runtime for high-performance inference, decoupled from the training framework.
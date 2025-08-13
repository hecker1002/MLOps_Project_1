

# 🚀 End-to-End MLOps Project – From Data to Deployment

An **industrial-grade Machine Learning pipeline** that takes raw data from a live database, processes it through a robust CI/CD-enabled MLOps workflow, trains and validates a model, and deploys it on AWS using Docker & FastAPI — fully automated with GitHub Actions.

![MLOps Flow](assets/mlops_pipeline.png) <!-- optional: insert a pipeline diagram -->

---

## 📌 Features

* **Automated Project Structure Generation** – Uses `template.py` to scaffold folders/files instantly.
* **Environment Isolation** – Reproducible builds using Conda environments & `requirements.txt`.
* **Cloud-Hosted NoSQL Database** – MongoDB Atlas for real-time data storage & retrieval.
* **Modular Components** – Data Ingestion, Validation, Transformation, Training, and Model Pushing.
* **Model Versioning & Storage** – AWS S3 integration for storing and retrieving models.
* **FastAPI Deployment** – Model served via a REST API with async support.
* **Containerized & Cloud-Ready** – Dockerized for portability, deployed on AWS EC2.
* **CI/CD Pipeline** – Automated testing, build, and deployment with GitHub Actions.

---

## 🏗️ Pipeline Overview

| Stage                      | Description                                                                                |
| -------------------------- | ------------------------------------------------------------------------------------------ |
| **1. Project Setup**       | Auto-generate folders & files with `template.py`; configure `setup.py` & `pyproject.toml`. |
| **2. Environment Setup**   | Create & activate a dedicated Conda environment; install dependencies.                     |
| **3. Database Setup**      | Connect to MongoDB Atlas; store & retrieve datasets securely via environment variables.    |
| **4. Data Ingestion**      | Pull raw data from MongoDB, split into train/test, store artifacts.                        |
| **5. Data Validation**     | Validate schema & columns using `schema.yaml`.                                             |
| **6. Data Transformation** | Scale & preprocess data for training.                                                      |
| **7. Model Training**      | Train ML model with predefined hyperparameters; save if performance improves.              |
| **8. Model Storage**       | Push trained model to AWS S3 for versioning.                                               |
| **9. Model Deployment**    | Deploy via FastAPI; containerize with Docker.                                              |
| **10. CI/CD Automation**   | GitHub Actions pipeline for build, push, and deploy to AWS EC2.                            |

---

## 🛠️ Tech Stack

**Languages & Frameworks:**

* Python, FastAPI, Pandas, Scikit-learn, PyMongo

**Cloud & Infrastructure:**

* MongoDB Atlas, AWS S3, AWS ECR, AWS EC2

**DevOps & Automation:**

* Docker, GitHub Actions, CI/CD, Environment Variables

---

## 📂 Project Structure

```
.
├── src/
│   ├── components/           # Modular pipeline components
│   ├── entity/               # Config & artifact entities
│   ├── utils/                # Helper functions
│   ├── constants/            # Global constants
│   ├── pipelines/            # Training & prediction pipelines
│   └── config/               # DB & cloud configurations
├── artifacts/                # Generated datasets & reports (gitignored)
├── .github/workflows/        # CI/CD workflows
├── Dockerfile
├── requirements.txt
├── setup.py
└── README.md
```

---

## ⚡ Quick Start

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/mlops-project.git
cd mlops-project
```

### 2️⃣ Create and activate Conda environment

```bash
conda create -n mlops-env python=3.10 -y
conda activate mlops-env
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set up environment variables

```bash
export MONGODB_URL="your_mongo_connection_string"
export AWS_ACCESS_KEY_ID="your_aws_key"
export AWS_SECRET_ACCESS_KEY="your_aws_secret"
```

### 5️⃣ Run training pipeline

```bash
python src/pipelines/training_pipeline.py
```

### 6️⃣ Deploy with FastAPI

```bash
uvicorn app:app --reload
```

---

## 🌐 Deployment

* **Docker** – Build and run locally:

  ```bash
  docker build -t mlops-app .
  docker run -p 5000:5000 mlops-app
  ```
* **AWS EC2** – Pull Docker image from AWS ECR & run.
* **CI/CD** – Triggered on `git push` to `main`, fully automating build & deploy.

---

## 📊 Key Highlights for Recruiters

✅ **End-to-End Ownership** – Covers *data ingestion → deployment*
✅ **Production-Grade MLOps** – Environment variables, logging, exception handling, artifacts
✅ **Cloud-Native** – MongoDB Atlas + AWS S3 + AWS EC2 + AWS ECR
✅ **Automation First** – GitHub Actions CI/CD pipeline
✅ **Scalable API** – FastAPI with async support

---

## 🧠 Future Enhancements

* Add monitoring with Prometheus & Grafana
* Enable A/B testing for model selection
* Integrate MLflow for experiment tracking

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first to discuss.

---

## 📜 License

MIT License. See `LICENSE` for details.


# Network Security - Phishing Data Detection

## Overview

This project focuses on building a machine learning pipeline for detecting phishing attempts using network and web data. It automates ingestion, validation, transformation, and model training to classify phishing versus legitimate activity. The workflow is modular, supporting reproducibility, experiment tracking, and cloud artifact storage.

## Features

- **Data Ingestion:** Automated loading and verification of raw data from CSV or MongoDB.
- **Data Validation:** Schema validation, sanity checks, and statistical analysis.
- **Data Transformation:** Preprocessing features, handling missing values, encoding, and train-test splitting.
- **Model Training:** Multiple classifiers (Logistic Regression, KNN, Decision Tree, Random Forest, AdaBoost, Gradient Boosting), hyperparameter tuning, and evaluation metrics.
- **Experiment Tracking:** Supports MLflow and DagsHub for experiment management.
- **Cloud Integration:** Syncing of artifacts and trained models to AWS S3.

## Project Structure

```
network-security/
├── main.py                         # Entry point for running the full pipeline
├── push_data.py                    # Script to push data into MongoDB
├── networksecurity/
│   ├── components/                 # Pipeline stages: ingestion, validation, transformation, model trainer
│   ├── entity/                     # Configuration and artifact classes
│   ├── pipeline/                   # Pipeline orchestration
│   ├── utils/                      # Utilities for file I/O, evaluation, etc.
│   ├── logging/                    # Custom logging setup
│   ├── exception/                  # Custom exceptions
│   └── cloud/                      # S3 sync utility
├── requirements.txt
├── setup.py
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.7+
- pip (Python package manager)
- MongoDB (optional, if using push_data.py for data ingestion)
- AWS account (for S3 syncing)
- [DagsHub](https://dagshub.com/) (optional, for MLflow experiment tracking)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/saksham3232/network-security.git
   cd network-security
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (for MongoDB, AWS, etc.):
   - `MONGO_DB_URL`: MongoDB connection string
   - `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`: AWS credentials

### Usage

#### Run the End-to-End ML Pipeline

```bash
python main.py
```

This will:
- Ingest data
- Validate data
- Transform features
- Train and evaluate models
- Sync artifacts and models to S3

#### Push Data to MongoDB

```bash
python push_data.py
```
_Edit the script with your data file path and MongoDB collection names as needed._

## Model Training Details

- Supports multiple algorithms (Logistic Regression, KNN, Decision Tree, etc.)
- Uses cross-validation and GridSearchCV for hyperparameter tuning
- Saves the best model and data transformer as pickle files in `final_model/`

## Contributing

Feel free to open issues or submit pull requests for improvements or new features.

## Contact

- Author: Saksham Maurya
- Email: sakshammaurya3232@gmail.com

---

*This project was developed as a part of a network security coursework and is focused on phishing detection tasks.*

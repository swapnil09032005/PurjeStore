# PurjeStore Data Architecture

## 1. Development Data Source

The recovered 177 CSV files are the primary development source.

Purpose:

- discovery
- profiling
- relationship analysis
- cleaning
- EDA
- analytical dataset construction
- feature engineering
- ML experimentation

---

## 2. Live Data Source

A separate MariaDB/MySQL connection provides current data.

Purpose:

- dashboard refresh
- current analytics
- current predictions
- ML inference
- future automation

---

## 3. Separation Principle

Development data and live data must remain logically separated.

Development:

    CSV
      |
      v
    Cleaning
      |
      v
    Processing
      |
      v
    Features
      |
      v
    Analytics / ML

Live:

    MariaDB/MySQL
          |
          v
    Read / Extraction Layer
          |
          v
    Validated Processing
          |
       +--+--+
       |     |
       v     v
    Dashboard ML Inference

---

## 4. ML Training vs Inference

Training:

    Development Data
          |
          v
    Feature Engineering
          |
          v
    Model Training
          |
          v
    Model Validation
          |
          v
    Approved Model

Inference:

    Live Database
          |
          v
    Current Features
          |
          v
    Approved Model
          |
          v
    Predictions

---

## 5. Future Retraining

Automated retraining is NOT assumed.

It will only be implemented if:

- sufficient data exists
- target remains valid
- data quality is acceptable
- model performance can be validated
- retraining provides business value

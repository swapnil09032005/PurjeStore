# PurjeStore ML Architecture

Machine learning problems will NOT be selected merely because
they are common e-commerce problems.

The actual PurjeStore data will determine:

- target availability
- target quality
- prediction horizon
- feature availability
- sample size
- class balance
- business relevance
- feasibility

---

## Development

    CSV Data
       |
       v
    Feature Engineering
       |
       v
    Training Dataset
       |
       v
    Model Experimentation
       |
       v
    Validation
       |
       v
    Approved Model

---

## Live Inference

    Live Database
          |
          v
    Current Feature Data
          |
          v
    Approved Model
          |
          v
    Prediction
          |
          v
    Dashboard / Decision Support

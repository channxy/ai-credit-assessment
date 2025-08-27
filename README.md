# 🏦 AI-Powered Credit Assessment Platform

> **Next-generation credit assessment that goes beyond traditional scoring**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 Overview

This project is a **proof-of-concept (PoC)** for an **AI-driven credit assessment solution** that moves beyond legacy credit scoring. Instead of relying solely on repayment history, it integrates **multi-dimensional data sources** such as:

* 📈 **Financial Behavior** → Transactions, income patterns, savings, debts
* 👩‍💼 **Career & Industry** → Salary progression, job stability, industry volatility, employment gaps
* 🏠 **Housing & Assets** → Home ownership, rental stability, loan-to-asset ratios
* 🌏 **Macroeconomic & Job Market Data** → Industry demand, regional employment trends
* 👥 **Social & Lifestyle Indicators** → Spending behavior, responsible community engagement (non-invasive, opt-in)
* 💳 **Traditional Credit Data** → Credit utilization, repayment history, limits

The goal: **fairer, explainable, and future-proof creditworthiness evaluations** while minimizing bias.

 The system is designed to be:

* **Accurate** → Powered by AI models trained on structured & unstructured data.
* **Explainable** → Every score comes with clear reasoning and contributing factors.
* **Scalable** → Built on modern, modular architecture with extensibility in mind.
* **Realistic** → Takes into account real-life dynamics such as career stability, housing ownership, and market conditions.

---

## ✨ Key Features

* **Creditworthiness Engine (AI-Driven)**

  * Combines income, debt, repayment history, spending patterns, and financial ratios.
  * Adjusts dynamically based on **career trajectory, industry health, and job stability**.
  * Incorporates **housing ownership status**, local property market conditions, and mortgage exposure.
  * Optionally integrates **social/economic indicators** for more holistic risk profiling.

* **Scenario Simulation ("What-If" Engine)**

  * Users can simulate life events (e.g., job change, salary bump, house purchase, market downturn).
  * Instantly see how such events impact their credit rating.

* **Transparent AI Insights**

  * Uses explainable AI (XAI) to show **why** a score was assigned.
  * Provides breakdown: “Career +5 pts, Debt -15 pts, Housing +10 pts, Job Market -5 pts.”

* **Frontend (React + ServiceBench Webkit)**

  * Built with **React** for speed and flexibility.
  * Uses **ServiceBench Webkit** for pre-styled, professional-grade components.
  * Provides dashboards, interactive charts, simulation inputs, and report views.

* **Backend (FastAPI + SQLite3 + AI Models)**

  * FastAPI for REST API endpoints and business logic.
  * SQLite3 (upgradeable to PostgreSQL) for data storage.
  * AI models (scikit-learn, TensorFlow/PyTorch) for credit scoring & simulations.

* **Test Data & Virtualization Layer**

  * Swagger-based service mocking for endpoints.
  * Synthetic test data generation for demo purposes.
  * Prompt-based test data augmentation.

* **Future Expansion**

  * Integration with real financial APIs (e.g., Plaid).
  * Career & job market APIs (LinkedIn, labor market data).
  * Housing/property market feeds.
  * Advanced AI explainability dashboards.

---

## 🏗️ Tech Stack

**Frontend:**

* React
* ServiceBench Webkit (UI kit for development)
* Recharts / D3.js (data visualization)

**Backend:**

* FastAPI
* SQLite3 (upgradeable to PostgreSQL)
* AI/ML (scikit-learn, TensorFlow, PyTorch)
* OpenAI API (for NLP, reasoning, synthetic data generation)

**Infrastructure:**

* Docker (containerization)
* Swagger (API docs & mock services)

---

## 🌟 Possible Extensions

* **Career & Industry Forecasting** → Use labor market APIs to simulate career risk
* **Salary Progression Models** → ML models to project income growth trajectories
* **Housing Market Integration** → Predictive analysis of property values & risk
* **Behavioral Finance Signals** → Insights from spending patterns & lifestyle
* **Social / Digital Identity Proofing** → Optional, privacy-first signals (e.g., digital footprint stability)
* **Fairness Auditing Module** → Detect and mitigate model bias

---

## 🎯 Target Use Cases

* **Banks & Financial Institutions** → Smarter underwriting, personalized loans
* **Fintech Startups** → Credit inclusion for underbanked populations
* **Regulators** → Bias auditing, transparency, fairness testing
* **Individuals** → Credit self-assessment + “what-if” planning tool

---

## 📌 Roadmap

* ✅ Phase 1: Backend API + ML credit scoring engine
* ✅ Phase 2: Frontend prototype with Service Bench WebKit
* 🔄 Phase 3: Integrate explainability & simulation
* 🔄 Phase 4: Expand datasets (career, salary, housing, macroeconomics)
* 🔮 Phase 5: Deploy production-ready cloud service

---
Access Points
Frontend: http://localhost:3000
Backend API: http://localhost:8000
API Documentation: http://localhost:8000/docs
Interactive API Docs: http://localhost:8000/redoc

---
ai-credit-assessment/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main application
│   ├── database.py         # Database configuration
│   ├── models/             # Database models
│   ├── schemas/            # Pydantic schemas
│   ├── routers/            # API endpoints
│   ├── services/           # AI models & business logic
│   └── utils/              # Utilities
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── App.js          # Main app
│   └── public/             # Static assets
├── data/                   # Database files
├── models/                 # AI model files
├── logs/                   # Application logs
├── requirements.txt        # Python dependencies
├── package.json           # Node.js dependencies
├── docker-compose.yml     # Docker configuration
├── setup.sh              # Setup script
└── run.sh                # Run script

---

## 🚀 How to Run the POC

### Prerequisites

- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **Git** for cloning the repository

### Quick Start (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/channxy/ai-credit-assessment
   cd ai-credit-assessment
   ```

2. **Run the automated setup**
   ```bash
   chmod +x setup.sh run.sh
   ./setup.sh
   ```

3. **Start the application**
   ```bash
   ./run.sh
   ```

4. **Access the application**
   - 🌐 **Frontend**: http://localhost:3000
   - 🔧 **Backend API**: http://localhost:8000
   - 📚 **API Documentation**: http://localhost:8000/docs
   - 📖 **Interactive API Docs**: http://localhost:8000/redoc

### Manual Setup

#### Option 1: Local Development

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Node.js dependencies**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

3. **Create environment file**
   ```bash
   # Create .env file with your configuration
   echo "DATABASE_URL=sqlite:///./data/credit_assessment.db" > .env
   echo "ENVIRONMENT=development" >> .env
   ```

4. **Start the backend server**
   ```bash
   python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Start the frontend (in a new terminal)**
   ```bash
   cd frontend
   npm start
   ```
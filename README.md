# AI Data Warehouse Analyst

AI-powered Streamlit application for warehouse sales analysis, automated data cleaning, and interactive business intelligence visualization.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-data-warehouse-analyst-pnvmvqtubkga8zk4knpzxw.streamlit.app/)

---

## Live Demo

🔗 https://ai-data-warehouse-analyst-pnvmvqtubkga8zk4knpzxw.streamlit.app/

---

## Overview

This project analyzes warehouse order and sales data using Python and Streamlit.  
The application automates data cleaning, applies business logic for revenue analysis, and provides interactive filtering and visualization features for decision-making.

The system was designed to simulate a lightweight business intelligence workflow for warehouse operations and reporting.

---

## Features

- Upload warehouse CSV datasets
- Automated missing-value handling
- Revenue calculation for shipped orders only
- Interactive filtering by product and date
- Data visualization dashboard
- Export filtered reports as CSV
- Automated deployment uptime monitoring using GitHub Actions + Playwright

---

## Tech Stack

### Backend / Data Processing
- Python
- Pandas
- NumPy

### Visualization & UI
- Streamlit
- Matplotlib
- Seaborn

### DevOps / Automation
- GitHub Actions
- Playwright

### Deployment
- Streamlit Community Cloud

---

## Project Structure

```bash
.
├── app/
│   └── main.py
├── generate_data.py
├── requirements.txt
├── README.md
└── .github/workflows/
```

- `app/main.py` → Streamlit application entry point
- `generate_data.py` → sample warehouse dataset generator
- `.github/workflows/` → automated uptime monitoring workflow

---

## Expected Dataset Format

The application expects CSV files containing the following columns:

| Column | Description |
|---|---|
| Date | Order date |
| Product | Product name |
| Units_Sold | Number of sold units |
| Status | Shipment status |
| Unit_Price | Product unit price |

---

## Local Installation

Clone the repository:

```bash
git clone https://github.com/trickefog12/ai-data-warehouse-analyst.git
cd ai-data-warehouse-analyst
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app/main.py
```

---

## Deployment & Reliability

The application is deployed on Streamlit Community Cloud.

To improve application availability and reduce inactivity-related hibernation, a GitHub Actions workflow using Playwright periodically visits the deployed application.

This simulates a lightweight uptime-monitoring approach commonly used in cloud-hosted demo environments.

---

## Engineering Decisions

### Median-Based Missing Value Handling
Median imputation was selected because it is more robust against outliers compared to mean substitution.

### Revenue Calculation Logic
Revenue is calculated only for orders with `Shipped` status to better reflect completed business transactions.

### Streamlit Framework
Streamlit was selected for rapid dashboard development and interactive data exploration.

### GitHub Actions + Playwright
Playwright automation was used to maintain deployment responsiveness and demonstrate CI/CD automation concepts.

---

## Limitations

- Requires a standardized CSV structure
- Public demo deployment only
- No database persistence
- No authentication system implemented

---

## Future Improvements

- Database integration (PostgreSQL / Supabase)
- User authentication
- Advanced KPI dashboard
- Forecasting and anomaly detection
- Docker containerization
- Cloud deployment pipeline improvements

---

## Why I Built This

I built this project as part of my transition from electrical engineering into software development, cloud technologies, and automation engineering.

The goal was to combine analytical thinking with practical Python development, deployment workflows, and business-focused data analysis.
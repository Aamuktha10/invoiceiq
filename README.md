# InvoiceIQ — AI Agent for Automated Invoice Processing

> **A production-ready multi-agent AI system that extracts, validates, and routes business invoices automatically in seconds.**

## Overview

InvoiceIQ is an AI-powered invoice processing system that automates one of the most common business workflows. Instead of manually entering invoice details, checking business rules, and forwarding invoices for approval, InvoiceIQ completes the entire workflow using a coordinated team of AI agents.

The application accepts invoice images or PDFs, extracts structured information using an AI vision model, validates the data against configurable business rules, determines the appropriate approval path, and maintains a session history of processed invoices.

---

## Problem Statement

Organizations process hundreds of invoices every month.

Traditional invoice processing involves:

* Opening invoice PDFs manually
* Entering invoice details into spreadsheets or ERP systems
* Checking budgets
* Detecting duplicate invoices
* Routing invoices for approval

This process typically takes **15–20 minutes per invoice**, is prone to human error, and delays payment processing.

InvoiceIQ automates the entire workflow in **under 10 seconds**.

---

## Features

* Upload invoice images or PDF documents
* AI-powered invoice data extraction
* Automatic field validation
* Budget limit verification
* Duplicate invoice detection
* Future-date detection
* Confidence score monitoring
* Intelligent approval routing
* Session history dashboard
* Responsive web interface
* Dark-themed UI

---

## Multi-Agent Architecture

InvoiceIQ uses a coordinated multi-agent pipeline.

### 1. ExtractionAgent

Uses **Groq Llama 4 Scout Vision** to extract structured invoice information, including:

* Vendor Name
* Invoice Number
* Invoice Date
* Total Amount
* Tax Amount
* Line Items
* Confidence Score

Output is returned as structured JSON.

---

### 2. ValidationAgent

Validates extracted information using business rules.

Checks include:

* Required fields
* Positive invoice amount
* Numeric validation
* Budget limit verification
* Duplicate invoice detection
* Future date detection
* AI confidence threshold

---

### 3. RoutingAgent

Determines the approval path.

Possible outcomes:

* ✅ Auto Approve
* ⚠️ Manager Review
* ❌ Reject

---

### 4. OrchestratorAgent

Coordinates all agents sequentially.

Responsibilities include:

* Managing workflow
* Passing outputs between agents
* Recording session history
* Returning final results

---

## Workflow

```text
Invoice Upload
      │
      ▼
ExtractionAgent
      │
      ▼
ValidationAgent
      │
      ▼
RoutingAgent
      │
      ▼
Final Decision
      │
      ▼
Session History
```

---

## Tech Stack

### Backend

* Python
* Flask

### Frontend

* HTML
* CSS
* JavaScript

### AI

* Groq API
* Llama 4 Scout Vision Model

### Deployment

* Railway

---

## Security

InvoiceIQ was designed with security in mind.

* Uploaded invoices are deleted immediately after processing.
* Session history is stored only in memory.
* File type and size validation is enforced.
* Environment variables are stored securely using a `.env` file.
* Sensitive credentials are excluded from Git using `.gitignore`.

---

## Project Structure

```text
invoiceiq/
│
├── agents/
│   ├── extraction_agent.py
│   ├── validation_agent.py
│   ├── routing_agent.py
│   └── orchestrator_agent.py
│
├── static/
│
├── templates/
│
├── uploads/
│
├── app.py
├── requirements.txt
├── Procfile
├── runtime.txt
└── README.md
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/Aamuktha10/invoiceiq.git

cd invoiceiq
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux/macOS**

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file.

```env
GROQ_API_KEY=your_api_key
```

### Run the application

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## Live Demo

**Live Application**

https://invoiceiq-production-e78e.up.railway.app

**Demo Video**

https://youtu.be/D79Tk21NLuE

---

## Repository

https://github.com/Aamuktha10/invoiceiq

---

## Future Improvements

* OCR fallback for low-quality invoices
* ERP integration (SAP, Oracle, QuickBooks)
* Email-based invoice ingestion
* Database-backed invoice history
* Multi-user authentication
* Analytics dashboard
* Role-based approvals
* Multi-language invoice support

---

## Course Concepts Applied

* Multi-Agent Systems
* AI Orchestration
* Prompt Engineering
* Vision Language Models
* Business Workflow Automation
* AI Document Processing
* Production Deployment
* RESTful Web Applications

---

## Author

**Aamuktha Jarathi**

B.Tech (Artificial Intelligence & Machine Learning)

GitHub: https://github.com/Aamuktha10

LinkedIn: https://www.linkedin.com/in/aamuktha-jarathi/

---

## License

This project was developed for the **Kaggle AI Agents Intensive Capstone** under the **Agents for Business** track and is available for educational and portfolio purposes.

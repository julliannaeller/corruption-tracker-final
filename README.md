# Corruption Tracker

A Python project that analyzes public spending data to detect **ghost projects** and flag **politicians with suspicious overspending**.

### 📊 Overview
This project uses real-world data from infrastructure budgets in the Philippines.  
By comparing **declared budgets** with **actual spending** and **completion outcomes**, it identifies irregularities that may indicate corruption or inefficiency.

### ⚙️ Features
- Reads and processes CSV files using **Pandas**
- Flags incomplete projects with large budget gaps
- Detects politicians overspending relative to declared income
- Generates clear data visualizations with **Matplotlib**

### 📁 Files
- `app.py` – main Python script  
- `projects.csv` – project budget and outcome data  
- `politicians.csv` – declared income and project spending data  
- `project_flags.csv`, `politician_flags.csv` – flagged results  
- `budget_gaps.png`, `declared_vs_actual.png` – generated charts  

### 🌍 Purpose
This project was inspired by recurring public-fund scandals in the Philippines, particularly **flood-control projects** where funds disappeared or outcomes remained incomplete.  
It demonstrates how **data transparency and quantitative analysis** can expose inefficiencies and promote accountability.

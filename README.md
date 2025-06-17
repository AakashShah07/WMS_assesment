Warehouse Management System AI — Submission
This project demonstrates an AI-powered Warehouse Management System (WMS) where sales data and SKU mappings are merged, cleaned, stored, and analyzed using natural language queries with powerful LLMs.

Problem Statement
Enable warehouse teams to easily analyze sales data without complex SQL queries or coding by leveraging:

Data Cleaning & Preparation

Centralized Database Storage

AI-powered Natural Language Querying

Tech Stack
Component	Technology
Frontend UI	Streamlit
Backend	Python (Pandas, OpenAI SDK, Baserow API)
AI Model	Groq API (LLaMA3-70B-8192)
Database	Baserow
Environment	Python-dotenv
Deployment	Docker / Local

Project Architecture
1️⃣ Data Cleaning (Pandas)
Uploads two CSV files:

Msku_With_Skus.csv (SKU Mapping)

Sales Data CSV

Merges data based on SKU codes.

Handles column name inconsistencies (SKU, sku, Quantity, quantity).

Fills missing MSKU values with "UNKNOWN".

Generates simple metrics: total orders, quantity sold, unique SKUs/MSKUs.

2️⃣ Database Storage (Baserow)
Cleaned merged data uploaded to Baserow Tables.

Provides a structured, accessible view for warehouse teams.

3️⃣ AI-Powered Analysis (Streamlit + Groq API)
Simple Streamlit UI where users upload files and ask any question.

Natural language questions are processed via Groq LLaMA3-70B model.

Groq API integrated using OpenAI-compatible SDK.

Baserow Table Sample
id	SKU	MSKU	Quantity
1	123	A45	5
2	456	B12	10

Demo Video
https://www.loom.com/share/23b53b93b9d2475da2cb93823addbf9b?sid=48e1ff3e-f76f-4674-9ab2-2cbfc856f441

Setup Instructions
1️⃣ Clone Repository

git clone https://github.com/AakashShah07/WMS_assesment
cd warehouse-wms-ai

2️⃣ Setup Virtual Environment

python3 -m venv venv
source venv/bin/activate
3️⃣ Install Dependencies

pip install -r requirements.txt
4️⃣ Create .env file
In your project root directory, create .env file:


GROQ_API_KEY=your_groq_api_key_here
5️⃣ Run Streamlit App

streamlit run app.py
AI Model Logic
Extract sample data (first 20 rows).

Build dynamic prompt with sample data and user query.

Send request to Groq API using LLaMA3-70B model.

Display response inside Streamlit UI.

Sample Questions
What are the top 5 selling MSKUs?

Which SKU has highest sales?

Total quantity sold?

How many orders processed?

Features
✅ Clean Data Merge (SKU & MSKU)

✅ Baserow Integration

✅ Groq LLaMA 3 AI Analysis

✅ Secure API Key Handling with .env

✅ Simple Streamlit User Interface

Credits
Developed by: Aakash Shah


📦 Warehouse Management System AI — Submission
This project demonstrates an AI-powered Warehouse Management System (WMS) where sales data and SKU mappings are merged, cleaned, stored, and analyzed using natural language queries with powerful LLMs.

🎯 Problem Statement
Enable warehouse teams to easily analyze sales data without complex SQL queries or coding, by leveraging:

Data Cleaning & Preparation

Centralized Database Storage

AI-powered Natural Language Querying

🛠 Tech Stack
Component	Technology Used
Frontend UI	Streamlit
Backend	Python (Pandas, OpenAI SDK, Baserow API)
AI Model	Groq API (LLaMA3-70B-8192)
Database	Baserow
Environment Management	Python-dotenv
Deployment Ready	Docker or Local

🔐 AI Key Management
API Keys are handled using environment variables via .env file for secure storage.

⚙ Project Architecture
1️⃣ Data Cleaning (Pandas)

Uploads two CSV files:

SKU Mapping (Msku_With_Skus.csv)

Sales Data CSV

Merges data based on SKU codes.

Handles column name inconsistencies (SKU, sku, Quantity, quantity).

Fills missing MSKU values with "UNKNOWN".

Generates simple metrics: total orders, quantity sold, unique SKUs/MSKUs.

2️⃣ Database Storage (Baserow)

Cleaned merged data uploaded to Baserow Tables.

Easy structured view for warehouse team.

3️⃣ AI-Powered Analysis (Streamlit + Groq API)

Simple Streamlit UI where user uploads files and asks any question.

Natural language questions are processed via Groq LLaMA3-70B model.

Groq API is integrated using OpenAI-compatible SDK.

📊 Sample Baserow Table
id	SKU	MSKU	Quantity	...
1	123	A45	5	...
2	456	B12	10	...

(as shown in Loom video)

🎥 Loom Video Demo
👉 Watch Full Demo Here

🚀 How to Setup & Run Locally
1️⃣ Clone Repository
bash
Copy
Edit
git clone <your-repo-link>
cd warehouse-wms-ai
2️⃣ Setup Virtual Environment
bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
3️⃣ Install Requirements
bash
Copy
Edit
pip install -r requirements.txt
4️⃣ Create .env File
Create a file called .env in the project root and add:

env
Copy
Edit
GROQ_API_KEY=your_groq_api_key_here
(Replace with your actual Groq API key)

5️⃣ Run Streamlit App
bash
Copy
Edit
streamlit run app.py
🧠 AI Model Logic
We take first few rows of cleaned dataset (head sample).

Convert it into CSV text.

Build dynamic prompt with this sample data and user query.

Send it to Groq API using LLaMA3-70B model.

🌟 Key Features
✅ Clean Data Merge (SKU & MSKU)
✅ Baserow Integration
✅ Groq LLaMA 3 AI Analysis
✅ Secure API Key Handling
✅ Streamlit UI
✅ Ready-to-deploy code

🤝 Credits
Developed by: Aakash Shah

Would you like me to also prepare:

✅ requirements.txt
✅ complete app.py with .env loaded
✅ data_cleaning.py separated
✅ fully ready full submission repo structure


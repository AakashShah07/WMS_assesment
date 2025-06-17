import streamlit as st
import pandas as pd
import openai
import os
from dotenv import load_dotenv



st.title("📦 Warehouse Management System - MVP")

load_dotenv()

# Read API Key from environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Option selection
mode = st.radio("Select processing mode:", 
                ["Single File (Pre-cleaned Data)", 
                 "Two Files (Merge SKU Mapping)", 
                 "AI Analysis (Requires API Key)"])

if mode == "Single File (Pre-cleaned Data)":
    uploaded_file = st.file_uploader("Upload cleaned sales CSV file", type=["csv"])

    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        st.write("Data Preview:")
        st.dataframe(data.head())

        total_orders = data.shape[0]

        # Handle quantity column variations
        if 'Quantity' in data.columns:
            total_quantity = data['Quantity'].sum()
        elif 'quantity' in data.columns:
            total_quantity = data['quantity'].sum()
        else:
            total_quantity = 'N/A'

        # Handle SKU column name variations
        if 'SKU' in data.columns:
            unique_skus = data['SKU'].nunique()
        elif 'sku' in data.columns:
            unique_skus = data['sku'].nunique()
        else:
            unique_skus = 'N/A'

        # Handle MSKU column variations
        if 'msku' in data.columns:
            unique_mskus = data['msku'].nunique()
        elif 'MSKU' in data.columns:
            unique_mskus = data['MSKU'].nunique()
        else:
            unique_mskus = 'N/A'

        st.subheader("Metrics:")
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        
        col1.metric("Total Orders", total_orders)
        col2.metric("Total Quantity", total_quantity)
        col3.metric("Unique SKUs", unique_skus)
        col4.metric("Unique MSKUs", unique_mskus)

elif mode == "Two Files (Merge SKU Mapping)":
    # Upload SKU Mapping File
    sku_mapping_file = st.file_uploader("Upload SKU Mapping (Msku_With_Skus.csv)", type=["csv"])
    # Upload Sales File
    sales_file = st.file_uploader("Upload Sales Data CSV", type=["csv"])

    if sku_mapping_file and sales_file:
        sku_mapping = pd.read_csv(sku_mapping_file)
        sales_data = pd.read_csv(sales_file)

        # Determine SKU column name in sales data
        sku_column = 'SKU' if 'SKU' in sales_data.columns else 'sku' if 'sku' in sales_data.columns else None
        
        if sku_column:
            # Merge based on SKU column
            merged = sales_data.merge(sku_mapping[['sku', 'msku']], 
                                    left_on=sku_column, 
                                    right_on='sku', 
                                    how='left')
            merged['msku'] = merged['msku'].fillna('UNKNOWN')

            st.write("Cleaned Sales Data:")
            st.dataframe(merged.head())

            # Simple metrics
            total_orders = len(merged)
            
            # Handle quantity column variations
            if 'Quantity' in merged.columns:
                total_quantity = merged['Quantity'].sum()
            elif 'quantity' in merged.columns:
                total_quantity = merged['quantity'].sum()
            else:
                total_quantity = 'N/A'
                
            unique_skus = merged[sku_column].nunique()
            unique_mskus = merged['msku'].nunique()

            st.subheader("Metrics:")
            col1, col2 = st.columns(2)
            col3, col4 = st.columns(2)
            
            col1.metric("Total Orders", total_orders)
            col2.metric("Total Quantity", total_quantity)
            col3.metric("Unique SKUs", unique_skus)
            col4.metric("Unique MSKUs", unique_mskus)

            # Download cleaned file
            csv = merged.to_csv(index=False).encode('utf-8')
            st.download_button("Download Cleaned File", csv, "cleaned_sales.csv", "text/csv")
        else:
            st.error("Could not find SKU column in sales data (tried 'SKU' and 'sku')")
    else:
        st.warning("Please upload both files to proceed.")

else:  # AI Analysis mode
    st.warning("Note: AI Analysis requires an OpenAI API key")
    
   
    # Upload SKU Mapping File
    sku_mapping_file = st.file_uploader("Upload SKU Mapping (Msku_With_Skus.csv)", type=["csv"])
    # Upload Sales File
    sales_file = st.file_uploader("Upload Sales Data CSV", type=["csv"])

    if sku_mapping_file and sales_file and api_key:
        sku_mapping = pd.read_csv(sku_mapping_file)
        sales_data = pd.read_csv(sales_file)

        # Determine SKU column name in sales data
        sku_column = 'SKU' if 'SKU' in sales_data.columns else 'sku' if 'sku' in sales_data.columns else None
        
        if sku_column:
            # Merge based on SKU column
            merged = sales_data.merge(sku_mapping[['sku', 'msku']], 
                                    left_on=sku_column, 
                                    right_on='sku', 
                                    how='left')
            merged['msku'] = merged['msku'].fillna('UNKNOWN')

            st.write("Cleaned Sales Data Preview:")
            st.dataframe(merged.head())

            # Simple metrics
            total_orders = len(merged)
            
            # Handle quantity column variations
            if 'Quantity' in merged.columns:
                total_quantity = merged['Quantity'].sum()
            elif 'quantity' in merged.columns:
                total_quantity = merged['quantity'].sum()
            else:
                total_quantity = 'N/A'
                
            unique_skus = merged[sku_column].nunique()
            unique_mskus = merged['msku'].nunique()

            st.subheader("Basic Metrics:")
            col1, col2 = st.columns(2)
            col3, col4 = st.columns(2)
            
            col1.metric("Total Orders", total_orders)
            col2.metric("Total Quantity", total_quantity)
            col3.metric("Unique SKUs", unique_skus)
            col4.metric("Unique MSKUs", unique_mskus)

            # AI Query Section
            st.header("🤖 AI Data Analysis")
            st.info("Ask natural language questions about your data")
            
            user_query = st.text_area("Question about your sales data (e.g., 'What are the top 5 selling products?')")
            
            if user_query:
                try:
                    client = openai.OpenAI(
                    api_key=GROQ_API_KEY,
                    base_url="https://api.groq.com/openai/v1"
                    )

                    # Give AI only sample of data to avoid very long prompt
                    sample_data = merged.head(20).to_csv(index=False)

                    prompt = f"""
                    You are an expert warehouse sales analyst.

                    Here is a sample of my merged data:
                    {sample_data}

                    Now answer the following question based on this data:
                    {user_query}
                    """

                    with st.spinner("Analyzing with Groq AI..."):
                        response = client.chat.completions.create(
                            model="llama3-70b-8192",
                            messages=[
                                {"role": "system", "content": "You are a helpful data analysis assistant."},
                                {"role": "user", "content": prompt}
                            ]
                        )
                        answer = response.choices[0].message.content

                    st.subheader("AI Response:")
                    st.write(answer)
                except Exception as e:
                    st.error(f"Error processing your request: {str(e)}")
        else:
            st.error("Could not find SKU column in sales data (tried 'SKU' and 'sku')")
    elif sku_mapping_file and sales_file and not api_key:
        st.error("Please enter your OpenAI API key to use AI features")
    else:
        st.warning("Please upload both files and enter your API key to proceed")
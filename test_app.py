import streamlit as st
import pandas as pd

st.title("📦 Warehouse Management System - MVP")

# Option selection
mode = st.radio("Select processing mode:", 
                ["Single File (Pre-cleaned Data)", "Two Files (Merge SKU Mapping)"])

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

        st.metric("Total Orders", total_orders)
        st.metric("Total Quantity", total_quantity)
        st.metric("Unique SKUs", unique_skus)
        st.metric("Unique MSKUs", unique_mskus)

else:  # Two Files (Merge SKU Mapping)
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
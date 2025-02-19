import pandas as pd
import streamlit as st

# Function to load and preprocess data from multiple files
def load_data(file_paths):
    dfs = []
    for file_path in file_paths:
        df = pd.read_csv(file_path)
        
        # Clean data: lowercase and strip whitespace for consistency
        df['customer_facility'] = df['customer_facility'].str.lower().str.strip()
        df['manufacturer_part'] = df['manufacturer_part'].astype(str).str.lower().str.strip()
        
        dfs.append(df)
    
    return dfs

# Function to search for matching rows in multiple DataFrames
def search_data(dfs, customer_facility, manufacturer_part):
    # Clean inputs
    customer_facility = customer_facility.lower().strip()
    manufacturer_part = str(manufacturer_part).lower().strip()
    
    results = []
    for df in dfs:
        # Filter DataFrame
        mask = (df['customer_facility'] == customer_facility) & (df['manufacturer_part'] == manufacturer_part)
        result = df[mask]
        results.append(result)
    
    # Combine results from all DataFrames
    combined_result = pd.concat(results, ignore_index=True)
    
    # Ensure only one entry for each unique customer_facility and manufacturer_part
    combined_result = combined_result.groupby(["customer_facility", "manufacturer_part"]).first().reset_index()
    
    return combined_result

# Streamlit UI
def main():
    st.title("DDS Insights")
    
    # Load data from multiple CSV files
    file_paths = ["output1.csv", "output3.csv","output5.csv","output6.csv"]  # Replace with your filenames if different
    dfs = load_data(file_paths)
    
    # User inputs
    customer_facility = st.text_input("Enter Customer Facility:")
    manufacturer_part = st.text_input("Enter Manufacturer Part:")
    
    if st.button("Search"):
        if not customer_facility or not manufacturer_part:
            st.warning("Please fill in both fields.")
        else:
            result = search_data(dfs, customer_facility, manufacturer_part)
            if not result.empty:
                st.success("I have the requested data !")
                for index, row in result.iterrows():
                    st.text(f"**Customer Facility** : {row['customer_facility']}")
                    st.text(f"**Manufacturer Part** : {row['manufacturer_part']}")
                    st.text(f"**Total Install base** : {row['total_install_base']}")  # Replace with actual column names
                    st.text(f"**Average days in use for Install base** : {row['avg_days_in_use']}")
                    st.text(f"**Total Spare units** : {row['spare_units']}")
                    st.text(f"**Average days in use for Spare units**: {row['avg_days_in_use_spare']}")
                    st.markdown(f"**Average Lifetime Days In Use**: {row['Average Lifetime Days In Use']}")
                    st.markdown(f"**Common Failures** : {row['Common_Failures']}")
                    st.markdown(f"**Mostly Affected Area** : {row['Analyzed Affected Areas']}")
                    st.markdown(f"**Mostly replaced parts** : {row['Analyzed Parts Replaced']}")
                    st.markdown(f"**Probable Cause** : {row['Analyzed Probable Cause']}")
                    #st.text(f"% In-Use Compared to Avg : {row['% In-Use Compared to Avg']}")
                    st.text("---")
            else:
                st.error("I don't have the requested data.")

if __name__ == "__main__":
    main()
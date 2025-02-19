import pandas as pd
import streamlit as st

# Function to load and preprocess data
def load_data(file_path):
    df = pd.read_csv(file_path)
    
    # Clean data: lowercase and strip whitespace for consistency
    df['customer_facility'] = df['customer_facility'].str.lower().str.strip()
    df['manufacturer_part'] = df['manufacturer_part'].astype(str).str.lower().str.strip()
    return df

# Function to search for matching rows
def search_data(df, customer_facility, manufacturer_part):
    # Clean inputs
    customer_facility = customer_facility.lower().strip()
    manufacturer_part = str(manufacturer_part).lower().strip()
    
    # Filter DataFrame
    mask = (df['customer_facility'] == customer_facility) & (df['manufacturer_part'] == manufacturer_part)
    result = df[mask]
    return result

# Streamlit UI
def main():
    st.title("DDS Insights")
    
    # Load data from single CSV file
    df = load_data("output1.csv")  # Replace with your filename if different
    
    # User inputs
    customer_facility = st.text_input("Enter Customer Facility:")
    manufacturer_part = st.text_input("Enter Manufacturer Part:")
    
    if st.button("Search"):
        if not customer_facility or not manufacturer_part:
            st.warning("Please fill in both fields.")
        else:
            result = search_data(df, customer_facility, manufacturer_part)
            if not result.empty:
                st.success("I have the requested data !")
                for index, row in result.iterrows():
                    st.text(f"Customer Facility is: {row['customer_facility']}")
                    st.text(f"Manufacturer Part is: {row['manufacturer_part']}")
                    st.text(f"Total Install base are : {row['total_install_base']}")  # Replace with actual column names
                    st.text(f"Average days in use : {row['avg_days_in_use']}")
                    st.text(f"Total Spare units are : {row['spare_units']}")
                    st.text(f"Average days in use of Spare units : {row['avg_days_in_use_spare']}")
                    st.text("---")
            else:
                st.error("I dont have the requested data.")

if __name__ == "__main__":
    main()
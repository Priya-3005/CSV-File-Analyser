import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Smart CSV Analyzer", layout="wide")

st.title("📊 Smart CSV Analyzer")
st.write("Upload a CSV file and get instant insights!")

# File Upload
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("🔍 Data Preview")
    st.dataframe(df.head())

    # Shape
    st.subheader("📐 Dataset Shape")
    st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    # Column Selection
    st.subheader("📌 Select Columns")
    selected_columns = st.multiselect("Choose columns", df.columns, default=df.columns)
    df_selected = df[selected_columns]

    # Missing Values
    st.subheader("❗ Missing Values")
    missing = df_selected.isnull().sum()
    st.write(missing[missing > 0])

    # Fill Missing Values Option
    if st.checkbox("Fill missing values with mean (numeric only)"):
        df_selected = df_selected.fillna(df_selected.mean(numeric_only=True))
        st.success("Missing values filled!")

    # Statistical Summary
    st.subheader("📊 Statistical Summary")
    st.write(df_selected.describe())

    # Correlation Heatmap
    st.subheader("🔥 Correlation Heatmap")
    numeric_df = df_selected.select_dtypes(include=['float64', 'int64'])

    if not numeric_df.empty:
        fig, ax = plt.subplots()
        sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)
    else:
        st.warning("No numeric columns available for correlation heatmap.")

    # Download Cleaned Data
    st.subheader("⬇️ Download Processed Data")
    csv = df_selected.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "processed_data.csv", "text/csv")

else:
    st.info("👆 Please upload a CSV file to get started.")
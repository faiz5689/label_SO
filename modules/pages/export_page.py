# modules/pages/export_page.py

import streamlit as st
import os
from modules.utils.data_exporter import DataExporter

# Configure the page
st.set_page_config(
    page_title="StackOverflow Data Export Tool",
    page_icon="📊",
    layout="wide"
)

# Set paths relative to script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "labeled_data")

def main():
    st.title("Labeled Data Export Tool")

    # Initialize exporter
    exporter = DataExporter(output_dir=OUTPUT_DIR)
    labeled_files = exporter.get_all_labeled_files()

    st.write(f"Found {len(labeled_files)} labeled data files")

    # Show file list
    if labeled_files:
        st.subheader("Available Data Files")

        # Display file information
        files_df = []
        for file_path in labeled_files:
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path) / 1024  # KB
            file_modified = os.path.getmtime(file_path)

            files_df.append({
                "Filename": file_name,
                "Size (KB)": f"{file_size:.2f}",
                "Last Modified": file_modified
            })

        st.dataframe(files_df)

        # Export options
        st.subheader("Export Options")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Merge All Files"):
                merged_file = exporter.merge_all_files()
                if merged_file:
                    st.success(f"Files merged successfully: {os.path.basename(merged_file)}")

                    # Provide download link
                    with open(merged_file, 'r') as f:
                        st.download_button(
                            label="Download Merged JSON",
                            data=f,
                            file_name=os.path.basename(merged_file),
                            mime="application/json"
                        )

        with col2:
            if st.button("Export to CSV"):
                csv_file = exporter.export_to_csv()
                if csv_file:
                    st.success(f"Data exported to CSV: {os.path.basename(csv_file)}")

                    # Provide download link
                    with open(csv_file, 'r') as f:
                        st.download_button(
                            label="Download CSV",
                            data=f,
                            file_name=os.path.basename(csv_file),
                            mime="text/csv"
                        )

        # Custom filename export
        st.subheader("Custom Export")

        custom_filename = st.text_input("Custom filename (optional)")
        export_format = st.radio("Export format", ["JSON", "CSV"])

        if st.button("Export with Custom Filename"):
            if export_format == "JSON":
                custom_file = exporter.merge_all_files(custom_filename if custom_filename else None)
                if custom_file:
                    st.success(f"Data exported to JSON: {os.path.basename(custom_file)}")

                    with open(custom_file, 'r') as f:
                        st.download_button(
                            label="Download Custom JSON",
                            data=f,
                            file_name=os.path.basename(custom_file),
                            mime="application/json"
                        )
            else:
                custom_file = exporter.export_to_csv(custom_filename if custom_filename else None)
                if custom_file:
                    st.success(f"Data exported to CSV: {os.path.basename(custom_file)}")

                    with open(custom_file, 'r') as f:
                        st.download_button(
                            label="Download Custom CSV",
                            data=f,
                            file_name=os.path.basename(custom_file),
                            mime="text/csv"
                        )
    else:
        st.warning("No labeled data files found. Please label some data first.")

if __name__ == "__main__":
    main()

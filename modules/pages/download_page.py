# modules/pages/download_page.py

import streamlit as st
import os
import json
from modules.utils.file_utils import get_labeled_files


def download_interface(annotator_name, output_dir):
    """Handle the download interface

    Args:
        annotator_name (str): Name of the annotator
        output_dir (str): Directory containing the labeled data
    """
    st.header("Download Your Labeled Data")
    st.info("Download your labeled data files to send to Faiz.")

    # Get all files for this annotator
    files = get_labeled_files(annotator_name, output_dir)

    if not files:
        st.warning(f"No labeled data found for annotator: {annotator_name}")
        return

    # Display each file with a download button
    st.subheader("Your Labeled Files")

    for file_path in files:
        filename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path) / 1024  # KB

        # Format the file information
        col1, col2 = st.columns([3, 1])

        with col1:
            st.write(f"**{filename}**")
            st.write(f"Size: {file_size:.2f} KB")

        with col2:
            with open(file_path, "r", encoding='utf-8') as f:
                file_content = f.read()
                st.download_button(
                    label="Download",
                    data=file_content,
                    file_name=filename,
                    mime="application/json",
                    key=f"download_{filename}"
                )

    # Combine all files option
    if len(files) > 1:
        st.subheader("Download All Labels")
        st.write("Combine all your labeled data into a single file:")

        all_data = []
        for file_path in files:
            try:
                with open(file_path, "r", encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        all_data.extend(data)
                    else:
                        all_data.append(data)
            except Exception as e:
                st.error(f"Error reading file {file_path}: {e}")

        if all_data:
            combined_filename = f"{annotator_name}_all_labels.json"
            combined_data = json.dumps(all_data, indent=2, ensure_ascii=False)
            st.download_button(
                label="Download All Labeled Data",
                data=combined_data,
                file_name=combined_filename,
                mime="application/json",
                key="download_all"
            )

    # Instructions for submitting
    st.subheader("How to Submit Your Labels")
    st.markdown("""
    1. Download your labeled data file(s) using the buttons above
    2. Send the file(s) to Faiz via message or upload in shared folder.
    3. Make sure to include your name in the files if possible, although I have added it to the file names and each entry.
    """)

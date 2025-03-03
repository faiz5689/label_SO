# app.py

import streamlit as st
import os
from modules.components.session_state import init_session_state
from modules.pages.label_page import labeling_interface
from modules.pages.download_page import download_interface
from modules.utils.data_loader import DataLoader

# Configure the page
st.set_page_config(
    page_title="StackOverflow Question Labeler",
    page_icon="📝",
    layout="wide"
)

# Set paths relative to the script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data/final_files")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "labeled_data")

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

def main():
    st.title("StackOverflow Question Labeler")

    # Initialize session state
    init_session_state()

    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")

        # Enter annotator name
        annotator_name = st.text_input("Annotator Name", "")
        if not annotator_name:
            st.warning("Please enter your name before starting.")
            return

        # Select dataset
        dataset_option = st.selectbox(
            "Select Dataset",
            ["Faiz_FJ", "FJ_only"]
        )

        # Tab selection
        tab_options = ["Label", "Download Data"]
        selected_tab = st.radio("Select Option", tab_options)
        if selected_tab != st.session_state.active_tab:
            st.session_state.active_tab = selected_tab
            st.rerun()

        # Load dataset based on selection (only if on Label tab)
        if st.session_state.active_tab == "Label":
            # Initialize the DataLoader
            loader = DataLoader(data_dir=DATA_DIR)
            dataset = loader.load_file(f"{dataset_option}.json")

            # Navigation
            setup_navigation(dataset, annotator_name, dataset_option)

    # Main content
    if st.session_state.active_tab == "Label":
        # Labeling interface
        labeling_interface(annotator_name, dataset_option, DATA_DIR, OUTPUT_DIR)
    else:
        # Download interface
        download_interface(annotator_name, OUTPUT_DIR)


def setup_navigation(dataset, annotator_name, dataset_option):
    from modules.utils.file_utils import is_post_labeled

    st.header("Navigation")

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous"):
            if st.session_state.current_index > 0:
                st.session_state.previous_index = st.session_state.current_index
                st.session_state.current_index -= 1
                st.session_state.question_key += 1

    with col2:
        if st.button("Next"):
            if st.session_state.current_index < len(dataset) - 1:
                st.session_state.previous_index = st.session_state.current_index
                st.session_state.current_index += 1
                st.session_state.question_key += 1

    # Jump to specific question
    new_index = st.number_input(
        "Go to question #",
        min_value=0,
        max_value=len(dataset)-1 if dataset else 0,
        value=st.session_state.current_index
    )

    if new_index != st.session_state.current_index:
        st.session_state.previous_index = st.session_state.current_index
        st.session_state.current_index = new_index
        st.session_state.question_key += 1

    # Progress
    if dataset:
        st.progress((st.session_state.current_index + 1) / len(dataset))
        st.write(f"Question {st.session_state.current_index + 1} of {len(dataset)}")

        # Show completed count
        labeled_count = 0
        for item in dataset:
            if is_post_labeled(item.get('post_id'), annotator_name, dataset_option, OUTPUT_DIR):
                labeled_count += 1
        st.write(f"You've labeled {labeled_count} of {len(dataset)} questions")


if __name__ == "__main__":
    main()

# ./modules/pages/label_page.py

import streamlit as st
import os
from datetime import datetime
from modules.utils.data_loader import DataLoader
from modules.utils.file_utils import save_labeled_data, is_post_labeled
from modules.components.session_state import ensure_post_evaluation
from modules.components.display import display_question_details, display_evaluation_preview
from modules.components.evaluation_form import model_evaluation_tabs
from modules.components.image_extraction import image_text_extraction_section, are_evaluations_complete


def add_tab_navigation(tab_names, current_tab_index=0):
    """Add duplicate tab navigation at the bottom of each tab for easier access

    Args:
        tab_names (list): List of all tab names
        current_tab_index (int, optional): Index of the current tab. Defaults to 0.
    """
    st.write("---")
    st.subheader("🔍 Quick Navigation")

    # Create a row of buttons representing each tab
    cols = st.columns(len(tab_names))

    for i, tab_name in enumerate(tab_names):
        with cols[i]:
            # Create a visually prominent button for each tab
            st.markdown(f"""
            <style>
            div[data-testid="stHorizontalBlock"] > div:nth-child({i+1}) {{
                text-align: center;
            }}
            </style>
            """, unsafe_allow_html=True)

            # Create button with tab name - use unique key combining current tab and target tab
            st.button(tab_name, key=f"bottom_nav_from_{current_tab_index}_to_{i}", use_container_width=True)

    # Add note about button functionality
    st.info("⚠️ Note: These buttons serve as visual reminders of the tabs at the top. Please scroll to the top to switch tabs.")


def labeling_interface(annotator_name, dataset_option, data_dir, output_dir):
    """Handle the labeling interface

    Args:
        annotator_name (str): Name of the annotator
        dataset_option (str): Dataset being used
        data_dir (str): Directory containing the data files
        output_dir (str): Directory for saving labeled data
    """
    # Load dataset based on selection
    loader = DataLoader(data_dir=data_dir)
    dataset = loader.load_file(f"{dataset_option}.json")

    if not dataset:
        st.warning(f"No data found or unable to load the data file: {data_dir}/{dataset_option}.json")
        return

    # Get current question
    current_question = dataset[st.session_state.current_index]
    current_post_id = current_question.get("post_id")

    # Check if this post has already been labeled
    already_labeled = is_post_labeled(current_post_id, annotator_name, dataset_option, output_dir)

    # Setup session state for this post
    ensure_post_evaluation(current_post_id, dataset_option)

    # Display warning if already labeled
    if already_labeled:
        st.warning(f"⚠️ You have already labeled this question. Your new submission will overwrite the previous one.")

    # Define tab names based on dataset
    if dataset_option == "Faiz_FJ":
        tab_names = ["Image Text Extraction", "GPT Evaluation", "Gemini Evaluation", "Llama Evaluation", "Submit All"]
    else:  # FJ_only.json
        tab_names = ["GPT Evaluation", "Gemini Evaluation", "Llama Evaluation", "Submit All"]

    # Create tabs for each section and a submit tab
    tabs = st.tabs(tab_names)

    if dataset_option == "Faiz_FJ":
        # Tab 1: Image Text Extraction
        with tabs[0]:
            display_question_details(current_question, current_post_id, show_image=True)
            question_key = f"img_extraction_{st.session_state.current_index}_{st.session_state.question_key}"
            image_text_extraction_section(current_question, current_post_id, question_key)

            # Add tab navigation at bottom with correct tab index
            add_tab_navigation(tab_names, 0)

        # Tab 2-4: Model Evaluations
        with tabs[1]:
            model_evaluation_tabs("GPT", current_question, f"gpt_{st.session_state.current_index}_{st.session_state.question_key}")

            # Add tab navigation at bottom with correct tab index
            add_tab_navigation(tab_names, 1)

        with tabs[2]:
            model_evaluation_tabs("Gemini", current_question, f"gemini_{st.session_state.current_index}_{st.session_state.question_key}")

            # Add tab navigation at bottom with correct tab index
            add_tab_navigation(tab_names, 2)

        with tabs[3]:
            model_evaluation_tabs("Llama", current_question, f"llama_{st.session_state.current_index}_{st.session_state.question_key}")

            # Add tab navigation at bottom with correct tab index
            add_tab_navigation(tab_names, 3)

        # Tab 5: Submit All
        with tabs[4]:
            st.header("Submit All Evaluations")
            st.info("Review all your evaluations before submitting. Make sure you have completed all the sections.")

            # Display preview of all evaluations
            display_evaluation_preview()

            # Check if all sections are completed
            all_complete = are_evaluations_complete(dataset_option)

            if not all_complete:
                st.warning("⚠️ Please complete all evaluation sections before submitting.")

            # Submit button
            if st.button("Submit All Evaluations", disabled=not all_complete):
                # Create submission object
                evaluation_data = st.session_state.current_evaluation.copy()
                evaluation_data.update({
                    "annotator": annotator_name,
                    "dataset": dataset_option,
                    "title": current_question.get("title"),
                    "timestamp": datetime.now().isoformat(),
                })

                # Save to file
                saved_file = save_labeled_data(evaluation_data, annotator_name, dataset_option, output_dir)

                # Show success message
                st.success(f"All evaluations submitted successfully and saved to {saved_file}")

                # Clear current evaluation for this post
                st.session_state.current_evaluation = {}

                # Increment the question key to force form reset
                st.session_state.question_key += 1

                # Move to next question if available
                if st.session_state.current_index < len(dataset) - 1:
                    st.session_state.previous_index = st.session_state.current_index
                    st.session_state.current_index += 1
                    st.rerun()

            # Add tab navigation at bottom with correct tab index
            add_tab_navigation(tab_names, 4)
    else:  # FJ_only.json
        # Tab 1-3: Model Evaluations
        with tabs[0]:
            model_evaluation_tabs("GPT", current_question, f"gpt_{st.session_state.current_index}_{st.session_state.question_key}")

            # Add tab navigation at bottom with correct tab index
            add_tab_navigation(tab_names, 0)

        with tabs[1]:
            model_evaluation_tabs("Gemini", current_question, f"gemini_{st.session_state.current_index}_{st.session_state.question_key}")

            # Add tab navigation at bottom with correct tab index
            add_tab_navigation(tab_names, 1)

        with tabs[2]:
            model_evaluation_tabs("Llama", current_question, f"llama_{st.session_state.current_index}_{st.session_state.question_key}")

            # Add tab navigation at bottom with correct tab index
            add_tab_navigation(tab_names, 2)

        # Tab 4: Submit All
        with tabs[3]:
            st.header("Submit All Evaluations")
            st.info("Review all your evaluations before submitting. Make sure you have completed all the sections.")

            # Display preview of all evaluations
            display_evaluation_preview()

            # Check if all sections are completed
            all_complete = are_evaluations_complete(dataset_option)

            if not all_complete:
                st.warning("⚠️ Please complete all evaluation sections before submitting.")

            # Submit button
            if st.button("Submit All Evaluations", disabled=not all_complete):
                # Create submission object
                evaluation_data = st.session_state.current_evaluation.copy()
                evaluation_data.update({
                    "annotator": annotator_name,
                    "dataset": dataset_option,
                    "title": current_question.get("title"),
                    "timestamp": datetime.now().isoformat(),
                })

                # Save to file
                saved_file = save_labeled_data(evaluation_data, annotator_name, dataset_option, output_dir)

                # Show success message
                st.success(f"All evaluations submitted successfully and saved to {saved_file}")

                # Clear current evaluation for this post
                st.session_state.current_evaluation = {}

                # Increment the question key to force form reset
                st.session_state.question_key += 1

                # Move to next question if available
                if st.session_state.current_index < len(dataset) - 1:
                    st.session_state.previous_index = st.session_state.current_index
                    st.session_state.current_index += 1
                    st.rerun()

            # Add tab navigation at bottom with correct tab index
            add_tab_navigation(tab_names, 3)

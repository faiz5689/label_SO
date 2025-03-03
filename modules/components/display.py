# ./modules/components/display.py

import streamlit as st
import requests
from PIL import Image
from io import BytesIO


def display_question_details(current_question, current_post_id, show_image=True):
    """Display question details

    Args:
        current_question (dict): The question data
        current_post_id (str): ID of the post
        show_image (bool, optional): Whether to show the image. Defaults to True.
    """
    # Display question details
    st.header(current_question.get("title", "Untitled Question"))
    st.subheader(f"Question ID: {current_post_id}")

    # Display question content
    st.subheader("Question Content")
    render_html(current_question.get("body", "No question body available."))

    # Display metadata
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Creation Date:** {current_question.get('creation_date', 'Unknown')}")
        st.write(f"**Score:** {current_question.get('score', 'Unknown')}")
    with col2:
        tags = current_question.get("tags", [])
        st.write("**Tags:**")
        st.write(", ".join(tags) if tags else "No tags")

    # Display image if requested
    if show_image:
        st.subheader("Image")
        image_url = current_question.get("image_link", "")
        if image_url:
            display_image(image_url)
            st.caption("Image from the question")
        else:
            st.info("No image available for this question.")


def display_image(image_url):
    """Display an image from a URL

    Args:
        image_url (str): URL of the image to display
    """
    if not image_url:
        return st.info("No image available for this question.")

    try:
        # Add user-agent header to avoid getting blocked
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(image_url, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors

        img = Image.open(BytesIO(response.content))
        # Use st.image without the use_container_width parameter
        st.image(img, width=None)  # You can set a specific width if needed, e.g., width=600
    except Exception as e:
        st.error(f"Error displaying image: {e}")
        st.markdown(f"[Link to image]({image_url})")

def render_html(html_string):
    """Render HTML safely with improved handling of different content types

    Args:
        html_string: HTML content to render
    """
    if html_string is None:
        return st.info("No content available.")

    # If it's not a string (e.g., it's a dictionary or other object), convert to string
    if not isinstance(html_string, str):
        try:
            html_string = str(html_string)
        except:
            return st.info("Content is not in a displayable format.")

    # Make sure the string is not empty
    if not html_string.strip():
        return st.info("No content available.")

    # Safely display the HTML content
    html_string = html_string.replace("\n", " ")
    return st.markdown(html_string, unsafe_allow_html=True)


def get_model_response(current_question, model_name, with_image=False):
    """Extract and return the model response from the question data

    Args:
        current_question (dict): The question data
        model_name (str): Name of the model (GPT, Gemini, Llama)
        with_image (bool, optional): Whether to get the with-image response. Defaults to False.

    Returns:
        str: The model's response
    """
    # Try different case variations of the field name
    field_variations = [
        f"{model_name}_{'with' if with_image else 'without'}_image_response",          # Gemini_with_image_response
        f"{model_name.lower()}_{'with' if with_image else 'without'}_image_response",  # gemini_with_image_response
        f"{model_name.upper()}_{'with' if with_image else 'without'}_image_response"   # GEMINI_with_image_response
    ]

    # Try each variation
    for field_name in field_variations:
        response = current_question.get(field_name)
        if response:
            return response

    # If no response is found, log the available fields to help diagnose the issue
    st.info(f"Debug: Available fields in JSON: {list(current_question.keys())}")

    # Return a placeholder message
    return f"No {model_name} response available for this question."


def display_evaluation_preview():
    """Display a preview of the current evaluations"""
    st.subheader("Preview of Your Evaluations")

    # Get current evaluation data
    eval_data = st.session_state.current_evaluation

    # Create expandable sections for each model with both with/without image evaluations
    for model in ["GPT", "Gemini", "Llama"]:
        with st.expander(f"{model} Evaluation", expanded=False):
            # With Image evaluation
            with_image_key = f"{model}_with_image_evaluation"
            with_image_data = eval_data.get(with_image_key, {})

            st.write(f"### {model} With Image Evaluation")
            if with_image_data:
                # Correctness
                st.write(f"**Correctness**: {'Correct' if with_image_data.get('correctness', {}).get('is_correct', True) else 'Incorrect'}")
                if not with_image_data.get('correctness', {}).get('is_correct', True):
                    st.write(f"- Issues: {', '.join(with_image_data.get('correctness', {}).get('issues', []))}")

                    # Code issues if any
                    if with_image_data.get('code_issues', {}).get('has_issues', False):
                        st.write(f"- Code Issues: {', '.join(with_image_data.get('code_issues', {}).get('types', []))}")
                        if "Non-Functional" in with_image_data.get('code_issues', {}).get('types', []):
                            st.write(f"  - Non-Functional Types: {', '.join(with_image_data.get('code_issues', {}).get('non_functional_types', []))}")

                # Consistency
                st.write(f"**Consistency**: {'Consistent' if with_image_data.get('consistency', {}).get('is_consistent', True) else 'Inconsistent'}")
                if not with_image_data.get('consistency', {}).get('is_consistent', True):
                    st.write(f"- Issues: {', '.join(with_image_data.get('consistency', {}).get('issues', []))}")

                # Comprehensiveness
                st.write(f"**Comprehensiveness**: {'Comprehensive' if with_image_data.get('is_comprehensive', True) else 'Not Comprehensive'}")

                # Conciseness
                st.write(f"**Conciseness**: {'Concise' if with_image_data.get('conciseness', {}).get('is_concise', True) else 'Not Concise'}")
                if not with_image_data.get('conciseness', {}).get('is_concise', True):
                    st.write(f"- Issues: {', '.join(with_image_data.get('conciseness', {}).get('issues', []))}")

                # Usefulness
                st.write(f"**Usefulness Rating**: {with_image_data.get('usefulness_rating', 3)}/5")

                # Notes
                if with_image_data.get('notes'):
                    st.write(f"**Notes**: {with_image_data.get('notes')}")
            else:
                st.write("*No evaluation provided yet*")

            # Without Image evaluation
            without_image_key = f"{model}_without_image_evaluation"
            without_image_data = eval_data.get(without_image_key, {})

            st.write(f"### {model} Without Image Evaluation")
            if without_image_data:
                # Correctness
                st.write(f"**Correctness**: {'Correct' if without_image_data.get('correctness', {}).get('is_correct', True) else 'Incorrect'}")
                if not without_image_data.get('correctness', {}).get('is_correct', True):
                    st.write(f"- Issues: {', '.join(without_image_data.get('correctness', {}).get('issues', []))}")

                    # Code issues if any
                    if without_image_data.get('code_issues', {}).get('has_issues', False):
                        st.write(f"- Code Issues: {', '.join(without_image_data.get('code_issues', {}).get('types', []))}")
                        if "Non-Functional" in without_image_data.get('code_issues', {}).get('types', []):
                            st.write(f"  - Non-Functional Types: {', '.join(without_image_data.get('code_issues', {}).get('non_functional_types', []))}")

                # Consistency
                st.write(f"**Consistency**: {'Consistent' if without_image_data.get('consistency', {}).get('is_consistent', True) else 'Inconsistent'}")
                if not without_image_data.get('consistency', {}).get('is_consistent', True):
                    st.write(f"- Issues: {', '.join(without_image_data.get('consistency', {}).get('issues', []))}")

                # Comprehensiveness
                st.write(f"**Comprehensiveness**: {'Comprehensive' if without_image_data.get('is_comprehensive', True) else 'Not Comprehensive'}")

                # Conciseness
                st.write(f"**Conciseness**: {'Concise' if without_image_data.get('conciseness', {}).get('is_concise', True) else 'Not Concise'}")
                if not without_image_data.get('conciseness', {}).get('is_concise', True):
                    st.write(f"- Issues: {', '.join(without_image_data.get('conciseness', {}).get('issues', []))}")

                # Usefulness
                st.write(f"**Usefulness Rating**: {without_image_data.get('usefulness_rating', 3)}/5")

                # Notes
                if without_image_data.get('notes'):
                    st.write(f"**Notes**: {without_image_data.get('notes')}")
            else:
                st.write("*No evaluation provided yet*")

    # Display related text if available (for Faiz_FJ dataset)
    if "related_text" in eval_data:
        with st.expander("Image Text Extraction", expanded=False):
            if eval_data.get("related_text"):
                st.write(f"**Extracted Text**: {eval_data.get('related_text')}")
            else:
                st.write("**Extracted Text**: (No relevant text in the image)")


def create_duplicate_tabs_navigation(tab_titles, current_tab_index):
    """Create a duplicate tab navigation bar at the bottom of the content"""
    st.write("---")
    st.write("**Navigate to:**")

    # Create columns for each tab
    cols = st.columns(len(tab_titles))

    # Display each tab button
    for i, title in enumerate(tab_titles):
        with cols[i]:
            # Make the current tab highlighted
            if i == current_tab_index:
                st.markdown(f"**[{title}]**", unsafe_allow_html=True)
            else:
                # For tabs other than the current one, make them clickable
                if st.button(title, key=f"bottom_tab_{i}"):
                    # This doesn't directly change tabs but will trigger a rerun
                    # We'll need to handle this in the calling function
                    return i

    # Return None if no tab was clicked
    return None

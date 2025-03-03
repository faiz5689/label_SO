# modules/components/image_extraction.py

import streamlit as st


def image_text_extraction_section(current_question, current_post_id, question_key):
    """Handle the image text extraction section

    Args:
        current_question (dict): The question data
        current_post_id (str): ID of the post
        question_key (str): Unique key for this question

    Returns:
        str: The extracted text
    """
    st.subheader("Image Text Extraction")
    st.write("""
    Analyze the relationship between the question content and the code in the image.
    Task:
    1. Carefully read the question, title, and body to understand the main problem or query.
    2. Examine the code image and identify any text/code segments that directly relate to or address the question.
    3. Extract the specific portions of text from the image that most closely connect to the question's context. Only from the image.
    4. Return only the relevant text.
    """)

    st.info("If the image does not contain any relevant text or code, you can leave this field empty.")

    related_text = st.text_area(
        "Extract the relevant text from the image that relates to the question:",
        value=st.session_state.current_evaluation.get("related_text", ""),
        height=150,
        key=f"{question_key}_related_text"
    )

    # Save to session state
    st.session_state.current_evaluation["related_text"] = related_text

    # Update the post evaluations
    post_id = st.session_state.current_evaluation["post_id"]
    st.session_state.post_evaluations[post_id] = st.session_state.current_evaluation

    return related_text


def are_evaluations_complete(dataset_option):
    """Check if all required evaluations are complete

    Args:
        dataset_option (str): Dataset being used

    Returns:
        bool: True if all evaluations are complete, False otherwise
    """
    eval_data = st.session_state.current_evaluation

    # Check if all models have both with and without image evaluations
    for model in ["GPT", "Gemini", "Llama"]:
        with_image_key = f"{model}_with_image_evaluation"
        without_image_key = f"{model}_without_image_evaluation"

        if with_image_key not in eval_data or without_image_key not in eval_data:
            return False

    # Check if related_text is present for Faiz_FJ dataset
    if dataset_option == "Faiz_FJ" and "related_text" not in eval_data:
        return False

    return True

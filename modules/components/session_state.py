# modules/components/session_state.py

import streamlit as st
from datetime import datetime


def init_session_state():
    """Initialize session state variables"""
    # Create a unique key for each question
    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0

    # Create keys for form fields
    if 'question_key' not in st.session_state:
        st.session_state.question_key = 0

    # Check if navigation occurred
    if 'previous_index' not in st.session_state:
        st.session_state.previous_index = -1

    # Tab selection
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "Label"

    # Initialize evaluation state for current post
    if 'current_evaluation' not in st.session_state:
        st.session_state.current_evaluation = {}

    # Initialize for navigation without losing progress
    if 'post_evaluations' not in st.session_state:
        st.session_state.post_evaluations = {}


def ensure_post_evaluation(post_id, dataset_option):
    """Ensure post_id exists in session state"""
    if post_id not in st.session_state.post_evaluations:
        # Initialize with template structure
        template = {
            "post_id": post_id,
            "timestamp": datetime.now().isoformat(),
        }

        # Add related_text field only for Faiz_FJ dataset
        if dataset_option == "Faiz_FJ":
            template["related_text"] = ""

        # Add evaluation fields for all models with separate with/without image evaluations
        for model in ["GPT", "Gemini", "Llama"]:
            # Create entry for with_image evaluation
            template[f"{model}_with_image_evaluation"] = {
                "correctness": {"is_correct": True, "issues": []},
                "consistency": {"is_consistent": True, "issues": []},
                "is_comprehensive": True,
                "conciseness": {"is_concise": True, "issues": []},
                "usefulness_rating": 3,
                "code_issues": {"has_issues": False, "types": [], "non_functional_types": []},
                "notes": ""
            }

            # Create entry for without_image evaluation
            template[f"{model}_without_image_evaluation"] = {
                "correctness": {"is_correct": True, "issues": []},
                "consistency": {"is_consistent": True, "issues": []},
                "is_comprehensive": True,
                "conciseness": {"is_concise": True, "issues": []},
                "usefulness_rating": 3,
                "code_issues": {"has_issues": False, "types": [], "non_functional_types": []},
                "notes": ""
            }

        st.session_state.post_evaluations[post_id] = template

    # Set current evaluation to this post's evaluation
    st.session_state.current_evaluation = st.session_state.post_evaluations[post_id]

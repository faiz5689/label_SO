# ./modules/utils/file_utils.py

import os
import json
import streamlit as st


def load_data(file_path):
    """Load data from a JSON file

    Args:
        file_path (str): Path to the JSON file

    Returns:
        list or dict: The loaded JSON data
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        return []
    except json.JSONDecodeError:
        st.error(f"Invalid JSON format in file: {file_path}")
        return []
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return []


def save_labeled_data(labeled_item, annotator_name, dataset_option, output_dir):
    """Save labeled data to a JSON file

    Args:
        labeled_item (dict): The labeled data to save
        annotator_name (str): Name of the annotator
        dataset_option (str): Dataset being used
        output_dir (str): Directory to save the file

    Returns:
        str: Path to the saved file
    """
    # Create a consistent filename for this annotator and dataset
    filename = f"{output_dir}/{annotator_name}_{dataset_option}_labels.json"

    # Initialize data array
    data = []

    # If file exists, load existing data
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, list):
                    data = [data]  # Convert to list if it's not already
        except (json.JSONDecodeError, FileNotFoundError) as e:
            st.error(f"Error loading existing data: {e}. Creating new file.")
            data = []

    # Check if post_id already exists and replace if it does
    post_id = labeled_item.get("post_id")
    data = [item for item in data if item.get("post_id") != post_id]

    # Add the new labeled item
    data.append(labeled_item)

    # Save the updated data
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return filename


def get_labeled_files(annotator_name, output_dir):
    """Get all labeled data files for an annotator

    Args:
        annotator_name (str): Name of the annotator
        output_dir (str): Directory containing the files

    Returns:
        list: List of file paths
    """
    if not os.path.exists(output_dir):
        return []

    files = []
    for filename in os.listdir(output_dir):
        if filename.startswith(annotator_name) and filename.endswith('_labels.json'):
            files.append(os.path.join(output_dir, filename))

    return files


def is_post_labeled(post_id, annotator_name, dataset_option, output_dir):
    """Check if a post has already been labeled

    Args:
        post_id (str): ID of the post
        annotator_name (str): Name of the annotator
        dataset_option (str): Dataset being used
        output_dir (str): Directory containing the labeled data

    Returns:
        bool: True if the post has been labeled, False otherwise
    """
    filename = f"{output_dir}/{annotator_name}_{dataset_option}_labels.json"

    if not os.path.exists(filename):
        return False

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, list):
                data = [data]

            # Check if this post_id exists in the data
            for item in data:
                if item.get('post_id') == post_id:
                    return True
    except:
        return False

    return False


def get_existing_labels(post_id, annotator_name, dataset_option, output_dir):
    """Get existing labels for a post if available

    Args:
        post_id (str): ID of the post
        annotator_name (str): Name of the annotator
        dataset_option (str): Dataset being used
        output_dir (str): Directory containing the labeled data

    Returns:
        dict: The existing labels or None if not found
    """
    filename = f"{output_dir}/{annotator_name}_{dataset_option}_labels.json"

    if not os.path.exists(filename):
        return None

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, list):
                data = [data]

            # Find the post with the matching post_id
            for item in data:
                if item.get('post_id') == post_id:
                    return item
    except:
        return None

    return None

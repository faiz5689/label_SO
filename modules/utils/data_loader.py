# ./modules/utils/data_loader.py

import json
import os

class DataLoader:
    """Utility class for loading and preprocessing JSON data files"""

    def __init__(self, data_dir="data/final_files"):
        self.data_dir = data_dir

    def load_file(self, filename):
        """Load a single JSON file

        Args:
            filename (str): Name of the file to load

        Returns:
            list or dict: The loaded JSON data
        """
        file_path = os.path.join(self.data_dir, filename)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: File not found - {file_path}")
            return []
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in file - {file_path}")
            return []
        except Exception as e:
            print(f"Error loading file {file_path}: {str(e)}")
            return []

    def load_faiz_fj(self):
        """Load the Faiz_FJ.json file"""
        return self.load_file("Faiz_FJ.json")

    def load_fj_only(self):
        """Load the FJ_only.json file"""
        return self.load_file("FJ_only.json")

    def get_question_by_id(self, post_id, source="Faiz_FJ"):
        """Get a specific question by its post_id

        Args:
            post_id (int): The post ID to search for
            source (str): Which file to search in ("Faiz_FJ" or "FJ_only")

        Returns:
            dict: The question data or None if not found
        """
        data = self.load_faiz_fj() if source == "Faiz_FJ" else self.load_fj_only()

        for item in data:
            if item.get("post_id") == post_id:
                return item

        return None

    def count_items(self):
        """Count the number of items in each file

        Returns:
            tuple: (faiz_fj_count, fj_only_count)
        """
        faiz_fj = self.load_faiz_fj()
        fj_only = self.load_fj_only()

        return len(faiz_fj), len(fj_only)

# Example usage
if __name__ == "__main__":
    loader = DataLoader()

    # Load the files
    faiz_fj_data = loader.load_faiz_fj()
    fj_only_data = loader.load_fj_only()

    # Print counts
    faiz_count, fj_count = loader.count_items()
    print(f"Found {faiz_count} items in Faiz_FJ.json")
    print(f"Found {fj_count} items in FJ_only.json")

    # Print a sample item
    if faiz_fj_data:
        sample = faiz_fj_data[0]
        print("\nSample item from Faiz_FJ.json:")
        print(f"Title: {sample.get('title', 'Unknown')}")
        print(f"Post ID: {sample.get('post_id', 'Unknown')}")
        print(f"Tags: {', '.join(sample.get('tags', []))}")

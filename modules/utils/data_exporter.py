# ./modules/utils/data_exporter.py

import json
import os
import pandas as pd
from datetime import datetime

class DataExporter:
    """Utility class for exporting labeled data to various formats"""

    def __init__(self, output_dir=None):
        # Use provided output_dir or default to a directory relative to this script
        if output_dir is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            self.output_dir = os.path.join(script_dir, "labeled_data")
        else:
            self.output_dir = output_dir

        os.makedirs(self.output_dir, exist_ok=True)

    def get_all_labeled_files(self):
        """Get a list of all labeled data files

        Returns:
            list: List of file paths
        """
        if not os.path.exists(self.output_dir):
            return []

        return [os.path.join(self.output_dir, f) for f in os.listdir(self.output_dir)
                if f.endswith('.json')]

    def merge_all_files(self, output_filename=None):
        """Merge all labeled data files into one

        Args:
            output_filename (str, optional): Name for the merged file.
                If None, a timestamp-based name will be used.

        Returns:
            str: Path to the merged file
        """
        all_files = self.get_all_labeled_files()

        if not all_files:
            print("No labeled data files found.")
            return None

        all_data = []

        for file_path in all_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_data = json.load(f)

                    # Handle both single items and lists of items
                    if isinstance(file_data, list):
                        all_data.extend(file_data)
                    else:
                        all_data.append(file_data)
            except Exception as e:
                print(f"Error reading file {file_path}: {str(e)}")

        # Create output filename with timestamp if not provided
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"merged_labeled_data_{timestamp}.json"

        output_path = os.path.join(self.output_dir, output_filename)

        # Save merged data
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2)

        print(f"Merged {len(all_data)} labeled items into {output_path}")
        return output_path

    def export_to_csv(self, output_filename=None):
        """Export labeled data to CSV format

        Args:
            output_filename (str, optional): Name for the CSV file.
                If None, a timestamp-based name will be used.

        Returns:
            str: Path to the CSV file
        """
        # First merge all data
        merged_file = self.merge_all_files()

        if not merged_file:
            return None

        # Load the merged data
        with open(merged_file, 'r', encoding='utf-8') as f:
            all_data = json.load(f)

        # Flatten the nested structure for CSV
        flattened_data = []

        for item in all_data:
            flat_item = {
                'post_id': item.get('post_id'),
                'title': item.get('title'),
                'annotator': item.get('annotator'),
                'timestamp': item.get('timestamp'),
                'related_text': item.get('part1', {}).get('related_text', '')
            }

            # Add part2 questions
            part2 = item.get('part2', {})
            for q_key, q_value in part2.items():
                flat_item[q_key] = q_value

            flattened_data.append(flat_item)

        # Create DataFrame
        df = pd.DataFrame(flattened_data)

        # Create output filename with timestamp if not provided
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"labeled_data_{timestamp}.csv"

        output_path = os.path.join(self.output_dir, output_filename)

        # Save to CSV
        df.to_csv(output_path, index=False, encoding='utf-8')

        print(f"Exported data to CSV: {output_path}")
        return output_path

# Example usage
if __name__ == "__main__":
    exporter = DataExporter()

    # Merge all labeled files
    merged_file = exporter.merge_all_files()

    # Export to CSV
    csv_file = exporter.export_to_csv()

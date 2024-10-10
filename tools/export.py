import pandas as pd

def export_to_csv(output_list, file_name):
    """
    Converts a list of dictionaries to a pandas DataFrame and exports it as a CSV file.
    
    Parameters:
    - output_list: list of dicts containing the data
    - file_name: string, the name of the file (with .csv extension) to export the DataFrame
    
    Returns:
    - None
    """
    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(output_list)
    
    # Export the DataFrame to a CSV file
    df.to_csv(file_name, index=False)
    print(f"Data exported successfully to {file_name}")

# utils.py
def load_sql(query_name):
    with open(f'sql/{query_name}.sql', 'r') as file:
        return file.read()

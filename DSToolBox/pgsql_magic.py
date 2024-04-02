from IPython.core.magic import register_cell_magic
from sqlalchemy import create_engine
import pandas as pd
from google.colab import userdata
from sqlalchemy import text


# connection_string = userdata.get('DO_Postgres')
connection_string = userdata.get('postgres_key')
# Create an SQLAlchemy engine
engine = create_engine(connection_string)

# Initialize a global dictionary to hold the results
results_dict = {}

@register_cell_magic
def sql(line, cell):
  """
Defines a cell magic for executing SQL queries within IPython notebooks and storing the results in a global dictionary.

:param line: A string to customize the key under which the resulting DataFrame is stored in the results dictionary.
:param cell: The SQL query to be executed.
:return: Prints a message indicating the key under which the query result is stored in the global dictionary.
Example:
%%sql myQuery
SELECT * FROM my_table
This would execute the SQL query "SELECT * FROM my_table", store the resulting DataFrame in the results_dict under a key like 'dfmyQuery1', and print "saved to results_dict[dfmyQuery1]".
"""
  global results_dict  # Refer to the global dictionary
  query = text(cell)
  with engine.connect() as conn:
      result = pd.read_sql_query(query, conn)
  dict_name = f'df{line}{len(results_dict)+1}'
  results_dict[dict_name] = result
  print(f'saved to results_dict[{dict_name}]')

import configparser

from google.cloud import bigquery
from google.api_core.exceptions import BadRequest, NotFound, Forbidden, Conflict

config = configparser.ConfigParser()
config.read("config.ini")
GCP_PROJECT = config["Cloud Configs"]["GCP_PROJECT"]

class BigQueryClass():
  """Execute BigQuery queries.

  Documentation: https://cloud.google.com/python/docs/reference/bigquery/latest/index.html
  """
  def __init__(self):
    self.client = bigquery.Client(project=GCP_PROJECT)

  def run_query(self, query: str) -> str:
    print(f"Executing query...{query}")
    error = None
    try:
      query_job = self.client.query(query)
    except BadRequest as e:
      error = f"ERROR: Invalid query - {str(e)}"
    except NotFound as e:
      error = f"ERROR: Resource not found - {str(e)}"
    except Forbidden as e:
      error = f"ERROR: Insufficient permissions - {str(e)}"
    except Conflict as e:
      error = f"ERROR: Concurrent modification - {str(e)}"
    except Exception as e:
      error = f"ERROR: An unexpected error occurred - {str(e)}"
    
    if error:
      print(error)
      return error

    try:
      rows = query_job.result()
      result = []
      for row in rows:
        row_data = ", ".join([f"{v}" for k, v in row.items()])
        result.append(row_data)
      return "\n".join(result)
    except Exception as e:
      error = f"ERROR: Failed to retrieve query results - {str(e)}"
      print(error)
      return error
import csv

def load_data_as_dict(file_name: str) -> dict:
    """
    Load CSV data and create dict from that
    """
    with open(file_name, mode='r') as file:
        reader = csv.reader(file)
        dic = { row[0]: row[1] for row in reader }
    return dic


def export_as_csv(filename, dic: dict) -> None:
  """
  Process and export as CSV file
  """
  list_included_tuple = [(key, value) for key, value in dic.items()]
  with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for tup in list_included_tuple:
      writer.writerow(tup)
def read_file(filepath):

  try:
    with open(filepath, "r") as file:
      return file.read()
  except FileNotFoundError:
    print(f"Error: File not found: {filepath}")
    return None

def write_file(filepath, data):

  try:
    with open(filepath, "w") as file:
      file.write(data)
  except IOError as error:
    print(f"Error writing to file: {error}")

def append_to_file(filepath, data):

  try:
    with open(filepath, "a") as file:
      file.write(data)
  except IOError as error:
    print(f"Error appending to file: {error}")

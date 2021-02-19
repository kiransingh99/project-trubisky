def isFloat(value):
  """Checks if a string can be converted into a floating point value.

  Args:
      value (str): test if this object can be converted into a float

  Returns:
      bool: true if 'value' can be converted into a float, false otherwise
  """
  
  try:
    float(value)
    return True
  except ValueError:
    return False
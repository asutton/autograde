


class Error:
  """Represents an error in the submission. Errors result in the
  deduction of points."""
  def __init__(self, msg):
    self.msg = msg

  def __str__(self):
    return "error: " + self.msg

class Note:
  """Represents a note about the submission. Notes do not generally
  result in the deduction of points."""
  
  def __init__(self, msg):
    self.msg = msg

  def __str__(self):
    return "note: " + self.msg

class Report(object):
  """An aggregation of diagnostic messages."""
  def __init__(self):
    self.diags = []

  def __nonzero__(self):
    for x in self.diags:
      if isinstance(x, Error):
        return False
    return True

  def __str__(self):
    msgs = [str(x) for x in self.diags]
    return "\n".join(msgs)

  def error(self, str):
    self.diags += [Error(str)]

  def note(self, str):
    self.diags += [Note(str)]


import uuid


class Response():
  def __init__(self, status_code, data, message):
    self.status_code = status_code
    self.message = message
    self.data = data

  def to_dict(self):
    response_dict = {
      'id': str(uuid.uuid4()),
      'version': '12.1.0',
      'status_code': self.status_code,
      'message': self.message
    }
    if self.data is not None:
      response_dict['data'] = self.data
    return response_dict

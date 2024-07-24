from werkzeug.exceptions import HTTPException

class AccessError(HTTPException):
    code = 403
    message = 'No message specified'

class AdminError(HTTPException):
    code = 403
    message = 'No message specified'

class PermissionError(HTTPException):
    code = 403
    message = 'No message specified'

class InputError(HTTPException):
    code = 400
    message = 'No message specified'

class DatabaseError(HTTPException):
    code = 500
    message = 'No message specified'

class BadRequest(HTTPException):
    code = 404
    message = 'No message specified'
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import os
import shutil
from urllib.parse import urlparse

# General JSON response to return in API response
def create_response(message: str, status_code: int, success: bool = False, **kwargs):
    """ General JSON response """
    
    return JSONResponse(
      status_code = status_code,
      content = {
          'success': success,
          'message': message,
          **jsonable_encoder(kwargs)
        }
    )

def create_local_dir(path):
  try:
    # Create upload directory if it doesn't exist
    os.makedirs(path, exist_ok=True)
  except Exception as e:
    print("Error in create local dir: ", e)
    raise e
    
def delete_local_file_dir(path):
  try:
    # Check if path exists
    if not os.path.exists(path):
      print(f"Path '{path}' doesn't exist")
      return False
    
    # Delete file or directory
    if os.path.isfile(path):
      os.remove(path)
    else:
      shutil.rmtree(path)
    return True
  except Exception as e:
    return False

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import os
import shutil
from urllib.parse import urlparse
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_voyageai import VoyageAIEmbeddings

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

def get_llm_details(llm):
  try:
    if llm == "openai":
        model_name = os.getenv('OPENAI_EMBEDDING_MODEL') or "text-embedding-ada-002"
        embedding_model = OpenAIEmbeddings(model=model_name)
        llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
    elif llm == "claude":
        model_name = os.getenv('CLAUDE_EMBEDDING_MODEL') or "voyage-3"
        embedding_model = VoyageAIEmbeddings(model=model_name, voyage_api_key=os.getenv('VOYAGE_API_KEY'))
        llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.2)
        
    return model_name, embedding_model, llm
  except Exception as e:
    print('➡ Error in get_llm_details:', e)
    raise e
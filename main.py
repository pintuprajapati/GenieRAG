from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
from rag_stack.routes import router as rag_router
from utils import create_local_dir
import config
from dotenv import load_dotenv
load_dotenv(override=True)

SHOW_DOCS_ENVIRONMENT = ("local")  # explicit list of allowed envs

# set url for swagger docs as null if api is not public
openapi_url="/api/openapi.json" if os.getenv('ENVIRONMENT') in SHOW_DOCS_ENVIRONMENT else None

# create required local dirs
create_local_dir(config.STATIC_DIR)
create_local_dir(config.UPLOAD_DIR)
create_local_dir(config.DOWNLOAD_DIR)
create_local_dir(config.MD_FILES_DIR)
create_local_dir(config.TEXT_FILES_DIR)
  
# Initialize FastAPI app
app = FastAPI(
    title="GenieRAG",
    openapi_url=openapi_url
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

########################## Define Routers ########################## 
app.include_router(rag_router)

########################## Main ##########################
if __name__ == "__main__":
    try:
        import uvicorn
        # if env is "local" then reload the server on every change
        reload = True if (os.getenv('ENVIRONMENT') == "local") else False
        reload = True
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=reload)
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


"""
Standalone entry point for PyInstaller bundling.
This file starts the FastAPI backend with uvicorn.
"""
import uvicorn
import os
import sys

# When bundled by PyInstaller, set the working directory to the exe location
if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='127.0.0.1',
        port=8000,
        reload=False,
        log_level='info',
    )

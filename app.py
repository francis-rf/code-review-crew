"""
FastAPI application for Code Review Crew
"""
import os
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import git

from src.crew import CodeReviewCrew
from src.logger import setup_logger
from src.config.settings import settings

logger = setup_logger(__name__)

# Validate settings
if not settings.validate():
    raise RuntimeError("Configuration validation failed. Please check your .env file.")

# Create necessary directories
settings.create_directories()

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
if settings.STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(settings.STATIC_DIR)), name="static")


@app.get("/")
async def read_root():
    """Serve the main HTML page"""
    html_file = settings.STATIC_DIR / "index.html"
    if html_file.exists():
        return FileResponse(html_file)
    return {"message": f"{settings.APP_NAME} is running"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/api/review/upload")
async def review_uploaded_file(file: UploadFile = File(...)):
    """
    Review a single uploaded Python file
    """
    if not file.filename.endswith('.py'):
        raise HTTPException(status_code=400, detail="Only Python files (.py) are supported")

    try:
        # Read file content
        content = await file.read()
        code_content = content.decode('utf-8')

        logger.info(f"Processing uploaded file: {file.filename}")

        # Initialize crew
        crew = CodeReviewCrew(
            code_file_path=file.filename,
            code_content=code_content,
            output_dir=str(settings.OUTPUT_DIR),
            config_dir=str(settings.CONFIG_DIR)
        )

        # Run analysis
        result = crew.run()

        # Get report content
        report_content = str(result.raw) if hasattr(result, 'raw') else str(result)

        return JSONResponse(content={
            "status": "success",
            "filename": file.filename,
            "report": report_content,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Error processing file: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/review/github")
async def review_github_repo(repo_url: str = Form(...), selected_files: Optional[str] = Form(None)):
    """
    Review files from a GitHub repository

    Args:
        repo_url: GitHub repository URL
        selected_files: Comma-separated list of relative file paths (optional, defaults to first 5 .py files)
    """
    if not repo_url:
        raise HTTPException(status_code=400, detail="Repository URL is required")

    temp_dir = None
    try:
        # Clone repository
        temp_dir = tempfile.mkdtemp()
        logger.info(f"Cloning repository: {repo_url}")

        git.Repo.clone_from(repo_url, temp_dir)

        # Find Python files
        py_files = []
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, temp_dir)
                    py_files.append(rel_path)

        if not py_files:
            raise HTTPException(status_code=404, detail="No Python files found in repository")

        # Parse selected files
        if selected_files:
            files_to_analyze = [f.strip() for f in selected_files.split(',')]
        else:
            files_to_analyze = py_files[:settings.GITHUB_DEFAULT_FILES]

        # Combine content from selected files
        combined_content = ""
        for file_rel in files_to_analyze:
            full_path = os.path.join(temp_dir, file_rel)
            if os.path.exists(full_path):
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        combined_content += f"\n\n=== FILE: {file_rel} ===\n{content}\n"
                except Exception as e:
                    logger.warning(f"Skipping {file_rel}: {e}")

        if not combined_content:
            raise HTTPException(status_code=404, detail="No valid files to analyze")

        # Initialize crew
        crew = CodeReviewCrew(
            code_file_path="GITHUB_REPO",
            code_content=combined_content,
            output_dir=str(settings.OUTPUT_DIR),
            config_dir=str(settings.CONFIG_DIR)
        )

        # Run analysis
        logger.info(f"Analyzing {len(files_to_analyze)} files from repository")
        result = crew.run()

        # Get report content
        report_content = str(result.raw) if hasattr(result, 'raw') else str(result)

        return JSONResponse(content={
            "status": "success",
            "repo_url": repo_url,
            "files_analyzed": files_to_analyze,
            "total_files": len(py_files),
            "report": report_content,
            "timestamp": datetime.now().isoformat()
        })

    except git.exc.GitCommandError as e:
        logger.error(f"Git error: {e}")
        raise HTTPException(status_code=400, detail=f"Failed to clone repository: {str(e)}")
    except Exception as e:
        logger.error(f"Error processing repository: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup temp directory
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except Exception as e:
                logger.warning(f"Failed to cleanup temp directory: {e}")


@app.get("/api/files/list")
async def list_python_files(repo_url: str):
    """
    List all Python files in a GitHub repository
    """
    if not repo_url:
        raise HTTPException(status_code=400, detail="Repository URL is required")

    temp_dir = None
    try:
        # Clone repository
        temp_dir = tempfile.mkdtemp()
        git.Repo.clone_from(repo_url, temp_dir)

        # Find Python files
        py_files = []
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, temp_dir)
                    file_size = os.path.getsize(full_path)
                    py_files.append({
                        "path": rel_path,
                        "size": file_size
                    })

        return JSONResponse(content={
            "status": "success",
            "repo_url": repo_url,
            "files": py_files,
            "total": len(py_files)
        })

    except Exception as e:
        logger.error(f"Error listing files: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except Exception as e:
                logger.warning(f"Failed to cleanup temp directory: {e}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD
    )

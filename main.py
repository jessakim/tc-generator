#!/usr/bin/env python3
"""
Gherkin Step Definition Matcher - Main Entry Point
"""

import uvicorn
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    """Main entry point for the application"""
    from config.settings import Settings
    from api.main import app
    
    settings = Settings()
    
    print("🚀 Starting Gherkin Step Matcher")
    print(f"📁 Framework path: {settings.framework_path}")
    print(f"🧠 Model: {settings.embedding_model}")
    print("📖 API docs: http://localhost:8000/docs")
    
    uvicorn.run(
        "api.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )

if __name__ == "__main__":
    main()
"""
Utility helpers for the AI Test Case Generator application
"""

import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from flask import Flask, jsonify


def setup_logging(app: Flask) -> None:
    """
    Setup logging configuration for the application
    
    Args:
        app: Flask application instance
    """
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Configure logging
    log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
    log_file = os.environ.get('LOG_FILE', 'logs/app.log')
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(getattr(logging, log_level))
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level))
    console_handler.setFormatter(formatter)
    
    # Configure app logger
    app.logger.setLevel(getattr(logging, log_level))
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level))
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    app.logger.info("Logging configured successfully")


def create_response(data: Optional[Dict[str, Any]] = None, 
                   error: Optional[str] = None, 
                   status_code: int = 200) -> tuple:
    """
    Create standardized API response
    
    Args:
        data: Response data dictionary
        error: Error message if any
        status_code: HTTP status code
        
    Returns:
        Tuple of (response, status_code)
    """
    response = {
        "timestamp": datetime.now().isoformat(),
        "status_code": status_code
    }
    
    if error:
        response["success"] = False
        response["error"] = error
    else:
        response["success"] = True
        if data:
            response.update(data)
    
    return jsonify(response), status_code


def validate_environment() -> Dict[str, Any]:
    """
    Validate required environment variables and configuration
    
    Returns:
        Dictionary with validation results
    """
    required_vars = ['ANTHROPIC_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    return {
        "valid": len(missing_vars) == 0,
        "missing_variables": missing_vars,
        "environment": os.environ.get('FLASK_ENV', 'development')
    }


def calculate_time_savings(test_case_count: int) -> Dict[str, float]:
    """
    Calculate estimated time savings from AI-generated test cases
    
    Args:
        test_case_count: Number of generated test cases
        
    Returns:
        Dictionary with time savings calculations
    """
    # Average time estimates (in hours)
    manual_time_per_case = 0.5  # 30 minutes per test case manually
    ai_generation_time = 0.05   # ~3 minutes total for AI generation
    review_time_per_case = 0.05  # 3 minutes review per case
    
    manual_total = test_case_count * manual_time_per_case
    ai_total = ai_generation_time + (test_case_count * review_time_per_case)
    time_saved = manual_total - ai_total
    efficiency_gain = (time_saved / manual_total) * 100 if manual_total > 0 else 0
    
    return {
        "manual_hours": round(manual_total, 2),
        "ai_hours": round(ai_total, 2),
        "time_saved_hours": round(time_saved, 2),
        "efficiency_gain_percent": round(efficiency_gain, 1)
    }


def format_test_steps(steps: list) -> str:
    """
    Format test steps for display
    
    Args:
        steps: List of test steps
        
    Returns:
        Formatted string of test steps
    """
    if not steps:
        return "No test steps provided"
    
    if isinstance(steps, str):
        return steps
    
    formatted_steps = ""
    for i, step in enumerate(steps, 1):
        formatted_steps += f"{i}. {step}\n"
    
    return formatted_steps.strip()


def get_priority_color(priority: str) -> str:
    """
    Get color code for priority level
    
    Args:
        priority: Priority level string
        
    Returns:
        Bootstrap color class
    """
    priority_colors = {
        'High': 'danger',
        'Medium': 'warning', 
        'Low': 'success'
    }
    
    return priority_colors.get(priority, 'secondary')


def get_test_type_icon(test_type: str) -> str:
    """
    Get icon for test type
    
    Args:
        test_type: Test type string
        
    Returns:
        Font Awesome icon class
    """
    type_icons = {
        'Functional': 'fas fa-cogs',
        'Security': 'fas fa-shield-alt',
        'UAT': 'fas fa-user-check',
        'Performance': 'fas fa-tachometer-alt',
        'Integration': 'fas fa-link',
        'Usability': 'fas fa-user-friends',
        'Accessibility': 'fas fa-universal-access'
    }
    
    return type_icons.get(test_type, 'fas fa-question-circle')


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe file operations
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    import re
    
    # Remove or replace unsafe characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove leading/trailing dots and spaces
    filename = filename.strip(' .')
    
    # Ensure filename is not too long
    if len(filename) > 100:
        name, ext = os.path.splitext(filename)
        filename = name[:96] + ext
    
    return filename


def generate_test_id(index: int, prefix: str = "TC") -> str:
    """
    Generate test case ID
    
    Args:
        index: Test case index
        prefix: ID prefix
        
    Returns:
        Formatted test case ID
    """
    return f"{prefix}{str(index).zfill(3)}"


def parse_user_story(story_text: str) -> Dict[str, str]:
    """
    Parse user story text to extract components
    
    Args:
        story_text: User story text
        
    Returns:
        Dictionary with parsed components
    """
    import re
    
    # Pattern to match "As a [role], I want [goal] so that [benefit]"
    pattern = r'as\s+a\s+([^,]+),?\s+i\s+want\s+([^,]+?)(?:\s+so\s+that\s+(.+))?$'
    match = re.search(pattern, story_text.lower())
    
    if match:
        return {
            "role": match.group(1).strip(),
            "goal": match.group(2).strip(),
            "benefit": match.group(3).strip() if match.group(3) else ""
        }
    
    return {
        "role": "user",
        "goal": story_text,
        "benefit": ""
    }


def get_application_info() -> Dict[str, Any]:
    """
    Get application information and status
    
    Returns:
        Dictionary with application info
    """
    return {
        "name": "AI Test Case Generator",
        "version": "1.0.0",
        "description": "Transform user stories into comprehensive test suites using Claude AI",
        "author": "Development Team",
        "environment": os.environ.get('FLASK_ENV', 'development'),
        "python_version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
        "startup_time": datetime.now().isoformat()
    }


def estimate_complexity_score(test_cases: list) -> Dict[str, Any]:
    """
    Estimate complexity score for generated test cases
    
    Args:
        test_cases: List of test case dictionaries
        
    Returns:
        Dictionary with complexity metrics
    """
    if not test_cases:
        return {"score": 0, "level": "None"}
    
    total_score = 0
    
    for test_case in test_cases:
        score = 0
        
        # Base score
        score += 1
        
        # Add points for complexity indicators
        if test_case.get('priority') == 'High':
            score += 2
        elif test_case.get('priority') == 'Medium':
            score += 1
        
        # Test steps complexity
        steps = test_case.get('test_steps', [])
        if isinstance(steps, list):
            score += min(len(steps), 5)  # Max 5 points for steps
        
        # Security/Performance tests are more complex
        if test_case.get('test_type') in ['Security', 'Performance']:
            score += 2
        
        # Negative/Edge cases are more complex
        if test_case.get('category') in ['Negative', 'Edge Case']:
            score += 1
        
        total_score += score
    
    avg_score = total_score / len(test_cases)
    
    # Determine complexity level
    if avg_score >= 8:
        level = "High"
    elif avg_score >= 5:
        level = "Medium"
    else:
        level = "Low"
    
    return {
        "score": round(avg_score, 2),
        "level": level,
        "total_score": total_score,
        "test_count": len(test_cases)
    }


def health_check_all_services() -> Dict[str, Any]:
    """
    Perform health check on all application services
    
    Returns:
        Dictionary with health status of all services
    """
    from app.services.anthropic_service import AnthropicService
    from app.services.export_service import ExportService
    from app.services.validation_service import ValidationService
    
    try:
        anthropic_service = AnthropicService()
        export_service = ExportService()
        validation_service = ValidationService()
        
        return {
            "overall_status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "anthropic": anthropic_service.health_check(),
                "export": export_service.health_check(),
                "validation": validation_service.health_check()
            },
            "environment": validate_environment()
        }
    except Exception as e:
        return {
            "overall_status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }
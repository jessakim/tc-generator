"""
Validation Service - Handles input validation for the application
"""

import re
import logging
from typing import Dict, List, Any, Union
from app.utils.constants import TEST_TYPES, PRIORITY_LEVELS, COMPLEXITY_LEVELS

logger = logging.getLogger(__name__)


class ValidationService:
    """Service for validating user inputs and data"""
    
    def __init__(self):
        """Initialize the validation service"""
        self.max_title_length = 200
        self.max_criteria_length = 5000
        self.min_title_length = 10
        self.min_criteria_length = 20
        logger.info("Validation service initialized")
    
    def validate_input(self, data: Dict[str, Any]) -> Dict[str, Union[bool, str]]:
        """
        Validate the complete input data for test case generation
        
        Args:
            data: Dictionary containing user input data
            
        Returns:
            Dictionary with 'valid' boolean and 'error' message if invalid
        """
        try:
            # Check if data exists
            if not data:
                return {"valid": False, "error": "No input data provided"}
            
            # Validate user story title
            title_validation = self.validate_user_story_title(data.get('user_story_title'))
            if not title_validation['valid']:
                return title_validation
            
            # Validate acceptance criteria
            criteria_validation = self.validate_acceptance_criteria(data.get('acceptance_criteria'))
            if not criteria_validation['valid']:
                return criteria_validation
            
            # Validate test types
            test_types_validation = self.validate_test_types(data.get('test_types'))
            if not test_types_validation['valid']:
                return test_types_validation
            
            # Validate priority level
            priority_validation = self.validate_priority_level(data.get('priority_level'))
            if not priority_validation['valid']:
                return priority_validation
            
            # Validate complexity level
            complexity_validation = self.validate_complexity_level(data.get('complexity'))
            if not complexity_validation['valid']:
                return complexity_validation
            
            # Validate boolean flags
            boolean_validation = self.validate_boolean_flags(data)
            if not boolean_validation['valid']:
                return boolean_validation
            
            logger.info("Input validation passed successfully")
            return {"valid": True, "error": None}
            
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            return {"valid": False, "error": f"Validation error: {str(e)}"}
    
    def validate_user_story_title(self, title: str) -> Dict[str, Union[bool, str]]:
        """
        Validate the user story title
        
        Args:
            title: User story title string
            
        Returns:
            Dictionary with validation result
        """
        if not title:
            return {"valid": False, "error": "User story title is required"}
        
        if not isinstance(title, str):
            return {"valid": False, "error": "User story title must be a string"}
        
        title = title.strip()
        
        if len(title) < self.min_title_length:
            return {"valid": False, "error": f"User story title must be at least {self.min_title_length} characters long"}
        
        if len(title) > self.max_title_length:
            return {"valid": False, "error": f"User story title cannot exceed {self.max_title_length} characters"}
        
        # Check for basic user story format (optional but recommended)
        user_story_pattern = r'(as\s+a|as\s+an)\s+.+\s+(i\s+want|i\s+need|i\s+would\s+like)\s+.+'
        if not re.search(user_story_pattern, title.lower()):
            logger.warning("Title doesn't follow standard user story format")
        
        return {"valid": True, "error": None}
    
    def validate_acceptance_criteria(self, criteria: str) -> Dict[str, Union[bool, str]]:
        """
        Validate the acceptance criteria
        
        Args:
            criteria: Acceptance criteria string
            
        Returns:
            Dictionary with validation result
        """
        if not criteria:
            return {"valid": False, "error": "Acceptance criteria is required"}
        
        if not isinstance(criteria, str):
            return {"valid": False, "error": "Acceptance criteria must be a string"}
        
        criteria = criteria.strip()
        
        if len(criteria) < self.min_criteria_length:
            return {"valid": False, "error": f"Acceptance criteria must be at least {self.min_criteria_length} characters long"}
        
        if len(criteria) > self.max_criteria_length:
            return {"valid": False, "error": f"Acceptance criteria cannot exceed {self.max_criteria_length} characters"}
        
        # Check for Given-When-Then format (optional but recommended)
        if not any(keyword in criteria.lower() for keyword in ['given', 'when', 'then']):
            logger.warning("Acceptance criteria doesn't follow Given-When-Then format")
        
        return {"valid": True, "error": None}
    
    def validate_test_types(self, test_types: List[str]) -> Dict[str, Union[bool, str]]:
        """
        Validate the selected test types
        
        Args:
            test_types: List of selected test types
            
        Returns:
            Dictionary with validation result
        """
        if not test_types:
            return {"valid": False, "error": "At least one test type must be selected"}
        
        if not isinstance(test_types, list):
            return {"valid": False, "error": "Test types must be provided as a list"}
        
        if len(test_types) == 0:
            return {"valid": False, "error": "At least one test type must be selected"}
        
        # Check if all test types are valid
        invalid_types = [t for t in test_types if t not in TEST_TYPES]
        if invalid_types:
            return {"valid": False, "error": f"Invalid test types: {', '.join(invalid_types)}"}
        
        # Check for duplicates
        if len(test_types) != len(set(test_types)):
            return {"valid": False, "error": "Duplicate test types are not allowed"}
        
        return {"valid": True, "error": None}
    
    def validate_priority_level(self, priority: str) -> Dict[str, Union[bool, str]]:
        """
        Validate the priority level
        
        Args:
            priority: Priority level string
            
        Returns:
            Dictionary with validation result
        """
        if not priority:
            # Default to Medium if not provided
            return {"valid": True, "error": None}
        
        if not isinstance(priority, str):
            return {"valid": False, "error": "Priority level must be a string"}
        
        if priority not in PRIORITY_LEVELS:
            return {"valid": False, "error": f"Invalid priority level. Must be one of: {', '.join(PRIORITY_LEVELS)}"}
        
        return {"valid": True, "error": None}
    
    def validate_complexity_level(self, complexity: str) -> Dict[str, Union[bool, str]]:
        """
        Validate the complexity level
        
        Args:
            complexity: Complexity level string
            
        Returns:
            Dictionary with validation result
        """
        if not complexity:
            # Default to Medium if not provided
            return {"valid": True, "error": None}
        
        if not isinstance(complexity, str):
            return {"valid": False, "error": "Complexity level must be a string"}
        
        if complexity not in COMPLEXITY_LEVELS:
            return {"valid": False, "error": f"Invalid complexity level. Must be one of: {', '.join(COMPLEXITY_LEVELS)}"}
        
        return {"valid": True, "error": None}
    
    def validate_boolean_flags(self, data: Dict[str, Any]) -> Dict[str, Union[bool, str]]:
        """
        Validate boolean flags in the input data
        
        Args:
            data: Input data dictionary
            
        Returns:
            Dictionary with validation result
        """
        boolean_fields = ['include_edge_cases', 'include_negative_cases']
        
        for field in boolean_fields:
            value = data.get(field)
            if value is not None and not isinstance(value, bool):
                return {"valid": False, "error": f"{field} must be a boolean value"}
        
        return {"valid": True, "error": None}
    
    def validate_test_case_data(self, test_case: Dict[str, Any]) -> Dict[str, Union[bool, str]]:
        """
        Validate a single test case data structure
        
        Args:
            test_case: Test case dictionary
            
        Returns:
            Dictionary with validation result
        """
        required_fields = [
            'test_id', 'title', 'description', 'test_type', 
            'priority', 'preconditions', 'test_steps', 
            'expected_result'
        ]
        
        # Check required fields
        for field in required_fields:
            if field not in test_case:
                return {"valid": False, "error": f"Missing required field: {field}"}
            
            if not test_case[field]:
                return {"valid": False, "error": f"Field {field} cannot be empty"}
        
        # Validate test_steps is a list
        if not isinstance(test_case.get('test_steps'), list):
            return {"valid": False, "error": "test_steps must be a list"}
        
        # Validate test_type
        if test_case.get('test_type') not in TEST_TYPES:
            return {"valid": False, "error": f"Invalid test_type: {test_case.get('test_type')}"}
        
        # Validate priority
        if test_case.get('priority') not in PRIORITY_LEVELS:
            return {"valid": False, "error": f"Invalid priority: {test_case.get('priority')}"}
        
        return {"valid": True, "error": None}
    
    def validate_export_data(self, test_cases: List[Dict[str, Any]]) -> Dict[str, Union[bool, str]]:
        """
        Validate test cases data for export
        
        Args:
            test_cases: List of test case dictionaries
            
        Returns:
            Dictionary with validation result
        """
        if not test_cases:
            return {"valid": False, "error": "No test cases provided for export"}
        
        if not isinstance(test_cases, list):
            return {"valid": False, "error": "Test cases must be provided as a list"}
        
        # Validate each test case
        for i, test_case in enumerate(test_cases):
            validation_result = self.validate_test_case_data(test_case)
            if not validation_result['valid']:
                return {"valid": False, "error": f"Test case {i+1}: {validation_result['error']}"}
        
        return {"valid": True, "error": None}
    
    def sanitize_input(self, text: str) -> str:
        """
        Sanitize user input to prevent injection attacks
        
        Args:
            text: Input text to sanitize
            
        Returns:
            Sanitized text
        """
        if not isinstance(text, str):
            return str(text)
        
        # Remove potentially dangerous characters
        text = text.strip()
        
        # Remove or escape HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text
    
    def validate_file_upload(self, file_data: bytes, filename: str) -> Dict[str, Union[bool, str]]:
        """
        Validate uploaded file data
        
        Args:
            file_data: File content as bytes
            filename: Original filename
            
        Returns:
            Dictionary with validation result
        """
        max_file_size = 5 * 1024 * 1024  # 5MB
        allowed_extensions = ['.json', '.csv', '.txt']
        
        # Check file size
        if len(file_data) > max_file_size:
            return {"valid": False, "error": "File size exceeds 5MB limit"}
        
        # Check file extension
        file_ext = filename.lower().split('.')[-1] if '.' in filename else ''
        if f'.{file_ext}' not in allowed_extensions:
            return {"valid": False, "error": f"File type not allowed. Supported: {', '.join(allowed_extensions)}"}
        
        return {"valid": True, "error": None}
    
    def health_check(self) -> Dict[str, Any]:
        """Check if the validation service is working"""
        try:
            # Test validation with dummy data
            test_data = {
                "user_story_title": "As a user, I want to test validation",
                "acceptance_criteria": "Given I provide valid data, when I validate, then it should pass",
                "test_types": ["Functional"],
                "priority_level": "Medium",
                "complexity": "Medium"
            }
            
            result = self.validate_input(test_data)
            
            return {
                "status": "healthy" if result['valid'] else "unhealthy",
                "test_validation": result
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
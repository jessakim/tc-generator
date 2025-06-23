"""
Anthropic Service - Simplified version for compatibility
"""

import os
import json
import logging
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class AnthropicService:
    """Service for interacting with Anthropic's Claude API using direct HTTP requests"""
    
    def __init__(self):
        """Initialize the Anthropic service"""
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.model = "claude-3-5-sonnet-20241022"
        self.headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01"
        }
        logger.info("Anthropic service initialized successfully")
    
    def generate_test_cases(self, 
                          user_story_title: str,
                          acceptance_criteria: str,
                          test_types: List[str],
                          include_edge_cases: bool = False,
                          include_negative_cases: bool = False,
                          priority_level: str = "Medium",
                          complexity: str = "Medium") -> Dict[str, Any]:
        """
        Generate test cases using Claude AI via HTTP requests
        
        Args:
            user_story_title: The user story title
            acceptance_criteria: Detailed acceptance criteria
            test_types: List of test types to generate
            include_edge_cases: Whether to include edge case scenarios
            include_negative_cases: Whether to include negative test cases
            priority_level: Overall priority level
            complexity: Complexity level for test case detail
            
        Returns:
            Dictionary containing generated test cases or error information
        """
        try:
            logger.info(f"Generating test cases for story: {user_story_title[:50]}...")
            
            # Build the prompt
            prompt = self._build_prompt(
                user_story_title, acceptance_criteria, test_types,
                include_edge_cases, include_negative_cases, priority_level, complexity
            )
            
            # Prepare request payload
            payload = {
                "model": self.model,
                "max_tokens": 4000,
                "temperature": 0.3,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            # Make HTTP request
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code != 200:
                error_msg = f"API request failed: {response.status_code} - {response.text}"
                logger.error(error_msg)
                return {"error": error_msg}
            
            response_data = response.json()
            
            # Extract the text content
            if "content" in response_data and len(response_data["content"]) > 0:
                response_text = response_data["content"][0]["text"]
            else:
                return {"error": "No content in API response"}
            
            # Parse the response
            result = self._parse_response(response_text)
            
            if result.get('success'):
                logger.info(f"Successfully generated {result.get('total_count', 0)} test cases")
            else:
                logger.error(f"Failed to parse Claude response: {result.get('error')}")
            
            return result
            
        except requests.exceptions.RequestException as e:
            error_msg = f"HTTP request error: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg}
        except Exception as e:
            error_msg = f"Error generating test cases: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg}
    
    def _build_prompt(self, title: str, criteria: str, test_types: List[str], 
                     edge_cases: bool, negative_cases: bool, priority: str, complexity: str) -> str:
        """Build the prompt for Claude AI"""
        
        # Adjust detail level based on complexity
        detail_instructions = {
            "Simple": "Generate concise test cases with basic steps.",
            "Medium": "Generate detailed test cases with comprehensive steps and validation.",
            "Complex": "Generate very detailed test cases with extensive steps, multiple validation points, and thorough error handling."
        }
        
        prompt = f"""You are an expert QA engineer with extensive experience in test case design. Generate comprehensive test cases for the following user story:

**User Story Title:** {title}

**Acceptance Criteria:**
{criteria}

**Test Generation Requirements:**
- Test Types: {', '.join(test_types)}
- Include Edge Cases: {'Yes' if edge_cases else 'No'}
- Include Negative Test Cases: {'Yes' if negative_cases else 'No'}
- Priority Level: {priority}
- Complexity Level: {complexity}

**Detail Level:** {detail_instructions.get(complexity, detail_instructions['Medium'])}

**Instructions:**
1. Generate 8-15 test cases that thoroughly cover the specified test types
2. Each test case MUST include all these fields:
   - test_id: Unique identifier (TC001, TC002, etc.)
   - title: Clear, descriptive test case title
   - description: Brief description of what this test validates
   - test_type: One of the requested test types
   - priority: High/Medium/Low based on risk and importance
   - preconditions: Prerequisites before executing the test
   - test_steps: Array of detailed, actionable steps
   - expected_result: Clear expected outcome
   - test_data: Sample data needed (if applicable)
   - category: Positive/Negative/Edge Case

3. **Quality Requirements:**
   - Test cases should be specific, measurable, and actionable
   - Cover both happy path and alternative scenarios as requested
   - Include data validation and boundary testing where applicable
   - Consider security implications for all test types
   - Ensure accessibility compliance where relevant
   - Include performance considerations when appropriate

4. **Test Case Distribution:**
   - Prioritize High-priority test cases for core functionality
   - Include Medium-priority for important but non-critical features
   - Add Low-priority for nice-to-have functionality
   - Balance positive, negative, and edge cases appropriately

**CRITICAL: Respond ONLY with valid JSON in this exact format:**

```json
[
    {{
        "test_id": "TC001",
        "title": "Descriptive test case title",
        "description": "Brief description of what this test validates",
        "test_type": "Functional",
        "priority": "High",
        "preconditions": "Prerequisites before executing the test",
        "test_steps": [
            "Step 1: Specific action to perform",
            "Step 2: Next specific action",
            "Step 3: Final verification step"
        ],
        "expected_result": "Clear, specific expected outcome",
        "test_data": "Sample data needed for testing (if applicable)",
        "category": "Positive"
    }},
    {{
        "test_id": "TC002",
        "title": "Another test case title",
        "description": "Description for second test case",
        "test_type": "Security",
        "priority": "Medium",
        "preconditions": "Different preconditions",
        "test_steps": [
            "Step 1: Different action",
            "Step 2: Security-focused validation"
        ],
        "expected_result": "Security-related expected result",
        "test_data": "Security test data if needed",
        "category": "Negative"
    }}
]
```

Generate comprehensive test cases now. Ensure all JSON is properly formatted and valid."""
        
        return prompt
    
    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Claude's response and extract test cases"""
        try:
            # Find the JSON array in the response
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            
            if start_idx == -1 or end_idx == 0:
                return {"error": "No JSON array found in response"}
            
            json_str = response_text[start_idx:end_idx]
            test_cases = json.loads(json_str)
            
            # Validate and enhance test cases
            enhanced_test_cases = []
            for i, test_case in enumerate(test_cases):
                # Ensure required fields exist
                if not test_case.get('test_id'):
                    test_case['test_id'] = f"TC{str(i+1).zfill(3)}"
                
                # Add generation metadata
                test_case['generated_at'] = datetime.now().isoformat()
                
                # Validate test_steps is a list
                if isinstance(test_case.get('test_steps'), str):
                    test_case['test_steps'] = [test_case['test_steps']]
                elif not isinstance(test_case.get('test_steps'), list):
                    test_case['test_steps'] = ["Invalid test steps format"]
                
                # Ensure all required fields have default values
                test_case.setdefault('title', f"Test Case {i+1}")
                test_case.setdefault('description', "No description provided")
                test_case.setdefault('test_type', "Functional")
                test_case.setdefault('priority', "Medium")
                test_case.setdefault('preconditions', "No specific preconditions")
                test_case.setdefault('expected_result', "No expected result specified")
                test_case.setdefault('test_data', "No test data required")
                test_case.setdefault('category', "Positive")
                
                enhanced_test_cases.append(test_case)
            
            return {
                "success": True,
                "test_cases": enhanced_test_cases,
                "total_count": len(enhanced_test_cases),
                "generated_at": datetime.now().isoformat(),
                "model_used": self.model
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            return {"error": f"Invalid JSON in response: {str(e)}"}
        except Exception as e:
            logger.error(f"Response parsing error: {str(e)}")
            return {"error": f"Error parsing response: {str(e)}"}
    
    def health_check(self) -> Dict[str, Any]:
        """Check if the Anthropic service is working"""
        try:
            # Make a simple API call to test connectivity
            payload = {
                "model": self.model,
                "max_tokens": 10,
                "messages": [{"role": "user", "content": "Hello"}]
            }
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            return {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "model": self.model,
                "status_code": response.status_code
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
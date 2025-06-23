#!/usr/bin/env python3
"""
AI Test Case Generator - Simple Deployment Version
Single file app that works on any platform
"""

import os
import json
import logging
import tempfile
import csv
import io
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-secret-key-for-demo')

# Enable CORS
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Configuration
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"

@app.route('/')
def index():
    """Main page with test types data"""
    # Provide test types data to template
    test_types = [
        {'value': 'Functional', 'label': 'Functional Testing'},
        {'value': 'Integration', 'label': 'Integration Testing'},
        {'value': 'Security', 'label': 'Security Testing'},
        {'value': 'Performance', 'label': 'Performance Testing'},
        {'value': 'Usability', 'label': 'Usability Testing'},
        {'value': 'Accessibility', 'label': 'Accessibility Testing'},
        {'value': 'API', 'label': 'API Testing'},
        {'value': 'Database', 'label': 'Database Testing'},
        {'value': 'Mobile', 'label': 'Mobile Testing'},
        {'value': 'Cross-browser', 'label': 'Cross-browser Testing'},
        {'value': 'UAT', 'label': 'User Acceptance Testing'},
        {'value': 'Regression', 'label': 'Regression Testing'}
    ]
    
    return render_template('index.html', test_types=test_types)

@app.route('/api/test-types')
def get_test_types():
    """Get available test types"""
    test_types = [
        {'value': 'Functional', 'label': 'Functional Testing'},
        {'value': 'Integration', 'label': 'Integration Testing'},
        {'value': 'Security', 'label': 'Security Testing'},
        {'value': 'Performance', 'label': 'Performance Testing'},
        {'value': 'Usability', 'label': 'Usability Testing'},
        {'value': 'Accessibility', 'label': 'Accessibility Testing'},
        {'value': 'API', 'label': 'API Testing'},
        {'value': 'Database', 'label': 'Database Testing'},
        {'value': 'Mobile', 'label': 'Mobile Testing'},
        {'value': 'Cross-browser', 'label': 'Cross-browser Testing'},
        {'value': 'UAT', 'label': 'User Acceptance Testing'},
        {'value': 'Regression', 'label': 'Regression Testing'}
    ]
    return jsonify(test_types)

@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'has_api_key': bool(ANTHROPIC_API_KEY)
    })

@app.route('/api/generate', methods=['POST'])
def generate_test_cases():
    """Generate test cases using Anthropic Claude"""
    try:
        # Check API key
        if not ANTHROPIC_API_KEY:
            return jsonify({
                'error': 'ANTHROPIC_API_KEY environment variable not set'
            }), 500

        # Get request data
        data = request.get_json() or {}
        
        # Extract parameters
        user_story_title = data.get('user_story_title', '').strip()
        acceptance_criteria = data.get('acceptance_criteria', '').strip()
        test_types = data.get('test_types', [])
        include_edge_cases = data.get('include_edge_cases', False)
        include_negative_cases = data.get('include_negative_cases', False)
        priority_level = data.get('priority_level', 'Medium')
        complexity = data.get('complexity', 'Medium')

        # Validate inputs
        if not user_story_title:
            return jsonify({'error': 'User story title is required'}), 400
        if not acceptance_criteria:
            return jsonify({'error': 'Acceptance criteria is required'}), 400
        if not test_types:
            return jsonify({'error': 'At least one test type must be selected'}), 400

        # Build prompt
        prompt = build_claude_prompt(
            user_story_title, acceptance_criteria, test_types,
            include_edge_cases, include_negative_cases, priority_level, complexity
        )

        # Call Anthropic API
        headers = {
            'x-api-key': ANTHROPIC_API_KEY,
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01'
        }

        payload = {
            'model': 'claude-3-5-sonnet-20241022',
            'max_tokens': 4000,
            'messages': [{'role': 'user', 'content': prompt}]
        }

        logger.info("Calling Anthropic API...")
        response = requests.post(ANTHROPIC_API_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code != 200:
            logger.error(f"API error: {response.status_code} - {response.text}")
            return jsonify({'error': f'AI service error: {response.status_code}'}), 500

        # Parse response
        response_data = response.json()
        claude_response = response_data['content'][0]['text']
        
        # Extract test cases
        result = parse_claude_response(claude_response)
        
        if result.get('success'):
            logger.info(f"Generated {result.get('total_count', 0)} test cases")
            return jsonify(result)
        else:
            return jsonify({'error': result.get('error', 'Failed to parse response')}), 400

    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timeout - please try again'}), 408
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {str(e)}")
        return jsonify({'error': 'Failed to connect to AI service'}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/export/<format>')
def export_test_cases(format):
    """Export test cases"""
    try:
        # Get test cases data from query parameter
        test_cases_data = request.args.get('data')
        if not test_cases_data:
            return jsonify({'error': 'No test cases data provided'}), 400
        
        # Validate format
        if format not in ['csv', 'json']:
            return jsonify({'error': 'Format must be csv or json'}), 400
        
        # Parse test cases
        try:
            test_cases = json.loads(test_cases_data)
        except json.JSONDecodeError:
            return jsonify({'error': 'Invalid test cases data'}), 400
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'test_cases_{timestamp}.{format}'
        
        if format == 'csv':
            # Create CSV
            output = io.StringIO()
            fieldnames = [
                'test_id', 'title', 'description', 'test_type', 'priority',
                'preconditions', 'test_steps', 'expected_result', 'test_data', 'category'
            ]
            
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            
            for test_case in test_cases:
                # Handle test_steps array
                test_steps = test_case.get('test_steps', [])
                if isinstance(test_steps, list):
                    test_steps_str = '; '.join(test_steps)
                else:
                    test_steps_str = str(test_steps)
                
                writer.writerow({
                    'test_id': test_case.get('test_id', ''),
                    'title': test_case.get('title', ''),
                    'description': test_case.get('description', ''),
                    'test_type': test_case.get('test_type', ''),
                    'priority': test_case.get('priority', ''),
                    'preconditions': test_case.get('preconditions', ''),
                    'test_steps': test_steps_str,
                    'expected_result': test_case.get('expected_result', ''),
                    'test_data': test_case.get('test_data', ''),
                    'category': test_case.get('category', '')
                })
            
            csv_data = output.getvalue()
            output.close()
            
            return app.response_class(
                csv_data,
                mimetype='text/csv',
                headers={'Content-Disposition': f'attachment; filename={filename}'}
            )
            
        else:  # JSON
            export_data = {
                'exported_at': datetime.now().isoformat(),
                'total_test_cases': len(test_cases),
                'test_cases': test_cases
            }
            
            return app.response_class(
                json.dumps(export_data, indent=2),
                mimetype='application/json',
                headers={'Content-Disposition': f'attachment; filename={filename}'}
            )
            
    except Exception as e:
        logger.error(f"Export failed: {str(e)}")
        return jsonify({'error': f'Export failed: {str(e)}'}), 500

def build_claude_prompt(title, criteria, test_types, edge_cases, negative_cases, priority, complexity):
    """Build the prompt for Claude"""
    
    detail_levels = {
        "Simple": "Generate concise test cases with basic steps.",
        "Medium": "Generate detailed test cases with comprehensive steps.",
        "Complex": "Generate very detailed test cases with extensive validation."
    }
    
    prompt = f"""You are an expert QA engineer. Generate comprehensive test cases for this user story:

**User Story:** {title}

**Acceptance Criteria:**
{criteria}

**Requirements:**
- Test Types: {', '.join(test_types)}
- Include Edge Cases: {'Yes' if edge_cases else 'No'}
- Include Negative Cases: {'Yes' if negative_cases else 'No'}
- Priority: {priority}
- Complexity: {complexity}

{detail_levels.get(complexity, detail_levels['Medium'])}

Generate 8-12 test cases. Respond ONLY with valid JSON in this format:

[
    {{
        "test_id": "TC001",
        "title": "Clear test case title",
        "description": "What this test validates",
        "test_type": "Functional",
        "priority": "High",
        "preconditions": "Prerequisites",
        "test_steps": [
            "Step 1: Action to perform",
            "Step 2: Next action",
            "Step 3: Verification"
        ],
        "expected_result": "Expected outcome",
        "test_data": "Required test data",
        "category": "Positive"
    }}
]

Return only the JSON array, no other text."""
    
    return prompt

def parse_claude_response(response_text):
    """Parse Claude's response"""
    try:
        # Find JSON array
        start_idx = response_text.find('[')
        end_idx = response_text.rfind(']') + 1
        
        if start_idx == -1 or end_idx == 0:
            return {"error": "No JSON array found in response"}
        
        json_str = response_text[start_idx:end_idx]
        test_cases = json.loads(json_str)
        
        # Validate and enhance
        enhanced_test_cases = []
        for i, test_case in enumerate(test_cases):
            # Ensure required fields
            test_case.setdefault('test_id', f"TC{str(i+1).zfill(3)}")
            test_case.setdefault('title', f"Test Case {i+1}")
            test_case.setdefault('description', "No description")
            test_case.setdefault('test_type', "Functional")
            test_case.setdefault('priority', "Medium")
            test_case.setdefault('preconditions', "None")
            test_case.setdefault('expected_result', "Verify functionality")
            test_case.setdefault('test_data', "N/A")
            test_case.setdefault('category', "Positive")
            
            # Ensure test_steps is a list
            if not isinstance(test_case.get('test_steps'), list):
                test_case['test_steps'] = ["No steps provided"]
            
            test_case['generated_at'] = datetime.now().isoformat()
            enhanced_test_cases.append(test_case)
        
        return {
            "success": True,
            "test_cases": enhanced_test_cases,
            "total_count": len(enhanced_test_cases),
            "generated_at": datetime.now().isoformat(),
            "model_used": "Claude 3.5 Sonnet"
        }
        
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON: {str(e)}"}
    except Exception as e:
        return {"error": f"Parsing error: {str(e)}"}

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print("🚀 Starting AI Test Case Generator...")
    print(f"📍 Port: {port}")
    print(f"🔑 API Key configured: {bool(ANTHROPIC_API_KEY)}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)

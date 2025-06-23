"""
Export Service - Handles exporting test cases to different formats
"""

import csv
import json
import io
import logging
from datetime import datetime
from typing import List, Dict, Any
from flask import send_file

logger = logging.getLogger(__name__)


class ExportService:
    """Service for exporting test cases to various formats"""
    
    def __init__(self):
        """Initialize the export service"""
        logger.info("Export service initialized")
    
    def export_to_csv(self, test_cases: List[Dict[str, Any]]) -> Any:
        """
        Export test cases to CSV format
        
        Args:
            test_cases: List of test case dictionaries
            
        Returns:
            Flask send_file response with CSV attachment
        """
        try:
            if not test_cases:
                raise ValueError("No test cases provided for export")
            
            logger.info(f"Exporting {len(test_cases)} test cases to CSV")
            
            # Create in-memory string buffer
            output = io.StringIO()
            
            # Define CSV fieldnames
            fieldnames = [
                'test_id', 'title', 'description', 'test_type', 'priority',
                'preconditions', 'test_steps', 'expected_result', 'test_data', 
                'category', 'generated_at'
            ]
            
            # Create CSV writer
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            
            # Write test cases
            for test_case in test_cases:
                # Prepare row data
                row = {}
                for field in fieldnames:
                    value = test_case.get(field, '')
                    
                    # Convert lists to pipe-separated strings
                    if isinstance(value, list):
                        if field == 'test_steps':
                            value = ' | '.join(str(step) for step in value)
                        else:
                            value = ', '.join(str(item) for item in value)
                    
                    # Ensure value is string
                    row[field] = str(value) if value is not None else ''
                
                writer.writerow(row)
            
            # Convert to bytes
            output.seek(0)
            csv_data = output.getvalue().encode('utf-8')
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'test_cases_{timestamp}.csv'
            
            logger.info(f"CSV export completed: {filename}")
            
            return send_file(
                io.BytesIO(csv_data),
                mimetype='text/csv',
                as_attachment=True,
                download_name=filename
            )
            
        except Exception as e:
            logger.error(f"CSV export failed: {str(e)}")
            raise
    
    def export_to_json(self, test_cases: List[Dict[str, Any]]) -> Any:
        """
        Export test cases to JSON format
        
        Args:
            test_cases: List of test case dictionaries
            
        Returns:
            Flask send_file response with JSON attachment
        """
        try:
            if not test_cases:
                raise ValueError("No test cases provided for export")
            
            logger.info(f"Exporting {len(test_cases)} test cases to JSON")
            
            # Create export data structure
            export_data = {
                "metadata": {
                    "export_timestamp": datetime.now().isoformat(),
                    "total_test_cases": len(test_cases),
                    "export_format": "json",
                    "version": "1.0.0"
                },
                "test_cases": test_cases
            }
            
            # Convert to JSON with pretty formatting
            json_data = json.dumps(export_data, indent=2, ensure_ascii=False)
            json_bytes = json_data.encode('utf-8')
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'test_cases_{timestamp}.json'
            
            logger.info(f"JSON export completed: {filename}")
            
            return send_file(
                io.BytesIO(json_bytes),
                mimetype='application/json',
                as_attachment=True,
                download_name=filename
            )
            
        except Exception as e:
            logger.error(f"JSON export failed: {str(e)}")
            raise
    
    def export_to_excel(self, test_cases: List[Dict[str, Any]]) -> Any:
        """
        Export test cases to Excel format (future enhancement)
        
        Args:
            test_cases: List of test case dictionaries
            
        Returns:
            Flask send_file response with Excel attachment
        """
        # TODO: Implement Excel export using openpyxl
        # This would require adding openpyxl to requirements.txt
        raise NotImplementedError("Excel export not yet implemented")
    
    def export_to_jira_csv(self, test_cases: List[Dict[str, Any]]) -> Any:
        """
        Export test cases in Jira-compatible CSV format
        
        Args:
            test_cases: List of test case dictionaries
            
        Returns:
            Flask send_file response with Jira CSV attachment
        """
        try:
            if not test_cases:
                raise ValueError("No test cases provided for export")
            
            logger.info(f"Exporting {len(test_cases)} test cases to Jira CSV format")
            
            # Create in-memory string buffer
            output = io.StringIO()
            
            # Jira-compatible fieldnames
            fieldnames = [
                'Summary', 'Issue Type', 'Priority', 'Description',
                'Test Steps', 'Expected Results', 'Labels'
            ]
            
            # Create CSV writer
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            
            # Convert test cases to Jira format
            for test_case in test_cases:
                # Format test steps for Jira
                test_steps_formatted = ""
                if isinstance(test_case.get('test_steps'), list):
                    for i, step in enumerate(test_case['test_steps'], 1):
                        test_steps_formatted += f"{i}. {step}\n"
                else:
                    test_steps_formatted = str(test_case.get('test_steps', ''))
                
                # Create Jira row
                jira_row = {
                    'Summary': f"{test_case.get('test_id', '')} - {test_case.get('title', '')}",
                    'Issue Type': 'Test',
                    'Priority': test_case.get('priority', 'Medium'),
                    'Description': f"*Preconditions:* {test_case.get('preconditions', '')}\n\n*Test Data:* {test_case.get('test_data', '')}",
                    'Test Steps': test_steps_formatted.strip(),
                    'Expected Results': test_case.get('expected_result', ''),
                    'Labels': f"{test_case.get('test_type', '').lower()},{test_case.get('category', '').lower()}"
                }
                
                writer.writerow(jira_row)
            
            # Convert to bytes
            output.seek(0)
            csv_data = output.getvalue().encode('utf-8')
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'jira_test_cases_{timestamp}.csv'
            
            logger.info(f"Jira CSV export completed: {filename}")
            
            return send_file(
                io.BytesIO(csv_data),
                mimetype='text/csv',
                as_attachment=True,
                download_name=filename
            )
            
        except Exception as e:
            logger.error(f"Jira CSV export failed: {str(e)}")
            raise
    
    def get_export_statistics(self, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate export statistics for test cases
        
        Args:
            test_cases: List of test case dictionaries
            
        Returns:
            Dictionary containing export statistics
        """
        try:
            if not test_cases:
                return {"total": 0}
            
            # Count by priority
            priority_counts = {}
            type_counts = {}
            category_counts = {}
            
            for test_case in test_cases:
                # Count priorities
                priority = test_case.get('priority', 'Unknown')
                priority_counts[priority] = priority_counts.get(priority, 0) + 1
                
                # Count test types
                test_type = test_case.get('test_type', 'Unknown')
                type_counts[test_type] = type_counts.get(test_type, 0) + 1
                
                # Count categories
                category = test_case.get('category', 'Unknown')
                category_counts[category] = category_counts.get(category, 0) + 1
            
            return {
                "total": len(test_cases),
                "by_priority": priority_counts,
                "by_type": type_counts,
                "by_category": category_counts,
                "estimated_execution_time_hours": len(test_cases) * 0.5  # Estimate 30 min per test case
            }
            
        except Exception as e:
            logger.error(f"Failed to generate export statistics: {str(e)}")
            return {"error": str(e)}
    
    def health_check(self) -> Dict[str, Any]:
        """Check if the export service is working"""
        try:
            # Test with dummy data
            dummy_test_case = [{
                "test_id": "TC001",
                "title": "Health Check Test",
                "description": "Test case for health check",
                "test_type": "Functional",
                "priority": "Low",
                "preconditions": "None",
                "test_steps": ["Check health"],
                "expected_result": "Healthy",
                "test_data": "None",
                "category": "Positive"
            }]
            
            stats = self.get_export_statistics(dummy_test_case)
            
            return {
                "status": "healthy",
                "supported_formats": ["csv", "json", "jira_csv"],
                "test_stats": stats
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
"""
Test case data model
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class TestCase:
    """Test case data model"""
    test_id: str
    title: str
    description: str
    test_type: str
    priority: str
    preconditions: str
    test_steps: List[str]
    expected_result: str
    test_data: Optional[str] = None
    category: Optional[str] = "Positive"
    generated_at: Optional[str] = None
    
    def __post_init__(self):
        if self.generated_at is None:
            self.generated_at = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'test_id': self.test_id,
            'title': self.title,
            'description': self.description,
            'test_type': self.test_type,
            'priority': self.priority,
            'preconditions': self.preconditions,
            'test_steps': self.test_steps,
            'expected_result': self.expected_result,
            'test_data': self.test_data,
            'category': self.category,
            'generated_at': self.generated_at
        }
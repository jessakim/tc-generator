"""
User story data model
"""

from dataclasses import dataclass
from typing import List


@dataclass
class UserStory:
    """User story data model"""
    title: str
    acceptance_criteria: str
    test_types: List[str]
    include_edge_cases: bool = False
    include_negative_cases: bool = False
    priority_level: str = "Medium"
    complexity: str = "Medium"
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'title': self.title,
            'acceptance_criteria': self.acceptance_criteria,
            'test_types': self.test_types,
            'include_edge_cases': self.include_edge_cases,
            'include_negative_cases': self.include_negative_cases,
            'priority_level': self.priority_level,
            'complexity': self.complexity
        }
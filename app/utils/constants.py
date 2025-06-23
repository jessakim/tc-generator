"""Application constants and configuration values."""

# Test types available for generation
TEST_TYPES = [
    'Functional',
    'Security', 
    'UAT',
    'Performance',
    'Integration',
    'Usability',
    'Accessibility'
]

# Priority levels
PRIORITY_LEVELS = ['Low', 'Medium', 'High']

# Complexity levels  
COMPLEXITY_LEVELS = ['Simple', 'Medium', 'Complex']

# Export formats
EXPORT_FORMATS = ['json', 'csv']

# Maximum input lengths
MAX_TITLE_LENGTH = 200
MAX_CRITERIA_LENGTH = 5000

# Rate limiting
DEFAULT_RATE_LIMIT = "60 per minute"

"""
Age calculation and age-appropriate content filtering utilities
"""
from datetime import date, datetime
from typing import Dict, List, Optional, Tuple

def calculate_age(date_of_birth: date) -> int:
    """
    Calculate age in years from date of birth
    
    Args:
        date_of_birth: Date of birth
        
    Returns:
        Current age in years
    """
    today = date.today()
    age = today.year - date_of_birth.year
    
    # Adjust if birthday hasn't occurred this year yet
    if (today.month, today.day) < (date_of_birth.month, date_of_birth.day):
        age -= 1
        
    return age

def get_age_category(age: int) -> str:
    """
    Get age category for the person
    
    Args:
        age: Age in years
        
    Returns:
        Age category: 'child', 'teenager', 'young_adult', 'adult', 'senior'
    """
    if age < 13:
        return 'child'
    elif age < 18:
        return 'teenager'
    elif age < 20:
        return 'young_adult'
    else:  # 20 and above
        return 'adult'

def get_allowed_categories(age: int) -> List[str]:
    """
    Get list of prediction categories that are appropriate for the given age
    
    Args:
        age: Age in years
        
    Returns:
        List of allowed category names
    """
    # Anyone 20 or older: No restrictions, all categories allowed
    if age >= 20:
        return ['general', 'health', 'parents', 'education', 'career', 'marriage', 'wealth', 'children', 'custom']
    
    # Children (0-12): Education, parents, health, general development
    elif age < 13:
        return ['general', 'health', 'parents', 'education', 'custom']
    
    # Teenagers (13-17): Education, parents, health, early career guidance
    elif age < 18:
        return ['general', 'health', 'parents', 'education', 'career', 'custom']
    
    # Young adults (18-19): Most categories except children
    else:  # age is 18 or 19
        return ['general', 'health', 'parents', 'education', 'career', 'marriage', 'wealth', 'custom']

def is_category_allowed(category: str, age: int) -> bool:
    """
    Check if a prediction category is appropriate for the given age
    
    Args:
        category: Category to check
        age: Age in years
        
    Returns:
        True if category is allowed, False otherwise
    """
    allowed = get_allowed_categories(age)
    return category in allowed

def get_age_appropriate_message(category: str, age: int) -> Optional[str]:
    """
    Get a message explaining why a category is not appropriate for the given age
    
    Args:
        category: Requested category
        age: Age in years
        
    Returns:
        Message string if category is not appropriate, None otherwise
    """
    if is_category_allowed(category, age):
        return None
    
    age_category = get_age_category(age)
    
    messages = {
        'child': {
            'marriage': f"Marriage predictions are not relevant for a {age}-year-old child. Focus is on education, health, and overall development.",
            'career': f"Career predictions are not appropriate for a {age}-year-old child. Focus should be on education and learning.",
            'wealth': f"Wealth and financial predictions are not relevant for a {age}-year-old child.",
            'children': f"This topic is not appropriate for a {age}-year-old child."
        },
        'teenager': {
            'marriage': f"Marriage predictions are not appropriate for a {age}-year-old teenager. Focus is on education and personal development.",
            'wealth': f"Detailed wealth predictions are not relevant for a {age}-year-old teenager. Focus should be on education and future career planning.",
            'children': f"This topic is not appropriate for a {age}-year-old teenager."
        },
        'young_adult': {
            'children': f"Children predictions may not be relevant yet for a {age}-year-old. This category is available from age 20 onwards."
        }
    }
    
    return messages.get(age_category, {}).get(category, 
        f"The category '{category}' may not be the most relevant for a {age}-year-old person.")

def get_age_context_for_prompt(age: int, name: str) -> str:
    """
    Get age-appropriate context to include in AI prompts
    
    Args:
        age: Age in years
        name: Person's name
        
    Returns:
        Context string to include in prompt
    """
    age_category = get_age_category(age)
    
    contexts = {
        'child': f"{name} is {age} years old (a child). Focus predictions on education, learning, health, family relationships, and overall development. Avoid topics like marriage, career, or financial planning.",
        'teenager': f"{name} is {age} years old (a teenager). Focus on education, personal growth, health, and early career/educational guidance. Avoid marriage or wealth accumulation topics.",
        'young_adult': f"{name} is {age} years old (a young adult). Focus on career development, education completion, health, and relationships. Career establishment and personal development are key themes.",
        'adult': f"{name} is {age} years old. Provide comprehensive predictions covering all life areas including career, relationships, health, wealth, and family matters."
    }
    
    return contexts.get(age_category, f"{name} is {age} years old.")

def filter_prediction_topics(age: int) -> List[str]:
    """
    Get list of topics that should be covered in comprehensive predictions
    
    Args:
        age: Age in years
        
    Returns:
        List of topics appropriate for the age
    """
    age_category = get_age_category(age)
    
    topics = {
        'child': [
            'Overall development and personality',
            'Education and learning abilities',
            'Health and vitality',
            'Relationship with parents and family',
            'Natural talents and interests'
        ],
        'teenager': [
            'Education and academic success',
            'Personality development',
            'Health patterns',
            'Relationship with family',
            'Early career interests and guidance',
            'Suitable fields of study'
        ],
        'young_adult': [
            'Career path and professional direction',
            'Education completion',
            'Health patterns',
            'Relationships and marriage prospects',
            'Financial planning basics',
            'Personal development'
        ],
        'adult': [
            'Career and profession',
            'Marriage and relationships',
            'Health patterns',
            'Wealth and finances',
            'Children and family',
            'Overall life direction'
        ]
    }
    
    return topics.get(age_category, topics['adult'])

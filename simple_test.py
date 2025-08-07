#!/usr/bin/env python3
"""
Simple test to verify predefined response logic
"""

from predefined_responses import predefined_manager

def test_logic():
    """Test the predefined response logic"""
    
    question = "How can I advance from Senior Developer to Tech Lead?"
    
    # Test 1: Default preferences
    default_prefs = {
        'interests': ['Technology', 'Leadership'],
        'careerLevel': 'Entry Level',  # Frontend format
        'goal': 'advancement',
        'industry': 'All Industries',
        'location': 'Remote',
        'experience': '3-5 years'
    }
    
    print("Test 1: Default preferences")
    should_use, question_type = predefined_manager.should_use_predefined_response(question, default_prefs)
    print(f"Should use predefined: {should_use}")
    print(f"Question type: {question_type}")
    
    # Test 2: LinkedIn connected
    linkedin_prefs = {
        'interests': ['Engineering', 'Technology', 'Leadership'],
        'career_level': 'Entry Level',
        'goal': 'advancement',
        'industry': 'Manufacturing',
        'location': 'On-site',
        'experience': '1-3 years',
        'linkedin_connected': True
    }
    
    print("\nTest 2: LinkedIn connected")
    should_use, question_type = predefined_manager.should_use_predefined_response(question, linkedin_prefs)
    print(f"Should use predefined: {should_use}")
    print(f"Question type: {question_type}")
    
    # Test 3: Modified preferences
    modified_prefs = {
        'interests': ['Marketing', 'Leadership'],
        'careerLevel': 'Senior',
        'goal': 'skill',
        'industry': 'Marketing',
        'location': 'Hybrid',
        'experience': '6-10 years'
    }
    
    print("\nTest 3: Modified preferences")
    should_use, question_type = predefined_manager.should_use_predefined_response(question, modified_prefs)
    print(f"Should use predefined: {should_use}")
    print(f"Question type: {question_type}")

if __name__ == "__main__":
    test_logic()

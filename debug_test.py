#!/usr/bin/env python3
"""
Debug test to see what's happening with response generation
"""

from predefined_responses import predefined_manager

def debug_test():
    """Debug the response generation"""
    
    question = "How can I advance from Senior Developer to Tech Lead?"
    
    # Test with default preferences
    default_prefs = {
        'interests': ['Technology', 'Leadership'],
        'careerLevel': 'Entry Level',
        'goal': 'advancement',
        'industry': 'All Industries',
        'location': 'Remote',
        'experience': '3-5 years'
    }
    
    print("Testing with default preferences:")
    print(f"Preferences: {default_prefs}")
    
    # Check if predefined response should be used
    should_use, question_type = predefined_manager.should_use_predefined_response(question, default_prefs)
    print(f"Should use predefined: {should_use}")
    print(f"Question type: {question_type}")
    
    if should_use:
        # Get the actual response
        response = predefined_manager.get_personality_aware_response(question_type, default_prefs)
        print(f"Response preview: {response[:100]}...")
        print(f"Is predefined: {'Perfect! I can see you\'re interested in Technology' in response}")
    else:
        print("Using LLM response")

if __name__ == "__main__":
    debug_test()

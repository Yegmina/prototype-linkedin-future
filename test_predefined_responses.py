#!/usr/bin/env python3
"""
Test script for predefined responses functionality
"""

from predefined_responses import predefined_manager

def test_predefined_responses():
    """Test the predefined responses with default preferences"""
    
    # Default preferences (same as in the system)
    default_preferences = {
        'interests': ['Technology', 'Leadership'],
        'career_level': 'Entry Level',
        'goal': 'advancement',
        'industry': 'All Industries',
        'location': 'Remote',
        'experience': '3-5 years'
    }
    
    # Test questions
    test_questions = [
        "How can I advance from Senior Developer to Tech Lead?",
        "What skills do I need for a Director position?",
        "Show me remote job opportunities in tech",
        "What workshops are available for leadership skills?",
        "This is a random question that should not match"
    ]
    
    print("🧪 Testing Predefined Responses System")
    print("=" * 50)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n📝 Test {i}: {question}")
        print("-" * 30)
        
        # Check if predefined response should be used
        should_use, question_type = predefined_manager.should_use_predefined_response(question, default_preferences)
        
        if should_use:
            print(f"✅ Matches predefined question type: {question_type}")
            response = predefined_manager.get_personality_aware_response(question_type, default_preferences)
            print(f"📄 Response preview: {response[:100]}...")
        else:
            print("❌ No predefined response match")
            response = predefined_manager.get_response(question, default_preferences)
            print(f"📄 Fallback response preview: {response[:100]}...")
    
    print("\n" + "=" * 50)
    print("✅ Testing completed!")

if __name__ == "__main__":
    test_predefined_responses()

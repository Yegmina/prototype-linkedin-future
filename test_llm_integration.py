#!/usr/bin/env python3
"""
Test script for LLM integration functionality
"""

from predefined_responses import predefined_manager

def test_llm_integration():
    """Test LLM integration with various scenarios"""
    
    print("🧪 Testing LLM Integration System")
    print("=" * 50)
    
    # Test scenarios
    test_cases = [
        {
            "name": "Predefined question with default preferences",
            "message": "How can I advance from Senior Developer to Tech Lead?",
            "preferences": {
                'interests': ['Technology', 'Leadership'],
                'career_level': 'Entry Level',
                'goal': 'advancement',
                'industry': 'All Industries',
                'location': 'Remote',
                'experience': '3-5 years'
            },
            "expected": "predefined"
        },
        {
            "name": "Non-predefined question with default preferences",
            "message": "What jobs should I enroll in?",
            "preferences": {
                'interests': ['Technology', 'Leadership'],
                'career_level': 'Entry Level',
                'goal': 'advancement',
                'industry': 'All Industries',
                'location': 'Remote',
                'experience': '3-5 years'
            },
            "expected": "llm"
        },
        {
            "name": "Predefined question with changed preferences",
            "message": "How can I advance from Senior Developer to Tech Lead?",
            "preferences": {
                'interests': ['Marketing', 'Sales'],
                'career_level': 'Senior',
                'goal': 'skill',
                'industry': 'Technology',
                'location': 'On-site',
                'experience': '6-10 years'
            },
            "expected": "llm"
        },
        {
            "name": "Random question with default preferences",
            "message": "How do I become a data scientist?",
            "preferences": {
                'interests': ['Technology', 'Leadership'],
                'career_level': 'Entry Level',
                'goal': 'advancement',
                'industry': 'All Industries',
                'location': 'Remote',
                'experience': '3-5 years'
            },
            "expected": "llm"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test_case['name']}")
        print("-" * 40)
        print(f"Message: {test_case['message']}")
        print(f"Preferences: {test_case['preferences']}")
        print(f"Expected: {test_case['expected']}")
        
        try:
            # Get response
            response = predefined_manager.get_response(
                test_case['message'], 
                test_case['preferences']
            )
            
            # Determine if it's predefined or LLM
            should_use, question_type = predefined_manager.should_use_predefined_response(
                test_case['message'], 
                test_case['preferences']
            )
            
            actual = "predefined" if should_use else "llm"
            
            if actual == test_case['expected']:
                print(f"✅ Correctly used {actual} response")
            else:
                print(f"❌ Expected {test_case['expected']}, got {actual}")
            
            # Show response preview
            preview = response[:100] + "..." if len(response) > 100 else response
            print(f"📄 Response preview: {preview}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ LLM Integration testing completed!")

if __name__ == "__main__":
    test_llm_integration()

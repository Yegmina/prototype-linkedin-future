#!/usr/bin/env python3
"""
Demo script showing LLM integration logic
"""

from predefined_responses import predefined_manager

def demo_llm_logic():
    """Demonstrate the LLM integration logic"""
    
    print("🎯 LLM Integration Demo")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        {
            "scenario": "Predefined question with default preferences",
            "message": "How can I advance from Senior Developer to Tech Lead?",
            "preferences": {
                'interests': ['Technology', 'Leadership'],
                'career_level': 'Entry Level',
                'goal': 'advancement',
                'location': 'Remote',
                'experience': '3-5 years'
            }
        },
        {
            "scenario": "Non-predefined question (should use LLM)",
            "message": "What jobs should I enroll in?",
            "preferences": {
                'interests': ['Technology', 'Leadership'],
                'career_level': 'Entry Level',
                'goal': 'advancement',
                'location': 'Remote',
                'experience': '3-5 years'
            }
        },
        {
            "scenario": "Predefined question with changed preferences (should use LLM)",
            "message": "How can I advance from Senior Developer to Tech Lead?",
            "preferences": {
                'interests': ['Marketing', 'Sales'],
                'career_level': 'Senior',
                'goal': 'skill',
                'location': 'On-site',
                'experience': '6-10 years'
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test_case['scenario']}")
        print("-" * 40)
        print(f"Question: {test_case['message']}")
        print(f"Preferences: {test_case['preferences']}")
        
        # Check if predefined response should be used
        should_use, question_type = predefined_manager.should_use_predefined_response(
            test_case['message'], 
            test_case['preferences']
        )
        
        print(f"Should use predefined: {should_use}")
        print(f"Question type: {question_type}")
        
        # Get the actual response
        response = predefined_manager.get_response(
            test_case['message'], 
            test_case['preferences']
        )
        
        # Show response type and preview
        response_type = "Predefined" if should_use else "LLM-Generated"
        print(f"Response type: {response_type}")
        
        # Show first 150 characters of response
        preview = response[:150] + "..." if len(response) > 150 else response
        print(f"Response preview: {preview}")
        
        print()
    
    print("=" * 50)
    print("✅ Demo completed!")
    print("\n💡 Key Points:")
    print("• Predefined responses only used for exact 4 questions with default preferences")
    print("• LLM used for all other questions or when preferences are changed")
    print("• System gracefully falls back when API key is not available")

if __name__ == "__main__":
    demo_llm_logic()

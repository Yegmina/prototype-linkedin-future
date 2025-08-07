#!/usr/bin/env python3
"""
Test script to demonstrate predefined responses for LinkedIn-connected vs non-LinkedIn users
"""

from linkedin_profile_analyzer import linkedin_analyzer
from predefined_responses import predefined_manager

def test_predefined_responses():
    """Test predefined responses for different user scenarios"""
    
    print("🧪 Testing Predefined Responses Logic")
    print("=" * 60)
    
    # Test questions
    test_questions = [
        "How can I advance from Senior Developer to Tech Lead?",
        "What skills do I need for a Director position?",
        "Show me remote job opportunities in tech",
        "What workshops are available for leadership skills?"
    ]
    
    # Scenario 1: Default preferences (no LinkedIn)
    print("\n📋 SCENARIO 1: Default Preferences (No LinkedIn)")
    print("-" * 50)
    
    default_preferences = {
        'interests': ['Technology', 'Leadership'],
        'career_level': 'Entry Level',
        'goal': 'advancement',
        'industry': 'All Industries',
        'location': 'Remote',
        'experience': '3-5 years'
    }
    
    for question in test_questions:
        print(f"\n❓ Question: {question}")
        response = predefined_manager.get_response(question, default_preferences)
        print(f"📄 Response Type: {'Predefined' if 'Perfect! I can see you\'re interested in Technology' in response else 'LLM'}")
        print(f"📝 Preview: {response[:100]}...")
    
    # Scenario 2: LinkedIn-connected user (Chase Thompson)
    print("\n\n📋 SCENARIO 2: LinkedIn-Connected User (Chase Thompson)")
    print("-" * 50)
    
    linkedin_url = "https://www.linkedin.com/in/chase-thompson012/"
    profile_data = linkedin_analyzer.analyze_profile(linkedin_url)
    linkedin_preferences = linkedin_analyzer.update_user_preferences(profile_data)
    
    print(f"👤 Profile: {profile_data['name']} - {profile_data['title']}")
    print(f"🏢 Company: {profile_data['company']}")
    print(f"🎯 Industry: {profile_data['industry']}")
    print(f"💼 Skills: {', '.join(profile_data['skills'][:3])}")
    
    for question in test_questions:
        print(f"\n❓ Question: {question}")
        response = predefined_manager.get_response(question, linkedin_preferences)
        print(f"📄 Response Type: {'LinkedIn Predefined' if profile_data['name'] in response else 'LLM'}")
        print(f"📝 Preview: {response[:100]}...")
    
    # Scenario 3: Modified preferences (no LinkedIn)
    print("\n\n📋 SCENARIO 3: Modified Preferences (No LinkedIn)")
    print("-" * 50)
    
    modified_preferences = {
        'interests': ['Marketing', 'Leadership'],
        'career_level': 'Senior',
        'goal': 'skill',
        'industry': 'Marketing',
        'location': 'Hybrid',
        'experience': '6-10 years'
    }
    
    for question in test_questions:
        print(f"\n❓ Question: {question}")
        response = predefined_manager.get_response(question, modified_preferences)
        print(f"📄 Response Type: {'LLM' if 'Perfect! I can see you\'re interested in Technology' not in response else 'Predefined'}")
        print(f"📝 Preview: {response[:100]}...")
    
    print("\n" + "=" * 60)
    print("✅ Predefined Responses testing completed!")

if __name__ == "__main__":
    test_predefined_responses()

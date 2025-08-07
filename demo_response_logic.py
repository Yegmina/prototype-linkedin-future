#!/usr/bin/env python3
"""
Demo script to show predefined response logic for LinkedIn vs non-LinkedIn users
"""

from linkedin_profile_analyzer import linkedin_analyzer
from predefined_responses import predefined_manager

def demo_response_logic():
    """Demonstrate the response logic for different scenarios"""
    
    print("🎯 LinkedIn Profile Connection - Response Logic Demo")
    print("=" * 60)
    
    # Test question
    question = "How can I advance from Senior Developer to Tech Lead?"
    
    print(f"\n❓ Test Question: {question}")
    print("-" * 50)
    
    # Scenario 1: Default preferences (no LinkedIn)
    print("\n📋 SCENARIO 1: Default Preferences (No LinkedIn)")
    default_preferences = {
        'interests': ['Technology', 'Leadership'],
        'career_level': 'Entry Level',
        'goal': 'advancement',
        'industry': 'All Industries',
        'location': 'Remote',
        'experience': '3-5 years'
    }
    
    response1 = predefined_manager.get_response(question, default_preferences)
    print(f"📄 Response Type: {'Predefined' if 'Perfect! I can see you\'re interested in <strong>Technology</strong>' in response1 else 'LLM'}")
    print(f"📝 Preview: {response1[:120]}...")
    
    # Scenario 2: LinkedIn-connected user
    print("\n📋 SCENARIO 2: LinkedIn-Connected User (Chase Thompson)")
    linkedin_url = "https://www.linkedin.com/in/chase-thompson012/"
    profile_data = linkedin_analyzer.analyze_profile(linkedin_url)
    linkedin_preferences = linkedin_analyzer.update_user_preferences(profile_data)
    
    print(f"👤 Profile: {profile_data['name']} - {profile_data['title']}")
    print(f"🏢 Company: {profile_data['company']}")
    print(f"🎯 Industry: {profile_data['industry']}")
    
    response2 = predefined_manager.get_response(question, linkedin_preferences)
    print(f"📄 Response Type: {'LinkedIn Predefined' if profile_data['name'] in response2 else 'LLM'}")
    print(f"📝 Preview: {response2[:120]}...")
    
    # Scenario 3: Modified preferences (no LinkedIn)
    print("\n📋 SCENARIO 3: Modified Preferences (No LinkedIn)")
    modified_preferences = {
        'interests': ['Marketing', 'Leadership'],
        'career_level': 'Senior',
        'goal': 'skill',
        'industry': 'Marketing',
        'location': 'Hybrid',
        'experience': '6-10 years'
    }
    
    response3 = predefined_manager.get_response(question, modified_preferences)
    print(f"📄 Response Type: {'LLM' if 'Perfect! I can see you\'re interested in <strong>Technology</strong>' not in response3 else 'Predefined'}")
    print(f"📝 Preview: {response3[:120]}...")
    
    print("\n" + "=" * 60)
    print("✅ Demo completed! The system now uses:")
    print("   • Predefined responses for default preferences (no LinkedIn)")
    print("   • LinkedIn-specific predefined responses for LinkedIn-connected users")
    print("   • LLM responses for modified preferences (no LinkedIn)")

if __name__ == "__main__":
    demo_response_logic()

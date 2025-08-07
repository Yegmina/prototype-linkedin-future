#!/usr/bin/env python3
"""
Test script for LinkedIn profile connection functionality
"""

from linkedin_profile_analyzer import linkedin_analyzer
from predefined_responses import predefined_manager

def test_linkedin_connection():
    """Test LinkedIn profile connection with Chase Thompson's profile"""
    
    print("🧪 Testing LinkedIn Profile Connection")
    print("=" * 50)
    
    # Test with Chase Thompson's LinkedIn profile
    linkedin_url = "https://www.linkedin.com/in/chase-thompson012/"
    
    print(f"📋 Testing with profile: {linkedin_url}")
    print("-" * 40)
    
    # Analyze the profile
    profile_data = linkedin_analyzer.analyze_profile(linkedin_url)
    
    if profile_data:
        print("✅ Profile Analysis Results:")
        print(f"   Name: {profile_data['name']}")
        print(f"   Title: {profile_data['title']}")
        print(f"   Company: {profile_data['company']}")
        print(f"   Location: {profile_data['location']}")
        print(f"   Skills: {', '.join(profile_data['skills'])}")
        print(f"   Experience Level: {profile_data['experience_level']}")
        print(f"   Industry: {profile_data['industry']}")
        print()
        
        # Update user preferences
        updated_preferences = linkedin_analyzer.update_user_preferences(profile_data)
        print("✅ Updated User Preferences:")
        for key, value in updated_preferences.items():
            if key != 'profile_data':
                print(f"   {key}: {value}")
        print()
        
        # Get personalized suggestions
        suggestions = linkedin_analyzer.get_personalized_suggestions(profile_data)
        print("✅ Personalized Suggestions:")
        print(f"   Welcome: {suggestions['welcome_message']}")
        print(f"   Summary: {suggestions['profile_summary']}")
        print(f"   Career Path: {suggestions['career_path']}")
        print(f"   Skill Gaps: {', '.join(suggestions['skill_gaps'])}")
        print()
        
        # Test predefined responses with LinkedIn data
        print("✅ Testing Predefined Responses with LinkedIn Data:")
        print("-" * 40)
        
        test_questions = [
            "How can I advance from Senior Developer to Tech Lead?",
            "What skills do I need for a Director position?",
            "Show me remote job opportunities in tech",
            "What workshops are available for leadership skills?"
        ]
        
        for question in test_questions:
            print(f"\n📝 Question: {question}")
            response = predefined_manager.get_response(question, updated_preferences)
            print(f"📄 Response preview: {response[:150]}...")
        
    else:
        print("❌ Failed to analyze profile")
    
    print("\n" + "=" * 50)
    print("✅ LinkedIn Profile Connection testing completed!")

if __name__ == "__main__":
    test_linkedin_connection()

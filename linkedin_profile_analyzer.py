"""
LinkedIn Profile Analyzer for LinkedIn Future Career Planning Platform

This module analyzes LinkedIn profile URLs and automatically updates user preferences
based on the profile information. For presentation purposes only.
"""

import re
import logging
from typing import Dict, Optional, Tuple
from urllib.parse import urlparse

# Configure logging
logger = logging.getLogger(__name__)

class LinkedInProfileAnalyzer:
    """Analyzes LinkedIn profiles and extracts relevant information"""
    
    def __init__(self):
        # Sample profile data for demonstration
        self.sample_profiles = {
            "chase-thompson012": {
                "name": "Chase Thompson",
                "title": "Mechanical Engineering Student | Passionate about Automotive Design and Innovation",
                "company": "Weber State University",
                "location": "Ogden, Utah, United States",
                "skills": ["SOLIDWORKS", "MATLAB", "Data Analysis", "Leadership", "Spot Welding"],
                "experience_level": "Entry Level",
                "education": "Bachelor of Science - BS, Mechanical Engineering",
                "interests": ["Engineering", "Technology", "Leadership"],
                "career_goal": "advancement",
                "preferred_location": "On-site",
                "years_experience": "1-3 years",
                "industry": "Manufacturing",
                "summary": "Seeking a long-term career with opportunities for growth and advancement in the aerospace and manufacturing industries."
            },
            "john-doe-tech": {
                "name": "John Doe",
                "title": "Senior Software Engineer | Full Stack Developer",
                "company": "TechCorp",
                "location": "San Francisco, CA",
                "skills": ["JavaScript", "Python", "React", "Node.js", "Leadership"],
                "experience_level": "Senior",
                "education": "Bachelor of Science - BS, Computer Science",
                "interests": ["Technology", "Leadership"],
                "career_goal": "advancement",
                "preferred_location": "Remote",
                "years_experience": "6-10 years",
                "industry": "Technology",
                "summary": "Experienced software engineer looking to advance to technical leadership roles."
            },
            "sarah-marketing": {
                "name": "Sarah Johnson",
                "title": "Marketing Manager | Digital Marketing Specialist",
                "company": "Marketing Solutions Inc",
                "location": "New York, NY",
                "skills": ["Digital Marketing", "Social Media", "Analytics", "Leadership", "Strategy"],
                "experience_level": "Mid-Level",
                "education": "Bachelor of Arts - BA, Marketing",
                "interests": ["Marketing", "Leadership"],
                "career_goal": "skill",
                "preferred_location": "Hybrid",
                "years_experience": "3-5 years",
                "industry": "Marketing",
                "summary": "Marketing professional focused on developing digital marketing skills and leadership capabilities."
            }
        }
    
    def extract_profile_id(self, linkedin_url: str) -> Optional[str]:
        """Extract profile ID from LinkedIn URL"""
        try:
            # Parse the URL
            parsed = urlparse(linkedin_url)
            
            # Extract profile ID from path
            path_parts = parsed.path.strip('/').split('/')
            
            # Look for 'in' followed by profile ID
            for i, part in enumerate(path_parts):
                if part == 'in' and i + 1 < len(path_parts):
                    profile_id = path_parts[i + 1]
                    # Remove any trailing parameters
                    profile_id = profile_id.split('?')[0]
                    return profile_id
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting profile ID: {e}")
            return None
    
    def analyze_profile(self, linkedin_url: str) -> Optional[Dict]:
        """Analyze LinkedIn profile and return extracted information"""
        
        profile_id = self.extract_profile_id(linkedin_url)
        if not profile_id:
            logger.warning(f"Could not extract profile ID from URL: {linkedin_url}")
            return None
        
        # For demonstration, use sample data
        if profile_id in self.sample_profiles:
            profile_data = self.sample_profiles[profile_id].copy()
            profile_data['profile_id'] = profile_id
            profile_data['linkedin_url'] = linkedin_url
            logger.info(f"Profile analyzed successfully: {profile_id}")
            return profile_data
        else:
            # Return default profile for unknown IDs
            logger.info(f"Using default profile for unknown ID: {profile_id}")
            return self._get_default_profile(profile_id, linkedin_url)
    
    def _get_default_profile(self, profile_id: str, linkedin_url: str) -> Dict:
        """Get default profile data for unknown profile IDs"""
        return {
            "name": "LinkedIn User",
            "title": "Professional",
            "company": "Company",
            "location": "Location",
            "skills": ["Technology", "Leadership"],
            "experience_level": "Entry Level",
            "education": "Bachelor's Degree",
            "interests": ["Technology", "Leadership"],
            "career_goal": "advancement",
            "preferred_location": "Remote",
            "years_experience": "3-5 years",
            "industry": "Technology",
            "summary": "Professional seeking career advancement opportunities.",
            "profile_id": profile_id,
            "linkedin_url": linkedin_url
        }
    
    def update_user_preferences(self, profile_data: Dict) -> Dict:
        """Update user preferences based on LinkedIn profile data"""
        
        # Map profile data to user preferences
        preferences = {
            'interests': profile_data.get('interests', ['Technology', 'Leadership']),
            'career_level': profile_data.get('experience_level', 'Entry Level'),
            'goal': profile_data.get('career_goal', 'advancement'),
            'industry': profile_data.get('industry', 'Technology'),
            'location': profile_data.get('preferred_location', 'Remote'),
            'experience': profile_data.get('years_experience', '3-5 years'),
            'linkedin_connected': True,
            'profile_data': profile_data
        }
        
        logger.info(f"User preferences updated based on LinkedIn profile: {profile_data.get('name', 'Unknown')}")
        return preferences
    
    def get_personalized_suggestions(self, profile_data: Dict) -> Dict:
        """Generate personalized suggestions based on profile data"""
        
        name = profile_data.get('name', 'User')
        skills = profile_data.get('skills', [])
        experience_level = profile_data.get('experience_level', 'Entry Level')
        industry = profile_data.get('industry', 'Technology')
        
        suggestions = {
            'welcome_message': f"Welcome, {name}! I've analyzed your LinkedIn profile and personalized your experience.",
            'profile_summary': f"Based on your profile, you're a {experience_level} professional in {industry} with expertise in {', '.join(skills[:3])}.",
            'recommended_questions': self._get_recommended_questions(profile_data),
            'skill_gaps': self._identify_skill_gaps(profile_data),
            'career_path': self._suggest_career_path(profile_data)
        }
        
        return suggestions
    
    def _get_recommended_questions(self, profile_data: Dict) -> list:
        """Get recommended questions based on profile"""
        experience_level = profile_data.get('experience_level', 'Entry Level')
        industry = profile_data.get('industry', 'Technology')
        
        if experience_level == 'Entry Level':
            return [
                "How can I advance from my current role?",
                "What skills should I develop for career growth?",
                "Show me entry-level opportunities in my field"
            ]
        elif experience_level == 'Mid-Level':
            return [
                "What skills do I need for senior positions?",
                "How can I transition to leadership roles?",
                "Show me mid-level opportunities in my industry"
            ]
        else:  # Senior
            return [
                "What skills do I need for executive positions?",
                "How can I advance to director level?",
                "Show me senior leadership opportunities"
            ]
    
    def _identify_skill_gaps(self, profile_data: Dict) -> list:
        """Identify potential skill gaps based on profile"""
        skills = profile_data.get('skills', [])
        experience_level = profile_data.get('experience_level', 'Entry Level')
        
        common_gaps = {
            'Entry Level': ['Project Management', 'Strategic Thinking', 'Leadership'],
            'Mid-Level': ['Executive Communication', 'Strategic Planning', 'Team Leadership'],
            'Senior': ['Board Communication', 'Strategic Vision', 'Change Management']
        }
        
        return common_gaps.get(experience_level, ['Leadership', 'Strategic Thinking'])
    
    def _suggest_career_path(self, profile_data: Dict) -> str:
        """Suggest career path based on profile"""
        experience_level = profile_data.get('experience_level', 'Entry Level')
        industry = profile_data.get('industry', 'Technology')
        
        paths = {
            'Entry Level': f"Focus on skill development and gaining experience in {industry}",
            'Mid-Level': f"Develop leadership skills and specialize in {industry}",
            'Senior': f"Build executive presence and strategic thinking in {industry}"
        }
        
        return paths.get(experience_level, "Focus on continuous learning and skill development")

# Global instance for easy access
linkedin_analyzer = LinkedInProfileAnalyzer()

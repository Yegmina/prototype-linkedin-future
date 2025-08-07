"""
Predefined Responses Module for LinkedIn Future Career Planning Platform

This module handles predefined responses for common career planning questions
when users have default settings. It provides personalized responses that
reference user preferences and personality traits.
"""

import re
from typing import Dict, List, Optional, Tuple
from llm_integration import llm_generator

class PredefinedResponseManager:
    """Manages predefined responses with personality and preference awareness"""
    
    def __init__(self):
        self.default_preferences = {
            'interests': ['Technology', 'Leadership'],
            'career_level': 'Entry Level',
            'goal': 'advancement',
            'industry': 'All Industries',
            'location': 'Remote',
            'experience': '3-5 years'
        }
        
        # Define the four main questions with their variations
        self.main_questions = {
            'advancement': [
                'how can i advance from senior developer to tech lead',
                'advance from senior developer to tech lead',
                'senior developer to tech lead',
                'advancement to tech lead',
                'become tech lead',
                'tech lead advancement'
            ],
            'director_skills': [
                'what skills do i need for a director position',
                'skills for director position',
                'director position skills',
                'become director',
                'director role requirements',
                'executive skills needed'
            ],
            'remote_jobs': [
                'show me remote job opportunities in tech',
                'remote job opportunities tech',
                'remote tech jobs',
                'remote opportunities',
                'tech remote positions',
                'work from home tech jobs'
            ],
            'leadership_workshops': [
                'what workshops are available for leadership skills',
                'leadership skills workshops',
                'leadership workshops',
                'leadership training',
                'workshops for leadership',
                'leadership development workshops'
            ]
        }
        
        # LinkedIn-specific resources
        self.linkedin_resources = {
            'jobs': 'https://www.linkedin.com/jobs/',
            'learning': 'https://www.linkedin.com/learning/',
            'events': 'https://www.linkedin.com/events/',
            'groups': 'https://www.linkedin.com/groups/',
            'networking': 'https://www.linkedin.com/mynetwork/'
        }

    def is_default_preferences(self, user_preferences: Dict) -> bool:
        """Check if user has default preferences"""
        for key, value in self.default_preferences.items():
            if key in user_preferences:
                if isinstance(value, list):
                    if set(user_preferences[key]) != set(value):
                        return False
                else:
                    if user_preferences[key] != value:
                        return False
        return True

    def match_question(self, user_message: str) -> Optional[str]:
        """Match user message to predefined questions"""
        user_message_lower = user_message.lower().strip()
        
        for question_type, variations in self.main_questions.items():
            for variation in variations:
                if variation in user_message_lower:
                    return question_type
        
        return None

    def get_personality_aware_response(self, question_type: str, user_preferences: Dict) -> str:
        """Generate personality-aware predefined response"""
        
        # Extract user preferences for personalization
        interests = user_preferences.get('interests', ['Technology', 'Leadership'])
        career_level = user_preferences.get('career_level', 'Entry Level')
        goal = user_preferences.get('goal', 'advancement')
        location = user_preferences.get('location', 'Remote')
        experience = user_preferences.get('experience', '3-5 years')
        
        # Personalize based on user's interests and preferences
        tech_focus = 'Technology' in interests
        leadership_focus = 'Leadership' in interests
        remote_preference = location == 'Remote'
        advancement_goal = goal == 'advancement'
        
        if question_type == 'advancement':
            return self._get_advancement_response(tech_focus, leadership_focus, remote_preference, experience)
        elif question_type == 'director_skills':
            return self._get_director_skills_response(tech_focus, leadership_focus, advancement_goal)
        elif question_type == 'remote_jobs':
            return self._get_remote_jobs_response(tech_focus, leadership_focus, experience)
        elif question_type == 'leadership_workshops':
            return self._get_leadership_workshops_response(tech_focus, leadership_focus, remote_preference)
        
        return "I understand your question. Let me provide personalized recommendations based on your profile."

    def _get_advancement_response(self, tech_focus: bool, leadership_focus: bool, remote_preference: bool, experience: str) -> str:
        """Generate advancement response with personality awareness"""
        
        response = f"""Perfect! I can see you're interested in <strong>Technology</strong> and <strong>Leadership</strong> - that's an excellent combination for advancing to Tech Lead! 🚀

Based on your <strong>{experience}</strong> of experience and preference for <strong>remote work</strong>, here's your personalized advancement roadmap:

<h3>🎯 Your Path to Tech Lead</h3>

<h4>1. Leadership Development</h4> <em>(Since you're already interested in Leadership!)</em>
• <strong>Mentorship</strong>: Start mentoring junior developers in your team
• <strong>Communication</strong>: Practice explaining complex technical concepts to non-technical stakeholders
• <strong>Decision-making</strong>: Take ownership of technical decisions and their business impact

<h4>2. Technical Excellence</h4> <em>(Leveraging your Technology interest)</em>
• <strong>System Design</strong>: Master large-scale system architecture
• <strong>Code Review</strong>: Lead code review processes and establish best practices
• <strong>Technical Strategy</strong>: Align technical decisions with business objectives

<h4>3. Remote Leadership Skills</h4> <em>(Perfect for your remote preference!)</em>
• <strong>Virtual Team Management</strong>: Learn to lead distributed teams effectively
• <strong>Remote Communication</strong>: Master async communication and documentation
• <strong>Remote Culture Building</strong>: Foster team collaboration in virtual environments

<h3>📚 Recommended Resources on LinkedIn</h3>

• <strong>LinkedIn Learning</strong>: "Becoming a Tech Lead" course series
• <strong>LinkedIn Jobs</strong>: Search for "Tech Lead Remote" positions to understand requirements
• <strong>LinkedIn Groups</strong>: Join "Tech Leadership" and "Remote Engineering" groups
• <strong>LinkedIn Events</strong>: Attend virtual tech leadership conferences

<h3>🎯 Next Steps</h3>

1. <strong>Update your LinkedIn profile</strong> to reflect leadership aspirations
2. <strong>Connect with Tech Leads</strong> in your network for mentorship
3. <strong>Share your technical insights</strong> on LinkedIn to build thought leadership
4. <strong>Apply for internal Tech Lead opportunities</strong> or remote positions

Your combination of <strong>Technology expertise</strong> and <strong>Leadership interest</strong> positions you perfectly for this transition! 

I've updated your "Recommended for You" section with specific Tech Lead opportunities and LinkedIn resources. Check out the recommendations below! 🔗"""

        return response

    def _get_director_skills_response(self, tech_focus: bool, leadership_focus: bool, advancement_goal: bool) -> str:
        """Generate director skills response with personality awareness"""
        
        response = f"""Excellent question! I can see you're focused on <strong>Leadership</strong> and have <strong>advancement</strong> as your primary goal - you're thinking strategically! 🎯

Based on your <strong>Technology</strong> background and <strong>Leadership</strong> interests, here's what you need for a Director position:

<h3>🏆 Director-Level Skills Framework</h3>

<h4>1. Strategic Leadership</h4> <em>(Building on your Leadership interest!)</em>
• <strong>Vision Setting</strong>: Define and communicate organizational direction
• <strong>Strategic Planning</strong>: Align technology initiatives with business objectives
• <strong>Change Management</strong>: Lead organizational transformation initiatives

<h4>2. Business Acumen</h4> <em>(Essential for advancement!)</em>
• <strong>P&L Management</strong>: Understand financial impact of technical decisions
• <strong>Market Analysis</strong>: Stay ahead of industry trends and competitive landscape
• <strong>Stakeholder Management</strong>: Work effectively with C-suite and board members

<h4>3. Executive Communication</h4> <em>(Perfect for your Leadership focus!)</em>
• <strong>Board Presentations</strong>: Present complex technical concepts to executives
• <strong>Influence Without Authority</strong>: Lead cross-functional teams and initiatives
• <strong>External Representation</strong>: Represent your organization at industry events

<h4>4. Technology Strategy</h4> <em>(Leveraging your Technology expertise!)</em>
• <strong>Technology Roadmap</strong>: Develop long-term technology strategy
• <strong>Innovation Leadership</strong>: Drive digital transformation initiatives
• <strong>Risk Management</strong>: Balance innovation with operational stability

<h3>📚 LinkedIn Resources for Director Development</h3>

• <strong>LinkedIn Learning</strong>: "Executive Leadership" and "Strategic Management" courses
• <strong>LinkedIn Jobs</strong>: Search "Director Technology" to understand role requirements
• <strong>LinkedIn Groups</strong>: Join "Technology Directors" and "Executive Leadership" groups
• <strong>LinkedIn Events</strong>: Attend executive leadership conferences and summits

<h3>🎯 Your Competitive Advantages</h3>

Your <strong>Technology</strong> background gives you a unique edge - you can bridge the gap between technical and business perspectives, which is crucial for Director roles!

<h3>🚀 Immediate Actions</h3>

1. <strong>Enhance your LinkedIn profile</strong> with strategic achievements
2. <strong>Connect with Directors</strong> in your industry for mentorship
3. <strong>Share strategic insights</strong> on LinkedIn to build executive presence
4. <strong>Pursue executive education</strong> programs or MBA courses

Your <strong>advancement</strong> mindset and <strong>Leadership</strong> focus show you're ready for this next level! 

I've updated your "Recommended for You" section with Director-level opportunities and executive development resources. Check out the recommendations below! 🔗"""

        return response

    def _get_remote_jobs_response(self, tech_focus: bool, leadership_focus: bool, experience: str) -> str:
        """Generate remote jobs response with personality awareness"""
        
        response = f"""Fantastic! I can see you're interested in <strong>Technology</strong> and <strong>Leadership</strong> - that's a powerful combination for remote opportunities! 🌐

Based on your <strong>{experience}</strong> of experience, here are the best remote tech opportunities for your profile:

<h3>💼 Remote Tech Opportunities Perfect for You</h3>

<h4>1. Senior Developer Roles</h4> <em>(Leveraging your Technology expertise!)</em>
• <strong>Full-Stack Development</strong>: Remote positions at innovative startups
• <strong>Backend Engineering</strong>: Senior roles at established tech companies
• <strong>DevOps Engineering</strong>: Infrastructure and automation roles

<h4>2. Tech Lead Positions</h4> <em>(Perfect for your Leadership interest!)</em>
• <strong>Engineering Team Lead</strong>: Lead development teams remotely
• <strong>Technical Project Manager</strong>: Manage technical projects and teams
• <strong>Architecture Lead</strong>: Design and implement technical solutions

<h4>3. Leadership Opportunities</h4> <em>(Building on your Leadership focus!)</em>
• <strong>Engineering Manager</strong>: Manage remote engineering teams
• <strong>Product Manager</strong>: Lead product development initiatives
• <strong>Technical Consultant</strong>: Provide strategic technical guidance

<h3>🔍 Top Remote Companies Hiring</h3>

• <strong>GitLab</strong>: Fully remote company with excellent leadership opportunities
• <strong>Automattic</strong>: WordPress parent company with global remote teams
• <strong>Buffer</strong>: Social media company with strong remote culture
• <strong>Zapier</strong>: Automation platform with leadership development programs

<h3>📚 LinkedIn Job Search Strategy</h3>

<h4>Search Terms to Use:</h4>
• "Senior Developer Remote"
• "Tech Lead Remote"
• "Engineering Manager Remote"
• "Technology Leadership Remote"

<h4>LinkedIn Features:</h4>
• <strong>LinkedIn Jobs</strong>: Use remote filter and save searches
• <strong>LinkedIn Recruiter</strong>: Connect with hiring managers directly
• <strong>LinkedIn Groups</strong>: Join "Remote Work" and "Tech Leadership" groups
• <strong>LinkedIn Events</strong>: Attend virtual tech job fairs

<h3>🎯 Your Remote Work Advantages</h3>

Your <strong>Technology</strong> skills are highly transferable to remote work, and your <strong>Leadership</strong> interest positions you well for remote team management roles!

<h3>🚀 Next Steps</h3>

1. <strong>Optimize your LinkedIn profile</strong> for remote opportunities
2. <strong>Set up job alerts</strong> for remote tech positions
3. <strong>Network with remote professionals</strong> on LinkedIn
4. <strong>Showcase remote work skills</strong> in your profile and posts

Your combination of <strong>Technology expertise</strong> and <strong>Leadership aspirations</strong> makes you highly attractive to remote-first companies! 

I've updated your "Recommended for You" section with remote job opportunities and LinkedIn resources. Check out the recommendations below! 🔗"""

        return response

    def _get_leadership_workshops_response(self, tech_focus: bool, leadership_focus: bool, remote_preference: bool) -> str:
        """Generate leadership workshops response with personality awareness"""
        
        response = f"""Excellent choice! I can see you're already interested in <strong>Leadership</strong> - that's the first step! 🎯

Based on your <strong>Technology</strong> background and preference for <strong>remote work</strong>, here are the best leadership workshops for your career:

<h3>🎓 Leadership Workshops Perfect for You</h3>

<h4>1. Technology Leadership Programs</h4> <em>(Leveraging your Technology expertise!)</em>
• <strong>LinkedIn Learning</strong>: "Tech Leadership" course series
• <strong>Coursera</strong>: "Leading Technology Teams" specialization
• <strong>edX</strong>: "Technology Leadership" micro-masters program

<h4>2. Remote Leadership Development</h4> <em>(Perfect for your remote preference!)</em>
• <strong>Virtual Leadership Workshops</strong>: Remote team management skills
• <strong>Async Communication Training</strong>: Leading distributed teams effectively
• <strong>Remote Culture Building</strong>: Creating strong virtual team dynamics

<h4>3. Executive Leadership Programs</h4> <em>(Building on your Leadership interest!)</em>
• <strong>Harvard Business School Online</strong>: Leadership courses
• <strong>MIT Sloan</strong>: Executive leadership programs
• <strong>Stanford Graduate School</strong>: Technology leadership workshops

<h3>📅 Upcoming LinkedIn Events</h3>

<h4>Virtual Leadership Conferences:</h4>
• <strong>Tech Leadership Summit</strong>: Virtual conference with networking
• <strong>Remote Leadership Forum</strong>: Focus on distributed team management
• <strong>Executive Development Series</strong>: Monthly leadership workshops

<h4>LinkedIn Learning Paths:</h4>
• <strong>"Becoming a Tech Leader"</strong> - Complete learning path
• <strong>"Remote Team Management"</strong> - Specialized course series
• <strong>"Executive Communication"</strong> - Leadership communication skills

<h3>🎯 Workshop Recommendations by Interest</h3>

<h4>For Technology Focus:</h4>
• Technical leadership workshops
• System architecture leadership
• Innovation management programs

<h4>For Leadership Development:</h4>
• Executive coaching programs
• Strategic thinking workshops
• Change management training

<h4>For Remote Work:</h4>
• Virtual team building workshops
• Remote communication training
• Distributed leadership programs

<h3>🚀 LinkedIn Learning Strategy</h3>

1. <strong>Complete LinkedIn Learning paths</strong> in leadership
2. <strong>Join LinkedIn Groups</strong> for leadership development
3. <strong>Attend LinkedIn Events</strong> and virtual conferences
4. <strong>Connect with leadership coaches</strong> and mentors

<h3>💡 Your Leadership Journey</h3>

Your <strong>Technology</strong> background gives you a unique perspective on leadership, and your interest in <strong>Leadership</strong> shows you're ready to develop these skills!

<h3>🎯 Immediate Actions</h3>

1. <strong>Enroll in LinkedIn Learning leadership courses</strong>
2. <strong>Register for upcoming virtual leadership events</strong>
3. <strong>Join leadership-focused LinkedIn groups</strong>
4. <strong>Connect with leadership mentors</strong> in your network

Your combination of <strong>Technology expertise</strong> and <strong>Leadership aspirations</strong> makes you a perfect candidate for these programs! 

I've updated your "Recommended for You" section with leadership workshops and LinkedIn Learning resources. Check out the recommendations below! 🔗"""

        return response

    def should_use_predefined_response(self, user_message: str, user_preferences: Dict) -> Tuple[bool, Optional[str]]:
        """Determine if predefined response should be used"""
        
        # Only use predefined responses for the exact four main questions with default preferences
        # This ensures LLM is used for all other questions and when preferences are changed
        
        # Check if user has default preferences
        if not self.is_default_preferences(user_preferences):
            return False, None
        
        # Check if message matches predefined questions exactly
        question_type = self.match_question(user_message)
        if question_type:
            return True, question_type
        
        return False, None

    def get_response(self, user_message: str, user_preferences: Dict) -> str:
        """Get appropriate response (predefined or LLM-generated)"""
        
        should_use, question_type = self.should_use_predefined_response(user_message, user_preferences)
        
        if should_use and question_type:
            return self.get_personality_aware_response(question_type, user_preferences)
        
        # Use real LLM for dynamic responses when predefined response doesn't apply
        return llm_generator.generate_response(user_message, user_preferences)

    def _get_fallback_response(self, user_message: str, user_preferences: Dict) -> str:
        """Generate fallback response when predefined response doesn't apply"""
        
        interests = user_preferences.get('interests', ['Technology', 'Leadership'])
        goal = user_preferences.get('goal', 'advancement')
        
        return f"""I understand you're asking about "{user_message}". 

Based on your interests in <strong>{', '.join(interests)}</strong> and your goal of <strong>{goal}</strong>, I'd be happy to help you explore this topic further. 

You can:
• Ask me about career advancement strategies
• Inquire about specific skills for leadership roles
• Explore remote job opportunities
• Find leadership workshops and events

What specific aspect would you like to dive deeper into? I'm here to provide personalized guidance based on your career goals! 🚀"""

# Global instance for easy access
predefined_manager = PredefinedResponseManager()

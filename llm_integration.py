"""
LLM Integration Module for LinkedIn Future Career Planning Platform

This module provides integration with Google's Gemini API for generating
dynamic, personalized responses when predefined answers are not available.
"""

import os
import logging
from typing import Dict, Optional
import google.generativeai as genai

# Configure logging
logger = logging.getLogger(__name__)

class LLMResponseGenerator:
    """Generates dynamic responses using Google's Gemini API"""
    
    def __init__(self):
        #self.api_key = os.getenv('GEMINI_API_KEY')
        self.api_key = "AIzaSyB3Ywk1Fs6xpneBMFWEu9ZY1HJNT8UqteA"
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.is_available = True
            logger.info("Gemini API configured successfully")
        else:
            self.is_available = False
            logger.warning("GEMINI_API_KEY not found. LLM responses will be disabled.")
    
    def generate_response(self, user_message: str, user_preferences: Dict) -> str:
        """Generate a dynamic response using Gemini API"""
        
        if not self.is_available:
            return self._get_fallback_response(user_message, user_preferences)
        
        try:
            # Create a context-aware prompt
            prompt = self._create_prompt(user_message, user_preferences)
            
            # Generate response
            response = self.model.generate_content(prompt)
            
            # Convert markdown to HTML for web display
            html_response = self._convert_markdown_to_html(response.text)
            
            logger.info("LLM response generated successfully")
            return html_response
            
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            return self._get_fallback_response(user_message, user_preferences)
    
    def _create_prompt(self, user_message: str, user_preferences: Dict) -> str:
        """Create a context-aware prompt for the LLM"""
        
        interests = user_preferences.get('interests', [])
        career_level = user_preferences.get('career_level', 'Entry Level')
        goal = user_preferences.get('goal', 'advancement')
        location = user_preferences.get('location', 'Remote')
        experience = user_preferences.get('experience', '3-5 years')
        
        prompt = f"""You are a professional career planning assistant for LinkedIn Future, a career development platform. 

**CRITICAL: The user is asking this specific question: "{user_message}"**

User Context:
- Interests: {', '.join(interests)}
- Career Level: {career_level}
- Goal: {goal}
- Preferred Location: {location}
- Experience: {experience}

**IMPORTANT: Your response MUST directly answer their specific question: "{user_message}"**

Please provide a comprehensive, personalized response that:
1. **DIRECTLY ANSWERS their specific question** - this is the most important part
2. Acknowledges their specific interests and preferences
3. Provides actionable career advice related to their question
4. Mentions relevant LinkedIn resources (LinkedIn Learning, LinkedIn Jobs, LinkedIn Events, LinkedIn Groups)
5. Suggests specific next steps related to their question
6. Uses a professional but friendly tone
7. Includes emojis sparingly for engagement
8. References their career goals and experience level
9. Provides specific, actionable recommendations that directly address their question

**FORMAT REQUIREMENTS:**
- Start with a direct answer to their question
- Use HTML tags like <strong>, <em>, <h3>, <h4>, <ul>, <li> for web display
- Make their specific question the focus of your entire response
- If they ask about events, prioritize event recommendations
- If they ask about jobs, prioritize job-related advice
- If they ask about skills, prioritize skill development resources

**SPECIFIC EXAMPLES:**
- If they ask "find useful events for me" → Focus on specific LinkedIn Events, upcoming conferences, workshops, etc.
- If they ask "what jobs should I enroll in" → Focus on specific job opportunities, application strategies, etc.
- If they ask about skills → Focus on specific LinkedIn Learning courses, skill development paths, etc.

**REMEMBER: Their question "{user_message}" is the most important thing to address!**"""

        return prompt
    
    def _convert_markdown_to_html(self, markdown_text: str) -> str:
        """Convert markdown formatting to HTML for web display"""
        
        # Basic markdown to HTML conversion
        html = markdown_text
        
        # Convert **text** to <strong>text</strong>
        import re
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        
        # Convert *text* to <em>text</em>
        html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
        
        # Convert ## headings to <h3>
        html = re.sub(r'^##\s+(.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        
        # Convert ### headings to <h4>
        html = re.sub(r'^###\s+(.*?)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
        
        # Convert bullet points to <ul><li>
        html = re.sub(r'^\s*•\s+(.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
        html = re.sub(r'^\s*-\s+(.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
        
        # Wrap consecutive <li> elements in <ul>
        lines = html.split('\n')
        in_list = False
        result_lines = []
        
        for line in lines:
            if line.strip().startswith('<li>'):
                if not in_list:
                    result_lines.append('<ul>')
                    in_list = True
                result_lines.append(line)
            else:
                if in_list:
                    result_lines.append('</ul>')
                    in_list = False
                result_lines.append(line)
        
        if in_list:
            result_lines.append('</ul>')
        
        html = '\n'.join(result_lines)
        
        return html
    
    def _get_fallback_response(self, user_message: str, user_preferences: Dict) -> str:
        """Fallback response when LLM is not available"""
        
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
llm_generator = LLMResponseGenerator()

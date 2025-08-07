from flask import Flask, render_template, request, jsonify
import os
import logging
from predefined_responses import predefined_manager
from linkedin_profile_analyzer import linkedin_analyzer

app = Flask(__name__)

# Configure Flask app
app.config['SECRET_KEY'] = 'linkedin-future-secret-key-2024'
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    """Main route - serves the LinkedIn Future career planning platform"""
    app.logger.info('Main page accessed')
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint for chat functionality"""
    data = request.get_json()
    user_message = data.get('message', '')
    
    app.logger.info(f'Chat request received: {user_message[:50]}...')
    
    # Get user preferences from request (default to default preferences)
    user_preferences = data.get('preferences', {
        'interests': ['Technology', 'Leadership'],
        'career_level': 'Entry Level',
        'goal': 'advancement',
        'industry': 'All Industries',
        'location': 'Remote',
        'experience': '3-5 years'
    })
    
    # Use predefined responses if applicable
    response = predefined_manager.get_response(user_message, user_preferences)
    
    app.logger.info('Chat response generated successfully')
    
    return jsonify({
        'response': response,
        'status': 'success'
    })

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    """API endpoint for getting personalized recommendations"""
    # Get filter parameters from request
    career_level = request.args.get('career_level', '')
    interests = request.args.getlist('interests')
    goal = request.args.get('goal', 'advancement')
    
    app.logger.info(f'Recommendations requested - Level: {career_level}, Goal: {goal}, Interests: {interests}')
    
    # Generate recommendations based on filters
    recommendations = generate_recommendations(career_level, interests, goal)
    
    app.logger.info(f'Generated {len(recommendations["courses"])} courses, {len(recommendations["jobs"])} jobs, {len(recommendations["events"])} events, {len(recommendations["workshops"])} workshops')
    
    return jsonify({
        'recommendations': recommendations,
        'status': 'success'
    })

@app.route('/api/upload-cv', methods=['POST'])
def upload_cv():
    """API endpoint for CV upload and analysis"""
    if 'cv_file' not in request.files:
        app.logger.warning('CV upload attempted without file')
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['cv_file']
    if file.filename == '':
        app.logger.warning('CV upload attempted with empty filename')
        return jsonify({'error': 'No file selected'}), 400
    
    app.logger.info(f'CV upload received: {file.filename}')
    
    # In a real app, you would process the CV file here
    # For now, we'll simulate CV analysis
    analysis_result = simulate_cv_analysis(file.filename)
    
    app.logger.info(f'CV analysis completed for {file.filename}')
    
    return jsonify({
        'message': f'CV uploaded successfully: {file.filename}',
        'analysis': analysis_result,
        'status': 'success'
    })

@app.route('/api/connect-linkedin', methods=['POST'])
def connect_linkedin():
    """API endpoint for LinkedIn profile connection"""
    data = request.get_json()
    linkedin_url = data.get('linkedin_url', '')
    
    if not linkedin_url:
        app.logger.warning('LinkedIn connection attempted without URL')
        return jsonify({'error': 'No LinkedIn URL provided'}), 400
    
    app.logger.info(f'LinkedIn profile connection requested: {linkedin_url}')
    
    try:
        # Analyze the LinkedIn profile
        profile_data = linkedin_analyzer.analyze_profile(linkedin_url)
        
        if not profile_data:
            return jsonify({'error': 'Could not analyze LinkedIn profile'}), 400
        
        # Update user preferences based on profile
        updated_preferences = linkedin_analyzer.update_user_preferences(profile_data)
        
        # Get personalized suggestions
        suggestions = linkedin_analyzer.get_personalized_suggestions(profile_data)
        
        app.logger.info(f'LinkedIn profile connected successfully: {profile_data.get("name", "Unknown")}')
        
        return jsonify({
            'message': f'LinkedIn profile connected successfully!',
            'profile_data': profile_data,
            'updated_preferences': updated_preferences,
            'suggestions': suggestions,
            'status': 'success'
        })
        
    except Exception as e:
        app.logger.error(f'Error connecting LinkedIn profile: {e}')
        return jsonify({'error': 'Error connecting LinkedIn profile'}), 500

def generate_chat_response(user_message):
    """Generate chat responses based on user input"""
    lower_message = user_message.lower()
    
    if 'advance' in lower_message or 'tech lead' in lower_message:
        return """Great question! To advance from Senior Developer to Tech Lead, I recommend:

1. **Leadership Skills**: Take courses in team management and communication
2. **Technical Excellence**: Continue mastering your technical skills
3. **Mentorship**: Start mentoring junior developers
4. **Strategic Thinking**: Learn about system architecture and business impact
5. **Networking**: Attend tech leadership events and conferences

I've updated your recommendations with relevant courses and workshops!"""
    
    elif 'director' in lower_message or 'executive' in lower_message:
        return """For Director-level positions, you'll need to develop:

1. **Strategic Leadership**: Ability to set vision and direction
2. **Business Acumen**: Understanding of P&L, market dynamics
3. **Change Management**: Leading organizational transformation
4. **Stakeholder Management**: Working with C-suite and board
5. **Industry Knowledge**: Deep understanding of your sector

Consider executive coaching programs and MBA courses for these skills."""
    
    elif 'job' in lower_message or 'opportunity' in lower_message:
        return """Based on your profile, I found several remote tech opportunities:

• Senior positions at innovative startups
• Tech Lead roles at established companies  
• Remote-first organizations with great benefits

I've updated your job recommendations with the best matches for your skills and experience level."""
    
    elif 'workshop' in lower_message or 'event' in lower_message:
        return """Here are upcoming workshops and events perfect for your career goals:

• Leadership workshops for tech professionals
• Industry conferences with networking opportunities
• Skill-building workshops in your areas of interest
• Executive development programs

I've highlighted the most relevant events in your recommendations!"""
    
    else:
        return f"I understand you're interested in {user_message}. Let me analyze your profile and current filters to provide personalized recommendations. I've updated your suggestions based on your career goals and interests."

def generate_recommendations(career_level, interests, goal):
    """Generate personalized recommendations based on user filters"""
    recommendations = {
        'courses': [],
        'jobs': [],
        'events': [],
        'workshops': []
    }
    
    # Contextual recommendations based on goal
    if goal == 'advancement':
        # Focus on skill development and training programs
        recommendations['courses'].append({
            'title': 'LinkedIn Learning: Becoming a Tech Lead',
            'description': 'Comprehensive course series for advancing to Tech Lead position',
            'duration': '12 hours',
            'price': 'Free with LinkedIn Premium',
            'format': 'Online',
            'type': 'COURSE',
            'link': 'https://www.linkedin.com/learning/paths/becoming-a-tech-lead'
        })
        
        recommendations['jobs'].append({
            'title': 'Senior Trainee Program - Tech Leadership',
            'description': 'Structured program for senior developers transitioning to leadership',
            'location': 'Remote',
            'salary': 'Training + Salary',
            'company': 'TechCorp',
            'type': 'JOB',
            'link': 'https://www.linkedin.com/jobs/search/?keywords=senior%20trainee%20tech%20lead'
        })
        
        recommendations['events'].append({
            'title': 'Tech Leadership Practice Group',
            'description': 'Join a community of aspiring tech leaders for practice and mentorship',
            'date': 'Weekly',
            'location': 'Virtual Practice Sessions',
            'price': 'Free',
            'type': 'EVENT',
            'link': 'https://www.linkedin.com/groups/tech-leadership-practice'
        })
        
        recommendations['workshops'].append({
            'title': 'LinkedIn Learning: Executive Leadership Program',
            'description': 'Advanced leadership skills for senior professionals',
            'duration': '16 weeks',
            'price': 'Free with LinkedIn Premium',
            'spots': 'Unlimited',
            'type': 'WORKSHOP',
            'link': 'https://www.linkedin.com/learning/paths/executive-leadership-program'
        })
    
    elif goal == 'skill':
        # Focus on learning events and skill development
        recommendations['courses'].append({
            'title': 'LinkedIn Learning: Tech Leadership Course Series',
            'description': 'Comprehensive leadership development for tech professionals',
            'duration': '20 hours',
            'price': 'Free with LinkedIn Premium',
            'format': 'Online',
            'type': 'COURSE',
            'link': 'https://www.linkedin.com/learning/paths/tech-leadership-course-series'
        })
        
        recommendations['jobs'].append({
            'title': 'Leadership Practice Group',
            'description': 'Join a community for practicing leadership skills and scenarios',
            'location': 'Virtual',
            'salary': 'Practice Sessions',
            'company': 'Community',
            'type': 'JOB',
            'link': 'https://www.linkedin.com/groups/leadership-practice-group'
        })
        
        recommendations['events'].append({
            'title': 'Leadership Learning Events Series',
            'description': 'Monthly events featuring leadership experts and interactive workshops',
            'date': 'Monthly',
            'location': 'Virtual Learning Events',
            'price': 'Free',
            'type': 'EVENT',
            'link': 'https://www.linkedin.com/events/leadership-learning-series'
        })
        
        recommendations['workshops'].append({
            'title': 'LinkedIn Leadership Development Workshop',
            'description': 'Interactive workshop for developing leadership skills',
            'duration': '8 hours',
            'price': 'Free with LinkedIn Premium',
            'spots': 'Unlimited',
            'type': 'WORKSHOP',
            'link': 'https://www.linkedin.com/learning/courses/leadership-development-workshop'
        })
    
    elif goal == 'job':
        # Focus on job opportunities and networking events
        recommendations['courses'].append({
            'title': 'LinkedIn Job Search Mastery Course',
            'description': 'Learn effective job search strategies and LinkedIn optimization',
            'duration': '4 hours',
            'price': 'Free with LinkedIn Premium',
            'format': 'Online',
            'type': 'COURSE',
            'link': 'https://www.linkedin.com/learning/courses/job-search-mastery'
        })
        
        recommendations['jobs'].append({
            'title': 'Senior Tech Lead - Remote',
            'description': 'Leading development team in innovative tech company',
            'location': 'Remote',
            'salary': '$140k-180k',
            'company': 'TechCorp',
            'type': 'JOB',
            'link': 'https://www.linkedin.com/jobs/search/?keywords=tech%20lead%20remote'
        })
        
        recommendations['events'].append({
            'title': 'Tech Jobs Fair 2025',
            'description': 'Virtual job fair with top tech companies hiring remote positions',
            'date': 'Dec 20, 2025',
            'location': 'Virtual Job Fair',
            'price': 'Free',
            'type': 'EVENT',
            'link': 'https://www.linkedin.com/company/tech-jobs-fair/'
        })
        
        recommendations['workshops'].append({
            'title': 'LinkedIn Networking Workshop',
            'description': 'Learn how to network effectively on LinkedIn for job opportunities',
            'duration': '2 hours',
            'price': 'Networking Skills',
            'spots': 'Virtual',
            'type': 'WORKSHOP',
            'link': 'https://www.linkedin.com/learning/courses/linkedin-networking-workshop'
        })
    
    else:
        # Default recommendations for other goals
        recommendations['courses'].append({
            'title': 'LinkedIn Learning: Becoming a Tech Lead',
            'description': 'Comprehensive course series for advancing to Tech Lead position',
            'duration': '12 hours',
            'price': 'Free with LinkedIn Premium',
            'format': 'Online',
            'type': 'COURSE',
            'link': 'https://www.linkedin.com/learning/paths/becoming-a-tech-lead'
        })
        
        recommendations['jobs'].append({
            'title': 'Senior Tech Lead - Remote',
            'description': 'Leading development team in innovative tech company',
            'location': 'Remote',
            'salary': '$120k-150k',
            'company': 'TechCorp',
            'type': 'JOB',
            'link': 'https://www.linkedin.com/jobs/search/?keywords=senior%20tech%20lead%20remote'
        })
    
    recommendations['events'].append({
            'title': 'LinkedIn Tech Leadership Summit 2025',
            'description': 'Virtual conference with industry leaders and networking opportunities',
            'date': 'Dec 15, 2025',
            'location': 'Virtual (LinkedIn Events)',
            'price': 'Free',
            'type': 'EVENT',
            'link': 'https://www.linkedin.com/events/tech-leadership-summit-2025'
        })
        
    recommendations['workshops'].append({
            'title': 'LinkedIn Learning: Strategic Thinking Workshop',
        'description': 'Develop strategic thinking skills for executive roles',
            'duration': '6 hours',
            'price': 'Free with LinkedIn Premium',
            'spots': 'Unlimited',
            'type': 'WORKSHOP',
            'link': 'https://www.linkedin.com/learning/courses/strategic-thinking-for-leaders'
    })
    
    return recommendations

def simulate_cv_analysis(filename):
    """Simulate CV analysis and return insights"""
    return {
        'skills_identified': ['JavaScript', 'Python', 'React', 'Node.js', 'Leadership'],
        'experience_level': 'Senior',
        'recommended_roles': ['Tech Lead', 'Senior Developer', 'Engineering Manager'],
        'skill_gaps': ['Strategic Planning', 'Executive Communication'],
        'recommended_courses': ['Leadership in Tech', 'Strategic Management']
    }

@app.errorhandler(404)
def not_found(error):
    app.logger.warning(f'404 error: {request.url}')
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f'500 error: {error}')
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Create necessary directories if they don't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    app.logger.info("🚀 LinkedIn Future Career Planning Platform")
    app.logger.info("📍 Server starting on http://localhost:5000")
    app.logger.info("📁 Static files served from /static/")
    app.logger.info("🎨 Templates rendered from /templates/")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 
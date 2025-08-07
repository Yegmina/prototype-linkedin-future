// Career Planning Assistant - Interactive Features with Flask Backend

// Global variables
let currentFilters = {
    interests: ['Technology', 'Leadership'],
    careerLevel: 'Entry Level',
    goal: 'advancement',
    industry: 'All Industries',
    location: 'Remote',
    experience: '3-5 years'
};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    setupEventListeners();
    updateActiveFilters();
    loadRecommendations();
    
    // Show default recommendations for users with default preferences
    showDefaultRecommendations();
}

// Event Listeners Setup
function setupEventListeners() {
    // Interest input handling
    const interestInput = document.getElementById('interestInput');
    if (interestInput) {
        interestInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                addInterest(this.value);
                this.value = '';
            }
        });
    }

    // Filter chip removal
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('fa-times')) {
            const tag = e.target.parentElement;
            removeFilter(tag.textContent.replace('×', '').trim());
        }
    });

    // Checkbox and radio button changes
    document.addEventListener('change', function(e) {
        if (e.target.type === 'checkbox' || e.target.type === 'radio') {
            updateFilters();
        }
    });

    // Select changes
    document.addEventListener('change', function(e) {
        if (e.target.tagName === 'SELECT') {
            updateFilters();
        }
    });
}

// Interest Management
function addInterest(interest) {
    if (interest.trim() && !currentFilters.interests.includes(interest.trim())) {
        currentFilters.interests.push(interest.trim());
        updateInterestTags();
        updateActiveFilters();
        loadRecommendations();
    }
}

function removeInterest(interest) {
    currentFilters.interests = currentFilters.interests.filter(i => i !== interest);
    updateInterestTags();
    updateActiveFilters();
    loadRecommendations();
}

function updateInterestTags() {
    const tagsContainer = document.getElementById('interestTags');
    if (tagsContainer) {
        tagsContainer.innerHTML = currentFilters.interests.map(interest => 
            `<span class="tag">${interest}<i class="fas fa-times"></i></span>`
        ).join('');
    }
}

// Filter Management
function updateFilters() {
    const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
    const radios = document.querySelectorAll('input[type="radio"]:checked');
    const selects = document.querySelectorAll('select');

    // Update career level
    const careerLevelCheckboxes = document.querySelectorAll('input[name="career-level"]:checked');
    if (careerLevelCheckboxes.length > 0) {
        currentFilters.careerLevel = Array.from(careerLevelCheckboxes).map(cb => cb.parentElement.textContent.trim()).join(', ');
    }

    // Update goal
    const selectedGoal = document.querySelector('input[name="goal"]:checked');
    if (selectedGoal) {
        currentFilters.goal = selectedGoal.value;
    }

    // Update industry and location
    selects.forEach(select => {
        if (select.selectedIndex > 0) {
            if (select.options[select.selectedIndex].text.includes('Industry')) {
                currentFilters.industry = select.value;
            } else if (select.options[select.selectedIndex].text.includes('Location')) {
                currentFilters.location = select.value;
            }
        }
    });

    updateActiveFilters();
    loadRecommendations();
}

function removeFilter(filterText) {
    // Remove from interests
    if (currentFilters.interests.includes(filterText)) {
        removeInterest(filterText);
        return;
    }

    // Remove from other filters
    if (filterText.includes('Level')) {
        currentFilters.careerLevel = '';
    }

    updateActiveFilters();
    loadRecommendations();
}

function updateActiveFilters() {
    const activeFiltersContainer = document.querySelector('.active-filters');
    if (!activeFiltersContainer) return;

    const filters = [];
    
    // Add interests
    currentFilters.interests.forEach(interest => {
        filters.push(`<span class="filter-chip">${interest}<i class="fas fa-times"></i></span>`);
    });

    // Add career level
    if (currentFilters.careerLevel) {
        filters.push(`<span class="filter-chip">${currentFilters.careerLevel}<i class="fas fa-times"></i></span>`);
    }

    // Add goal
    const goalText = getGoalText(currentFilters.goal);
    if (goalText) {
        filters.push(`<span class="filter-chip">${goalText}<i class="fas fa-times"></i></span>`);
    }

    activeFiltersContainer.innerHTML = filters.join('');
}

function getGoalText(goal) {
    const goalMap = {
        'advancement': 'Career Advancement',
        'skill': 'Skill Development',
        'job': 'Job Search',
        'retirement': 'Retirement Planning'
    };
    return goalMap[goal] || '';
}

// Chat Functionality with Flask Backend
function askQuestion(question) {
    addMessage(question, 'user');
    processQuestionWithBackend(question);
    document.getElementById('recommendationsSection').style.display = 'block';
}

function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (message) {
        addMessage(message, 'user');
        input.value = '';
        processQuestionWithBackend(message);
        document.getElementById('recommendationsSection').style.display = 'block';
    }
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

function addMessage(message, sender) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const icon = sender === 'user' ? 'fas fa-user' : 'fas fa-robot';
    const messageContent = `
        <div class="message-content">
            <i class="${icon}"></i>
            <div>
                <p>${message}</p>
            </div>
        </div>
    `;
    
    messageDiv.innerHTML = messageContent;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addAssistantMessage(message, isTyping = false) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';
    
    const typingIndicator = isTyping ? '<div class="loading"></div>' : '';
    const messageContent = `
        <div class="message-content">
            <i class="fas fa-robot"></i>
            <div>
                ${isTyping ? typingIndicator : `<div class="message-text">${message}</div>`}
            </div>
        </div>
    `;
    
    messageDiv.innerHTML = messageContent;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return messageDiv;
}

function processQuestionWithBackend(question) {
    // Show typing indicator
    const typingMessage = addAssistantMessage('', true);
    
    // Send request to Flask backend with user preferences
    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            message: question,
            preferences: currentFilters
        })
    })
    .then(response => response.json())
    .then(data => {
        // Remove typing indicator
        typingMessage.remove();
        
        // Add assistant response
        addAssistantMessage(data.response);
        
        // Show recommendations section
        document.getElementById('recommendationsSection').style.display = 'block';
        
        // Update recommendations based on the question
        updateRecommendationsBasedOnQuestion(question);
    })
    .catch(error => {
        console.error('Error:', error);
        typingMessage.remove();
        addAssistantMessage('Sorry, I encountered an error. Please try again.');
    });
}

// Recommendations Management with Flask Backend
function loadRecommendations() {
    // Build query parameters from current filters
    const params = new URLSearchParams();
    params.append('career_level', currentFilters.careerLevel);
    params.append('goal', currentFilters.goal);
    currentFilters.interests.forEach(interest => {
        params.append('interests', interest);
    });

    // Fetch recommendations from Flask backend
    fetch(`/api/recommendations?${params.toString()}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                updateRecommendationsFromBackend(data.recommendations);
            }
        })
        .catch(error => {
            console.error('Error loading recommendations:', error);
        });
}

function updateRecommendationsFromBackend(recommendations) {
    const cards = document.querySelectorAll('.card');
    
    // Update course recommendations
    if (recommendations.courses.length > 0 && cards[0]) {
        const course = recommendations.courses[0];
        updateCard(cards[0], {
            title: course.title,
            description: course.description,
            type: course.type,
            icon: 'fas fa-graduation-cap',
            details: [course.duration, course.price, course.format],
            button: 'Learn More on LinkedIn',
            link: course.link
        });
    }
    
    // Update job recommendations
    if (recommendations.jobs.length > 0 && cards[1]) {
        const job = recommendations.jobs[0];
        updateCard(cards[1], {
            title: job.title,
            description: job.description,
            type: job.type,
            icon: 'fas fa-briefcase',
            details: [job.location, job.salary, job.company],
            button: 'Apply on LinkedIn',
            link: job.link
        });
    }
    
    // Update event recommendations
    if (recommendations.events.length > 0 && cards[2]) {
        const event = recommendations.events[0];
        updateCard(cards[2], {
            title: event.title,
            description: event.description,
            type: event.type,
            icon: 'fas fa-calendar',
            details: [event.date, event.location, event.price],
            button: 'Register on LinkedIn',
            link: event.link
        });
    }
    
    // Update workshop recommendations
    if (recommendations.workshops.length > 0 && cards[3]) {
        const workshop = recommendations.workshops[0];
        updateCard(cards[3], {
            title: workshop.title,
            description: workshop.description,
            type: workshop.type,
            icon: 'fas fa-tools',
            details: [workshop.duration, workshop.price, workshop.spots],
            button: 'Join on LinkedIn',
            link: workshop.link
        });
    }
}

function updateRecommendationsBasedOnQuestion(question) {
    const lowerQuestion = question.toLowerCase();
    const cards = document.querySelectorAll('.card');
    
    // Career Advancement - Focus on skill development and leadership training
    if (lowerQuestion.includes('advance') || lowerQuestion.includes('lead')) {
        updateCard(cards[0], {
            title: 'LinkedIn Learning: Becoming a Tech Lead',
            description: 'Comprehensive course series for advancing to Tech Lead position',
            type: 'COURSE',
            icon: 'fas fa-graduation-cap',
            details: ['12 hours', 'Free with LinkedIn Premium', 'Online'],
            button: 'Learn More on LinkedIn',
            link: 'https://www.linkedin.com/learning/paths/becoming-a-tech-lead'
        });
        
        updateCard(cards[1], {
            title: 'Senior Trainee Program - Tech Leadership',
            description: 'Structured program for senior developers transitioning to leadership',
            type: 'JOB',
            icon: 'fas fa-briefcase',
            details: ['Remote', 'Training + Salary', 'TechCorp'],
            button: 'Apply on LinkedIn',
            link: 'https://www.linkedin.com/jobs/search/?keywords=senior%20trainee%20tech%20lead'
        });
        
        updateCard(cards[2], {
            title: 'Tech Leadership Practice Group',
            description: 'Join a community of aspiring tech leaders for practice and mentorship',
            type: 'EVENT',
            icon: 'fas fa-calendar',
            details: ['Weekly', 'Virtual Practice Sessions', 'Free'],
            button: 'Join on LinkedIn',
            link: 'https://www.linkedin.com/groups/tech-leadership-practice'
        });
        
        updateCard(cards[3], {
            title: 'LinkedIn Learning: Executive Leadership Program',
            description: 'Advanced leadership skills for senior professionals',
            type: 'WORKSHOP',
            icon: 'fas fa-tools',
            details: ['16 weeks', 'Free with LinkedIn Premium', 'Online'],
            button: 'Join on LinkedIn',
            link: 'https://www.linkedin.com/learning/paths/executive-leadership-program'
        });
    }
    
    // Director Skills - Focus on executive development and strategic training
    if (lowerQuestion.includes('director') || lowerQuestion.includes('executive')) {
        updateCard(cards[0], {
            title: 'LinkedIn Learning: Executive Leadership Program',
            description: 'Advanced leadership skills for senior professionals',
            type: 'COURSE',
            icon: 'fas fa-graduation-cap',
            details: ['16 weeks', 'Free with LinkedIn Premium', 'Online'],
            button: 'Learn More on LinkedIn',
            link: 'https://www.linkedin.com/learning/paths/executive-leadership-program'
        });
        
        updateCard(cards[1], {
            title: 'Executive Trainee Program',
            description: 'Structured program for mid-level managers transitioning to executive roles',
            type: 'JOB',
            icon: 'fas fa-briefcase',
            details: ['Hybrid', 'Executive Training', 'Fortune 500'],
            button: 'Apply on LinkedIn',
            link: 'https://www.linkedin.com/jobs/search/?keywords=executive%20trainee%20program'
        });
        
        updateCard(cards[2], {
            title: 'Executive Leadership Practice Forum',
            description: 'Monthly practice sessions with current executives and board members',
            type: 'EVENT',
            icon: 'fas fa-calendar',
            details: ['Monthly', 'Virtual Executive Sessions', 'Premium'],
            button: 'Register on LinkedIn',
            link: 'https://www.linkedin.com/events/executive-leadership-forum'
        });
        
        updateCard(cards[3], {
            title: 'Strategic Leadership Workshop',
            description: 'Intensive workshop for developing strategic thinking and executive presence',
            type: 'WORKSHOP',
            icon: 'fas fa-tools',
            details: ['3 days', 'Executive Coaching', 'In-Person'],
            button: 'Join on LinkedIn',
            link: 'https://www.linkedin.com/learning/courses/strategic-leadership-workshop'
        });
    }
    
    // Job Search - Focus on actual job opportunities and networking events
    if (lowerQuestion.includes('job') || lowerQuestion.includes('opportunity') || lowerQuestion.includes('remote')) {
        updateCard(cards[0], {
            title: 'LinkedIn Job Search Mastery Course',
            description: 'Learn effective job search strategies and LinkedIn optimization',
            type: 'COURSE',
            icon: 'fas fa-graduation-cap',
            details: ['4 hours', 'Free with LinkedIn Premium', 'Online'],
            button: 'Learn More on LinkedIn',
            link: 'https://www.linkedin.com/learning/courses/job-search-mastery'
        });
        
        updateCard(cards[1], {
            title: 'Senior Tech Lead - Remote',
            description: 'Leading development team in innovative tech company',
            type: 'JOB',
            icon: 'fas fa-briefcase',
            details: ['Remote', '$140k-180k', 'TechCorp'],
            button: 'Apply on LinkedIn',
            link: 'https://www.linkedin.com/jobs/search/?keywords=tech%20lead%20remote'
        });
        
        updateCard(cards[2], {
            title: 'Tech Jobs Fair 2025',
            description: 'Virtual job fair with top tech companies hiring remote positions',
            type: 'EVENT',
            icon: 'fas fa-calendar',
            details: ['Dec 20, 2025', 'Virtual Job Fair', 'Free'],
            button: 'Register on LinkedIn',
            link: 'https://www.linkedin.com/company/tech-jobs-fair/'
        });
        
        updateCard(cards[3], {
            title: 'LinkedIn Networking Workshop',
            description: 'Learn how to network effectively on LinkedIn for job opportunities',
            type: 'WORKSHOP',
            icon: 'fas fa-tools',
            details: ['2 hours', 'Networking Skills', 'Virtual'],
            button: 'Join on LinkedIn',
            link: 'https://www.linkedin.com/learning/courses/linkedin-networking-workshop'
        });
    }
    
    // Leadership Workshops - Focus on learning events and skill development
    if (lowerQuestion.includes('workshop') || lowerQuestion.includes('leadership') || lowerQuestion.includes('skill')) {
        updateCard(cards[0], {
            title: 'LinkedIn Learning: Tech Leadership Course Series',
            description: 'Comprehensive leadership development for tech professionals',
            type: 'COURSE',
            icon: 'fas fa-graduation-cap',
            details: ['20 hours', 'Free with LinkedIn Premium', 'Online'],
            button: 'Learn More on LinkedIn',
            link: 'https://www.linkedin.com/learning/paths/tech-leadership-course-series'
        });
        
        updateCard(cards[1], {
            title: 'Leadership Practice Group',
            description: 'Join a community for practicing leadership skills and scenarios',
            type: 'JOB',
            icon: 'fas fa-briefcase',
            details: ['Virtual', 'Practice Sessions', 'Community'],
            button: 'Join on LinkedIn',
            link: 'https://www.linkedin.com/groups/leadership-practice-group'
        });
        
        updateCard(cards[2], {
            title: 'Leadership Learning Events Series',
            description: 'Monthly events featuring leadership experts and interactive workshops',
            type: 'EVENT',
            icon: 'fas fa-calendar',
            details: ['Monthly', 'Virtual Learning Events', 'Free'],
            button: 'Register on LinkedIn',
            link: 'https://www.linkedin.com/events/leadership-learning-series'
        });
        
        updateCard(cards[3], {
            title: 'LinkedIn Leadership Development Workshop',
            description: 'Interactive workshop for developing leadership skills',
            type: 'WORKSHOP',
            icon: 'fas fa-tools',
            details: ['8 hours', 'Free with LinkedIn Premium', 'Unlimited'],
            button: 'Join on LinkedIn',
            link: 'https://www.linkedin.com/learning/courses/leadership-development-workshop'
        });
    }
}

function updateCard(card, data) {
    if (!card) return;
    
    const header = card.querySelector('.card-header');
    const title = card.querySelector('h4');
    const description = card.querySelector('p');
    const details = card.querySelector('.card-details');
    const button = card.querySelector('.card-btn');
    
    if (header) {
        header.innerHTML = `<i class="${data.icon}"></i><span class="card-type">${data.type}</span>`;
    }
    
    if (title) title.textContent = data.title;
    if (description) description.textContent = data.description;
    
    // Update button with LinkedIn link if available
    if (button) {
        button.textContent = data.button;
        if (data.link) {
            button.onclick = function() {
                window.open(data.link, '_blank');
            };
        }
    }
    
    if (details && data.details) {
        details.innerHTML = data.details.map(detail => 
            `<span><i class="fas fa-info-circle"></i> ${detail}</span>`
        ).join('');
    }
}

function updateRecommendationsBasedOnFilters() {
    // Update recommendations based on current filters
    const cards = document.querySelectorAll('.card');
    
    if (currentFilters.goal === 'advancement') {
        // Show advancement-focused recommendations
        updateCard(cards[0], {
            title: 'LinkedIn Learning: Executive Leadership Program',
            description: 'Advanced leadership skills for senior professionals',
            type: 'COURSE',
            icon: 'fas fa-graduation-cap',
            details: ['16 weeks', 'Free with LinkedIn Premium', 'Online'],
            button: 'Learn More on LinkedIn',
            link: 'https://www.linkedin.com/learning/paths/executive-leadership-program'
        });
    }
    
    if (currentFilters.interests.includes('Technology')) {
        // Show tech-focused recommendations
        updateCard(cards[1], {
            title: 'Tech Lead Position - Remote',
            description: 'Leading development team in innovative tech company',
            type: 'JOB',
            icon: 'fas fa-briefcase',
            details: ['Remote', '$140k-180k', 'TechCorp'],
            button: 'Apply on LinkedIn',
            link: 'https://www.linkedin.com/jobs/search/?keywords=tech%20lead%20remote'
        });
    }
}

// LinkedIn Connection
function connectLinkedIn() {
    // Prompt user for LinkedIn URL
    const linkedinUrl = prompt('Please enter your LinkedIn profile URL:', 'https://www.linkedin.com/in/');
    
    if (linkedinUrl && linkedinUrl.trim() !== '') {
        connectLinkedInToBackend(linkedinUrl.trim());
    }
}

function connectLinkedInToBackend(linkedinUrl) {
    // Show loading message
    addAssistantMessage('Connecting to your LinkedIn profile...', true);
    
    fetch('/api/connect-linkedin', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            linkedin_url: linkedinUrl
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Remove loading message
            const messages = document.querySelectorAll('.message.assistant');
            const lastMessage = messages[messages.length - 1];
            if (lastMessage) {
                lastMessage.remove();
            }
            
            // Update user preferences
            updateUserPreferencesFromLinkedIn(data.updated_preferences);
            
            // Show personalized welcome message
            const welcomeMessage = `
                <h3>🎉 LinkedIn Profile Connected!</h3>
                <p><strong>${data.suggestions.welcome_message}</strong></p>
                <p>${data.suggestions.profile_summary}</p>
                
                <h4>📊 Your Profile Analysis:</h4>
                <ul>
                    <li><strong>Name:</strong> ${data.profile_data.name}</li>
                    <li><strong>Title:</strong> ${data.profile_data.title}</li>
                    <li><strong>Company:</strong> ${data.profile_data.company}</li>
                    <li><strong>Location:</strong> ${data.profile_data.location}</li>
                    <li><strong>Skills:</strong> ${data.profile_data.skills.join(', ')}</li>
                </ul>
                
                <h4>🎯 Recommended Questions for You:</h4>
                <ul>
                    ${data.suggestions.recommended_questions.map(q => `<li>${q}</li>`).join('')}
                </ul>
                
                <h4>💡 Skill Development Areas:</h4>
                <p>Consider developing: <strong>${data.suggestions.skill_gaps.join(', ')}</strong></p>
                
                <h4>🚀 Career Path Suggestion:</h4>
                <p>${data.suggestions.career_path}</p>
                
                <p><em>Your preferences have been automatically updated based on your LinkedIn profile!</em></p>
            `;
            
            addAssistantMessage(welcomeMessage);
            
            // Update recommendations
            loadRecommendations();
            
        } else {
            addAssistantMessage('Error connecting LinkedIn profile. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        addAssistantMessage('Error connecting LinkedIn profile. Please try again.');
    });
}

function updateUserPreferencesFromLinkedIn(preferences) {
    // Update current filters with LinkedIn data
    currentFilters = {
        interests: preferences.interests || currentFilters.interests,
        careerLevel: preferences.career_level || currentFilters.careerLevel,
        goal: preferences.goal || currentFilters.goal,
        industry: preferences.industry || currentFilters.industry,
        location: preferences.location || currentFilters.location,
        experience: preferences.experience || currentFilters.experience,
        linkedinConnected: true
    };
    
    // Update UI elements
    updateInterestTags();
    updateActiveFilters();
    
    // Update form elements
    updateFormElements(preferences);
}

function updateFormElements(preferences) {
    // Update career level checkboxes
    if (preferences.career_level) {
        document.querySelectorAll('input[name="career-level"]').forEach(cb => {
            cb.checked = cb.parentElement.textContent.trim().includes(preferences.career_level);
        });
    }
    
    // Update goal radio buttons
    if (preferences.goal) {
        const goalRadio = document.querySelector(`input[name="goal"][value="${preferences.goal}"]`);
        if (goalRadio) goalRadio.checked = true;
    }
    
    // Update location select
    if (preferences.location) {
        const locationSelect = document.querySelector('select');
        if (locationSelect) {
            Array.from(locationSelect.options).forEach(option => {
                if (option.text.includes(preferences.location)) {
                    locationSelect.value = option.value;
                }
            });
        }
    }
}

// CV Upload with Flask Backend
function uploadCV() {
    // Create file input element
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.pdf,.doc,.docx';
    input.onchange = function(e) {
        const file = e.target.files[0];
        if (file) {
            uploadCVToBackend(file);
        }
    };
    input.click();
}

function uploadCVToBackend(file) {
    const formData = new FormData();
    formData.append('cv_file', file);
    
    // Show loading message
    addAssistantMessage('Analyzing your CV...', true);
    
    fetch('/api/upload-cv', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Remove loading message
            const messages = document.querySelectorAll('.message.assistant');
            const lastMessage = messages[messages.length - 1];
            if (lastMessage) {
                lastMessage.remove();
            }
            
            // Add success message with analysis
            const analysis = data.analysis;
            const message = `CV uploaded successfully! Here's what I found:

**Skills Identified**: ${analysis.skills_identified.join(', ')}
**Experience Level**: ${analysis.experience_level}
**Recommended Roles**: ${analysis.recommended_roles.join(', ')}
**Skill Gaps**: ${analysis.skill_gaps.join(', ')}
**Recommended Courses**: ${analysis.recommended_courses.join(', ')}

I've updated your recommendations based on your experience!`;
            
            addAssistantMessage(message);
            loadRecommendations();
        } else {
            addAssistantMessage('Error uploading CV. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        addAssistantMessage('Error uploading CV. Please try again.');
    });
}

// Utility Functions
function resetFilters() {
    currentFilters = {
        interests: [],
        careerLevel: '',
        goal: 'advancement',
        industry: 'All Industries',
        location: 'Remote',
        experience: '3-5 years'
    };
    
    // Reset form elements
    document.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = false);
    document.querySelectorAll('input[type="radio"]').forEach(rb => rb.checked = false);
    document.querySelectorAll('select').forEach(select => select.selectedIndex = 0);
    
    // Reset interest tags
    updateInterestTags();
    updateActiveFilters();
    loadRecommendations();
    
    addAssistantMessage('Filters have been reset. I\'ve updated your recommendations based on your default preferences.');
}

function resetChatAndRecommendations() {
    // Clear chat messages
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.innerHTML = '';
    
    // Hide recommendations section
    document.getElementById('recommendationsSection').style.display = 'none';
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('LinkedIn Future Career Planning Platform initialized with Flask backend');
});

function showRecommendationPrompt(title) {
    addAssistantMessage(`Would you like more details about "${title}"?`);
}

function showDefaultRecommendations() {
    // Check if user has default preferences
    const isDefault = isDefaultPreferences(currentFilters);
    
    if (isDefault) {
        // Show recommendations section
        document.getElementById('recommendationsSection').style.display = 'block';
        
        // Update cards with default LinkedIn-focused recommendations
        updateDefaultRecommendationCards();
    }
}

function isDefaultPreferences(preferences) {
    const defaultPrefs = {
        interests: ['Technology', 'Leadership'],
        career_level: 'Entry Level',
        goal: 'advancement',
        industry: 'All Industries',
        location: 'Remote',
        experience: '3-5 years'
    };
    
    for (let key in defaultPrefs) {
        if (preferences[key]) {
            if (Array.isArray(defaultPrefs[key])) {
                if (!arraysEqual(preferences[key], defaultPrefs[key])) {
                    return false;
                }
            } else {
                if (preferences[key] !== defaultPrefs[key]) {
                    return false;
                }
            }
        }
    }
    return true;
}

function arraysEqual(a, b) {
    if (a.length !== b.length) return false;
    return a.every((val, index) => val === b[index]);
}

function updateDefaultRecommendationCards() {
    const cards = document.querySelectorAll('.card');
    
    // Default recommendations focused on career advancement (since that's the default goal)
    updateCard(cards[0], {
        title: 'LinkedIn Learning: Becoming a Tech Lead',
        description: 'Comprehensive course series for advancing to Tech Lead position',
        type: 'COURSE',
        icon: 'fas fa-graduation-cap',
        details: ['12 hours', 'Free with LinkedIn Premium', 'Online'],
        button: 'Learn More on LinkedIn',
        link: 'https://www.linkedin.com/learning/paths/becoming-a-tech-lead'
    });
    
    // Senior trainee program for skill development
    updateCard(cards[1], {
        title: 'Senior Trainee Program - Tech Leadership',
        description: 'Structured program for senior developers transitioning to leadership',
        type: 'JOB',
        icon: 'fas fa-briefcase',
        details: ['Remote', 'Training + Salary', 'TechCorp'],
        button: 'Apply on LinkedIn',
        link: 'https://www.linkedin.com/jobs/search/?keywords=senior%20trainee%20tech%20lead'
    });
    
    // Practice group for skill development
    updateCard(cards[2], {
        title: 'Tech Leadership Practice Group',
        description: 'Join a community of aspiring tech leaders for practice and mentorship',
        type: 'EVENT',
        icon: 'fas fa-calendar',
        details: ['Weekly', 'Virtual Practice Sessions', 'Free'],
        button: 'Join on LinkedIn',
        link: 'https://www.linkedin.com/groups/tech-leadership-practice'
    });
    
    // Executive leadership program for advancement
    updateCard(cards[3], {
        title: 'LinkedIn Learning: Executive Leadership Program',
        description: 'Advanced leadership skills for senior professionals',
        type: 'WORKSHOP',
        icon: 'fas fa-tools',
        details: ['16 weeks', 'Free with LinkedIn Premium', 'Online'],
        button: 'Join on LinkedIn',
        link: 'https://www.linkedin.com/learning/paths/executive-leadership-program'
    });
}
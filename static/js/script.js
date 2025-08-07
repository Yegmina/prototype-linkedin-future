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
                ${isTyping ? typingIndicator : `<p>${message}</p>`}
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
    
    // Send request to Flask backend
    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            message: question
        })
    })
    .then(response => response.json())
    .then(data => {
        // Remove typing indicator
        typingMessage.remove();
        
        // Add assistant response
        addAssistantMessage(data.response);
        
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
            button: 'Learn More'
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
            button: 'Apply Now'
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
            button: 'Register'
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
            button: 'Join Workshop'
        });
    }
}

function updateRecommendationsBasedOnQuestion(question) {
    const lowerQuestion = question.toLowerCase();
    const cards = document.querySelectorAll('.card');
    
    if (lowerQuestion.includes('advance') || lowerQuestion.includes('lead')) {
        // Update cards for career advancement
        updateCard(cards[0], {
            title: 'Advanced Leadership Program',
            description: 'Comprehensive program for senior professionals transitioning to leadership roles',
            type: 'COURSE',
            icon: 'fas fa-graduation-cap',
            details: ['12 weeks', 'Free', 'Online'],
            button: 'Enroll Now'
        });
    }
    
    if (lowerQuestion.includes('job') || lowerQuestion.includes('opportunity')) {
        // Update cards for job search
        updateCard(cards[1], {
            title: 'Senior Software Engineer - Remote',
            description: 'Leading development team in innovative fintech company',
            type: 'JOB',
            icon: 'fas fa-briefcase',
            details: ['Remote', '$130k-160k', 'FinTech Corp'],
            button: 'Apply Now'
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
    if (button) button.textContent = data.button;
    
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
            title: 'Executive Leadership Program',
            description: 'Advanced leadership skills for senior professionals',
            type: 'COURSE',
            icon: 'fas fa-graduation-cap',
            details: ['16 weeks', '$2,500', 'Hybrid'],
            button: 'Learn More'
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
            button: 'Apply Now'
        });
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
# LLM Integration for LinkedIn Future Career Planning Platform

## Overview

This document explains the LLM (Large Language Model) integration that provides dynamic, personalized responses when predefined answers are not available or when user preferences are changed.

## How It Works

### Response Selection Logic

The system uses a smart decision tree to determine which type of response to provide:

1. **Predefined Responses**: Used only for the exact four main questions with default preferences
   - "How can I advance from Senior Developer to Tech Lead?"
   - "What skills do I need for a Director position?"
   - "Show me remote job opportunities in tech"
   - "What workshops are available for leadership skills?"

2. **LLM-Generated Responses**: Used for all other scenarios
   - Any question not in the predefined list
   - When user preferences are changed from defaults
   - For personalized, context-aware responses

### LLM Integration Features

- **Google Gemini API**: Uses Google's Gemini Pro model for dynamic responses
- **Context-Aware**: Incorporates user preferences (interests, career level, goals, etc.)
- **LinkedIn-Focused**: Emphasizes LinkedIn resources and career development
- **HTML Formatting**: Converts markdown to HTML for web display
- **Fallback Support**: Graceful degradation when API is unavailable

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Key

#### Option A: Environment Variable (Recommended)
```bash
export GEMINI_API_KEY="your_gemini_api_key_here"
```

#### Option B: .env File
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Get Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key and add it to your environment

## Usage Examples

### Scenario 1: Predefined Question with Default Preferences
```python
message = "How can I advance from Senior Developer to Tech Lead?"
preferences = {
    'interests': ['Technology', 'Leadership'],
    'career_level': 'Entry Level',
    'goal': 'advancement',
    'location': 'Remote',
    'experience': '3-5 years'
}
# Result: Uses predefined response
```

### Scenario 2: Non-Predefined Question
```python
message = "What jobs should I enroll in?"
preferences = {
    'interests': ['Technology', 'Leadership'],
    'career_level': 'Entry Level',
    'goal': 'advancement',
    'location': 'Remote',
    'experience': '3-5 years'
}
# Result: Uses LLM-generated response
```

### Scenario 3: Changed Preferences
```python
message = "How can I advance from Senior Developer to Tech Lead?"
preferences = {
    'interests': ['Marketing', 'Sales'],
    'career_level': 'Senior',
    'goal': 'skill',
    'location': 'On-site',
    'experience': '6-10 years'
}
# Result: Uses LLM-generated response (preferences changed)
```

## Testing

Run the LLM integration test:

```bash
python test_llm_integration.py
```

This will test various scenarios to ensure the system correctly chooses between predefined and LLM responses.

## API Response Format

The LLM generates responses in HTML format with proper tags:

```html
<h3>Career Guidance for You</h3>
<p>Based on your interests in <strong>Technology</strong> and <strong>Leadership</strong>...</p>
<h4>Recommended Actions</h4>
<ul>
<li>Update your LinkedIn profile</li>
<li>Connect with industry professionals</li>
<li>Enroll in relevant courses</li>
</ul>
```

## Error Handling

- **API Unavailable**: Falls back to generic response
- **Invalid API Key**: Logs warning and uses fallback
- **Network Issues**: Graceful error handling with fallback
- **Rate Limiting**: Handled by Google's API client

## Benefits

1. **Personalization**: Responses tailored to user preferences
2. **Flexibility**: Handles any career-related question
3. **Consistency**: Maintains LinkedIn focus across all responses
4. **Reliability**: Fallback system ensures always-on functionality
5. **Scalability**: Can handle unlimited question variations

## Configuration

### Customizing the LLM Prompt

Edit the `_create_prompt` method in `llm_integration.py` to modify:
- Response tone and style
- LinkedIn resource emphasis
- Career advice focus areas
- HTML formatting preferences

### Adjusting Response Selection

Modify the `should_use_predefined_response` method in `predefined_responses.py` to change:
- When predefined responses are used
- Preference matching criteria
- Question matching logic

## Monitoring and Logging

The system includes comprehensive logging:
- API connection status
- Response generation success/failure
- Error details for debugging
- Performance metrics

Check the application logs for detailed information about LLM usage and any issues.

## Security Considerations

- API keys are stored as environment variables
- No sensitive data is logged
- API responses are sanitized for web display
- Rate limiting is handled automatically

## Troubleshooting

### Common Issues

1. **"LLM responses will be disabled"**
   - Check that GEMINI_API_KEY is set correctly
   - Verify the API key is valid

2. **"Error generating LLM response"**
   - Check network connectivity
   - Verify API quota and limits
   - Review error logs for details

3. **Responses not personalized**
   - Ensure user preferences are being passed correctly
   - Check the prompt generation logic

### Debug Mode

Enable debug logging to see detailed information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Future Enhancements

- Support for multiple LLM providers
- Response caching for performance
- Advanced prompt engineering
- User feedback integration
- Response quality metrics

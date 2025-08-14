import google.generativeai as genai
from decouple import config  # Add this import

class GeminiAIService:
    def __init__(self):
        api_key = config('GEMINI_API_KEY', default=None)  
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        else:
            self.model = None
    
    def generate_response(self, ticket_subject, ticket_message, category):
        if not self.model:
            return "AI service not configured. Please set GEMINI_API_KEY."
            
        prompt = f"""
        You are an experienced customer support specialist for a professional service company. Generate a helpful, empathetic, and solution-oriented response to this customer inquiry.

        TICKET DETAILS:
        Category: {category}
        Subject: {ticket_subject}
        Customer Message: {ticket_message}

        RESPONSE GUIDELINES:
        1. Start with acknowledgment and empathy
        2. Address the specific issue mentioned
        3. Provide clear, actionable solutions or next steps
        4. Include relevant troubleshooting steps for technical issues
        5. For billing issues, mention account verification and resolution timeline
        6. For general inquiries, provide comprehensive information
        7. End with offer for further assistance
        8. Keep tone professional yet friendly
        9. Length: 2-4 sentences for simple issues, up to 6 sentences for complex ones
        10. Avoid overly formal language - use conversational but professional tone

        CATEGORY-SPECIFIC APPROACHES:
        - Technical: Include troubleshooting steps, system checks, or escalation options
        - Billing: Mention account review, payment verification, or refund processes
        - General: Provide informative answers with helpful resources or contacts

        Generate only the response message, no additional formatting or labels.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"AI response temporarily unavailable. Error: {str(e)}"
from flask import Blueprint, request, jsonify
from models.faq_model import FAQ
import re

chatbot_bp = Blueprint('chatbot', __name__)

def extract_keywords(text):
    """Extract keywords from user message"""
    text = text.lower()
    # Remove common words that don't add meaning
    stop_words = {'the', 'a', 'an', 'is', 'are', 'what', 'how', 'can', 'do', 'does', 'i', 'you', 'me', 'my', 'your'}
    words = re.findall(r'\w+', text)
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    return keywords

def find_best_match(user_message):
    """Find the best matching FAQ for user's question"""
    keywords = extract_keywords(user_message)
    faqs = FAQ.find_all()
    
    best_match = None
    max_score = 0
    
    for faq in faqs:
        score = 0
        faq_keywords = faq.get('keywords', [])
        faq_question = faq.get('question', '').lower()
        faq_answer = faq.get('answer', '').lower()
        
        # Check for exact phrase matches (higher score)
        user_lower = user_message.lower()
        for faq_keyword in faq_keywords:
            if faq_keyword in user_lower:
                score += 5
        
        # Check for keyword matches
        for keyword in keywords:
            if keyword in faq_keywords:
                score += 3
            # Check if keyword is in question or answer
            if keyword in faq_question:
                score += 2
            if keyword in faq_answer:
                score += 1
            # Partial matches
            for faq_keyword in faq_keywords:
                if keyword in faq_keyword or faq_keyword in keyword:
                    score += 1
        
        if score > max_score:
            max_score = score
            best_match = faq
    
    # Return match only if score is above threshold
    return best_match if max_score >= 3 else None

@chatbot_bp.route('/ask', methods=['POST'])
def ask_chatbot():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Handle greetings
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']
        if any(greeting in user_message.lower() for greeting in greetings):
            return jsonify({
                'success': True,
                'answer': 'Hello! How can I assist you today? Feel free to ask me anything about jobs, applications, interviews, or company policies.',
                'question': None,
                'category': 'Greeting'
            }), 200
        
        # Handle thank you
        thanks = ['thank', 'thanks', 'appreciate']
        if any(thank in user_message.lower() for thank in thanks):
            return jsonify({
                'success': True,
                'answer': 'You\'re welcome! If you have any other questions, feel free to ask. I\'m here to help!',
                'question': None,
                'category': 'Thanks'
            }), 200
        
        match = find_best_match(user_message)
        
        if match:
            return jsonify({
                'success': True,
                'answer': match['answer'],
                'question': match['question'],
                'category': match.get('category', 'General')
            }), 200
        else:
            # Provide helpful fallback with suggestions
            return jsonify({
                'success': True,
                'answer': 'I\'m sorry, I couldn\'t find a specific answer to your question. Here are some things I can help you with:\n\n• Available job positions\n• Application and resume tips\n• Interview preparation\n• Hiring process timeline\n• Required skills and qualifications\n• Company policies\n\nPlease try rephrasing your question or contact HR at hr@company.com for personalized assistance.',
                'question': None,
                'category': 'Unknown'
            }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chatbot_bp.route('/faqs', methods=['GET'])
def get_all_faqs():
    try:
        faqs = FAQ.find_all()
        result = []
        for faq in faqs:
            result.append({
                'id': str(faq['_id']),
                'question': faq.get('question'),
                'answer': faq.get('answer'),
                'category': faq.get('category')
            })
        
        return jsonify({
            'success': True,
            'faqs': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chatbot_bp.route('/seed', methods=['POST'])
def seed_faqs():
    try:
        FAQ.seed_default_faqs()
        return jsonify({
            'success': True,
            'message': 'FAQs seeded successfully'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

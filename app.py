from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

CORS(app)

# Supabase Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')

if SUPABASE_URL and SUPABASE_ANON_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    print("✅ Supabase connected successfully!")
else:
    print("⚠️ Supabase credentials not found. Using fallback mode.")
    supabase = None

# Hugging Face API for sentiment analysis
def analyze_sentiment(text):
    """Analyze sentiment/emotion using Hugging Face. Robust to different response formats."""
    try:
        headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY', 'hf_demo')}"}
        payload = {"inputs": text}

        # Prefer an emotion model for richer labels; fallback to sentiment if unavailable
        model_urls = [
            # Emotions: joy, sadness, anger, fear, disgust, surprise, neutral
            "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base",
            # Sentiment: positive/neutral/negative (twitter roberta latest)
            "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest",
            # Sentiment (binary): POSITIVE/NEGATIVE
            "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english",
        ]

        def parse_predictions(predictions):
            # Expected shapes:
            # [[{"label":"joy","score":0.91}, ...]]
            # [[{"label":"positive","score":0.93}, ...]]
            # [[{"label":"LABEL_0","score":0.7}, ...]]
            if not isinstance(predictions, list) or len(predictions) == 0:
                return None
            scores = predictions[0]
            if not isinstance(scores, list) or len(scores) == 0:
                return None
            best = max(scores, key=lambda x: x.get('score', 0))
            raw_label = str(best.get('label', '')).upper()

            # Normalize labels
            label_map = {
                'LABEL_0': 'negative',
                'LABEL_1': 'neutral',
                'LABEL_2': 'positive',
                'NEGATIVE': 'negative',
                'NEUTRAL': 'neutral',
                'POSITIVE': 'positive',
                'JOY': 'happy',
                'SADNESS': 'sad',
                'ANGER': 'angry',
                'FEAR': 'fear',
                'DISGUST': 'disgust',
                'SURPRISE': 'surprise',
            }
            normalized = label_map.get(raw_label, raw_label.lower() if raw_label else 'neutral')
            return {
                'emotion_label': normalized,
                'sentiment_score': float(best.get('score', 0.5))
            }

        for url in model_urls:
            try:
                r = requests.post(url, headers=headers, json=payload, timeout=20)
                if r.status_code == 200:
                    parsed = parse_predictions(r.json())
                    if parsed:
                        return parsed
            except Exception as api_err:
                print(f"HF request error for {url}: {api_err}")

        # Fallback if all models fail
        return {'emotion_label': 'neutral', 'sentiment_score': 0.5}

    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return {'emotion_label': 'neutral', 'sentiment_score': 0.5}

# IntaSend Payment Integration
def create_intasend_payment(amount, plan_type):
    """Create payment using IntaSend API"""
    try:
        # IntaSend API configuration
        INTASEND_API_KEY = os.getenv('INTASEND_API_KEY')
        INTASEND_PUBLISHABLE_KEY = os.getenv('INTASEND_PUBLISHABLE_KEY')
        
        if not INTASEND_API_KEY:
            # Fallback for demo purposes
            return {
                'success': True,
                'payment_url': 'https://intasend.com/demo-payment',
                'payment_id': f'demo_{datetime.now().strftime("%Y%m%d%H%M%S")}'
            }
        
        # IntaSend API endpoint
        API_URL = "https://api.intasend.com/v1/checkout/"
        
        headers = {
            "Authorization": f"Bearer {INTASEND_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "amount": amount,
            "currency": "USD",
            "description": f"Mood Journal {plan_type.title()} Plan",
            "success_url": "http://localhost:5000/payment/success",
            "cancel_url": "http://localhost:5000/payment/cancel",
            "metadata": {
                "plan_type": plan_type,
                "app": "mood_journal"
            }
        }
        
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            return {
                'success': True,
                'payment_url': result.get('payment_url'),
                'payment_id': result.get('payment_id')
            }
        else:
            print(f"IntaSend API error: {response.text}")
            return {
                'success': False,
                'error': 'Payment initialization failed'
            }
            
    except Exception as e:
        print(f"Error creating IntaSend payment: {e}")
        return {
            'success': False,
            'error': str(e)
        }

@app.route('/')
def index():
    """Serve the main application"""
    return render_template('index.html')

@app.route('/api/entries', methods=['GET'])
def get_entries():
    """Get all journal entries from Supabase"""
    try:
        if supabase:
            # Query from Supabase
            response = supabase.table('journal_entries').select('*').order('created_at', desc=True).execute()
            entries = response.data
        else:
            # Fallback: return empty list
            entries = []
        
        return jsonify(entries)
    except Exception as e:
        print(f"Error getting entries: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/analyze', methods=['POST'])
def analyze_emotion():
    """Analyze emotion without saving to database"""
    try:
        data = request.get_json()
        content = data.get('content', '').strip()
        
        if not content:
            return jsonify({'error': 'Content is required'}), 400
        
        # Analyze sentiment
        sentiment_result = analyze_sentiment(content)

        # Add AI provider info and friendlier message
        label = sentiment_result.get('emotion_label', 'neutral')
        score = sentiment_result.get('sentiment_score', 0.5)
        sentiment_result['ai_provider'] = 'huggingface'
        if label in ['happy', 'joy', 'positive']:
            message = "You're expressing positive feelings. Keep noting what made your day better."
        elif label in ['sad', 'negative']:
            message = "I'm sensing sadness. Consider writing what might help you feel a bit better."
        elif label in ['angry']:
            message = "There’s anger in your words. A short break or deep breaths could help."
        elif label in ['fear']:
            message = "I see some fear/anxiety. Identifying one small step can reduce it."
        elif label in ['disgust']:
            message = "You might be feeling aversion. Noting triggers can provide clarity."
        elif label in ['surprise']:
            message = "Surprise detected. Capture what was unexpected and how you felt."
        else:
            message = "Neutral tone detected. Add more detail to capture your feelings."
        sentiment_result['detailed_analysis'] = f"{label.title()} ({score*100:.0f}%). {message}"
        
        return jsonify(sentiment_result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/entries', methods=['POST'])
def create_entry():
    """Create a new journal entry with sentiment analysis"""
    try:
        data = request.get_json()
        content = data.get('content', '').strip()
        
        if not content:
            return jsonify({'error': 'Content is required'}), 400
        
        # Get emotion data from request or analyze if not provided
        emotion_label = data.get('emotion_label')
        sentiment_score = data.get('sentiment_score')
        ai_provider = data.get('ai_provider', 'huggingface')
        detailed_analysis = data.get('detailed_analysis')
        
        if not emotion_label or sentiment_score is None:
            # Analyze sentiment if not provided
            sentiment_result = analyze_sentiment(content)
            emotion_label = sentiment_result['emotion_label']
            sentiment_score = sentiment_result['sentiment_score']
            ai_provider = sentiment_result.get('ai_provider', 'huggingface')
            detailed_analysis = sentiment_result.get('detailed_analysis')
        
        # Prepare entry data
        entry_data = {
            'content': content,
            'sentiment_score': sentiment_score,
            'emotion_label': emotion_label,
            'ai_provider': ai_provider,
            'detailed_analysis': detailed_analysis
        }
        
        if supabase:
            # Insert into Supabase
            response = supabase.table('journal_entries').insert(entry_data).execute()
            new_entry = response.data[0] if response.data else entry_data
        else:
            # Fallback: return the data without saving
            new_entry = entry_data
            new_entry['id'] = datetime.now().timestamp()
            print("⚠️ Supabase not available. Entry not saved.")
        
        return jsonify(new_entry), 201
        
    except Exception as e:
        print(f"Error creating entry: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/entries/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    """Delete a journal entry from Supabase"""
    try:
        if supabase:
            # Delete from Supabase
            supabase.table('journal_entries').delete().eq('id', entry_id).execute()
        else:
            print("⚠️ Supabase not available. Entry not deleted.")
        
        return jsonify({'message': 'Entry deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get mood statistics for charts from Supabase"""
    try:
        if supabase:
            # Get all entries from Supabase
            response = supabase.table('journal_entries').select('*').execute()
            entries = response.data
        else:
            # Fallback: return empty stats
            entries = []
        
        # Count emotions
        emotion_counts = {}
        for entry in entries:
            emotion = entry.get('emotion_label', 'neutral')
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Get recent entries for trend
        recent_entries = entries[:10]  # Get last 10 entries
        trend_data = [
            {
                'date': entry.get('created_at', '').split('T')[0] if entry.get('created_at') else '',
                'score': entry.get('sentiment_score', 0.5),
                'emotion': entry.get('emotion_label', 'neutral')
            }
            for entry in recent_entries
        ]
        
        return jsonify({
            'emotion_counts': emotion_counts,
            'trend_data': trend_data,
            'total_entries': len(entries)
        })
        
    except Exception as e:
        print(f"Error getting stats: {e}")
        return jsonify({'error': str(e)}), 500

# Payment Routes
@app.route('/api/payment/initiate', methods=['POST'])
def initiate_payment():
    """Initiate payment with IntaSend"""
    try:
        data = request.get_json()
        plan_type = data.get('plan_type', 'basic')
        amount = data.get('amount', 5.99)
        
        # Create payment record in Supabase
        payment_data = {
            'plan_type': plan_type,
            'amount': amount,
            'status': 'pending'
        }
        
        if supabase:
            response = supabase.table('payments').insert(payment_data).execute()
            payment = response.data[0] if response.data else payment_data
        else:
            payment = payment_data
            payment['id'] = datetime.now().timestamp()
            print("⚠️ Supabase not available. Payment not saved.")
        
        # Create IntaSend payment
        payment_result = create_intasend_payment(amount, plan_type)
        
        if payment_result['success']:
            # Update payment record with IntaSend payment ID
            if supabase and payment.get('id'):
                supabase.table('payments').update({
                    'intasend_payment_id': payment_result.get('payment_id')
                }).eq('id', payment['id']).execute()
            
            return jsonify({
                'success': True,
                'payment_url': payment_result['payment_url'],
                'payment_id': payment.get('id')
            })
        else:
            return jsonify({
                'success': False,
                'error': payment_result.get('error', 'Payment failed')
            }), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/payment/success')
def payment_success():
    """Handle successful payment"""
    payment_id = request.args.get('payment_id')
    
    if payment_id and supabase:
        try:
            supabase.table('payments').update({
                'status': 'completed'
            }).eq('intasend_payment_id', payment_id).execute()
        except Exception as e:
            print(f"Error updating payment status: {e}")
    
    return render_template('payment_success.html')

@app.route('/payment/cancel')
def payment_cancel():
    """Handle cancelled payment"""
    payment_id = request.args.get('payment_id')
    
    if payment_id and supabase:
        try:
            supabase.table('payments').update({
                'status': 'cancelled'
            }).eq('intasend_payment_id', payment_id).execute()
        except Exception as e:
            print(f"Error updating payment status: {e}")
    
    return render_template('payment_cancel.html')

@app.route('/api/payments', methods=['GET'])
def get_payments():
    """Get all payments from Supabase"""
    try:
        if supabase:
            response = supabase.table('payments').select('*').order('created_at', desc=True).execute()
            payments = response.data
        else:
            payments = []
        
        return jsonify(payments)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

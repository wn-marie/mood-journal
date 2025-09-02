# Simple test without external API calls
import requests
import json

BASE_URL = "http://localhost:5000"

def test_basic_functionality():
    print("🧪 Testing Basic Functionality...")
    
    # Test 1: Check if server is running
    print("\n1. Testing server connection...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print(f"❌ Server returned: {response.status_code}")
    except Exception as e:
        print(f"❌ Server connection failed: {e}")
        return
    
    # Test 2: Test emotion analysis with fallback
    print("\n2. Testing emotion analysis...")
    try:
        response = requests.post(f"{BASE_URL}/api/ai/analyze", 
                               json={"content": "I had a wonderful day today!"})
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Emotion analysis working: {result['emotion_label']} ({result['sentiment_score']:.2f})")
        else:
            print(f"❌ Emotion analysis failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Emotion analysis error: {e}")
    
    # Test 3: Create entry with emotion data
    print("\n3. Testing entry creation with emotion data...")
    try:
        entry_data = {
            "content": "I'm feeling great today!",
            "emotion_label": "positive",
            "sentiment_score": 0.85,
            "ai_provider": "huggingface",
            "detailed_analysis": "User shows positive emotions with high confidence."
        }
        response = requests.post(f"{BASE_URL}/api/entries", json=entry_data)
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Entry created: ID {result['id']}")
        else:
            print(f"❌ Entry creation failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Entry creation error: {e}")
    
    # Test 4: Get entries
    print("\n4. Testing get entries...")
    try:
        response = requests.get(f"{BASE_URL}/api/entries")
        if response.status_code == 200:
            entries = response.json()
            print(f"✅ Retrieved {len(entries)} entries")
            if entries:
                print(f"   Latest entry: {entries[0]['content'][:50]}...")
        else:
            print(f"❌ Get entries failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Get entries error: {e}")
    
    print("\n🎉 Basic Testing Complete!")

if __name__ == "__main__":
    test_basic_functionality()

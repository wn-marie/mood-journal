# Test script to verify all features are working
import requests
import json

BASE_URL = "http://localhost:5000"

def test_api_endpoints():
    print("🧪 Testing Mood Journal API Endpoints...")
    
    # Test 1: Analyze emotion
    print("\n1. Testing emotion analysis...")
    try:
        response = requests.post(f"{BASE_URL}/api/ai/analyze", 
                               json={"content": "I had a wonderful day today!"})
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Emotion analysis working: {result['emotion_label']} ({result['sentiment_score']:.2f})")
        else:
            print(f"❌ Emotion analysis failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Emotion analysis error: {e}")
    
    # Test 2: Create entry
    print("\n2. Testing entry creation...")
    try:
        response = requests.post(f"{BASE_URL}/api/entries", 
                               json={"content": "I'm feeling great today!"})
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Entry created: ID {result['id']}")
        else:
            print(f"❌ Entry creation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Entry creation error: {e}")
    
    # Test 3: Get entries
    print("\n3. Testing get entries...")
    try:
        response = requests.get(f"{BASE_URL}/api/entries")
        if response.status_code == 200:
            entries = response.json()
            print(f"✅ Retrieved {len(entries)} entries")
        else:
            print(f"❌ Get entries failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get entries error: {e}")
    
    # Test 4: Get stats
    print("\n4. Testing get stats...")
    try:
        response = requests.get(f"{BASE_URL}/api/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Stats retrieved: {stats['total_entries']} total entries")
            print(f"   Emotion counts: {stats['emotion_counts']}")
        else:
            print(f"❌ Get stats failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get stats error: {e}")
    
    # Test 5: Payment initiation
    print("\n5. Testing payment initiation...")
    try:
        response = requests.post(f"{BASE_URL}/api/payment/initiate", 
                               json={"plan_type": "basic", "amount": 5.99})
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Payment initiated: {result.get('payment_id', 'N/A')}")
        else:
            print(f"❌ Payment initiation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Payment initiation error: {e}")
    
    print("\n🎉 API Testing Complete!")

if __name__ == "__main__":
    test_api_endpoints()

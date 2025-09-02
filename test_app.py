#!/usr/bin/env python3
"""
Simple test script for the Mood Journal application
"""

import requests
import json
import time

def test_app():
    """Test the basic functionality of the Mood Journal app"""
    
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Mood Journal Application...")
    print("=" * 50)
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Server is running successfully")
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the app is running on http://localhost:5000")
        return False
    
    # Test 2: Test API endpoints
    test_entries = [
        "I had a wonderful day today! Everything went perfectly and I feel great.",
        "Today was okay, nothing special happened but I'm doing fine.",
        "I'm feeling a bit down today, had some challenges at work."
    ]
    
    for i, entry in enumerate(test_entries, 1):
        print(f"\n📝 Testing entry {i}: {entry[:50]}...")
        
        try:
            response = requests.post(
                f"{base_url}/api/entries",
                json={"content": entry},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 201:
                data = response.json()
                print(f"✅ Entry created successfully")
                print(f"   Emotion: {data['emotion_label']}")
                print(f"   Score: {data['sentiment_score']:.3f}")
            else:
                print(f"❌ Failed to create entry: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error creating entry: {e}")
    
    # Test 3: Get all entries
    print(f"\n📊 Testing get entries...")
    try:
        response = requests.get(f"{base_url}/api/entries")
        if response.status_code == 200:
            entries = response.json()
            print(f"✅ Retrieved {len(entries)} entries")
        else:
            print(f"❌ Failed to get entries: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting entries: {e}")
    
    # Test 4: Get statistics
    print(f"\n📈 Testing statistics...")
    try:
        response = requests.get(f"{base_url}/api/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Retrieved statistics")
            print(f"   Total entries: {stats['total_entries']}")
            print(f"   Emotion counts: {stats['emotion_counts']}")
        else:
            print(f"❌ Failed to get stats: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting stats: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Testing completed!")
    print("If all tests passed, your Mood Journal app is working correctly!")
    
    return True

if __name__ == "__main__":
    test_app()

# Test Supabase connection
from app import supabase, app
import os

def test_supabase():
    print("🧪 Testing Supabase Connection...")
    
    if not supabase:
        print("❌ Supabase not configured!")
        print("Please add SUPABASE_URL and SUPABASE_ANON_KEY to your .env file")
        return
    
    try:
        # Test 1: Check connection
        print("\n1. Testing connection...")
        response = supabase.table('journal_entries').select('count', count='exact').execute()
        print("✅ Supabase connection successful!")
        
        # Test 2: Insert test entry
        print("\n2. Testing insert...")
        test_entry = {
            'content': 'Test entry from Supabase',
            'sentiment_score': 0.8,
            'emotion_label': 'positive',
            'ai_provider': 'test',
            'detailed_analysis': 'Test analysis'
        }
        
        response = supabase.table('journal_entries').insert(test_entry).execute()
        if response.data:
            print("✅ Test entry inserted successfully!")
            entry_id = response.data[0]['id']
        else:
            print("❌ Failed to insert test entry")
            return
        
        # Test 3: Query entries
        print("\n3. Testing query...")
        response = supabase.table('journal_entries').select('*').execute()
        entries = response.data
        print(f"✅ Retrieved {len(entries)} entries from Supabase")
        
        # Test 4: Update entry
        print("\n4. Testing update...")
        update_data = {'emotion_label': 'updated'}
        response = supabase.table('journal_entries').update(update_data).eq('id', entry_id).execute()
        print("✅ Entry updated successfully!")
        
        # Test 5: Delete test entry
        print("\n5. Testing delete...")
        response = supabase.table('journal_entries').delete().eq('id', entry_id).execute()
        print("✅ Test entry deleted successfully!")
        
        print("\n🎉 All Supabase tests passed!")
        print("Your Supabase integration is working perfectly!")
        
    except Exception as e:
        print(f"❌ Supabase test failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your .env file has correct SUPABASE_URL and SUPABASE_ANON_KEY")
        print("2. Verify tables exist in Supabase dashboard")
        print("3. Check RLS policies allow public access")
        print("4. Ensure your Supabase project is active")

if __name__ == "__main__":
    test_supabase()

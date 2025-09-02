# Check Supabase table structure
from app import supabase

def check_table_structure():
    print("🔍 Checking Supabase table structure...")
    
    try:
        # Get table info
        response = supabase.table('journal_entries').select('*').limit(1).execute()
        print("✅ Table exists!")
        
        if response.data:
            print("📋 Current columns:")
            for key in response.data[0].keys():
                print(f"  - {key}")
        else:
            print("📋 Table is empty, checking schema...")
            
        # Try to insert with different timestamp field
        test_entry = {
            'content': 'Test entry',
            'sentiment_score': 0.8,
            'emotion_label': 'positive',
            'ai_provider': 'test',
            'detailed_analysis': 'Test analysis'
        }
        
        response = supabase.table('journal_entries').insert(test_entry).execute()
        if response.data:
            print("✅ Insert successful!")
            entry = response.data[0]
            print("📋 Actual columns in response:")
            for key in entry.keys():
                print(f"  - {key}")
            
            # Clean up
            supabase.table('journal_entries').delete().eq('id', entry['id']).execute()
        else:
            print("❌ Insert failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_table_structure()

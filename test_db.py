# Database test script
from app import app, db, JournalEntry

def test_database():
    print("🧪 Testing Database Connection...")
    
    with app.app_context():
        try:
            # Test database connection
            with db.engine.connect() as conn:
                conn.execute(db.text("SELECT 1"))
            print("✅ Database connection successful")
            
            # Test table creation
            db.create_all()
            print("✅ Tables created/verified")
            
            # Test inserting a record
            test_entry = JournalEntry(
                content="Test entry",
                sentiment_score=0.8,
                emotion_label="positive",
                ai_provider="test",
                detailed_analysis="Test analysis"
            )
            db.session.add(test_entry)
            db.session.commit()
            print("✅ Test entry inserted successfully")
            
            # Test querying
            entries = JournalEntry.query.all()
            print(f"✅ Retrieved {len(entries)} entries from database")
            
            # Clean up test entry
            db.session.delete(test_entry)
            db.session.commit()
            print("✅ Test entry cleaned up")
            
        except Exception as e:
            print(f"❌ Database error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_database()

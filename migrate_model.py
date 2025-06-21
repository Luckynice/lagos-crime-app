# Run this ONCE to fix existing tuple models
import joblib

print("🔧 Migrating old model format...")
try:
    old_model = joblib.load("models/crime_model.pkl")
    
    if isinstance(old_model, tuple):
        print("Found tuple format - extracting pipeline...")
        pipeline = old_model[0]
        joblib.dump(pipeline, "models/crime_model.pkl")
        print("✅ Migration successful!")
    else:
        print("Model already in correct format")
except Exception as e:
    print(f"❌ Migration failed: {e}")
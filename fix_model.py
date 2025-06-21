import joblib

# Load the tuple
model_tuple = joblib.load("models/crime_model.pkl")

# Extract the pipeline (assuming it's first element)
pipeline = model_tuple[0]  

# Re-save JUST the pipeline
joblib.dump(pipeline, "models/crime_model_fixed.pkl")

print("✅ Model re-saved as single pipeline object")
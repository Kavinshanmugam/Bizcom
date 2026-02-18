import pandas as pd
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# This is necessary so your browser doesn't block the data
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Define the path to your data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "data", "AI_Risk_Questions.csv")

# 2. Function to load questions
def load_questions_from_csv():
    if not os.path.exists(CSV_FILE):
        print(f"ERROR: File not found at {CSV_FILE}")
        return []
    
    # Load the CSV
    df = pd.read_csv(CSV_FILE)
    
    # Clean up column names (removes hidden spaces)
    df.columns = df.columns.str.strip()
    
    # Return as a list of dictionaries
    return df.to_dict(orient="records")

# 3. Create an API endpoint to serve these questions
@app.get("/api/questions")
async def get_questions():
    questions = load_questions_from_csv()
    return {"count": len(questions), "data": questions}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

from fastapi import FastAPI, HTTPException
import pandas as pd

app = FastAPI()

# Load CSV into DataFrame (adjust filename as needed)
CSV_FILE = "data.csv"
df = pd.read_csv(CSV_FILE)

@app.get("/")
def home():
    return {"message": "CSV REST API is running"}

@app.get("/data")
def get_all_data():
    """Return entire CSV as JSON"""
    return df.to_dict(orient="records")

@app.get("/data/{row_id}")
def get_row(row_id: int):
    """Return a specific row by index"""
    if 0 <= row_id < len(df):
        return df.iloc[row_id].to_dict()
    raise HTTPException(status_code=404, detail="Row not found")

@app.get("/filter")
def filter_data(column: str, value: str):
    """Filter data by column value"""
    if column not in df.columns:
        raise HTTPException(status_code=400, detail="Invalid column name")
    filtered = df[df[column].astype(str) == value]
    return filtered.to_dict(orient="records")
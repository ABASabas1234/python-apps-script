from fastapi import FastAPI
import numpy as np
import pandas as pd

app = FastAPI(title="Python Apps Script API")

@app.get("/")
def home():
    return {"status": "Python server is running"}

@app.get("/calculate")
def calculate():
    numbers = np.array([10, 20, 30])
    data = pd.DataFrame({"numbers": numbers})

    return {
        "total": int(data["numbers"].sum()),
        "average": float(data["numbers"].mean())
    }

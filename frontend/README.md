### Installation

#### Backend

1. ```cd backend```

2. ```python -m venv venv```

3. ```source venv/bin/activate  # On Windows use `venv\Scripts\activate```

4. ```pip install -r requirements.txt```

5. ```pip install fastapi[all]```

#### Frontend

1. ```npm install```


### Running the application

1. Backend

```uvicorn app.main:app --reload --host 0.0.0.0 --port 8000```

2. Frontend

```npm run dev```
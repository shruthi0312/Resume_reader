Steps to Get Project working

1) Create Virtual Environment.
    python -m venv venv

2) Acticate Virtual Environment
    venv\Scripts\activate (Windows)
    source venv/bin/activate (macOS)

3) installing Requirements
    pip install -r requirements.txt

4) Run Server using Uvicorn
    uvicorn main:app --reload
    main -> it it the file where our APIs are
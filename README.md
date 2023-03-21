# Social Media App API using FastAPI

This is a simple API built using FastAPI framework that serves as a backend for a social media application. This API can be used to perform basic CRUD (Create, Read, Update, Delete) operations on user profiles, posts, comments and likes.

## Requirements

To use this API, you need the following:

- Python 3.7+
- FastAPI
- SQLAlchemy
- uvicorn (ASGI server)

## Installation

1. Clone the repository:
    
    ```git clone https://github.com/ReuelNixon/Social-Media-App-API.git```

2. Navigate to the project directory:
        
    ```cd Social-Media-App-API```

3. Create a virtual environment:
    
    ```python -m venv venv```

4. Activate the virtual environment:
    
    ```venv\Scripts\activate```

5. Install the requirements:
    
    ```pip install -r requirements.txt```

6. Start the server:
    
    ```uvicorn app.main:app --reload```

7. Go to http://127.0.0.1:8000/docs to access the interactive API documentation using Swagger UI.

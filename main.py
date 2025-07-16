from fastapi import Body, FastAPI


app = FastAPI()

@app.get('/')
def hello() -> dict:
    return {"message" : "Hello World!"}

@app.get('/posts')
def post() -> dict:
    return {'data': 'this is the post'}

@app.post('/createposts')
def create_posts(payload: dict = Body(...)) -> dict:
    return {'message': 'post created successfully', "post": payload}


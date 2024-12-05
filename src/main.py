from fastapi import FastAPI

app = FastAPI()

if __name__ == '__main__':
    print("Yo tout le monde c'est gotaga")

@app.get("/")
async def read_root():
    return {"Hello": "World"}
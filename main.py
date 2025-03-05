from fastapi import FastAPI
import uvicorn

try:
    from app.router import router as routes
except Exception as e:
    print(f"Error importing routes: {e}")

app = FastAPI(title="Blog Management API")


@app.get("/")
def root():
    return {"msg": "Welcome to Root"}


app.include_router(routes)


if __name__ == "__main__":
    uvicorn.run(app)

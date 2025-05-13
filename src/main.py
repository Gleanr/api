from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from routers.auth import router as auth_router
from routers.article import router as articles_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(articles_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")

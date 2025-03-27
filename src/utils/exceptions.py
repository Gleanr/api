from fastapi import HTTPException, status


def raise_unauthorized_exception(detail: str = "Incorrect username or password"):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
    )


def user_exists_exception(detail: str = "Username already exists"):
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=detail,
    )

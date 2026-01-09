from fastapi.responses import RedirectResponse

def get():
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response

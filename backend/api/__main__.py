'''
if __name__ == "__main__":
    from backend.api.api import app
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=3321)
    '''
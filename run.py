import uvicorn






if __name__ == '__main__':
    uvicorn.run("app.main:app", host='localhost', port=8000, log_level="info",workers=4, reload = True)
    print("running")
"""
FastAPI controller.
"""
import socket

import uvicorn
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "We Live Baby."}


# non api fx
def get_free_port():
    s = socket.socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port


if __name__ == "__main__":
    uvicorn.run('api:app', host='localhost', port=1337, reload=True)
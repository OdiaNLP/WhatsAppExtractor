import os
import re

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from starlette.responses import FileResponse

from wextractor.extractor import process_file, write_extract_file

app = FastAPI()


@app.post("/files/")
async def create_files(file: UploadFile = File(...)):
    file2store = await file.read()
    csv_list = process_file(re.compile(r'\n(?=\d)').split(file2store.decode("utf-8")))
    op_filename = os.path.join(os.getcwd(), "report_file.csv")
    await write_extract_file(op_filename, csv_list)
    return FileResponse(op_filename, media_type='application/octet-stream', filename="report.csv")


@app.get("/")
async def main():
    content = """
    <body>
    <form action="/files/" enctype="multipart/form-data" method="post">
    <input name="file" type="file" multiple>
    <input type="submit">
    </form>
    </body>
    """
    return HTMLResponse(content=content)

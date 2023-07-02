import argparse
from tempfile import TemporaryDirectory

import uvicorn
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from minutes_maker import MinutesMaker


class OutputData(BaseModel):
    timeline: str
    summary: str


class MinutesMakerAPI:
    def __init__(self, model: str, cpu_threads: int = 1, num_workers: int = 1):
        self.app = FastAPI()
        self.mm = MinutesMaker(
            model=model, cpu_threads=cpu_threads, num_workers=num_workers
        )

        self.app.add_api_route(
            "/minutes_maker",
            self.minutes_maker,
            methods=["POST"],
            response_model=OutputData,
        )
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    async def minutes_maker(
        self,
        file: UploadFile = File(...),
        filename: str = Form(...),
        language: str = Form(...),
        category: str = Form(...),
        content: str = Form(...),
    ) -> OutputData:
        file = await file.read()
        with TemporaryDirectory() as tempdir:
            # use the same extension as the uploaded file
            with open(f"{tempdir}/{filename}", "wb") as f:
                f.write(file)
            timeline, summary = self.mm(
                audio_or_video_file_path=f"{tempdir}/{filename}",
                language=language,
                category=category,
                content=content,
            )
        return OutputData(timeline=timeline, summary=summary)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "-m",
        "--model",
        type=str,
        default="gpt-3.5-turbo-16k-0613",
        help="model name for summarization (default: gpt-3.5-turbo-16k-0613)",
    )
    argparser.add_argument(
        "-t",
        "--cpu_threads",
        type=int,
        default=0,
        help="number of threads for CPU whisper inference (default: 0 for auto)",
    )
    argparser.add_argument(
        "-w",
        "--num_workers",
        type=int,
        default=1,
        help="number of workers for whisper inference (default: 1 for non-parallel)",
    )
    argparser.add_argument(
        "-p",
        "--port",
        type=int,
        default=10355,
        help="port number for API (default: 10355)",
    )
    args = argparser.parse_args()

    mm_api = MinutesMakerAPI(
        model=args.model, cpu_threads=args.cpu_threads, num_workers=args.num_workers
    )
    uvicorn.run(mm_api.app, host="0.0.0.0", port=args.port)

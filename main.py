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
    """
    API for Minutes Maker.

    Attributes
    ----------
    app : FastAPI
        FastAPI instance.
    mm : MinutesMaker
        MinutesMaker instance.

    Methods
    -------
    minutes_maker
        Minutes Maker API endpoint.
    """

    def __init__(self, model: str, cpu_threads: int = 0, num_workers: int = 1):
        """
        Initialize MinutesMakerAPI.

        Parameters
        ----------
        model : str
            model name for summarization.
        cpu_threads : int, optional
            number of threads for CPU whisper inference,
            by default 0 for auto.
        num_workers : int, optional
            number of workers for whisper inference,
            by default 1 for non-parallel.
        """
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
        """
        Minutes Maker API endpoint called when a POST request is sent to
        "/minutes_maker".

        This method is composed of the following steps:

        1. Save the file to a temporary directory.
        2. Make timeline and summary of the meeting or lecture.
        3. Return timeline and summary.

        Parameters
        ----------
        file : UploadFile
            audio or video file.
        filename : str
            filename of the uploaded file.
        language : str
            language of the uploaded file, "en" or "ja".
        category : str
            category of the uploaded file, "meeting" or "lecture".
        content : str
            topic of the meeting or lecture in the uploaded file.

        Returns
        -------
        OutputData
            timeline and summary of the uploaded file.
        """
        # 0. await file.read() to get bytes
        file = await file.read()

        with TemporaryDirectory() as tempdir:
            # 1. save the file to a temporary directory
            with open(f"{tempdir}/{filename}", "wb") as f:
                f.write(file)

            # 2. make timeline and summary of the meeting or lecture
            timeline, summary = self.mm(
                audio_or_video_file_path=f"{tempdir}/{filename}",
                language=language,
                category=category,
                content=content,
            )

        # 3. return timeline and summary
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

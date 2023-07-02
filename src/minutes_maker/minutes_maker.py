import logging
import subprocess
from typing import Literal, Union

from dotenv import load_dotenv

from ._prompts import (
    EnglishLecturePrompts,
    EnglishMeetingPrompts,
    JapaneseLecturePrompts,
    JapaneseMeetingPrompts,
)
from ._summarizer import Summarizer
from ._transcriber import Transcriber

load_dotenv()

logging.basicConfig(level=logging.INFO)


class MinutesMaker:
    def __init__(
        self,
        model: str = "gpt-3.5-turbo-16k-0613",
        *,
        cpu_threads: int = 0,
        num_workers: int = 1,
    ) -> None:
        """
        Initialize the MinutesMaker class with a Summarizer and
        a Transcriber.

        Parameters
        ----------
        model : str, optional
            The OpenAI model to be used for summarization,
            by default "gpt-3.5-turbo-16k-0613".
        cpu_threads : int, optional
            The number of CPU threads to use for inference,
            by default 0 (auto).
        num_workers : int, optional
            The number of workers to use for inference,
            by default 1 (non-parallel).
        """
        self.__summarizer = Summarizer(model=model)
        self.__transcriber = Transcriber(
            device="cuda" if self.__check_cuda() else "cpu",
            cpu_threads=cpu_threads,
            num_workers=num_workers,
        )

        # Somehow cannot extend the Enum class,
        # we cannot make base class for prompts.
        self.__prompts: Union[
            JapaneseLecturePrompts,
            JapaneseMeetingPrompts,
            EnglishLecturePrompts,
            EnglishMeetingPrompts,
        ] = None

    def __call__(
        self,
        audio_or_video_file_path: str,
        language: Literal["ja", "en"] = "ja",
        category: Literal["meeting", "lecture"] = "meeting",
        content: str = "",
        *,
        beam_size: int = 5,
    ) -> tuple[str, str]:
        """
        Transcribe and summarize an audio or video file.

        Parameters
        ----------
        audio_or_video_file_path : str
            The path to the audio or video file to be summarized.
        language : Literal["ja", "en"], optional
            The language of the text to be summarized,
            by default "ja".
        category : Literal["meeting", "lecture"], optional
            The type of the audio to be summarized,
            by default "meeting"
        content : str, optional
            The content of the audio or video file to be summarized.
            e.g. 商品開発, engineering, etc.
            by default "".
        beam_size : int, optional
            The beam size to use for inference,
            by default 5.

        Returns
        -------
        tuple[str, str]
            The transcribed timeline and its summary.
        """
        if language == "ja":
            if category == "meeting":
                self.__prompts = JapaneseMeetingPrompts
            elif category == "lecture":
                self.__prompts = JapaneseLecturePrompts
            else:
                raise ValueError(
                    f"category must be either 'meeting' or 'lecture', but got {category}."
                )
        elif language == "en":
            if category == "meeting":
                self.__prompts = EnglishMeetingPrompts
            elif category == "lecture":
                self.__prompts = EnglishLecturePrompts
            else:
                raise ValueError(
                    f"category must be either 'meeting' or 'lecture', but got {category}."
                )

        results = self.__transcriber.convert_and_transcribe(
            audio_or_video_file_path,
            prompt=self.__prompts.TRANSCRIBE_FORMAT.value.format(content=content),
            beam_size=beam_size,
        )
        return results.timeline, self.__summarizer.summarize(
            results.transcript, prompts=self.__prompts
        )

    def __check_cuda(self) -> bool:
        """
        Check if CUDA is available.
        This method evaluates the output of `nvidia-smi` command.
        If the output contains "NVIDIA-SMI", return True.

        Returns
        -------
        bool
            Whether CUDA is available or not.
        """
        try:
            output = subprocess.check_output("nvidia-smi", shell=True)
            if "NVIDIA-SMI" in output.decode("utf-8"):
                return True
            else:
                return False
        except Exception:
            return False

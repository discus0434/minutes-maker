import logging
from dataclasses import dataclass
from typing import Literal

from faster_whisper import WhisperModel
from pydub import AudioSegment


@dataclass(frozen=True)
class TranscribeData:
    timeline: str
    transcript: str


class Transcriber:
    def __init__(
        self,
        device: Literal["cpu", "cuda"] = "cuda",
        *,
        cpu_threads: int = 0,
        num_workers: int = 1,
    ) -> None:
        """
        Initialize the transcriber.

        Parameters
        ----------
        device : str, optional
            The device to use for inference, by default 'cuda'.
        cpu_threads : int, optional
            The number of CPU threads to use for inference,
            by default 0 (auto).
        num_workers : int, optional
            The number of workers to use for inference,
            by default 1 (non-parallel).
        """

        # Load the model
        self.model = WhisperModel(
            model_size_or_path="large-v2" if device == "cuda" else "base",
            device=device,
            compute_type="int8_float16" if device == "cuda" else "int8",
            cpu_threads=cpu_threads,
            num_workers=num_workers,
        )

    def convert_and_transcribe(
        self,
        audio_or_video_file_path: str,
        *,
        prompt: str = "",
        beam_size: int = 5,
    ) -> TranscribeData:
        """
        Transcribe an audio or video file.

        Parameters
        ----------
        audio_or_video_file_path : str
            The path to the video or audio file.
        prompt : str, optional
            The initial prompt to make the model easier to understand
            the context, by default "".
        beam_size : int, optional
            The beam size to use for beam search, by default 5.

        Returns
        -------
        TranscribeData
            The transcribed text and the timeline of the audio file.
        """
        # Extract or convert audio from input file if it is a .mp3 file
        audio_file_path = self.__convert_to_audio(audio_or_video_file_path)

        # Transcribe the audio file
        return self.__transcribe(
            audio_file_path=audio_file_path, prompt=prompt, beam_size=beam_size
        )

    def __transcribe(
        self,
        audio_file_path: str,
        *,
        prompt: str = "",
        beam_size: int = 5,
    ) -> TranscribeData:
        """
        Transcribe an audio file.

        Parameters
        ----------
        audio_file_path : str
            The path to the audio file.
        prompt : str, optional
            The initial prompt to make the model easier to understand
            the context, by default "".

        Returns
        -------
        TranscribeData
            The transcribed text and the timeline of the audio file.
        """
        segments, info = self.model.transcribe(
            audio_file_path, initial_prompt=prompt, beam_size=beam_size
        )

        logging.info(
            "Detected language '%s' with probability %f"
            % (info.language, info.language_probability)
        )

        transcripts: list[str] = []
        timelines: list[str] = []
        for segment in segments:
            timeline = f"[{int(segment.start // 60)}m{int(segment.start % 60)}s -> {int(segment.end // 60)}m{int(segment.end % 60)}s] **{segment.text.strip()}**"
            logging.info(timeline)

            timelines.append(timeline)
            transcripts.append(segment.text)

        return TranscribeData(
            timeline="\n\n".join(timelines), transcript="\n".join(transcripts)
        )

    def __convert_to_audio(self, audio_or_video_file_path: str) -> str:
        """
        Extract audio from a video file and save it as an mp3 file.

        Parameters
        ----------
        audio_or_video_file_path : str
            The path to the video or audio file.

        Returns
        -------
        str
            The path to the output mp3 file.
        """
        audio = AudioSegment.from_file(audio_or_video_file_path)
        audio_file_path = audio_or_video_file_path.rsplit(".", 1)[0] + ".mp3"
        audio.export(audio_file_path, format="mp3")

        return audio_file_path

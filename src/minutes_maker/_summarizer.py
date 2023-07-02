import logging
import os
from typing import Union

import openai
import tiktoken

from ._prompts import (
    EnglishLecturePrompts,
    EnglishMeetingPrompts,
    JapaneseLecturePrompts,
    JapaneseMeetingPrompts,
)


class Summarizer:
    """
    A class to summarize research papers using OpenAI's API.

    Attributes
    ----------
    model : str
        The OpenAI model to be used for summarization.
    language : Literal["ja", "en"]
    """

    def __init__(self, model: str = "gpt-3.5-turbo-16k-0613") -> None:
        """
        Initialize the Summarizer class with an OCRModel instance and
        set the OpenAI API key.

        Parameters
        ----------
        model : str, optional
            The OpenAI model to be used for summarization,
            by default "gpt-3.5-turbo-16k-0613".
        """
        self.__model = model
        self.__tokenizer = tiktoken.encoding_for_model(self.__model)

        openai.organization = os.getenv("OPENAI_ORGANIZATION", "")
        openai.api_key = os.getenv("OPENAI_API_KEY")

        if "16k" in self.__model:
            self.__max_context_length = 12500
            self.__max_generation_length = 3000
        elif "32k" in self.__model:
            self.__max_context_length = 28500
            self.__max_generation_length = 3000
        else:
            self.__max_context_length = 4500
            self.__max_generation_length = 3000
            logging.warning(
                "Warning: The model you are using is not suitable for summarization.",
                "You should use 'gpt-3.5-turbo-16k-0613' or 'gpt-4-32k'.",
            )

        # Somehow cannot extend the Enum class,
        # we cannot make base class for prompts.
        self.__prompts: Union[
            JapaneseLecturePrompts,
            JapaneseMeetingPrompts,
            EnglishLecturePrompts,
            EnglishMeetingPrompts,
        ] = None

    def summarize(
        self,
        transcript: str,
        prompts: Union[
            JapaneseLecturePrompts,
            JapaneseMeetingPrompts,
            EnglishLecturePrompts,
            EnglishMeetingPrompts,
        ],
    ) -> str:
        """
        Summarize the given text using OpenAI's language model.

        Parameters
        ----------
        transcript : str
            The transcript of the meeting.
            Texts are split into sentences by newline characters.
        prompts : Union[
            JapaneseLecturePrompts,
            JapaneseMeetingPrompts,
            EnglishLecturePrompts,
            EnglishMeetingPrompts
        ]
            The prompts to be used for summarization.

        Returns
        -------
        str
            The summarized text.
        """
        self.__prompts = prompts
        response = openai.ChatCompletion.create(
            model=self.__model,
            max_tokens=self.__max_generation_length,
            messages=[
                {
                    "role": "system",
                    "content": self.__prompts.SUMMARIZE_SYSTEM_PROMPT.value.format(
                        transcript=self.__shortening_transcript(transcript)
                    ),
                },
                {
                    "role": "user",
                    "content": self.__prompts.SUMMARIZE_USER_PROMPT_FOR_SUMMARY.value,
                },
            ],
        )
        return response["choices"][0]["message"]["content"]

    def __shortening_transcript(self, transcript: str) -> str:
        """
        Shorten the given transcript using OpenAI's language model.

        Parameters
        ----------
        transcript : str
            The transcript of the meeting.
            Texts are split into sentences by newline characters.

        Returns
        -------
        str
            The shortened text.
        """
        tokenized = self.__tokenizer.encode(transcript)
        while len(tokenized) > self.__max_context_length:
            logging.info(
                f"transcript is too long ({len(tokenized)} tokens)",
                "shortening transcript...",
            )
            # seperate `tokenized` by newline token with the close index
            # to `self.__max_context_length`
            close_token_idx = None
            for i, token in enumerate(
                tokenized[
                    self.__max_context_length - 100 : self.__max_context_length + 200
                ]
            ):
                if token in [198, 345, 627, 4999, 5380, 9174, 95532]:
                    close_token_idx = self.__max_context_length - 100 + i
                    break

            # if no newline token is close to `self.__max_context_length` th,
            # just split `tokenized` at `self.__max_context_length`
            if close_token_idx is None:
                close_token_idx = self.__max_context_length

            # shorten the part of transcript
            shortened = openai.ChatCompletion.create(
                model=self.__model,
                max_tokens=self.__max_generation_length,
                messages=[
                    {
                        "role": "system",
                        "content": self.__prompts.SUMMARIZE_SYSTEM_PROMPT.value.format(
                            transcript=self.__tokenizer.decode(
                                tokenized[:close_token_idx]
                            )
                        ),
                    },
                    {
                        "role": "user",
                        "content": self.__prompts.SUMMARIZE_USER_PROMPT_FOR_SHORTENING.value,
                    },
                ],
            )["choices"][0]["message"]["content"]

            # concatenate the shortened part and the rest of transcript
            tokenized = (
                self.__tokenizer.encode(f"{shortened}\n") + tokenized[close_token_idx:]
            )

            logging.info(f"shortened transcript to {len(tokenized)} tokens.")

        return self.__tokenizer.decode(tokenized)

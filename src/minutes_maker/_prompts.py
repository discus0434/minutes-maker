import inspect
from enum import Enum


class JapaneseMeetingPrompts(Enum):
    """
    Enum for storing prompts for meeting minutes in Japanese.

    Attributes
    ----------
    TRANSCRIBE_FORMAT : str
        The format string for the prompt for transcribing the audio.
        Used in `src/minutes_maker/_transcriber.py`.

    SUMMARIZE_SYSTEM_PROMPT : str
        The system message for summarizing the audio.
        Used in `src/minutes_maker/_summarizer.py`.

    SUMMARIZE_USER_PROMPT_FOR_SUMMARY : str
        The user message for summarizing the audio.
        Used in `src/minutes_maker/_summarizer.py`.

    SUMMARIZE_USER_PROMPT_FOR_SHORTENING : str
        The user message for shortening the transcript.
        Used in `src/minutes_maker/_summarizer.py`.
    """

    TRANSCRIBE_FORMAT: str = "{content}に関する、ミーティングの書き起こし。"
    SUMMARIZE_SYSTEM_PROMPT: str = inspect.cleandoc(
        """
        以下のテキストは、ある日本語の会議の内容を文字起こししたものです。
        文字起こしは機械学習モデルによって行われており、その精度は100%ではありません。
        また、文字起こしの結果には、会議の参加者の発言以外にも、雑音や会議の進行に関する記述が含まれている可能性があります。
        それを踏まえた上で、以下の文字起こしを読み、ユーザーの質問に答えてください。

        '''
        {transcript}
        '''
        """
    )
    SUMMARIZE_USER_PROMPT_FOR_SUMMARY: str = inspect.cleandoc(
        """
        会議の文字起こしの内容から、以下の3点について日本語でまとめてください。
        なお、markdown形式で、重要な点を太字にしたり、タイトル部分を大きくしたりなど、読みやすいように工夫して記述してください。

        ## 1. 会議のサマリ
        ## 2. 会議の決定事項
        ## 3. 会議の結論から考えられるToDoもしくはNext Action
        """
    )
    SUMMARIZE_USER_PROMPT_FOR_SHORTENING: str = inspect.cleandoc(
        """
        この文字起こしは長すぎるため、要点を確実に押さえながら要約してください。
        なお、この文字起こしはより長い文字起こし文の一部切り出したものである可能性があることに注意してください。
        """
    )


class EnglishMeetingPrompts(Enum):
    """
    Enum for storing prompts for meeting minutes in English.

    Attributes
    ----------
    TRANSCRIBE_FORMAT : str
        The format string for the prompt for transcribing the audio.
        Used in `src/minutes_maker/_transcriber.py`.

    SUMMARIZE_SYSTEM_PROMPT : str
        The system message for summarizing the audio.
        Used in `src/minutes_maker/_summarizer.py`.

    SUMMARIZE_USER_PROMPT_FOR_SUMMARY : str
        The user message for summarizing the audio.
        Used in `src/minutes_maker/_summarizer.py`.

    SUMMARIZE_USER_PROMPT_FOR_SHORTENING : str
        The user message for shortening the transcript.
        Used in `src/minutes_maker/_summarizer.py`.
    """

    TRANSCRIBE_FORMAT: str = "Transcription of the meeting regarding {content}."
    SUMMARIZE_SYSTEM_PROMPT: str = inspect.cleandoc(
        """
        The following text is a transcription of a meeting in English.
        The transcription is done by a machine learning model, and its accuracy is not 100%.
        Also, the transcription results may include not only the participants' remarks, but also background noise and descriptions of the meeting's progress.
        Bearing this in mind, please read the transcription below and answer the user's question.

        '''
        {transcript}
        '''
        """
    )
    SUMMARIZE_USER_PROMPT_FOR_SUMMARY: str = inspect.cleandoc(
        """
        From the content of the meeting transcription, please summarize the following three points in English.
        Please note, describe it in markdown format, emphasizing important points in bold, making the title parts bigger, and so on, for easier reading.

        ## 1. Meeting Summary
        ## 2. Decisions Made in the Meeting
        ## 3. ToDos or Next Actions from Meeting Conclusions
        """
    )
    SUMMARIZE_USER_PROMPT_FOR_SHORTENING: str = inspect.cleandoc(
        """
        This transcription is too long, please summarize it while ensuring the key points are captured.
        Please note that this transcription may be a part cut out from a longer transcription.
        """
    )


class JapaneseLecturePrompts(Enum):
    """
    Enum for storing prompts for lecture transcripts and summaries in Japanese.

    Attributes
    ----------
    TRANSCRIBE_FORMAT : str
        The format string for the prompt for transcribing the audio.
        Used in `src/minutes_maker/_transcriber.py`.

    SUMMARIZE_SYSTEM_PROMPT : str
        The system message for summarizing the audio.
        Used in `src/minutes_maker/_summarizer.py`.

    SUMMARIZE_USER_PROMPT_FOR_SUMMARY : str
        The user message for summarizing the audio.
        Used in `src/minutes_maker/_summarizer.py`.

    SUMMARIZE_USER_PROMPT_FOR_SHORTENING : str
        The user message for shortening the transcript.
        Used in `src/minutes_maker/_summarizer.py`.
    """

    TRANSCRIBE_FORMAT: str = "{content}に関する、レクチャーの書き起こし。"
    SUMMARIZE_SYSTEM_PROMPT: str = inspect.cleandoc(
        """
        以下のテキストは、ある日本語のレクチャーの内容を文字起こししたものです。
        文字起こしは機械学習モデルによって行われており、その精度は100%ではありません。
        また、文字起こしの結果には、レクチャーの参加者の発言以外にも、雑音やレクチャーの進行に関する記述が含まれている可能性があります。
        それを踏まえた上で、以下の文字起こしを読み、ユーザーの質問に答えてください。

        '''
        {transcript}
        '''
        """
    )
    SUMMARIZE_USER_PROMPT_FOR_SUMMARY: str = inspect.cleandoc(
        """
        レクチャーの文字起こしの内容から、以下の3点について日本語でまとめてください。
        なお、markdown形式で、重要な点を太字にしたり、タイトル部分を大きくしたりなど、読みやすいように工夫して記述してください。

        ## 1. レクチャーのサマリ
        ## 2. レクチャーで説明された主要なポイント
        ## 3. レクチャーの結論から考えられるToDoもしくはNext Action
        """
    )
    SUMMARIZE_USER_PROMPT_FOR_SHORTENING: str = inspect.cleandoc(
        """
        この文字起こしは長すぎるため、要点を確実に押さえながら要約してください。
        なお、この文字起こしはより長い文字起こし文の一部切り出したものである可能性があることに注意してください。
        """
    )


class EnglishLecturePrompts(Enum):
    """
    Enum for storing prompts for lecture transcripts and summaries in English.

    Attributes
    ----------
    TRANSCRIBE_FORMAT : str
        The format string for the prompt for transcribing the audio.
        Used in `src/minutes_maker/_transcriber.py`.

    SUMMARIZE_SYSTEM_PROMPT : str
        The system message for summarizing the audio.
        Used in `src/minutes_maker/_summarizer.py`.

    SUMMARIZE_USER_PROMPT_FOR_SUMMARY : str
        The user message for summarizing the audio.
        Used in `src/minutes_maker/_summarizer.py`.

    SUMMARIZE_USER_PROMPT_FOR_SHORTENING : str
        The user message for shortening the transcript.
        Used in `src/minutes_maker/_summarizer.py`.
    """

    TRANSCRIBE_FORMAT: str = "Transcription of the lecture regarding {content}."
    SUMMARIZE_SYSTEM_PROMPT: str = inspect.cleandoc(
        """
        The following text is a transcription of a lecture in English.
        The transcription is done by a machine learning model, and its accuracy is not 100%.
        Also, the transcription results may include not only the speakers' remarks, but also background noise and descriptions of the lecture's progress.
        Bearing this in mind, please read the transcription below and answer the user's question.

        '''
        {transcript}
        '''
        """
    )
    SUMMARIZE_USER_PROMPT_FOR_SUMMARY: str = inspect.cleandoc(
        """
        From the content of the lecture transcription, please summarize the following three points in English.
        Please note, describe it in markdown format, emphasizing important points in bold, making the title parts bigger, and so on, for easier reading.

        ## 1. Lecture Summary
        ## 2. Key Points Explained in the Lecture
        ## 3. ToDos or Next Actions from Lecture Conclusions
        """
    )
    SUMMARIZE_USER_PROMPT_FOR_SHORTENING: str = inspect.cleandoc(
        """
        This transcription is too long, please summarize it while ensuring the key points are captured.
        Please note that this transcription may be a part cut out from a longer transcription.
        """
    )

from uuid import UUID


class AudioRecordingAlreadyDownloadedException(Exception):

    status_code: int = 409

    def __init__(self, user_id: UUID, video_id: str):

        super().__init__(f'Audio recording for user \'{user_id}\' and video ID \'{video_id}\' already downloaded')

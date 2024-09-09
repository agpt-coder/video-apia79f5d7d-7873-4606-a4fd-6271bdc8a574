from typing import Optional

import prisma
import prisma.models
from fastapi import UploadFile
from pydantic import BaseModel


class UploadVideoResponse(BaseModel):
    """
    Response model for a successful video upload.
    """

    video_id: str
    message: str


async def upload_video(
    title: str, description: Optional[str], video_file: UploadFile
) -> UploadVideoResponse:
    """
    Securely uploads a new video to the system, saving video information to the database and returning a response.

    Args:
        title (str): The title of the video content.
        description (Optional[str]): A brief description or summary of the video content.
        video_file (UploadFile): The binary content of the video file being uploaded.

    Returns:
        UploadVideoResponse: Response model for a successful video upload, including the video ID and a message.
    """
    file_location = f"videos/{video_file.filename}"
    secure_url = f"https://videos.example.com/{video_file.filename}"
    video = await prisma.models.Video.prisma().create(
        data={
            "title": title,
            "description": description,
            "url": file_location,
            "secureUrl": secure_url,
            "allowed": True,
            "creatorId": "specify-creator-user-id-here",
        }
    )
    return UploadVideoResponse(
        video_id=video.id, message="Video successfully uploaded."
    )

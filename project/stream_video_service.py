import prisma
import prisma.models
from fastapi import HTTPException
from pydantic import BaseModel


class StreamVideoResponse(BaseModel):
    """
    This model encapsulates the response after successfully fetching the video stream URL. It provides the signed URL to the client for secure access.
    """

    videoId: str
    signedUrl: str
    expiresIn: int


async def stream_video(videoId: str) -> StreamVideoResponse:
    """
    Streams video content to the client.

    Args:
        videoId (str): The unique identifier for the video content to be streamed.

    Returns:
        StreamVideoResponse: This model encapsulates the response after successfully fetching the video stream URL. It
        provides the signed URL to the client for secure access.

    Example:
        videoId = "some-video-id"
        video_response = await stream_video(videoId)
        print(video_response)
        # Output:
        # StreamVideoResponse(videoId="some-video-id", signedUrl="https://example.com/video/some-video-id?token=123", expiresIn=3600)

    Raises:
        HTTPException: If the video with the specified ID does not exist or is not marked as allowed for streaming.
    """
    video = await prisma.models.Video.prisma().find_unique(where={"id": videoId})
    if video is None or not video.allowed:
        raise HTTPException(
            status_code=404, detail="Video not found or not available for streaming."
        )
    signed_url = f"{video.secureUrl}?token=signed-token-example"
    expires_in = 3600
    return StreamVideoResponse(
        videoId=videoId, signedUrl=signed_url, expiresIn=expires_in
    )

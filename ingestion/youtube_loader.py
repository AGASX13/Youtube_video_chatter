import time
from typing import Optional
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable

class YouTubeLoader:
    """Load and fetch transcripts from YouTube videos."""

    def __init__(self, language_codes: list[str] | None = None, retry_attempts: int = 3):
        self.language_codes = language_codes or ["en"]
        self.retry_attempts = retry_attempts

    def fetch_transcript(self, url: str) -> Optional[str]:
        """Fetch transcript with robust fallback logic and retries."""
        try:
            # Extract Video ID (Simplified for example)
            video_id = url.split("v=")[-1] 
            
            if not video_id:
                print(f"Invalid YouTube URL: {url}")
                return None

            # 1. Instantiate the API client (Required in modern versions)
            ytt_api = YouTubeTranscriptApi()

            for attempt in range(1, self.retry_attempts + 1):
                try:
                    # 2. Use the instance method .list() instead of the static .list_transcripts()
                    transcript_list = ytt_api.list(video_id)
                    
                    transcript_obj = None
                    try:
                        # Try preferred languages (manually created first)
                        transcript_obj = transcript_list.find_manually_created_transcript(self.language_codes)
                    except NoTranscriptFound:
                        try:
                            # Fallback to generated in preferred languages
                            transcript_obj = transcript_list.find_generated_transcript(self.language_codes)
                        except NoTranscriptFound:
                            # Final fallback: just get whatever is available
                            transcript_obj = next(iter(transcript_list))

                    if transcript_obj:
                        # 3. Use .fetch() on the resulting transcript object
                        data = transcript_obj.fetch()
                        full_text = " ".join([entry["text"] for entry in data])
                        return full_text

                except (TranscriptsDisabled, VideoUnavailable) as e:
                    print(f"Permanent Error: {str(e)}")
                    return None
                except Exception as e:
                    # Retry logic for transient/network errors
                    if attempt < self.retry_attempts:
                        wait_time = 2 ** attempt
                        print(f"Attempt {attempt} failed, retrying in {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                    else:
                        print(f"Max retries reached. Final error: {str(e)}")
                        return None
            return None

        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None

    def fetch_and_clean(self, url: str) -> Optional[str]:
        transcript = self.fetch_transcript(url)
        if transcript:
            # Basic clean logic
            return " ".join(transcript.split()) 
        return None

if __name__ == "__main__":
    loader = YouTubeLoader(language_codes=['en', 'es'])
    test_url = "https://www.youtube.com/watch?v=eIho2S0ZahI"
    result = loader.fetch_and_clean(test_url)
    if result:
        print(f"Success! Length: {len(result)}")
        print(f"Snippet: {result[:100]}...")
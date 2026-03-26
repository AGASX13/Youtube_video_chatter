import time
from typing import Optional
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, VideoUnavailable

class YouTubeLoader:
    """Load and fetch transcripts from YouTube videos."""

    def __init__(self, language_codes: list[str] | None = None, retry_attempts: int = 3):
        # Define the fallback hierarchy here (e.g., ['en', 'de'])
        self.language_codes = language_codes or ["en"]
        self.retry_attempts = retry_attempts

        # Instantiate once to reuse internal HTTP sessions across multiple requests
        self.api_client = YouTubeTranscriptApi()

    def fetch_transcript(self, url: str) -> Optional[str]:
        """Fetch transcript utilizing the direct fetch() method."""
        try:
            # Extract Video ID safely (ignoring extra URL parameters like &t=45s)
            if "v=" in url:
                video_id = url.split("v=")[-1].split("&")[0] 
            else:
                video_id = url # Fallback in case just the ID is passed
            
            if not video_id:
                print(f"Invalid YouTube URL: {url}")
                return None

            for attempt in range(1, self.retry_attempts + 1):
                try:
                    # Using the working fetch paradigm you discovered.
                    # The library natively handles iterating through the language fallbacks.
                    transcript_data = self.api_client.fetch(
                        video_id, 
                        languages=self.language_codes
                    )
                    
                    if transcript_data:
                        # Extract and join the text blocks from the returned list of dictionaries
                        # 3. Extract text safely, handling both Objects and Dictionaries
                        text_fragments = []
                        for entry in transcript_data:
                            # If it's an object with a .text attribute (Your current scenario)
                            if hasattr(entry, 'text'):
                                text_fragments.append(entry.text)
                            # Fallback: If it's a standard dictionary (Older versions)
                            elif isinstance(entry, dict) and "text" in entry:
                                text_fragments.append(entry["text"])
                            else:
                                # Log or ignore unknown structures
                                continue
                                
                        full_text = " ".join(text_fragments)
                        return full_text

                except (TranscriptsDisabled, VideoUnavailable) as e:
                    print(f"Permanent Error: Video {video_id} - {str(e)}")
                    return None
                except Exception as e:
                    # Catch transient network/bot detection errors
                    if attempt < self.retry_attempts:
                        wait_time = 2 ** attempt
                        print(f"Attempt {attempt} failed ({str(e)}), retrying in {wait_time}s...")
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
            # Clean text by replacing excessive whitespace/newlines with a single space
            return " ".join(transcript.split()) 
        return None

if __name__ == "__main__":
    # Test the loader with your specific language fallback
    loader = YouTubeLoader(language_codes=['de', 'en'])
    test_url = "https://www.youtube.com/watch?v=eIho2S0ZahI"
    
    print(f"Attempting to fetch transcript for {test_url}...")
    result = loader.fetch_and_clean(test_url)
    
    if result:
        print(f"\nSuccess! Transcript length: {len(result)} characters")
        print(f"Snippet: {result[:200]}...")
    else:
        print("\nFailed to retrieve transcript.")
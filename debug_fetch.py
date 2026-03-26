import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound

video_id = 'eIho2S0ZahI'

print("=== Testing transcript fetching ===\n")

# Get the TranscriptList object
transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
print(f"1. Got transcript_list: {type(transcript_list)}")

# Try find_transcript with 'en'
print("\n2. Trying find_transcript(['en']):")
try:
    trans_obj = transcript_list.find_transcript(['en'])
    print(f"   ✓ Found: {trans_obj}")
    transcript = trans_obj.fetch()
    print(f"   ✓ Fetched: {len(transcript)} items")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Try find_manually_created_transcript
print("\n3. Trying find_manually_created_transcript(['en', 'es', 'fr', 'de']):")
try:
    trans_obj = transcript_list.find_manually_created_transcript(['en', 'es', 'fr', 'de'])
    print(f"   ✓ Found: {trans_obj}")
    transcript = trans_obj.fetch()
    print(f"   ✓ Fetched: {len(transcript)} items")
except NoTranscriptFound as e:
    print(f"   ✗ NoTranscriptFound: {e}")
except Exception as e:
    print(f"   ✗ Error: {type(e).__name__}: {e}")

# Try iterating the transcript_list
print("\n4. Iterating transcript_list:")
try:
    transcripts = list(transcript_list)
    print(f"   ✓ Got {len(transcripts)} transcripts")
    if transcripts:
        print(f"   First one: {transcripts[0]}")
        transcript = transcripts[0].fetch()
        print(f"   ✓ Fetched: {len(transcript)} items")
except Exception as e:
    print(f"   ✗ Error: {type(e).__name__}: {e}")

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from youtube_transcript_api import YouTubeTranscriptApi

# Get the TranscriptList object
tl = YouTubeTranscriptApi.list_transcripts('eIho2S0ZahI')

print("=== TranscriptList Object Structure ===")
print(f"Type: {type(tl)}")
print(f"\nAll attributes and methods:")
for attr in sorted(dir(tl)):
    if not attr.startswith('_'):
        print(f"  - {attr}")

print("\n=== Checking specific attributes ===")
print(f"Has 'manually_created_transcripts': {hasattr(tl, 'manually_created_transcripts')}")
print(f"Has 'generated_transcripts': {hasattr(tl, 'generated_transcripts')}")
print(f"Has '_manually_created_transcripts': {hasattr(tl, '_manually_created_transcripts')}")
print(f"Has '_generated_transcripts': {hasattr(tl, '_generated_transcripts')}")

print("\n=== Trying different access patterns ===")
try:
    print(f"tl['manually_created']: {tl['manually_created']}")
except Exception as e:
    print(f"tl['manually_created'] - Error: {e}")

try:
    print(f"tl.get('manually_created'): {tl.get('manually_created')}")
except Exception as e:
    print(f"tl.get('manually_created') - Error: {e}")

print("\n=== Trying iteration ===")
try:
    for item in tl:
        print(f"Item: {item}")
        break
except Exception as e:
    print(f"Iteration error: {e}")

print("\n=== Checking __dict__ ===")
print(f"Object dict: {tl.__dict__ if hasattr(tl, '__dict__') else 'No __dict__'}")

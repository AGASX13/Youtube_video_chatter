from youtube_transcript_api import YouTubeTranscriptApi

video_id = "eIho2S0ZahI"

transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

for t in transcript_list:
    transcript = t.fetch()
    print("Language:", t.language)
    print(transcript[:5])
    break
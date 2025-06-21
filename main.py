from ttsfm import TTSClient, AudioFormat, Voice


def main():
    client = TTSClient()
    
    response = client.generate_speech(
        text="Hello! This is TTSFM - a free TTS service.",
        voice=Voice.CORAL,
        response_format=AudioFormat.OPUS
    )

    # Save the audio file
    response.save_to_file("output")

if __name__ == "__main__":
    main()

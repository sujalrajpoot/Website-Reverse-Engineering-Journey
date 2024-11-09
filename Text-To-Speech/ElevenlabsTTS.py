# Main Website Url: https://elevenlabs.io/?from=shyamsundar5735

import requests
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def ElevenlabsTTS(text: str, voice_name: str = "Brian", filename: str = "STREAM_AUDIOS/output_audio", verbose: bool = True) -> str:
    """
    Converts text to speech using the ElevenLabs TTS API and saves the generated audio files in sequence.

    Args:
        text (str): The text to be converted to speech.
        voice_name (str): The name of the voice to use for TTS. Default is "Brian".
        filename (str): The base name for the saved audio file. Each chunk will have a unique suffix.
        verbose (bool): If True, print status messages. Default is True.

    Returns:
        str: Message indicating success when all audio files have been saved.
    """

    # Dictionary of available voices and their IDs
    available_voices = {
        "Brian": "nPczCjzI2devNBz1zQrb", "Alice": "Xb7hH8MSUJpSbSDYk0k2", "Bill": "pqHfZKP75CvOlQylNhV4",
        "Callum": "N2lVS1w4EtoT3dr4eOWO", "Charlie": "IKne3meq5aSn9XLyUdCD", "Charlotte": "XB0fDUnXU5powFXDhCwa",
        "Chris": "iP95p4xoKVk53GoZ742B", "Daniel": "onwK4e9ZLuTAKqWW03F9", "Eric": "cjVigY5qzO86Huf0OWal",
        "George": "JBFqnCBsd6RMkjVDRZzb", "Jessica": "cgSgspJ2msm6clMCkdW9", "Laura": "FGY2WhTYpPnrIDTdsKH5",
        "Liam": "TX3LPaxmHKxFdv7VOQHJ", "Lily": "pFZP5JQG7iQjIQuC4Bku", "Matilda": "XrExE9yKIg1WjnnlVkGX",
        "Sarah": "EXAVITQu4vr4xnSDxMaL", "Will": "bIHbv24MWmeRgasZH58o"
    }

    # Check if the voice name is valid
    if voice_name not in available_voices:
        return f"Invalid voice name. Available voices are: {', '.join(available_voices.keys())}"

    # Headers required for the API request
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://elevenlabs.io',
        'referer': 'https://elevenlabs.io/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }

    voice_id = available_voices[voice_name]
    params = {'allow_unauthenticated': '1'}

    # Create the directory if it doesn't exist
    os.makedirs("STREAM_AUDIOS", exist_ok=True)

    # Split text into manageable chunks
    sentences = re.split(r'(?<!\b\w\.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    audio_files = []  # List to store generated audio file paths in sequence

    def generate_audio(part_text: str, part_number: int):
        """
        Generate audio for each text part and save in sequence.
        
        Keeps retrying until a successful response is received.

        Args:
            part_text (str): The text part to convert to speech.
            part_number (int): The sequence number of the text part.

        Returns:
            tuple: Part number and audio data if successful, else (part_number, None).
        """
        print(f"Chunk Text: {part_text}\n")
        while True:  # Loop until we get a successful response
            try:
                json_data = {'text': part_text, 'model_id': 'eleven_multilingual_v2'}
                response = requests.post(
                    f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}',
                    params=params, headers=headers, json=json_data, timeout=None
                )
                response.raise_for_status()
                if response.ok and response.status_code == 200:
                    audio_data = response.content
                    return part_number, audio_data
            except requests.RequestException as e:
                print(f"Error occurred: {e}. Retrying...\n")
                time.sleep(1)  # Short delay before retrying

    def save_audio_file(part_number, audio_data):
        """
        Save audio data to a file in the correct sequence.

        Args:
            part_number (int): The sequence number of the part.
            audio_data (bytes): The audio data to save.

        Returns:
            str: The filename where the audio data was saved.
        """
        part_filename = f"{filename}_{part_number}.mp3"
        with open(part_filename, 'wb') as audio_file:
            audio_file.write(audio_data)
        if verbose:
            print(f"Audio saved as {part_filename}.\n")
        return part_filename

    # Start downloading audio files using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(generate_audio, sentence.strip(), i + 1): i for i, sentence in enumerate(sentences) if sentence.strip()}
        
        # Ensure audio files are stored in order as they complete
        audio_results = {}
        for future in as_completed(futures):
            part_number, audio_data = future.result()
            if audio_data:
                audio_results[part_number] = audio_data
                # Save files sequentially once the required part is available
                while len(audio_files) + 1 in audio_results:
                    current_number = len(audio_files) + 1
                    saved_filename = save_audio_file(current_number, audio_results.pop(current_number))
                    audio_files.append(saved_filename)
    
    return "All Audio Files Saved Successfully."

if __name__ == "__main__":
    print(ElevenlabsTTS("Artificial Intelligence (AI) has transformed numerous industries, and its impact on daily life is only growing. From simple tasks like recommending movies to complex processes like diagnosing diseases, AI is reshaping the way we live, work, and interact with the world around us. Machine learning, a subset of AI, allows computers to learn from data, identify patterns, and make decisions with minimal human intervention. This has led to significant advances in image recognition, speech processing, and autonomous vehicles, among other areas. One of the most intriguing aspects of AI is natural language processing, which aims to bridge the gap between human communication and machine interpretation. Chatbots, language translators, and virtual assistants like Siri and Alexa have become commonplace, yet they represent just the beginning of what AI-powered language understanding can achieve. In the future, AI could enable real-time, flawless translation of any language, breaking down communication barriers on a global scale.Furthermore, AI's predictive capabilities are aiding in fields like healthcare, finance, and climate science. In healthcare, AI algorithms analyze medical images to assist doctors in early diagnosis of illnesses, potentially saving lives. In finance, AI-driven predictive models are being used to detect fraudulent transactions and to provide personalized investment advice. Similarly, in climate science, AI models analyze complex climate data to predict weather patterns, assisting in disaster preparedness and response.Despite its impressive capabilities, AI also poses ethical and societal challenges. Issues such as data privacy, bias in decision-making algorithms, and the potential for job displacement are frequently discussed. Governments and organizations are working to create regulations that ensure AI is developed and used responsibly, balancing innovation with societal good. As AI technology continues to evolve, it's crucial that its development is guided by ethical considerations, ensuring a future where technology benefits humanity as a whole."))
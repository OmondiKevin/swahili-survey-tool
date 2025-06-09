"""
Automatic Speech Recognition (ASR) module for the Swahili Survey Engine.

This module provides functionality to transcribe audio recordings of survey responses
from Swahili to text using OpenAI's Whisper model.
"""

import os
import tempfile
from typing import Dict, List

import torch
import whisper
from pydub import AudioSegment


class ASR:
    """
    A class to handle Automatic Speech Recognition for Swahili audio.
    
    This class uses OpenAI's Whisper model to transcribe Swahili audio recordings
    to text, which can then be processed as survey responses.
    """

    def __init__(self, model_size: str = "base"):
        """
        Initialize the ASR with a Whisper model.
        
        Args:
            model_size: Size of the Whisper model to use. Options are "tiny", "base", 
                       "small", "medium", "large". Larger models are more accurate
                       but require more computational resources.
        """
        self.model_size = model_size
        self.model = None

        # Check if CUDA is available for GPU acceleration
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Load the model
        try:
            self.model = whisper.load_model(model_size, device=self.device)
            print(f"Loaded Whisper model '{model_size}' on {self.device}")
        except Exception as e:
            print(f"Warning: Could not load Whisper model: {e}")

    def transcribe_audio(self, audio_file: str, language: str = "sw") -> Dict:
        """
        Transcribe an audio file to text.
        
        Args:
            audio_file: Path to the audio file to transcribe.
            language: Language code for the audio. Default is "sw" for Swahili.
                     Set to None for automatic language detection.
        
        Returns:
            A dictionary with the transcription results, including the text and confidence.
            
        Raises:
            FileNotFoundError: If the audio file does not exist.
            ValueError: If the model is not loaded or the audio file format is not supported.
        """
        if not self.model:
            raise ValueError("Whisper model not loaded")

        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Audio file not found: {audio_file}")

        # Ensure the audio file is in a format Whisper can process
        audio_file = self._ensure_compatible_format(audio_file)

        # Transcribe the audio
        options = {"language": language} if language else {}
        result = self.model.transcribe(audio_file, **options)

        return result

    def _ensure_compatible_format(self, audio_file: str) -> str:
        """
        Ensure the audio file is in a format compatible with Whisper.
        
        Args:
            audio_file: Path to the audio file.
        
        Returns:
            Path to a compatible audio file (may be the same or a temporary file).
        """
        # Get the file extension
        _, ext = os.path.splitext(audio_file)
        ext = ext.lower()

        # If it's already a compatible format, return it
        if ext in ['.wav', '.mp3', '.flac']:
            return audio_file

        # Otherwise, convert it to WAV
        try:
            audio = AudioSegment.from_file(audio_file)

            # Create a temporary file
            temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            temp_path = temp_file.name
            temp_file.close()

            # Export to WAV
            audio.export(temp_path, format='wav')

            return temp_path

        except Exception as e:
            raise ValueError(f"Could not convert audio file to a compatible format: {e}")

    def batch_transcribe(self, audio_files: List[str], language: str = "sw") -> List[Dict]:
        """
        Transcribe multiple audio files to text.
        
        Args:
            audio_files: List of paths to audio files to transcribe.
            language: Language code for the audio. Default is "sw" for Swahili.
        
        Returns:
            A list of dictionaries with transcription results for each file.
        """
        results = []

        for audio_file in audio_files:
            try:
                result = self.transcribe_audio(audio_file, language)
                results.append({
                    'file': audio_file,
                    'text': result.get('text', ''),
                    'segments': result.get('segments', []),
                    'language': result.get('language', language),
                    'error': None
                })
            except Exception as e:
                results.append({
                    'file': audio_file,
                    'text': '',
                    'segments': [],
                    'language': language,
                    'error': str(e)
                })

        return results

    def transcribe_to_responses(self, audio_files: List[str], question_ids: List[str], language: str = "sw") -> List[
        Dict]:
        """
        Transcribe audio files and map them to survey question responses.
        
        Args:
            audio_files: List of paths to audio files to transcribe.
            question_ids: List of question IDs corresponding to each audio file.
            language: Language code for the audio. Default is "sw" for Swahili.
        
        Returns:
            A list of dictionaries with question IDs and transcribed responses.
            
        Raises:
            ValueError: If the lengths of audio_files and question_ids don't match.
        """
        if len(audio_files) != len(question_ids):
            raise ValueError("Number of audio files must match number of question IDs")

        transcriptions = self.batch_transcribe(audio_files, language)

        responses = []
        for i, transcription in enumerate(transcriptions):
            responses.append({
                'question_id': question_ids[i],
                'response': transcription.get('text', ''),
                'valid': bool(transcription.get('text', '').strip()) and not transcription.get('error'),
                'error': transcription.get('error')
            })

        return responses

    def transcribe_directory(self, directory: str, language: str = "sw") -> Dict[str, Dict]:
        """
        Transcribe all audio files in a directory.
        
        Args:
            directory: Path to the directory containing audio files.
            language: Language code for the audio. Default is "sw" for Swahili.
        
        Returns:
            A dictionary mapping file names to transcription results.
            
        Raises:
            FileNotFoundError: If the directory does not exist.
        """
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory not found: {directory}")

        # Get all audio files in the directory
        audio_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in ['.wav', '.mp3', '.flac', '.m4a', '.ogg']:
                    audio_files.append(os.path.join(root, file))

        # Transcribe all files
        transcriptions = self.batch_transcribe(audio_files, language)

        # Map file names to transcriptions
        results = {}
        for transcription in transcriptions:
            file_name = os.path.basename(transcription['file'])
            results[file_name] = transcription

        return results

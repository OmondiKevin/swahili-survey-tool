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
    def __init__(self, model_size: str = "base"):
        self.model_size = model_size
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        try:
            self.model = whisper.load_model(model_size, device=self.device)
            print(f"Loaded Whisper model '{model_size}' on {self.device}")
        except Exception as e:
            print(f"Warning: Could not load Whisper model: {e}")

    def transcribe_audio(self, audio_file: str, language: str = "sw") -> Dict:
        if not self.model:
            raise ValueError("Whisper model not loaded")
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Audio file not found: {audio_file}")
        audio_file = self._ensure_compatible_format(audio_file)
        options = {"language": language} if language else {}
        result = self.model.transcribe(audio_file, **options)
        return result

    def _ensure_compatible_format(self, audio_file: str) -> str:
        _, ext = os.path.splitext(audio_file)
        ext = ext.lower()
        if ext in ['.wav', '.mp3', '.flac']:
            return audio_file
        try:
            audio = AudioSegment.from_file(audio_file)
            temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            temp_path = temp_file.name
            temp_file.close()
            audio.export(temp_path, format='wav')
            return temp_path
        except Exception as e:
            raise ValueError(f"Could not convert audio file to a compatible format: {e}")

    def batch_transcribe(self, audio_files: List[str], language: str = "sw") -> List[Dict]:
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

    def transcribe_to_responses(self, audio_files: List[str], question_ids: List[str], language: str = "sw") -> List[Dict]:
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
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory not found: {directory}")
        audio_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in ['.wav', '.mp3', '.flac', '.m4a', '.ogg']:
                    audio_files.append(os.path.join(root, file))
        transcriptions = self.batch_transcribe(audio_files, language)
        results = {}
        for transcription in transcriptions:
            file_name = os.path.basename(transcription['file'])
            results[file_name] = transcription
        return results

    def transcribe_mapped_responses(self, audio_question_map: Dict[str, List[str]], language: str = "sw") -> List[Dict]:
        responses = []
        for audio_file, question_ids in audio_question_map.items():
            print(f"[ASR] Transcribing '{audio_file}' for questions: {question_ids}")
            try:
                result = self.transcribe_audio(audio_file, language)
                text = result.get('text', '').strip()
                for qid in question_ids:
                    responses.append({
                        'question_id': qid,
                        'response': text,
                        'valid': bool(text),
                        'error': None
                    })
            except Exception as e:
                for qid in question_ids:
                    responses.append({
                        'question_id': qid,
                        'response': '',
                        'valid': False,
                        'error': str(e)
                    })
        return responses

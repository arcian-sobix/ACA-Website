# ========================================
# ACA Bot Audio Manager
# Cypherpunk Audio Effects & Intro
# ========================================
import asyncio
import discord
from discord import FFmpegPCMAudio
import os
import random

class AudioManager:
    """Manages audio effects and intro sounds for the bot"""
    
    def __init__(self):
        self.audio_files = {
            'intro': 'assets/audio/cypherpunk-intro.mp3',
            'success': 'assets/audio/success-beep.mp3',
            'error': 'assets/audio/error-glitch.mp3',
            'achievement': 'assets/audio/achievement-unlock.mp3',
            'typing': 'assets/audio/matrix-typing.mp3'
        }
    
    async def play_intro(self, voice_client):
        """Play the cypherpunk intro audio"""
        if voice_client and voice_client.is_connected():
            try:
                source = FFmpegPCMAudio(self.audio_files['intro'])
                voice_client.play(source)
                while voice_client.is_playing():
                    await asyncio.sleep(0.1)
            except Exception as e:
                print(f"Error playing intro audio: {e}")
    
    async def play_success_sound(self, voice_client):
        """Play success beep sound"""
        if voice_client and voice_client.is_connected():
            try:
                source = FFmpegPCMAudio(self.audio_files['success'])
                voice_client.play(source)
            except:
                pass  # Ignore audio errors in production
    
    async def play_error_sound(self, voice_client):
        """Play error glitch sound"""
        if voice_client and voice_client.is_connected():
            try:
                source = FFmpegPCMAudio(self.audio_files['error'])
                voice_client.play(source)
            except:
                pass
    
    async def play_achievement_sound(self, voice_client):
        """Play achievement unlock sound"""
        if voice_client and voice_client.is_connected():
            try:
                source = FFmpegPCMAudio(self.audio_files['achievement'])
                voice_client.play(source)
            except:
                pass
    
    def create_audio_files(self):
        """Create placeholder audio files if they don't exist"""
        os.makedirs('assets/audio', exist_ok=True)
        
        # Create placeholder audio files
        for filename in self.audio_files.values():
            if not os.path.exists(filename):
                # Create silent audio file as placeholder
                with open(filename, 'wb') as f:
                    f.write(b'')  # Empty file as placeholder

# Global audio manager instance
audio_manager = AudioManager()
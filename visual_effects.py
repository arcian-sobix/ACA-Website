# ========================================
# ACA Bot Visual Effects Manager
# Cypherpunk Glitch & Pixel Effects
# ========================================
import discord
import random
import asyncio
from typing import List

class VisualEffectsManager:
    """Manages cypherpunk visual effects for embeds and messages"""
    
    def __init__(self):
        self.glitch_chars = ['▓', '▒', '░', '█', '▄', '▀', '▌', '▐', '▖', '▗', '▘', '▙', '▚', '▛', '▜', '▝']
        self.cypherpunk_colors = [
            0x00ff41,  # Matrix Green
            0x00d4ff,  # Cyan
            0xff00ff,  # Magenta
            0xffaa00,  # Orange
            0x8800ff,  # Purple
            0xff0088   # Pink
        ]
        self.matrix_chars = ['0', '1', '█', '▓', '▒', '░', '▄', '▀', '▌', '▐']
    
    def create_cypherpunk_embed(self, title: str, description: str = "", glitch_level: int = 3) -> discord.Embed:
        """Create a cypherpunk-styled embed with glitch effects"""
        # Random cypherpunk color
        color = random.choice(self.cypherpunk_colors)
        
        # Add glitch effects to title
        glitched_title = self._add_glitch_effects(title, glitch_level)
        
        embed = discord.Embed(
            title=glitched_title,
            description=description,
            color=color
        )
        
        # Add matrix-style footer
        embed.set_footer(
            text=self._generate_matrix_text(20),
            icon_url="attachment://arcium-logo-cypherpunk.png"
        )
        
        return embed
    
    def _add_glitch_effects(self, text: str, level: int) -> str:
        """Add glitch characters to text"""
        if level <= 0:
            return text
        
        result = list(text)
        for i in range(len(result)):
            if random.random() < (level * 0.1):  # 10% chance per level
                result[i] = random.choice(self.glitch_chars)
        
        return ''.join(result)
    
    def _generate_matrix_text(self, length: int) -> str:
        """Generate matrix-style random text"""
        return ''.join(random.choices(self.matrix_chars, k=length))
    
    def create_progress_bar(self, percentage: int, length: int = 20) -> str:
        """Create a cypherpunk-style progress bar"""
        filled = int((percentage / 100) * length)
        empty = length - filled
        
        filled_char = "█"
        empty_char = "▒"
        
        bar = filled_char * filled + empty_char * empty
        return f"[{bar}] {percentage}%"
    
    def create_ascii_art(self, text: str) -> str:
        """Create ASCII art for cypherpunk aesthetic"""
        ascii_patterns = {
            "ACA": """
    ██████╗ █████╗ ██╗   ██╗
    ██╔════╝██╔══██╗╚██╗ ██╔╝
    █████╗  ███████║ ╚████╔╝ 
    ██╔══╝  ██╔══██║  ╚██╔╝  
    ██║     ██║  ██║   ██║   
    ╚═╝     ╚═╝  ╚═╝   ╚═╝   
            """,
            "ARC": """
    ██████╗ ██████╗ ██████╗ 
    ██╔══██╗██╔══██╗██╔══██╗
    ██████╔╝██████╔╝██████╔╝
    ██╔══██╗██╔══██╗██╔══██╗
    ██║  ██║██║  ██║██║  ██║
    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
            """
        }
        return ascii_patterns.get(text.upper(), text)
    
    def glitch_text(self, text: str, intensity: float = 0.3) -> str:
        """Apply glitch effects to text"""
        if random.random() < intensity:
            # Replace some characters with glitch chars
            result = list(text)
            for i in range(len(result)):
                if random.random() < 0.1:  # 10% chance per character
                    result[i] = random.choice(self.glitch_chars)
            return ''.join(result)
        return text
    
    async def send_typing_effect(self, channel, duration: float = 2.0):
        """Send typing indicator with cypherpunk aesthetic"""
        await channel.trigger_typing()
        await asyncio.sleep(duration)

# Global visual effects manager
visual_effects = VisualEffectsManager()
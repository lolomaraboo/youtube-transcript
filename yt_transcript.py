#!/Library/Developer/CommandLineTools/usr/bin/python3
"""
YouTube Transcript Extractor
Extracts transcripts from YouTube videos and optionally saves them to Obsidian.
"""

import argparse
import sys
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List
import subprocess

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    print("❌ Module 'youtube-transcript-api' non installé.")
    print("   Installez-le avec : pip install youtube-transcript-api")
    sys.exit(1)


class YouTubeTranscript:
    def __init__(self, obsidian_path: Optional[str] = None):
        self.obsidian_path = Path(obsidian_path) if obsidian_path else None

    def extract_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from YouTube URL."""
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)',
            r'youtube\.com\/embed\/([^&\n?#]+)',
            r'youtube\.com\/v\/([^&\n?#]+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        # If it's already just an ID
        if re.match(r'^[A-Za-z0-9_-]{11}$', url):
            return url

        return None

    def get_transcript(self, video_id: str, languages: List[str] = ['fr', 'en']) -> Dict:
        """Get transcript for a YouTube video."""
        try:
            api = YouTubeTranscriptApi()
            result = api.fetch(video_id)

            # Extract text from snippets
            text_lines = [snippet.text for snippet in result]

            return {
                'success': True,
                'language': result.language_code,
                'entries': [{'text': s.text, 'start': s.start, 'duration': s.duration} for s in result],
                'text': '\n'.join(text_lines)
            }

        except Exception as e:
            error_msg = str(e)
            if 'transcript' in error_msg.lower():
                return {'success': False, 'error': 'Aucune transcription disponible pour cette vidéo'}
            return {'success': False, 'error': error_msg}

    def copy_to_clipboard(self, text: str) -> bool:
        """Copy text to clipboard (macOS)."""
        try:
            subprocess.run('pbcopy', text=True, input=text, check=True)
            return True
        except Exception as e:
            print(f"❌ Erreur copie presse-papier : {e}")
            return False

    def save_to_obsidian(self, video_id: str, transcript_text: str,
                        title: str = None, tags: List[str] = None,
                        url: str = None) -> bool:
        """Save transcript to Obsidian vault."""
        if not self.obsidian_path:
            print("❌ Chemin Obsidian non configuré")
            return False

        videos_path = self.obsidian_path / "content" / "videos"
        videos_path.mkdir(parents=True, exist_ok=True)

        # Clean title for filename
        safe_title = re.sub(r'[^\w\s-]', '', title or video_id)
        safe_title = re.sub(r'[-\s]+', '-', safe_title)[:50]

        filename = f"{safe_title}-{video_id}.md"
        filepath = videos_path / filename

        # Create YAML frontmatter
        frontmatter = [
            "---",
            f"title: \"{title or 'Sans titre'}\"",
            f"video_id: {video_id}",
            f"date: {datetime.now().strftime('%Y-%m-%d')}",
            f"url: {url or f'https://youtube.com/watch?v={video_id}'}",
        ]

        if tags:
            frontmatter.append(f"tags: [{', '.join(tags)}]")

        frontmatter.append("---")
        frontmatter.append("")

        # Write file
        content = '\n'.join(frontmatter) + '\n' + transcript_text

        try:
            filepath.write_text(content, encoding='utf-8')
            print(f"✅ Sauvegardé : {filepath}")
            return True
        except Exception as e:
            print(f"❌ Erreur sauvegarde : {e}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description='Extraire la transcription de vidéos YouTube',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  yt https://youtube.com/watch?v=VIDEO_ID           # Afficher la transcription
  yt VIDEO_ID --copy                                # Copier dans le presse-papier
  yt VIDEO_ID --save --title "Mon titre" --tags dev,python
        """
    )

    parser.add_argument('url', help='URL YouTube ou ID de vidéo')
    parser.add_argument('-c', '--copy', action='store_true',
                       help='Copier dans le presse-papier')
    parser.add_argument('-s', '--save', action='store_true',
                       help='Sauvegarder dans Obsidian')
    parser.add_argument('-t', '--title', help='Titre de la vidéo (pour Obsidian)')
    parser.add_argument('--tags', help='Tags séparés par des virgules')
    parser.add_argument('-l', '--languages', default='fr,en',
                       help='Langues préférées (défaut: fr,en)')
    parser.add_argument('-o', '--obsidian-path',
                       default='~/Documents/APP_HOME/CascadeProjects/windsurf-project/SecondBrain',
                       help='Chemin vers le vault Obsidian')

    args = parser.parse_args()

    # Initialize
    obsidian_path = Path(args.obsidian_path).expanduser()
    yt = YouTubeTranscript(obsidian_path=obsidian_path)

    # Extract video ID
    video_id = yt.extract_video_id(args.url)
    if not video_id:
        print(f"❌ URL invalide : {args.url}")
        sys.exit(1)

    print(f"🎥 Video ID: {video_id}")

    # Get transcript
    languages = args.languages.split(',')
    result = yt.get_transcript(video_id, languages)

    if not result['success']:
        print(f"❌ Erreur : {result['error']}")
        sys.exit(1)

    print(f"✅ Transcription récupérée ({result['language']})")

    transcript_text = result['text']

    # Copy to clipboard
    if args.copy:
        if yt.copy_to_clipboard(transcript_text):
            print("📋 Copié dans le presse-papier")

    # Save to Obsidian
    if args.save:
        tags = args.tags.split(',') if args.tags else []
        yt.save_to_obsidian(
            video_id=video_id,
            transcript_text=transcript_text,
            title=args.title,
            tags=tags,
            url=args.url
        )

    # Print transcript if not saving or copying
    if not args.copy and not args.save:
        print("\n" + "="*80 + "\n")
        print(transcript_text)
        print("\n" + "="*80)


if __name__ == '__main__':
    main()

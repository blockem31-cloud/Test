import secrets
import string
import webbrowser
import os
from datetime import datetime

class StreamKeyWebsite:
    def __init__(self):
        self.html_content = ""
        
    def generate_stream_key(self, platform="twitch", length=30):
        """Generiert einen sicheren Stream-Key"""
        alphabet = string.ascii_letters + string.digits
        stream_key = ''.join(secrets.choice(alphabet) for _ in range(length))
        
        platforms = {
            "twitch": "live_",
            "youtube": "yt_",
            "facebook": "fb_",
            "custom": "stream_"
        }
        
        prefix = platforms.get(platform.lower(), "stream_")
        return prefix + stream_key
    
    def create_html(self):
        """Erstellt das HTML für die Website"""
        
        # Generiere Beispiel-Keys
        twitch_key = self.generate_stream_key("twitch")
        youtube_key = self.generate_stream_key("youtube")
        facebook_key = self.generate_stream_key("facebook")
        
        self.html_content = f'''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>StreamMaster Pro - Key Generator & OBS Guide</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        .header {{
            text-align: center;
            color: white;
            padding: 40px 20px;
        }}

        .header h1 {{
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}

        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}

        .generator-box {{
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            margin-bottom: 30px;
        }}

        .key-display {{
            background: linear-gradient(45deg, #f3f3f3, #e9e9e9);
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            margin: 30px 0;
        }}

        .key-box {{
            background: #2c3e50;
            color: #00ff88;
            font-family: 'Courier New', monospace;
            font-size: 1.5em;
            padding: 20px;
            border-radius: 10px;
            letter-spacing: 2px;
            word-break: break-all;
            border: 3px solid #34495e;
            margin: 15px 0;
        }}

        .copy-btn {{
            background: #00ff88;
            color: #2c3e50;
            border: none;
            padding: 15px 40px;
            font-size: 1.2em;
            border-radius: 50px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s;
            box-shadow: 0 5px 15px rgba(0,255,136,0.3);
        }}

        .copy-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0,255,136,0.4);
        }}

        .platform-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}

        .platform-card {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            border: 3px solid transparent;
        }}

        .platform-card:hover {{
            transform: scale(1.05);
            border-color: white;
        }}

        .platform-card h3 {{
            font-size: 1.5em;
            margin-bottom: 10px;
        }}

        .platform-card .key-preview {{
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            background: rgba(0,0,0,0.3);
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
        }}

        .obs-guide {{
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}

        .obs-guide h2 {{
            color: #2c3e50;
            margin-bottom: 30px;
            font-size: 2em;
            border-bottom: 3px solid #00ff88;
            padding-bottom: 10px;
        }}

        .steps {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
        }}

        .step {{
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 15px;
            transition: all 0.3s;
        }}

        .step:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}

        .step-number {{
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5em;
            font-weight: bold;
            margin: 0 auto 20px;
        }}

        .step h3 {{
            color: #2c3e50;
            margin-bottom: 15px;
        }}

        .step p {{
            color: #666;
            line-height: 1.6;
        }}

        .server-list {{
            margin-top: 30px;
            padding: 20px;
            background: #f0f0f0;
            border-radius: 10px;
        }}

        .server-item {{
            display: flex;
            justify-content: space-between;
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }}

        .server-item:last-child {{
            border-bottom: none;
        }}

        .server-name {{
            font-weight: bold;
            color: #2c3e50;
        }}

        .server-url {{
            color: #667eea;
            font-family: 'Courier New', monospace;
        }}

        .footer {{
            text-align: center;
            color: white;
            padding: 40px 20px;
        }}

        .notification {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: #00ff88;
            color: #2c3e50;
            padding: 15px 25px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            transform: translateX(400px);
            transition: transform 0.3s;
            z-index: 1000;
        }}

        .notification.show {{
            transform: translateX(0);
        }}

        .custom-key-section {{
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 15px;
        }}

        .custom-input {{
            width: 100%;
            padding: 15px;
            font-size: 1.1em;
            border: 2px solid #ddd;
            border-radius: 10px;
            margin: 15px 0;
            font-family: 'Courier New', monospace;
        }}

        .generate-btn {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 1.1em;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s;
            width: 100%;
        }}

        .generate-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102,126,234,0.4);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎥 StreamMaster Pro</h1>
            <p>Generiere sichere Stream-Keys und erfahre, wie du mit OBS streamst</p>
            <p style="font-size: 0.9em; margin-top: 10px;">Generiert am: {datetime.now().strftime('%d.%m.%Y %H:%M')}</p>
        </div>

        <div class="generator-box">
            <h2 style="color: #2c3e50; margin-bottom: 20px;">Stream-Key Generator</h2>
            
            <div class="key-display">
                <h3 style="color: #2c3e50; margin-bottom: 15px;">Dein aktueller Stream-Key:</h3>
                <div class="key-box" id="currentKey">{twitch_key}</div>
                <button class="copy-btn" onclick="copyToClipboard()">📋 Key kopieren</button>
            </div>

            <h3 style="color: #2c3e50; margin-bottom: 15px;">Wähle eine Plattform:</h3>
            <div class="platform-grid">
                <div class="platform-card" onclick="setKey('{twitch_key}')">
                    <h3>Twitch</h3>
                    <p>live_**********</p>
                    <div class="key-preview">{twitch_key[:20]}...</div>
                </div>
                <div class="platform-card" onclick="setKey('{youtube_key}')">
                    <h3>YouTube</h3>
                    <p>yt_**********</p>
                    <div class="key-preview">{youtube_key[:20]}...</div>
                </div>
                <div class="platform-card" onclick="setKey('{facebook_key}')">
                    <h3>Facebook</h3>
                    <p>fb_**********</p>
                    <div class="key-preview">{facebook_key[:20]}...</div>
                </div>
                <div class="platform-card" onclick="generateCustomKey()">
                    <h3>Custom</h3>
                    <p>🔑 Neu generieren</p>
                    <div class="key-preview">Klicken für neuen Key</div>
                </div>
            </div>

            <div class="custom-key-section">
                <h3 style="color: #2c3e50; margin-bottom: 10px;">Custom Key Generator</h3>
                <input type="number" id="keyLength" class="custom-input" placeholder="Key-Länge (z.B. 30)" min="20" max="50" value="30">
                <button class="generate-btn" onclick="generateCustomKey()">🔑 Neuen Custom Key generieren</button>
            </div>
        </div>

        <div class="obs-guide">
            <h2>📺 OBS Studio Setup Guide</h2>
            
            <div class="steps">
                <div class="step">
                    <div class="step-number">1</div>
                    <h3>OBS installieren</h3>
                    <p>Lade OBS Studio von obsproject.com herunter und installiere es</p>
                </div>
                <div class="step">
                    <div class="step-number">2</div>
                    <h3>Quellen hinzufügen</h3>
                    <p>Füge Display Capture, Window Capture oder Video Capture Device hinzu</p>
                </div>
                <div class="step">
                    <div class="step-number">3</div>
                    <h3>Stream-Key eingeben</h3>
                    <p>Gehe zu Einstellungen > Stream > Stream-Key und füge deinen Key ein</p>
                </div>
                <div class="step">
                    <div class="step-number">4</div>
                    <h3>Stream starten</h3>
                    <p>Klicke auf "Stream starten" und du bist live!</p>
                </div>
            </div>

            <div class="server-list">
                <h3 style="color: #2c3e50; margin-bottom: 20px;">🌍 Streaming Server URLs</h3>
                <div class="server-item">
                    <span class="server-name">Twitch</span>
                    <span class="server-url">rtmp://live.twitch.tv/app/</span>
                </div>
                <div class="server-item">
                    <span class="server-name">YouTube</span>
                    <span class="server-url">rtmp://a.rtmp.youtube.com/live2</span>
                </div>
                <div class="server-item">
                    <span class="server-name">Facebook</span>
                    <span class="server-url">rtmps://live-api-s.facebook.com:443/rtmp/</span>
                </div>
                <div class="server-item">
                    <span class="server-name">Restream.io</span>
                    <span class="server-url">rtmp://live.restream.io/live</span>
                </div>
            </div>

            <div style="margin-top: 30px; padding: 20px; background: #e8f4fd; border-radius: 10px;">
                <h3 style="color: #2c3e50; margin-bottom: 15px;">⚡ Pro-Tipps für OBS:</h3>
                <ul style="color: #666; line-height: 1.8; margin-left: 20px;">
                    <li>Video-Bitrate: 2500-6000 Kbps für 1080p</li>
                    <li>Audio-Bitrate: 160 Kbps</li>
                    <li>Encoder: Hardware (NVENC) wenn verfügbar</li>
                    <li>Keyframe-Intervall: 2 Sekunden</li>
                    <li>Auflösung: 1920x1080 oder 1280x720</li>
                </ul>
            </div>
        </div>

        <div class="footer">
            <p>StreamMaster Pro - Dein professioneller Stream-Key Generator</p>
            <p style="font-size: 0.8em; margin-top: 10px;">🔒 Alle Keys werden lokal in deinem Browser generiert</p>
        </div>
    </div>

    <div class="notification" id="notification">
        ✅ Stream-Key wurde kopiert!
    </div>

    <script>
        function generateCustomKey() {{
            const length = document.getElementById('keyLength').value || 30;
            const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
            let key = 'custom_';
            
            for (let i = 0; i < length; i++) {{
                key += alphabet.charAt(Math.floor(Math.random() * alphabet.length));
            }}
            
            document.getElementById('currentKey').textContent = key;
            showNotification('✅ Neuer Custom Key wurde generiert!');
        }}

        function setKey(key) {{
            document.getElementById('currentKey').textContent = key;
            showNotification('✅ Plattform-Key wurde geladen!');
        }}

        function copyToClipboard() {{
            const keyText = document.getElementById('currentKey').textContent;
            navigator.clipboard.writeText(keyText).then(function() {{
                showNotification('✅ Stream-Key wurde kopiert!');
            }}, function(err) {{
                alert('Fehler beim Kopieren: ' + err);
            }});
        }}

        function showNotification(message) {{
            const notification = document.getElementById('notification');
            notification.textContent = message;
            notification.classList.add('show');
            
            setTimeout(() => {{
                notification.classList.remove('show');
            }}, 3000);
        }}

        // Tastatur-Shortcut für Kopieren (Strg+K)
        document.addEventListener('keydown', function(e) {{
            if (e.ctrlKey && e.key === 'k') {{
                e.preventDefault();
                copyToClipboard();
            }}
        }});
    </script>
</body>
</html>'''
    
    def save_and_open(self, filename="stream_key_generator.html"):
        """Speichert die HTML-Datei und öffnet sie im Browser"""
        
        # HTML-Datei speichern
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.html_content)
        
        # Absoluten Pfad holen
        absolute_path = os.path.abspath(filename)
        
        print(f"\n✅ Stream-Key Generator wurde erstellt!")
        print(f"📁 Datei gespeichert unter: {absolute_path}")
        print(f"🌐 Öffne im Browser...\n")
        
        # Im Standard-Browser öffnen
        webbrowser.open(f'file://{absolute_path}')
        
        return absolute_path
    
    def print_instructions(self):
        """Zeigt zusätzliche Anweisungen an"""
        print("="*60)
        print("📺 STREAM-KEY GENERATOR - ANLEITUNG")
        print("="*60)
        print("""
1️⃣  Die Website wurde in deinem Browser geöffnet
2️⃣  Wähle eine Plattform (Twitch, YouTube, Facebook)
3️⃣  Kopiere den generierten Key mit einem Klick
4️⃣  Öffne OBS Studio
5️⃣  Gehe zu: Einstellungen > Stream
6️⃣  Wähle deinen Streaming-Dienst
7️⃣  Füge den Stream-Key ein
8️⃣  Starte deinen Stream!

📌 WICHTIG:
- Teile deinen Stream-Key mit niemandem!
- Generiere bei Verdacht auf Missbrauch einen neuen Key
- Jede Plattform hat eigene Server-URLs (in der Website aufgelistet)

🎮 VIEL ERFOLG BEIM STREAMEN!
        """)
        print("="*60)

def main():
    """Hauptfunktion"""
    print("🎬 StreamMaster Pro - Stream-Key Generator wird gestartet...")
    
    # Generator erstellen
    generator = StreamKeyWebsite()
    
    # HTML erstellen
    generator.create_html()
    
    # Speichern und öffnen
    generator.save_and_open()
    
    # Anleitung zeigen
    generator.print_instructions()

if __name__ == "__main__":
    main()

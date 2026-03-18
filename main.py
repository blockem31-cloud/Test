import os
import secrets
import string
import uuid
import json
from datetime import datetime
from flask import Flask, render_template_string, jsonify, request

# Flask App initialisieren
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# In-Memory Speicher
streams = {}
stream_keys = {}
active_viewers = {}

class StreamHub:
    @staticmethod
    def generate_stream_key(username="anonymous", length=32):
        """Generiert einen sicheren Stream-Key"""
        random_part = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        stream_key = f"stream_{username}_{timestamp}_{random_part}"
        
        stream_id = str(uuid.uuid4())[:8]
        
        stream_data = {
            "id": stream_id,
            "username": username,
            "created": datetime.now().strftime("%d.%m.%Y %H:%M"),
            "active": False,
            "viewers": 0,
            "title": f"{username}'s Stream",
            "category": "Just Chatting",
            "key": stream_key
        }
        
        stream_keys[stream_key] = stream_data
        streams[stream_id] = stream_data
        
        return stream_key, stream_id
    
    @staticmethod
    def get_rtmp_url():
        railway_url = os.environ.get('RAILWAY_PUBLIC_DOMAIN', 'localhost')
        return f"rtmp://{railway_url}/live"

# HTML Template (All-in-One)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>StreamHub - Anonyme Streaming-Plattform</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #141414, #1a1a1a);
            color: white;
            min-height: 100vh;
        }

        .navbar {
            background: rgba(0,0,0,0.9);
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #ff3366;
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .logo {
            font-size: 1.8em;
            font-weight: bold;
            color: #ff3366;
            text-decoration: none;
        }

        .nav-links a {
            color: white;
            text-decoration: none;
            margin-left: 25px;
            padding: 8px 15px;
            border-radius: 20px;
            transition: all 0.3s;
        }

        .nav-links a:hover {
            background: #ff3366;
        }

        .nav-links .live-badge {
            background: #ff3366;
            animation: pulse 1.5s infinite;
        }

        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.7; }
            100% { opacity: 1; }
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }

        .hero {
            background: linear-gradient(45deg, #ff3366, #ff8c00);
            border-radius: 20px;
            padding: 40px;
            margin: 30px 0;
            text-align: center;
        }

        .hero h1 {
            font-size: 2.5em;
            margin-bottom: 20px;
        }

        .server-info {
            background: rgba(0,0,0,0.3);
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            font-size: 1.1em;
        }

        .server-info code {
            background: #333;
            padding: 5px 10px;
            border-radius: 5px;
            color: #00ff88;
            margin: 0 10px;
        }

        .copy-btn-small {
            background: #ff3366;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 5px;
            cursor: pointer;
        }

        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.95);
            z-index: 1000;
        }

        .modal-content {
            position: relative;
            width: 90%;
            max-width: 600px;
            margin: 50px auto;
            background: #1a1a1a;
            border-radius: 20px;
            padding: 30px;
            border: 1px solid #ff3366;
        }

        .close {
            position: absolute;
            top: 15px;
            right: 20px;
            font-size: 2em;
            color: #ff3366;
            cursor: pointer;
        }

        .form-group {
            margin: 20px 0;
        }

        .form-group label {
            display: block;
            margin-bottom: 8px;
            color: #ff3366;
        }

        .form-group input, .form-group select {
            width: 100%;
            padding: 12px;
            background: #333;
            border: 1px solid #444;
            border-radius: 8px;
            color: white;
            font-size: 1em;
        }

        .generate-btn {
            width: 100%;
            padding: 15px;
            background: #ff3366;
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1.2em;
            cursor: pointer;
            margin: 20px 0;
        }

        .generate-btn:hover {
            background: #ff1a4f;
            transform: translateY(-2px);
        }

        .key-result {
            margin-top: 30px;
            padding: 20px;
            background: #333;
            border-radius: 10px;
        }

        .key-box {
            background: #1a1a1a;
            color: #00ff88;
            font-family: 'Courier New', monospace;
            font-size: 1.1em;
            padding: 15px;
            border-radius: 8px;
            word-break: break-all;
            margin: 15px 0;
            border: 1px solid #ff3366;
        }

        .copy-btn {
            background: #00ff88;
            color: #1a1a1a;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
        }

        .obs-info {
            margin: 20px 0;
            padding: 15px;
            background: #222;
            border-radius: 8px;
        }

        .obs-info code {
            background: #1a1a1a;
            color: #ff3366;
            padding: 3px 8px;
            border-radius: 4px;
        }

        .start-stream-btn {
            width: 100%;
            padding: 15px;
            background: #00ff88;
            color: #1a1a1a;
            border: none;
            border-radius: 10px;
            font-size: 1.2em;
            font-weight: bold;
            cursor: pointer;
        }

        .section-title {
            margin: 40px 0 20px;
            font-size: 2em;
        }

        .stream-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin: 30px 0;
        }

        .stream-card {
            background: #222;
            border-radius: 15px;
            overflow: hidden;
            cursor: pointer;
            transition: all 0.3s;
            border: 1px solid #333;
        }

        .stream-card:hover {
            transform: translateY(-10px);
            border-color: #ff3366;
        }

        .stream-preview {
            height: 180px;
            background: linear-gradient(45deg, #ff3366, #ff8c00);
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }

        .preview-placeholder {
            font-size: 4em;
        }

        .live-badge {
            position: absolute;
            top: 10px;
            left: 10px;
            background: #ff3366;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 0.8em;
            font-weight: bold;
        }

        .viewer-count {
            position: absolute;
            bottom: 10px;
            right: 10px;
            background: rgba(0,0,0,0.7);
            padding: 5px 10px;
            border-radius: 5px;
        }

        .stream-info {
            padding: 20px;
        }

        .stream-title {
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 8px;
        }

        .streamer-name {
            color: #ff3366;
            margin-bottom: 5px;
        }

        .stream-category {
            color: #999;
            font-size: 0.9em;
        }

        .stream-player {
            max-width: 1200px;
        }

        .video-container {
            width: 100%;
            height: 400px;
            background: #000;
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 20px;
        }

        .video-placeholder {
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #1a1a1a, #222);
        }

        .spinner {
            width: 50px;
            height: 50px;
            border: 3px solid #333;
            border-top: 3px solid #ff3366;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 20px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .stream-info-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px;
            background: #222;
            border-radius: 10px;
            margin-bottom: 20px;
        }

        .viewer-stats {
            background: #ff3366;
            padding: 8px 15px;
            border-radius: 20px;
        }

        .chat-container {
            background: #1a1a1a;
            border-radius: 10px;
            overflow: hidden;
        }

        .chat-messages {
            height: 200px;
            overflow-y: auto;
            padding: 15px;
        }

        .chat-message {
            margin: 10px 0;
            color: #ccc;
        }

        .chat-message.system {
            color: #ff3366;
        }

        .chat-message .time {
            color: #666;
            font-size: 0.8em;
            margin-right: 10px;
        }

        .chat-message .username {
            color: #ff3366;
            font-weight: bold;
            margin-right: 10px;
        }

        .chat-input {
            display: flex;
            padding: 15px;
            background: #222;
        }

        .chat-input input {
            flex: 1;
            padding: 10px;
            background: #333;
            border: 1px solid #444;
            border-radius: 5px 0 0 5px;
            color: white;
        }

        .chat-input button {
            padding: 10px 20px;
            background: #ff3366;
            color: white;
            border: none;
            border-radius: 0 5px 5px 0;
            cursor: pointer;
        }

        .notification {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: #ff3366;
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            transform: translateX(400px);
            transition: transform 0.3s;
            z-index: 1000;
        }

        .notification.show {
            transform: translateX(0);
        }

        .footer {
            text-align: center;
            padding: 40px;
            border-top: 1px solid #333;
            margin-top: 50px;
            color: #666;
        }

        .timestamp {
            font-size: 0.8em;
            margin-top: 10px;
        }

        @media (max-width: 768px) {
            .hero h1 {
                font-size: 1.8em;
            }
            
            .modal-content {
                width: 95%;
                padding: 20px;
            }
            
            .video-container {
                height: 250px;
            }
        }
    </style>
</head>
<body>
    <div class="navbar">
        <a href="/" class="logo">🔴 StreamHub</a>
        <div class="nav-links">
            <a href="/">Home</a>
            <a href="#" class="live-badge" id="liveCount">🔴 LIVE (0)</a>
            <a href="#" onclick="showGenerator()">Key Generator</a>
        </div>
    </div>

    <div class="container">
        <div class="hero">
            <h1>StreamHub - Anonyme Streaming-Plattform</h1>
            <p>Generiere sichere Stream-Keys und starte sofort mit OBS</p>
            <div class="server-info">
                <strong>RTMP Server:</strong> 
                <code id="rtmpUrl">{{ rtmp_url }}</code>
                <button class="copy-btn-small" onclick="copyRtmpUrl()">📋</button>
            </div>
        </div>

        <!-- Key Generator Modal -->
        <div class="modal" id="keyGeneratorModal">
            <div class="modal-content">
                <span class="close" onclick="closeGenerator()">&times;</span>
                <h2>🔑 Stream-Key Generator</h2>
                
                <div class="form-group">
                    <label>Dein Name:</label>
                    <input type="text" id="username" placeholder="Anonymous" value="Streamer_{{ range(100, 999) | random }}">
                </div>
                
                <div class="form-group">
                    <label>Stream-Titel:</label>
                    <input type="text" id="title" placeholder="Mein Stream" value="Mein Live Stream">
                </div>
                
                <div class="form-group">
                    <label>Kategorie:</label>
                    <select id="category">
                        <option>Just Chatting</option>
                        <option>Gaming</option>
                        <option>Music</option>
                        <option>Creative</option>
                        <option>Sports</option>
                    </select>
                </div>
                
                <button class="generate-btn" onclick="generateKey()">🔑 Key generieren</button>
                
                <div class="key-result" id="keyResult" style="display: none;">
                    <h3>Dein Stream-Key:</h3>
                    <div class="key-box" id="generatedKey"></div>
                    <button class="copy-btn" onclick="copyKey()">📋 Key kopieren</button>
                    
                    <div class="obs-info">
                        <h4>📺 OBS Einstellungen:</h4>
                        <p><strong>Server:</strong> <code id="obsServer">{{ rtmp_url }}</code></p>
                        <p><strong>Stream-Key:</strong> <code id="obsKey"></code></p>
                    </div>
                    
                    <button class="start-stream-btn" onclick="startStream()">🔴 Stream starten</button>
                </div>
            </div>
        </div>

        <h2 class="section-title">🔴 Live jetzt</h2>
        <div class="stream-grid" id="streamGrid">
            {% for stream in streams %}
            <div class="stream-card" onclick="openStream('{{ stream.id }}')">
                <div class="stream-preview">
                    <div class="preview-placeholder">
                        {% if stream.category == 'Gaming' %}🎮
                        {% elif stream.category == 'Music' %}🎵
                        {% elif stream.category == 'Tech' %}💻
                        {% else %}📺{% endif %}
                    </div>
                    <span class="live-badge">LIVE</span>
                    <span class="viewer-count">👥 {{ stream.viewers }}</span>
                </div>
                <div class="stream-info">
                    <div class="stream-title">{{ stream.title }}</div>
                    <div class="streamer-name">👤 {{ stream.username }}</div>
                    <div class="stream-category">{{ stream.category }}</div>
                </div>
            </div>
            {% endfor %}
        </div>

        <!-- Stream Player Modal -->
        <div class="modal" id="streamModal">
            <div class="modal-content stream-player">
                <span class="close" onclick="closeStream()">&times;</span>
                
                <div class="video-container">
                    <div class="video-placeholder" id="videoPlaceholder">
                        <div class="spinner"></div>
                        <h3>Stream wird geladen...</h3>
                        <p>Warte auf Stream-Signal</p>
                    </div>
                </div>
                
                <div class="stream-info-bar">
                    <div class="stream-details" id="streamDetails">
                        <h3 id="streamTitle"></h3>
                        <p id="streamerName"></p>
                    </div>
                    <div class="viewer-stats" id="viewerStats">
                        👥 <span id="viewerCount">0</span> Zuschauer
                    </div>
                </div>
                
                <div class="chat-container">
                    <div class="chat-messages" id="chatMessages">
                        <div class="chat-message system">
                            <span class="time">System:</span> Willkommen im Stream!
                        </div>
                    </div>
                    
                    <div class="chat-input">
                        <input type="text" id="chatInput" placeholder="Chat als Anonymous...">
                        <button onclick="sendChat()">📨</button>
                    </div>
                </div>
            </div>
        </div>

        <div class="notification" id="notification"></div>
    </div>

    <div class="footer">
        <p>© 2024 StreamHub - Anonyme Streaming-Plattform</p>
        <p class="timestamp">Generiert: {{ current_time }}</p>
    </div>

    <script>
        let currentStreamId = null;
        let currentStreamKey = null;
        
        function showGenerator() {
            document.getElementById('keyGeneratorModal').style.display = 'block';
        }
        
        function closeGenerator() {
            document.getElementById('keyGeneratorModal').style.display = 'none';
        }
        
        function copyRtmpUrl() {
            const url = document.getElementById('rtmpUrl').textContent;
            navigator.clipboard.writeText(url);
            showNotification('✅ RTMP URL kopiert!');
        }
        
        async function generateKey() {
            const username = document.getElementById('username').value;
            const title = document.getElementById('title').value;
            const category = document.getElementById('category').value;
            
            const response = await fetch('/api/generate_key', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username, title, category})
            });
            
            const data = await response.json();
            
            if (data.success) {
                currentStreamKey = data.stream_key;
                document.getElementById('generatedKey').textContent = data.stream_key;
                document.getElementById('obsKey').textContent = data.stream_key;
                document.getElementById('obsServer').textContent = data.rtmp_url;
                document.getElementById('keyResult').style.display = 'block';
                showNotification('✅ Key generiert!');
            }
        }
        
        function copyKey() {
            const key = document.getElementById('generatedKey').textContent;
            navigator.clipboard.writeText(key);
            showNotification('✅ Key kopiert!');
        }
        
        async function startStream() {
            if (!currentStreamKey) return;
            
            // Hier Stream als live markieren
            showNotification('🔴 Stream ist bereit! Starte OBS...');
            closeGenerator();
            
            // Simuliere neuen Stream in der Grid
            addStreamToGrid();
        }
        
        function addStreamToGrid() {
            const username = document.getElementById('username').value;
            const title = document.getElementById('title').value;
            const category = document.getElementById('category').value;
            
            const grid = document.getElementById('streamGrid');
            const newCard = document.createElement('div');
            newCard.className = 'stream-card';
            newCard.innerHTML = `
                <div class="stream-preview">
                    <div class="preview-placeholder">🔴</div>
                    <span class="live-badge">LIVE</span>
                    <span class="viewer-count">👥 0</span>
                </div>
                <div class="stream-info">
                    <div class="stream-title">${title}</div>
                    <div class="streamer-name">👤 ${username}</div>
                    <div class="stream-category">${category}</div>
                </div>
            `;
            
            grid.prepend(newCard);
        }
        
        function openStream(streamId) {
            currentStreamId = streamId;
            document.getElementById('streamModal').style.display = 'block';
            
            // Simuliere Stream-Details
            document.getElementById('streamTitle').textContent = 'Live Stream';
            document.getElementById('streamerName').textContent = 'Streamer';
            
            // Starte Zuschauer-Simulation
            startViewerSimulation();
        }
        
        function closeStream() {
            document.getElementById('streamModal').style.display = 'none';
        }
        
        function startViewerSimulation() {
            let viewers = 0;
            setInterval(() => {
                viewers += Math.floor(Math.random() * 3);
                document.getElementById('viewerCount').textContent = viewers;
            }, 5000);
        }
        
        function sendChat() {
            const input = document.getElementById('chatInput');
            const message = input.value.trim();
            
            if (message) {
                const chatMessages = document.getElementById('chatMessages');
                const msgDiv = document.createElement('div');
                msgDiv.className = 'chat-message';
                msgDiv.innerHTML = `<span class="username">Anonymous:</span> ${message}`;
                chatMessages.appendChild(msgDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
                input.value = '';
            }
        }
        
        function showNotification(message) {
            const notification = document.getElementById('notification');
            notification.textContent = message;
            notification.classList.add('show');
            
            setTimeout(() => {
                notification.classList.remove('show');
            }, 3000);
        }
        
        // Chat-Enter-Taste
        document.getElementById('chatInput')?.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendChat();
            }
        });
        
        // Live-Count aktualisieren
        setInterval(() => {
            const cards = document.querySelectorAll('.stream-card').length;
            document.getElementById('liveCount').textContent = `🔴 LIVE (${cards})`;
        }, 5000);
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Hauptseite"""
    demo_streams = []
    for i in range(3):
        username = f"Streamer{i+1}"
        stream_data = {
            "id": str(uuid.uuid4())[:8],
            "username": username,
            "title": f"{username}'s Live Stream",
            "category": ["Gaming", "Music", "Tech"][i],
            "viewers": secrets.randbelow(1000) + 100
        }
        demo_streams.append(stream_data)
    
    return render_template_string(
        HTML_TEMPLATE,
        streams=demo_streams,
        current_time=datetime.now().strftime('%d.%m.%Y %H:%M'),
        rtmp_url=StreamHub.get_rtmp_url()
    )

@app.route('/api/generate_key', methods=['POST'])
def generate_key():
    """API-Endpunkt für Stream-Keys"""
    data = request.json
    username = data.get('username', 'Anonymous')
    title = data.get('title', 'Mein Stream')
    category = data.get('category', 'Just Chatting')
    
    stream_key, stream_id = StreamHub.generate_stream_key(username)
    
    streams[stream_id]['title'] = title
    streams[stream_id]['category'] = category
    
    return jsonify({
        'success': True,
        'stream_key': stream_key,
        'stream_id': stream_id,
        'rtmp_url': StreamHub.get_rtmp_url(),
        'message': 'Stream-Key erfolgreich generiert!'
    })

@app.route('/api/streams')
def get_streams():
    """API für aktive Streams"""
    active_streams = []
    for sid, stream in streams.items():
        if stream.get('active', False):
            active_streams.append({
                'id': sid,
                'username': stream['username'],
                'title': stream['title'],
                'category': stream['category'],
                'viewers': stream['viewers']
            })
    
    return jsonify({
        'success': True,
        'streams': active_streams,
        'count': len(active_streams)
    })

@app.route('/api/stream/<stream_id>')
def get_stream(stream_id):
    """API für einzelnen Stream"""
    if stream_id in streams:
        stream = streams[stream_id]
        stream['viewers'] += 1
        return jsonify({
            'success': True,
            'stream': {
                'id': stream_id,
                'username': stream['username'],
                'title': stream['title'],
                'category': stream['category'],
                'viewers': stream['viewers'],
                'created': stream['created']
            }
        })
    
    return jsonify({'success': False, 'error': 'Stream nicht gefunden'}), 404

@app.route('/api/stream/<stream_id>/start', methods=['POST'])
def start_stream(stream_id):
    """Stream starten"""
    if stream_id in streams:
        streams[stream_id]['active'] = True
        streams[stream_id]['viewers'] = 0
        return jsonify({'success': True, 'message': 'Stream gestartet!'})
    
    return jsonify({'success': False, 'error': 'Stream nicht gefunden'}), 404

@app.route('/health')
def health():
    """Health Check für Railway"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'streams': len(streams)
    })

# Für lokale Entwicklung
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

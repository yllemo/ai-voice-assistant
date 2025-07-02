import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import pyaudio
import wave
import tempfile
import os
import requests
from datetime import datetime
import whisper

class AIVoiceAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Voice Assistant")
        self.root.geometry("1200x900")
        
        # Dark theme colors - improved contrast
        self.colors = {
            'bg': '#1a1a1a',
            'surface': '#2a2a2a',
            'surface_light': '#3a3a3a',
            'surface_dark': '#1f1f1f',
            'primary': '#4a9eff',
            'primary_dark': '#3d7acc',
            'accent': '#ff6b6b',
            'success': '#00d4aa',
            'warning': '#ffb74d',
            'error': '#ff5252',
            'text': '#ffffff',
            'text_secondary': '#b8b8b8',
            'text_muted': '#888888',
            'border': '#404040'
        }
        
        # Configure root window
        self.root.configure(bg=self.colors['bg'])
        
        # Audio recording variables
        self.is_recording = False
        self.audio_frames = []
        self.audio_stream = None
        self.p = pyaudio.PyAudio()
        
        # Whisper model
        self.whisper_model = None
        self.model_loaded = False
        
        # LM Studio settings
        self.lm_studio_url = "http://localhost:1234/v1/chat/completions"
        self.api_key = "lm-studio"
        
        # Audio settings
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        
        # Conversation context
        self.conversation_history = []
        self.current_transcription = ""
        self.transcription_in_context = False
        
        # Initialize UI directly
        self.setup_dark_theme()
        self.setup_ui()
        self.load_whisper_model()
        
        print("AIVoiceAssistant initialized successfully")
    
    def setup_dark_theme(self):
        """Configure dark theme for ttk widgets"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles for dark theme
        style.configure('Dark.TButton', 
                       background=self.colors['primary'], 
                       foreground='white',
                       borderwidth=0,
                       relief='flat',
                       font=('Segoe UI', 10))
        style.map('Dark.TButton',
                 background=[('active', self.colors['primary_dark']),
                           ('pressed', self.colors['primary_dark'])])
        
        style.configure('Accent.TButton',
                       background=self.colors['accent'],
                       foreground='white',
                       borderwidth=0,
                       relief='flat',
                       font=('Segoe UI', 10, 'bold'))
        style.map('Accent.TButton',
                 background=[('active', '#e55555'),
                           ('pressed', '#e55555')])
        
        style.configure('Success.TButton',
                       background=self.colors['success'],
                       foreground='white',
                       borderwidth=0,
                       relief='flat',
                       font=('Segoe UI', 10))
        style.map('Success.TButton',
                 background=[('active', '#45a049'),
                           ('pressed', '#45a049')])
        
        style.configure('Dark.TEntry',
                       fieldbackground=self.colors['surface_light'],
                       background=self.colors['surface_light'],
                       foreground=self.colors['text'],
                       borderwidth=1,
                       relief='flat',
                       insertcolor=self.colors['text'])
    
    def setup_ui(self):
        print("Setting up UI...")
        
        # Create main layout
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        print("Main container created")
        
        # Title
        title_frame = tk.Frame(main_container, bg=self.colors['bg'])
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(title_frame, 
                              text="🎤 AI Voice Assistant", 
                              font=('Segoe UI', 24, 'bold'),
                              bg=self.colors['bg'],
                              fg=self.colors['primary'])
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame,
                                 text="Speak • Transcribe • Chat with AI",
                                 font=('Segoe UI', 12),
                                 bg=self.colors['bg'],
                                 fg=self.colors['text_secondary'])
        subtitle_label.pack()
        print("Title created")
        
        # Content area with resizable columns
        content_frame = tk.Frame(main_container, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        print("Content frame created")
        
        # Left Column - 40% of width, resizable
        left_column = tk.Frame(content_frame, bg=self.colors['bg'])
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        left_column.configure(width=480)  # Initial width
        print("Left column created")
        
        # Right Column - 60% of width, resizable
        right_column = tk.Frame(content_frame, bg=self.colors['bg'])
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        print("Right column created")
        
        # Setup sections
        self.setup_recording_section(left_column)
        self.setup_settings_section(left_column)
        self.setup_transcription_section(left_column)
        self.setup_chat_section(right_column)
        self.setup_status_bar(main_container)
        
        print("UI setup complete!")
    
    def create_section_frame(self, parent, title):
        """Create a styled section frame with title"""
        container = tk.Frame(parent, bg=self.colors['bg'])
        container.pack(fill=tk.BOTH, expand=False, pady=(0, 15))
        
        # Section title
        title_label = tk.Label(container,
                              text=title,
                              font=('Segoe UI', 12, 'bold'),
                              bg=self.colors['bg'],
                              fg=self.colors['primary'])
        title_label.pack(anchor=tk.W, pady=(0, 8))
        
        # Section content frame
        content_frame = tk.Frame(container, 
                                bg=self.colors['surface'],
                                relief='flat',
                                borderwidth=1)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        return content_frame
    
    def setup_recording_section(self, parent):
        recording_frame = self.create_section_frame(parent, "🎙️ Audio Recording")
        print("Recording section created")
        
        # Recording controls
        controls_frame = tk.Frame(recording_frame, bg=self.colors['surface'])
        controls_frame.pack(fill=tk.X, pady=10, padx=10)
        
        self.record_button = ttk.Button(controls_frame, 
                                       text="🔴 Start Recording", 
                                       style="Accent.TButton",
                                       command=self.toggle_recording)
        self.record_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(controls_frame, 
                  text="📁 Load File", 
                  style="Dark.TButton",
                  command=self.load_audio_file).pack(side=tk.LEFT)
        
        # Recording status
        self.recording_status = tk.Label(recording_frame,
                                        text="Ready to record",
                                        font=('Segoe UI', 10),
                                        bg=self.colors['surface'],
                                        fg=self.colors['text_secondary'])
        self.recording_status.pack(anchor=tk.W, padx=10, pady=(0, 10))
    
    def setup_settings_section(self, parent):
        settings_frame = self.create_section_frame(parent, "⚙️ LM Studio")
        print("Settings section created")
        
        settings_content = tk.Frame(settings_frame, bg=self.colors['surface'])
        settings_content.pack(fill=tk.X, pady=10, padx=10)
        
        # URL input
        url_frame = tk.Frame(settings_content, bg=self.colors['surface'])
        url_frame.pack(fill=tk.X, pady=(0, 8))
        
        tk.Label(url_frame, 
                text="Server URL:", 
                font=('Segoe UI', 10, 'bold'),
                bg=self.colors['surface'],
                fg=self.colors['text']).pack(side=tk.LEFT, padx=(0, 8))
        
        self.url_entry = ttk.Entry(url_frame, 
                                  style="Dark.TEntry",
                                  font=('Segoe UI', 9),
                                  width=35)
        self.url_entry.insert(0, self.lm_studio_url)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        
        ttk.Button(url_frame, 
                  text="🔗 Test", 
                  style="Dark.TButton",
                  command=self.test_lm_studio_connection).pack(side=tk.RIGHT)
        
        # Connection status
        self.connection_status = tk.Label(settings_content,
                                         text="● Not connected",
                                         font=('Segoe UI', 9),
                                         bg=self.colors['surface'],
                                         fg=self.colors['error'])
        self.connection_status.pack(anchor=tk.W)
    
    def setup_transcription_section(self, parent):
        transcription_frame = self.create_section_frame(parent, "📝 Transcription")
        # Make transcription section expandable in the left column
        transcription_frame.master.pack_configure(fill=tk.BOTH, expand=True)
        print("Transcription section created")
        
        # Transcription display
        text_frame = tk.Frame(transcription_frame, bg=self.colors['surface'])
        text_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        self.transcription_text = tk.Text(text_frame, 
                                         height=6,  # Reduced height for better proportions
                                         wrap=tk.WORD,
                                         bg=self.colors['surface_light'],
                                         fg=self.colors['text'],
                                         font=('Segoe UI', 11),
                                         relief='flat',
                                         borderwidth=1,
                                         insertbackground=self.colors['text'],
                                         selectbackground=self.colors['primary'])
        
        scrollbar_trans = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.transcription_text.yview)
        self.transcription_text.configure(yscrollcommand=scrollbar_trans.set)
        
        self.transcription_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        scrollbar_trans.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Transcription controls
        trans_controls = tk.Frame(transcription_frame, bg=self.colors['surface'])
        trans_controls.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.transcribe_button = ttk.Button(trans_controls, 
                                           text="🎯 Transcribe & Analyze", 
                                           style="Success.TButton",
                                           command=self.transcribe_and_send)
        self.transcribe_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(trans_controls, 
                  text="🗑️ Clear", 
                  style="Dark.TButton",
                  command=self.clear_transcription).pack(side=tk.LEFT)
    
    def setup_chat_section(self, parent):
        chat_frame = self.create_section_frame(parent, "💬 AI Conversation")
        # Make chat section fully expandable
        chat_frame.master.pack_configure(fill=tk.BOTH, expand=True)
        print("Chat section created")
        
        # Chat display
        chat_display_frame = tk.Frame(chat_frame, bg=self.colors['surface'])
        chat_display_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        self.chat_display = tk.Text(chat_display_frame,
                                   wrap=tk.WORD,
                                   bg=self.colors['surface_dark'],
                                   fg=self.colors['text'],
                                   font=('Segoe UI', 10),
                                   relief='flat',
                                   borderwidth=1,
                                   state=tk.DISABLED,
                                   insertbackground=self.colors['text'],
                                   selectbackground=self.colors['primary'])
        
        scrollbar_chat = ttk.Scrollbar(chat_display_frame, orient=tk.VERTICAL, command=self.chat_display.yview)
        self.chat_display.configure(yscrollcommand=scrollbar_chat.set)
        
        self.chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        scrollbar_chat.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure text tags
        self.chat_display.tag_configure("user", foreground=self.colors['primary'], font=('Segoe UI', 10, 'bold'))
        self.chat_display.tag_configure("assistant", foreground=self.colors['text'], font=('Segoe UI', 10))
        self.chat_display.tag_configure("error", foreground=self.colors['error'], font=('Segoe UI', 10))
        self.chat_display.tag_configure("system", foreground=self.colors['warning'], font=('Segoe UI', 9, 'italic'))
        self.chat_display.tag_configure("timestamp", foreground=self.colors['text_muted'], font=('Segoe UI', 8))
        
        # Chat input area
        chat_input_frame = tk.Frame(chat_frame, bg=self.colors['surface'])
        chat_input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        input_controls_frame = tk.Frame(chat_input_frame, bg=self.colors['surface'])
        input_controls_frame.pack(fill=tk.X)
        
        self.chat_input = tk.Text(input_controls_frame,
                                 height=3,
                                 wrap=tk.WORD,
                                 bg=self.colors['surface_light'],
                                 fg=self.colors['text'],
                                 font=('Segoe UI', 10),
                                 relief='flat',
                                 borderwidth=1,
                                 insertbackground=self.colors['text'],
                                 selectbackground=self.colors['primary'])
        self.chat_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.chat_input.bind("<Return>", self.handle_enter_key)
        self.chat_input.bind("<Control-Return>", lambda e: self.insert_newline())
        
        # Input buttons
        input_buttons_frame = tk.Frame(input_controls_frame, bg=self.colors['surface'])
        input_buttons_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        ttk.Button(input_buttons_frame,
                  text="📤 Send",
                  style="Success.TButton",
                  command=self.send_manual_message).pack(pady=(0, 5), fill=tk.X)
        
        ttk.Button(input_buttons_frame,
                  text="📝 Use Text",
                  style="Dark.TButton",
                  command=self.use_transcription_in_chat).pack(fill=tk.X)
        
        # Chat controls
        chat_controls = tk.Frame(chat_frame, bg=self.colors['surface'])
        chat_controls.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(chat_controls, 
                  text="🗑️ Clear Chat", 
                  style="Dark.TButton",
                  command=self.clear_chat).pack(side=tk.LEFT, padx=(0, 10))
        
        # Auto-analyze toggle
        self.auto_transcribe_var = tk.BooleanVar(value=True)
        auto_check = tk.Checkbutton(chat_controls,
                                   text="Auto-analyze transcript",
                                   variable=self.auto_transcribe_var,
                                   bg=self.colors['surface'],
                                   fg=self.colors['text'],
                                   selectcolor=self.colors['surface_light'],
                                   activebackground=self.colors['surface'],
                                   activeforeground=self.colors['text'],
                                   font=('Segoe UI', 9))
        auto_check.pack(side=tk.RIGHT)
    
    def setup_status_bar(self, parent):
        status_frame = tk.Frame(parent, bg=self.colors['surface_dark'], height=40)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(15, 0))
        status_frame.pack_propagate(False)
        print("Status bar created")
        
        # Status content
        status_content = tk.Frame(status_frame, bg=self.colors['surface_dark'])
        status_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        
        self.status_var = tk.StringVar()
        self.status_var.set("🟢 Ready")
        
        self.status_label = tk.Label(status_content,
                                    textvariable=self.status_var,
                                    bg=self.colors['surface_dark'],
                                    fg=self.colors['text'],
                                    font=('Segoe UI', 10),
                                    anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Whisper model status
        self.model_status = tk.Label(status_content,
                                    text="🔄 Loading Whisper...",
                                    bg=self.colors['surface_dark'],
                                    fg=self.colors['warning'],
                                    font=('Segoe UI', 9))
        self.model_status.pack(side=tk.RIGHT)

    # All the method implementations from before...
    def load_whisper_model(self):
        """Load Whisper model in a separate thread"""
        def load_model():
            try:
                self.model_status.config(text="🔄 Loading Whisper...", fg=self.colors['warning'])
                self.whisper_model = whisper.load_model("base")
                self.model_loaded = True
                self.model_status.config(text="✅ Whisper Ready", fg=self.colors['success'])
                self.status_var.set("🟢 Ready - Whisper model loaded")
            except Exception as e:
                self.model_status.config(text="❌ Whisper Failed", fg=self.colors['error'])
                self.status_var.set(f"❌ Error loading Whisper: {str(e)}")
        
        threading.Thread(target=load_model, daemon=True).start()
    
    def toggle_recording(self):
        """Start or stop audio recording"""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        """Start recording audio"""
        try:
            self.audio_frames = []
            self.audio_stream = self.p.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk
            )
            
            self.is_recording = True
            self.record_button.config(text="⏹️ Stop Recording")
            self.recording_status.config(text="🔴 Recording in progress...", fg=self.colors['error'])
            self.status_var.set("🔴 Recording audio...")
            
            threading.Thread(target=self.record_audio, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Recording Error", f"Failed to start recording: {str(e)}")
    
    def record_audio(self):
        """Record audio data"""
        while self.is_recording:
            try:
                data = self.audio_stream.read(self.chunk)
                self.audio_frames.append(data)
            except Exception as e:
                print(f"Recording error: {e}")
                break
    
    def stop_recording(self):
        """Stop recording audio"""
        self.is_recording = False
        
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
        
        self.record_button.config(text="🔴 Start Recording")
        self.recording_status.config(text="✅ Recording completed", fg=self.colors['success'])
        
        if self.audio_frames:
            self.save_recording()
            if self.auto_transcribe_var.get():
                self.transcribe_and_send()
    
    def save_recording(self):
        """Save the recorded audio to a temporary file"""
        try:
            self.temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            
            wf = wave.open(self.temp_audio_file.name, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.audio_frames))
            wf.close()
            
            self.transcribe_button.config(state="normal")
            
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save recording: {str(e)}")
    
    def load_audio_file(self):
        """Load an audio file for transcription"""
        file_path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[
                ("Audio Files", "*.wav *.mp3 *.m4a *.flac *.ogg"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            self.temp_audio_file = type('obj', (object,), {'name': file_path})()
            self.transcribe_button.config(state="normal")
            self.recording_status.config(text=f"📁 Loaded: {os.path.basename(file_path)}", fg=self.colors['success'])
    
    def transcribe_and_send(self):
        """Transcribe audio and automatically send to AI"""
        if not self.model_loaded:
            messagebox.showerror("Model Error", "Whisper model not loaded yet. Please wait.")
            return
        
        if not hasattr(self, 'temp_audio_file'):
            messagebox.showerror("Audio Error", "No audio file to transcribe.")
            return
        
        def process():
            try:
                self.status_var.set("🎯 Transcribing audio...")
                self.transcribe_button.config(state="disabled")
                
                result = self.whisper_model.transcribe(self.temp_audio_file.name)
                transcribed_text = result["text"].strip()
                
                if transcribed_text:
                    self.current_transcription = transcribed_text
                    
                    self.transcription_text.delete(1.0, tk.END)
                    self.transcription_text.insert(1.0, transcribed_text)
                    
                    self.add_transcription_to_context()
                    
                    if self.auto_transcribe_var.get():
                        self.status_var.set("🤖 Requesting initial analysis...")
                        initial_prompt = "Please provide a brief summary of this transcript and identify the main topics or key points discussed."
                        self.add_to_chat(f"🎤 Auto-analysis request: {initial_prompt}", "user")
                        self.get_ai_response(initial_prompt)
                    else:
                        self.status_var.set("✅ Transcription completed - Ready for questions")
                else:
                    self.status_var.set("⚠️ No speech detected in audio")
                
                self.transcribe_button.config(state="normal")
                
            except Exception as e:
                self.status_var.set("❌ Transcription failed")
                self.transcribe_button.config(state="normal")
                messagebox.showerror("Transcription Error", f"Failed to transcribe: {str(e)}")
        
        threading.Thread(target=process, daemon=True).start()
    
    def send_manual_message(self):
        """Send a manually typed message to the AI"""
        message = self.chat_input.get(1.0, tk.END).strip()
        if not message:
            return
        
        self.chat_input.delete(1.0, tk.END)
        self.add_to_chat(f"💬 You: {message}", "user")
        self.get_ai_response(message)
    
    def use_transcription_in_chat(self):
        """Insert current transcription into chat input"""
        if self.current_transcription:
            current_text = self.chat_input.get(1.0, tk.END).strip()
            if current_text:
                self.chat_input.insert(tk.END, f"\n\n{self.current_transcription}")
            else:
                self.chat_input.delete(1.0, tk.END)
                self.chat_input.insert(1.0, self.current_transcription)
        else:
            messagebox.showinfo("No Transcription", "No transcription available. Please record and transcribe audio first.")
    
    def add_transcription_to_context(self):
        """Add the current transcription to the AI context with specialized system prompt"""
        if self.current_transcription:
            self.conversation_history = []
            self.transcription_in_context = True
            self.add_to_chat("📋 Transcript loaded - AI is now ready to discuss this content", "system")
            self.status_var.set("📋 AI ready for transcript discussion")
        elif not self.current_transcription:
            messagebox.showinfo("No Transcript", "Please record and transcribe audio first.")
    
    def handle_enter_key(self, event):
        """Handle Enter key press in chat input"""
        if event.state & 0x1:  # Shift key is pressed
            return "break"
        else:
            self.send_manual_message()
            return "break"
    
    def insert_newline(self):
        """Insert a new line in the chat input"""
        self.chat_input.insert(tk.INSERT, "\n")
    
    def clear_transcription(self):
        """Clear the transcription text"""
        self.transcription_text.delete(1.0, tk.END)
        self.current_transcription = ""
    
    def test_lm_studio_connection(self):
        """Test connection to LM Studio"""
        def test_connection():
            try:
                self.lm_studio_url = self.url_entry.get()
                self.connection_status.config(text="🔄 Testing...", fg=self.colors['warning'])
                
                models_url = self.lm_studio_url.replace("/chat/completions", "/models")
                response = requests.get(models_url, timeout=5)
                
                if response.status_code == 200:
                    self.connection_status.config(text="● Connected", fg=self.colors['success'])
                    self.status_var.set("🟢 LM Studio connected successfully")
                else:
                    self.connection_status.config(text="● Connection failed", fg=self.colors['error'])
                    self.status_var.set(f"❌ Connection failed: {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                self.connection_status.config(text="● Connection failed", fg=self.colors['error'])
                self.status_var.set(f"❌ Connection error: {str(e)}")
        
        threading.Thread(target=test_connection, daemon=True).start()
    
    def get_ai_response(self, message):
        """Get response from LM Studio with transcript always in context"""
        def get_response():
            try:
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                }
                
                messages_to_send = []
                
                if self.current_transcription:
                    system_prompt = f"""You are an AI assistant specialized in analyzing and discussing transcribed content. Your role is to help users understand, analyze, and explore the following transcript.

TRANSCRIPT TO ANALYZE:
\"\"\"{self.current_transcription}\"\"\"

INSTRUCTIONS:
- Focus ALL responses on the content of this transcript
- Answer questions about what was said, implied, or discussed
- Provide analysis, summaries, insights, and clarifications about the transcript content
- Help identify key points, themes, action items, or important details
- If asked about topics not in the transcript, politely redirect to transcript-related discussion
- Be thorough and helpful in exploring the transcript content
- Maintain context of our entire conversation about this transcript

You should now be ready to answer any questions about this transcript content."""
                    
                    messages_to_send.append({
                        "role": "system", 
                        "content": system_prompt
                    })
                
                for msg in self.conversation_history:
                    if msg["role"] != "system":
                        messages_to_send.append(msg)
                
                messages_to_send.append({"role": "user", "content": message})
                
                if len(messages_to_send) > 31:
                    messages_to_send = [messages_to_send[0]] + messages_to_send[-30:]
                
                data = {
                    "model": "local-model",
                    "messages": messages_to_send,
                    "temperature": 0.7,
                    "max_tokens": 1500
                }
                
                response = requests.post(
                    self.lm_studio_url,
                    headers=headers,
                    json=data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    ai_message = result['choices'][0]['message']['content']
                    
                    self.conversation_history.append({"role": "user", "content": message})
                    self.conversation_history.append({"role": "assistant", "content": ai_message})
                    
                    self.add_to_chat(f"🤖 AI: {ai_message}", "assistant")
                    self.status_var.set("✅ Response received")
                else:
                    error_msg = f"API Error {response.status_code}: {response.text}"
                    self.add_to_chat(f"❌ Error: {error_msg}", "error")
                    self.status_var.set("❌ API error")
                    
            except requests.exceptions.RequestException as e:
                error_msg = f"Connection error: {str(e)}"
                self.add_to_chat(f"❌ Error: {error_msg}", "error")
                self.status_var.set("❌ Connection error")
            except Exception as e:
                error_msg = f"Unexpected error: {str(e)}"
                self.add_to_chat(f"❌ Error: {error_msg}", "error")
                self.status_var.set("❌ Unexpected error")
        
        threading.Thread(target=get_response, daemon=True).start()
    
    def add_to_chat(self, message, sender_type):
        """Add message to chat display with styling"""
        def update_chat():
            self.chat_display.config(state=tk.NORMAL)
            
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            self.chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
            self.chat_display.insert(tk.END, f"{message}\n\n", sender_type)
            
            self.chat_display.config(state=tk.DISABLED)
            self.chat_display.see(tk.END)
        
        self.root.after(0, update_chat)
    
    def clear_chat(self):
        """Clear the chat display and conversation history"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.conversation_history = []
        self.transcription_in_context = False
        self.status_var.set("🗑️ Chat cleared")
    
    def __del__(self):
        """Cleanup when the application is closed"""
        if hasattr(self, 'p'):
            self.p.terminate()
        
        if hasattr(self, 'temp_audio_file') and hasattr(self.temp_audio_file, 'name'):
            try:
                if os.path.exists(self.temp_audio_file.name):
                    os.unlink(self.temp_audio_file.name)
            except:
                pass

def main():
    root = tk.Tk()
    
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
    
    app = AIVoiceAssistant(root)
    
    def on_closing():
        """Handle application closing"""
        if app.is_recording:
            app.stop_recording()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
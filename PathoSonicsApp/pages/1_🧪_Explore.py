import streamlit as st
import numpy as np
import time

# Page configuration
st.set_page_config(page_title="Custom Sequencing Exploration", page_icon="🧪", layout="wide")

# 2. Global Theme Styling Injection (Updated Color Hierarchy)
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    @import url('https://googleapis.com');

    /* Background and global body text styling (Slate Silver) */
    .main, p, div, label, span { 
        font-family: 'Inter', sans-serif !important; 
        font-size: 1.05rem;
        color: #94A3B8 !important; /* Premium silver text */
    }
    
    /* Main App Titles (Vibrant Electric Cyan) */
    h1 { 
        font-family: 'Lora', serif !important; 
        color: #00E5FF !important; 
        font-weight: 700;
    }
    
    /* Secondary Section Subheaders */
    h2, h3, h4 {
        font-family: 'Lora', serif !important; 
        color: #CBD5E1 !important; /* Soft white/gray for balance */
        font-weight: 600;
    }
    
    .main { background-color: #0E1117; }
    
    /* Interactive Control Buttons (Cyan to Dark Cyan Hover) */
    div.stButton > button:first-child {
        background-color: #00E5FF !important; 
        color: #0E1117 !important; 
        font-weight: bold;
        border-radius: 8px; 
        border: none; 
        padding: 0.5rem 2rem;
        font-family: 'Inter', sans-serif !important;
    }
    div.stButton > button:first-child:hover {
        background-color: #00B2CC !important; 
        color: #FFFFFF !important;
    }
    </style>
    """, unsafe_allow_html=True)


# Custom Sidebar Branding Logo (Matching Home)
st.sidebar.markdown("""
  st.sidebar.image("logo.png", use_container_width=True)
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
except Exception:
    st.sidebar.warning("⚠️ logo.png asset not detected.")
    <div style='text-align: center; margin-bottom: 20px;'>
        <h1 style='font-size: 2.2rem; color: #00D2C4 !important; margin-bottom: 0px;'>PathoSonics</h1>
        <p style='font-size: 0.85rem; color: #888888; text-transform: uppercase; letter-spacing: 2px;'>Educational Sonification Lab</p>
    </div>
    <hr style='margin-top: 0px; margin-bottom: 20px; border-color: #1F2937;'>
""", unsafe_allow_html=True)

protein_scale = {
    'I': 36, 'V': 38, 'L': 40, 'F': 43, 'C': 45, 'M': 48, 'A': 50, 'G': 52, 'T': 55, 'S': 57,
    'W': 60, 'Y': 62, 'P': 64, 'H': 67, 'E': 69, 'Q': 72, 'D': 74, 'N': 76, 'K': 79, 'R': 81
}

def midi_to_freq(midi_num):
    return 440.0 * (2.0 ** ((midi_num - 69.0) / 12.0))

def generate_audio_signal(sequence):
    sample_rate = 44100
    note_duration = 0.3
    full_audio = np.array([], dtype=np.float32)
    
    for letter in sequence:
        if letter in protein_scale:
            freq = midi_to_freq(protein_scale[letter])
            t = np.linspace(0, note_duration, int(sample_rate * note_duration), False)
            note_wave = np.sin(freq * t * 2 * np.pi)
            envelope = np.sin(np.linspace(0, np.pi, len(note_wave)))
            full_audio = np.concatenate((full_audio, note_wave * envelope))
            
    return full_audio, sample_rate

st.title("➕ Custom Sequencing Sandbox")
st.write("Input raw uppercase FASTA strings below to evaluate custom biometric sonic signals.")
st.markdown("---")

user_input = st.text_area("Paste custom uppercase sequence markers here:", value="MARV")

if st.button("⚙️ Synthesize Custom Matrix", key="btn_sandbox_run"):
    clean_input = "".join(user_input.split()).upper()
    
    if len(clean_input) == 0:
        st.warning("Input canvas cannot be left blank.")
    else:
        status_text = st.empty()
        progress_bar = st.progress(0)
        
        stages = [
            ("🧬 Reading sandbox string data arrays...", 0.25),
            ("📊 Processing structural hydrophobicity levels...", 0.50),
            ("🎹 Assigning variables to Pentatonic musical targets...", 0.75),
            ("🎧 Compiling final wave audio data profiles...", 1.00)
        ]
        for message, pct in stages:
            status_text.text(message)
            progress_bar.progress(pct)
            time.sleep(0.4)
            
        audio_data, sr = generate_audio_signal(clean_input)
        status_text.empty()
        progress_bar.empty()
        
        st.success(f"✅ Success! Compiled {len(clean_input)} sequence elements.")
        st.audio(audio_data, sample_rate=sr)

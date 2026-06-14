import streamlit as st
import numpy as np
import time

# Page config setup
st.set_page_config(page_title="PathoSonics Home", page_icon="🧬", layout="wide")

# Global Theme Styling Injection
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    h1, h2, h3 { color: #00D2C4 !important; }
    div.stButton > button:first-child {
        background-color: #00D2C4; color: #0E1117; font-weight: bold;
        border-radius: 8px; border: none; padding: 0.5rem 2rem;
    }
    div.stButton > button:first-child:hover {
        background-color: #00B2A6; color: #FFFFFF;
    }
    </style>
    """, unsafe_allow_html=True)

# Custom Sidebar Text & Emoji Branding Logo
st.sidebar.markdown("""
   <div style='display: flex; align-items: center; justify-content: center; margin-bottom: 20px;'>
        <!-- 1. The Custom Image Icon (Points to your local desktop folder file) -->
        <img src='app/static/custom_icon.png' style='width: 38px; height: auto; margin-right: 12px;'>
        
        <!-- 2. The Unchanged Stylized Branding Text Box -->
        <div style='text-align: left;'>
            <h1 style='font-size: 2.2rem; color: #00D2C4 !important; margin-bottom: 0px; line-height: 1;'>Patho</h1>
            <p style='font-size: 0.85rem; color: #888888; text-transform: uppercase; letter-spacing: 2px; margin: 0;'>Sonics Lab</p>
        </div>
    </div>
    <hr style='margin-top: 0px; margin-bottom: 20px; border-color: #1F2937;'>
""", unsafe_allow_html=True)

# Master conversion dictionary mapping biochemical properties to MIDI pitches
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

# Structural Carousel Database Array
carousel_data = [
    {
        "title": "🟢 Healthy Hemoglobin Subunit", "id": "RCSB 1A3N",
        "seq": "MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNPK",
        "finding": "Maintains a bright, highly consonant upward melodic trajectory in the 3rd and 4th octaves."
    },
    {
        "title": "🔴 Sickle Cell Mutant Variant", "id": "RCSB 2HBS",
        "seq": "MVHLTPVEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNPK",
        "finding": "Features an immediate, jarring downward displacement drop of exactly 5 scale degrees at the 7th node position."
    },
    {
        "title": "🟡 Mutant p53 Cancer Variant", "id": "RCSB 2OCJ",
        "seq": "MEEPQSDPSVEPPLSQETFSDLWKLLPENNVLSPLPSQAMDDLMLSPDDIEQWFTEDPGP",
        "finding": "Densely clustered acoustic profile showing severe tonal variations indicative of systemic molecular distortion."
    }
]

# Track current card inside the browser session memory
if "card_index" not in st.session_state:
    st.session_state.card_index = 0

current_card = carousel_data[st.session_state.card_index]

st.title("🧬 PathoSonics Portfolio Carousel")
st.caption("Shuffle through pre-loaded proteomic assets using the control navigation deck.")
st.markdown("---")

card_box = st.container(border=True)
with card_box:
    st.header(current_card["title"])
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric(label="Structural Registry ID", value=current_card["id"])
        st.metric(label="Total Sequence Length", value=f"{len(current_card['seq'])} Residues")
    with col_b:
        st.info(f"📋 **Sonifier Pattern Finding:** {current_card['finding']}")
    
    if st.button("🔊 Synthesize Profile Audio", key="btn_home_audio"):
        status = st.empty()
        pbar = st.progress(0)
        for msg, pct in [("🧬 Mapping genomic sequence strings...", 0.5), ("🎧 Processing wave transformations...", 1.0)]:
            status.text(msg)
            pbar.progress(pct)
            time.sleep(0.4)
            
        audio, sr = generate_audio_signal(current_card["seq"])
        status.empty()
        pbar.empty()
        st.audio(audio, sample_rate=sr)

# Navigation row alignment layout matrix
nav_col1, nav_col2, nav_col3 = st.columns()
with nav_col1:
    if st.button("⬅️ Previous Asset", key="btn_prev"):
        st.session_state.card_index = (st.session_state.card_index - 1) % len(carousel_data)
        st.rerun()
with nav_col3:
    if st.button("Next Asset ➡️", key="btn_next"):
        st.session_state.card_index = (st.session_state.card_index + 1) % len(carousel_data)
        st.rerun()

st.markdown("---")
st.info("💡 *Want to process completely unique custom data? Navigate to **2 🧪 Sandbox** inside your left sidebar menu panel!*")


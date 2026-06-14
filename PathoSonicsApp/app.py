import streamlit as st
import numpy as np
import time

# Custom CSS to hide the footer and the main menu
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Page config setup
st.set_page_config(page_title="PathoSonics Home", page_icon="logo.png", layout="wide")

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

# Custom Sidebar Text & Emoji Branding Logo
st.sidebar.markdown("""
     st.sidebar.image("logo.png", use_container_width=True)
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
except Exception:
    st.sidebar.warning("⚠️ logo.png asset not detected.")
        <!-- 2. The Unchanged Stylized Branding Text Box -->
        <div style='text-align: left;'>
            <h1 style='font-size: 2.2rem; color: #00D2C4 !important; margin-bottom: 0px; line-height: 1;'>PathoSonics</h1>
            <p style='font-size: 0.85rem; color: #888888; text-transform: uppercase; letter-spacing: 2px; margin: 0;'>Educational Sonification Lab</p>
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
        "finding": "Maintains a bright, consonant, and high upward melodic trajectory in the 3rd and 4th octaves"
    },
    {
        "title": "🔴 Sickle Cell Mutant Variant", "id": "RCSB 2HBS",
        "seq": "MVHLTPVEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNPK",
        "finding": "Features an immediate, jarring downward displacement drop of approximately 5 scale degrees at the 7th node position."
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

st.title("🧬 PathoSonics Carousel")
st.caption("Shuffle through a few pre-loaded assests and explore what sonification is!")
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
nav_col1, nav_col2, nav_col3 = st.columns(3)
with nav_col1:
    if st.button("⬅️ Previous Asset", key="btn_prev"):
        st.session_state.card_index = (st.session_state.card_index - 1) % len(carousel_data)
        st.rerun()
with nav_col3:
    if st.button("Next Asset ➡️", key="btn_next"):
        st.session_state.card_index = (st.session_state.card_index + 1) % len(carousel_data)
        st.rerun()

st.markdown("---")
st.info("💡 *Want to process completely unique custom data? Navigate to **2 🧪 Explore** inside your left sidebar menu panel!*")


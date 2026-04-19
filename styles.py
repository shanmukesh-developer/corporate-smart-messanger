SHARED_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Montserrat:wght@400;500;600;700&display=swap');

    :root {
        --lux-gold: #D4AF37;
        --lux-gold-light: #F1D279;
        --obsidian: #0A0C10;
        --panel-bg: rgba(255, 255, 255, 0.04);
        --white: #FFFFFF;
        --platinum: #E2E8F0;
    }

    /* GLOBAL RESET */
    .stApp {
        background-color: var(--obsidian) !important;
        font-family: 'Montserrat', sans-serif !important;
        color: var(--platinum);
    }

    [data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
    #MainMenu, footer { visibility: hidden; }

    /* TYPOGRAPHY OVERHAUL */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: var(--lux-gold) !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
        margin-bottom: 0.8rem !important;
    }
    
    label, p, span, .stMarkdown {
        color: var(--platinum) !important;
        font-weight: 500 !important;
    }

    /* HARD CONTRAST INPUTS */
    .stTextInput label, .stSelectbox label {
        color: var(--lux-gold) !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 5px !important;
    }
    .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.07) !important;
        border: 2px solid rgba(212, 175, 55, 0.4) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 14px !important;
        font-weight: 500 !important;
    }
    .stTextInput input:focus {
        border-color: var(--lux-gold) !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
    }

    /* HARD CONTRAST BUTTONS - ZERO MERGE POLICY */
    .stButton > button {
        background: linear-gradient(135deg, var(--lux-gold) 0%, #B8860B 100%) !important;
        color: #000000 !important; /* ABSOLUTE BLACK TEXT FOR LEGIBILITY */
        font-weight: 800 !important;
        text-transform: uppercase;
        letter-spacing: 3px !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 1rem 3rem !important;
        width: 100%;
        box-shadow: 0 10px 40px rgba(0,0,0,0.6) !important;
        transition: 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        margin-top: 15px;
    }
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 50px rgba(212, 175, 55, 0.4) !important;
        filter: brightness(1.1);
    }

    /* CONTAINER SYSTEM */
    .stForm, [data-testid="stVerticalBlock"] > div > div > [data-testid="stVerticalBlock"] {
        background: var(--panel-bg) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 24px !important;
        padding: 3rem !important;
        box-shadow: 0 30px 100px rgba(0,0,0,0.7) !important;
        backdrop-filter: blur(30px) !important;
    }

    /* LOGO CIRCULAR REFINEMENT */
    .logo-container {
        text-align: center;
        margin-bottom: 2rem;
    }
    .logo-container img {
        border-radius: 50%;
        border: 2px solid var(--lux-gold);
        box-shadow: 0 0 40px rgba(212, 175, 55, 0.4);
        background: var(--obsidian);
        padding: 4px;
    }

    /* TABLES & METRICS */
    [data-testid="stMetricValue"] { color: var(--lux-gold) !important; font-weight: 700 !important; }
    .stTable { background: transparent !important; }

    /* FADE IN VFX */
    .vfx-entry {
        animation: luxFadeIn 1.2s ease-out forwards;
    }
    @keyframes luxFadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
"""

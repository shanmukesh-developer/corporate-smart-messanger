SHARED_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

    :root {
        --primary-gold: #D4AF37;
        --dark-gold: #996515;
        --midnight-navy: #0A0E1A;
        --glass-bg: rgba(255, 255, 255, 0.05);
        --glass-border: rgba(255, 255, 255, 0.1);
        --text-main: #FFFFFF;
        --text-dim: #A0AEC0;
    }

    /* GLOBAL RESET */
    .stApp {
        background-color: var(--midnight-navy);
        font-family: 'Outfit', sans-serif !important;
    }

    [data-testid="collapsedControl"] { display: none; }
    [data-testid="stSidebar"] { display: none; }

    /* SCROLLBAR */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: var(--midnight-navy); }
    ::-webkit-scrollbar-thumb { background: var(--dark-gold); border-radius: 10px; }

    /* SHIMMER GLASS CARD */
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
        position: relative;
        overflow: hidden;
        transition: all 0.5s cubic-bezier(0.19, 1, 0.22, 1);
    }
    .glass-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: -150%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            to right,
            transparent,
            rgba(212, 175, 55, 0.1),
            transparent
        );
        transform: skewX(-25deg);
        transition: 0.75s;
    }
    .glass-card:hover::before {
        left: 150%;
    }
    .glass-card:hover {
        border-color: var(--primary-gold);
        transform: scale(1.02);
        box-shadow: 0 15px 50px rgba(212, 175, 55, 0.1);
    }

    /* PREMIUM BUTTONS */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-gold) 0%, var(--dark-gold) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3) !important;
    }
    .stButton > button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 8px 25px rgba(212, 175, 55, 0.5) !important;
        filter: brightness(1.1);
    }

    /* TYPOGRAPHY */
    h1, h2, h3 {
        color: var(--primary-gold) !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }
    p, span, label {
        color: var(--text-dim) !important;
    }
    strong { color: var(--text-main) !important; }

    /* INPUTS */
    .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] {
        background-color: rgba(255,255,255,0.03) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 12px !important;
    }
    .stTextInput input:focus {
        border-color: var(--primary-gold) !important;
        box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.2) !important;
    }

    /* VFX ANIMATIONS */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .vfx-fade-in {
        animation: fadeInUp 0.8s ease-out forwards;
    }

    @keyframes glow {
        0% { box-shadow: 0 0 5px rgba(212, 175, 55, 0.2); }
        50% { box-shadow: 0 0 20px rgba(212, 175, 55, 0.4); }
        100% { box-shadow: 0 0 5px rgba(212, 175, 55, 0.2); }
    }
    .vfx-glow {
        animation: glow 3s infinite ease-in-out;
    }

    /* CHAT BUBBLES */
    [data-testid="stChatMessage"] {
        background: rgba(255,255,255,0.05) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
    }

    /* HIDE STREAMLIT BRANDING */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
"""

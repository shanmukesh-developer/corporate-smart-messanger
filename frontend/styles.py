SHARED_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

    :root {
        --primary-gold: #D4AF37;
        --dark-gold: #B8860B;
        --midnight-navy: #0A0E1A;
        --glass-bg: rgba(255, 255, 255, 0.02);
        --glass-border: rgba(212, 175, 55, 0.25);
        --text-main: #FFFFFF;
        --text-dim: #A0AEC0;
        --glow-gold: rgba(212, 175, 55, 0.4);
    }

    /* GLOBAL RESET & MASTERPIECE SCROLLBAR */
    .stApp {
        background-color: var(--midnight-navy);
        font-family: 'Outfit', sans-serif !important;
        color: var(--text-main);
    }

    ::-webkit-scrollbar { width: 10px; }
    ::-webkit-scrollbar-track { background: var(--midnight-navy); }
    ::-webkit-scrollbar-thumb { 
        background: linear-gradient(var(--dark-gold), var(--primary-gold)); 
        border-radius: 10px;
        border: 2px solid var(--midnight-navy);
    }

    [data-testid="collapsedControl"] { display: none; }
    [data-testid="stSidebar"] { display: none; }

    /* MASTERPIECE ANIMATIONS */
    @keyframes floating {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }

    @keyframes shine {
        0% { background-position: -200% center; }
        100% { background-position: 200% center; }
    }

    @keyframes border-glow {
        0% { border-color: rgba(212, 175, 55, 0.2); box-shadow: 0 0 5px rgba(212, 175, 55, 0.1); }
        50% { border-color: rgba(212, 175, 55, 0.8); box-shadow: 0 0 25px rgba(212, 175, 55, 0.3); }
        100% { border-color: rgba(212, 175, 55, 0.2); box-shadow: 0 0 5px rgba(212, 175, 55, 0.1); }
    }

    /* GLASS CARD EVOLUTION */
    .glass-card {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(35px) saturate(200%) !important;
        -webkit-backdrop-filter: blur(35px) saturate(200%) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 30px !important;
        padding: 2.5rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.9), inset 0 0 15px rgba(255,255,255,0.02) !important;
        transition: all 0.7s cubic-bezier(0.19, 1, 0.22, 1) !important;
        position: relative;
        overflow: hidden;
    }
    
    .glass-card:hover {
        transform: translateY(-15px) scale(1.03);
        border: 1px solid var(--primary-gold) !important;
        box-shadow: 0 40px 100px rgba(212, 175, 55, 0.15), 0 0 20px rgba(212, 175, 55, 0.1) !important;
    }

    /* PREMIUM TILE GRID ICON */
    .tile-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
        filter: drop-shadow(0 0 10px var(--glow-gold));
        transition: all 0.5s;
    }
    .glass-card:hover .tile-icon {
        transform: scale(1.2) rotate(5deg);
        filter: drop-shadow(0 0 25px var(--primary-gold));
    }

    /* ELITE BUTTONS */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-gold) 0%, var(--dark-gold) 100%) !important;
        background-size: 200% auto !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 18px !important;
        padding: 1rem 2.8rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 2.5px;
        transition: 0.5s !important;
        box-shadow: 0 10px 30px rgba(184, 134, 11, 0.3) !important;
        animation: shine 4s infinite linear;
    }
    .stButton > button:hover {
        background-position: right center !important;
        transform: translateY(-5px) scale(1.05) !important;
        box-shadow: 0 15px 45px rgba(212, 175, 55, 0.6) !important;
        filter: brightness(1.25);
    }

    /* TYPOGRAPHY */
    h1, h2, h3 {
        background: linear-gradient(to right, #FFFFFF 20%, var(--primary-gold) 40%, var(--dark-gold) 60%, #FFFFFF 80%);
        background-size: 200% auto;
        color: #000;
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 10s linear infinite;
        font-weight: 800 !important;
        letter-spacing: -1.5px;
    }
    
    .vfx-glow-text {
        text-shadow: 0 0 20px var(--glow-gold);
    }

    /* DASHBOARD WIDGETS */
    .stat-widget {
        background: rgba(212, 175, 55, 0.05);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.4s;
    }
    .stat-widget:hover {
        background: rgba(212, 175, 55, 0.1);
        transform: scale(1.05);
        border-color: var(--primary-gold);
    }

    /* CHAT BUBBLES MASTERPIECE */
    .stChatMessage {
        border-radius: 20px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        margin-bottom: 20px !important;
        background: rgba(255,255,255,0.02) !important;
    }

    /* VFX UTILITIES */
    .vfx-fade-in { animation: fadeInUp 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
    .vfx-floating { animation: floating 4s infinite ease-in-out; }
    .vfx-border-glow { animation: border-glow 5s infinite; }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(40px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* HIDE STREAMLIT BRANDING */
    #MainMenu, footer, header {visibility: hidden;}
</style>
"""

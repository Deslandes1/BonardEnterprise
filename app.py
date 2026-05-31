import streamlit as st
import pandas as pd
from datetime import datetime
import re
import json
import requests
from supabase import create_client, Client
from typing import Any, Dict, Optional, Tuple

# ============================================================
# GLOBAL SECURITY SHIELD (EMBEDDED) – same as GlobalInternet.py
# ============================================================
DEFAULT_PATTERNS = {
    "sql_injection": [
        r"(\%27)|(\')|(\-\-)|(\%23)|(#)",
        r"(union.*select)",
        r"(insert.*into)",
        r"(delete.*from)",
        r"(drop.*table)",
        r"(select.*from.*where)",
        r"(or\s+1\s*=\s*1)"
    ],
    "xss": [
        r"<script",
        r"javascript:",
        r"onload=",
        r"onerror=",
        r"onclick=",
        r"alert\(",
        r"prompt\("
    ],
    "path_traversal": [
        r"\.\./",
        r"\.\.\\",
        r"\.\.%2f"
    ],
    "command_injection": [
        r"(\|)|(\&)|(;)",
        r"(ping)|(nslookup)|(wget)"
    ],
    "malicious_user_agents": [
        r"sqlmap",
        r"nikto",
        r"nmap"
    ]
}

class SecurityException(Exception):
    pass

class WebAppShield:
    def __init__(self, app_name: str, api_key: str, dashboard_url: Optional[str] = None):
        self.app_name = app_name
        self.api_key = api_key
        self.dashboard_url = dashboard_url or "https://global-security-shield-built-by-gesner-deslandes-tul974fmulf5q.streamlit.app/?log="
        self.patterns = DEFAULT_PATTERNS.copy()
        self.custom_patterns = {}

    def add_custom_pattern(self, attack_type: str, pattern: str):
        if attack_type not in self.custom_patterns:
            self.custom_patterns[attack_type] = []
        self.custom_patterns[attack_type].append(pattern)

    def is_malicious(self, text: str) -> Tuple[bool, Optional[str]]:
        if not isinstance(text, str):
            return False, None
        for attack_type, patterns in self.patterns.items():
            for pat in patterns:
                if re.search(pat, text, re.IGNORECASE):
                    return True, attack_type
        for attack_type, patterns in self.custom_patterns.items():
            for pat in patterns:
                if re.search(pat, text, re.IGNORECASE):
                    return True, attack_type
        return False, None

    def sanitize_input(self, value: Any) -> Any:
        if isinstance(value, str):
            malicious, attack_type = self.is_malicious(value)
            if malicious:
                raise SecurityException(f"Blocked: potential {attack_type} attack")
            return value
        elif isinstance(value, dict):
            return {k: self.sanitize_input(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [self.sanitize_input(i) for i in value]
        else:
            return value

    def log_threat(self, request_data: Dict):
        try:
            payload = {
                "app_name": self.app_name,
                "api_key": self.api_key,
                "timestamp": datetime.utcnow().isoformat(),
                "data": request_data
            }
            log_url = f"{self.dashboard_url}{json.dumps(payload)}"
            requests.get(log_url, timeout=2)
        except Exception:
            pass

    def protect_streamlit(self):
        if hasattr(st, 'query_params') and st.query_params:
            for key, value in st.query_params.items():
                try:
                    self.sanitize_input(value)
                except SecurityException as e:
                    st.error("🚨 Security alert: Malicious input detected and blocked.")
                    self.log_threat({
                        "type": "query_param",
                        "key": key,
                        "value": value,
                        "error": str(e)
                    })
                    st.stop()
        st.sidebar.markdown("🛡️ **Global Security Shield active**")

# Initialise the shield (use your existing API key – it's just for logging)
shield = WebAppShield(
    app_name="BonardEnterprise",
    api_key="gl-MssTDLE9cATE4Iu7_tQkcxaFWcwwMr3e7S_Mdwgg",  # same key as your main site
    dashboard_url="https://global-security-shield-built-by-gesner-deslandes-tul974fmulf5q.streamlit.app/?log="
)

# ============================================================
# Supabase setup for comments
# ============================================================
SUPABASE_URL = st.secrets["supabase"]["url"]
SUPABASE_KEY = st.secrets["supabase"]["key"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ================== Page Config ==================
st.set_page_config(
    page_title="BONARDENTERPRISE Website",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================== Security Configuration ==================
ADMIN_PASSWORD = "BonardAdmin2026"

# ================== Apply Shield Protection ==================
shield.protect_streamlit()

# ================== Colorful, Modern Uniform Styling ==================
st.markdown(
    """
    <style>
    /* Force identical vibrant background on both the main page and sidebar wrappers */
    .stApp, [data-testid="stSidebar"], [data-testid="stSidebarUserContent"], section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%) !important;
        background-attachment: fixed !important;
        background-color: #0f172a !important;
    }
    
    /* Clean up default sidebar borders */
    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    /* Text styling */
    h1, h2, h3, h4, p, label, .stMarkdown, .stSelectbox label {
        color: #ffffff !important;
    }
    
    /* Top Contact Bar Header */
    .client-header-bar {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 12px 25px;
        border-radius: 12px;
        margin-bottom: 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
    }
    
    /* Product Cards */
    .product-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease;
    }
    .product-card:hover {
        transform: translateY(-5px);
        border-color: #00ebc7;
    }
    
    /* Category Badges */
    .category-badge {
        background: linear-gradient(90deg, #ff007f, #7928ca);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
    }
    
    /* Neon accents */
    .neon-text {
        color: #00ebc7 !important;
        text-shadow: 0 0 10px rgba(0, 235, 199, 0.5);
    }
    
    /* Footer */
    .footer-container {
        text-align: center;
        margin-top: 70px;
        padding: 30px;
        background: rgba(15, 23, 42, 0.6);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px 20px 0 0;
    }
    
    /* Input fields */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: rgba(255, 255, 255, 0.07) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Comment box */
    .comment-box {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 10px;
        margin: 5px 0;
        border-left: 3px solid #00ebc7;
    }
    .comment-meta {
        font-size: 0.7rem;
        color: #aaa;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ================== Localization Dictionary Matrix ==================
translations = {
    "English": {
        "subtitle": "Advanced Chemical Product Management & Storefront Inventory Layer",
        "top_contact": "🏢 WhatsApp Business Line:",
        "admin_title": "## 📥 Admin Upload Panel",
        "admin_desc": "Enter security password to access product upload fields.",
        "pass_label": "Enter Security Password:",
        "pass_success": "Access granted. Upload layers unlocked.",
        "pass_error": "Invalid administrative password.",
        "p_name": "Chemical Product Name:",
        "p_cat": "Chemical Category:",
        "p_price": "Price (e.g., USD or HTG):",
        "p_desc": "Product Specifications & Description:",
        "p_img": "Capture Photo or Choose from Gallery",
        "btn_publish": "Publish Product to Storefront",
        "msg_success": "has been published successfully!",
        "msg_error": "Product Name and Price fields are strictly required.",
        "catalog_title": "## 🛍️ Active Chemical Catalog",
        "catalog_empty": "The catalog is currently empty. Use the admin panel to upload inventory items.",
        "no_img": "ℹ️ No visual asset uploaded for this product layer.",
        "comments": "💬 Comments",
        "post_comment": "Post Comment",
        "your_name": "Your name (optional)",
        "your_comment": "Your comment",
        "reply": "Reply",
        "like": "👍 Like"
    },
    "French": {
        "subtitle": "Gestion Avancée des Produits Chimiques & Inventaire de la Vitrine",
        "top_contact": "🏢 Ligne WhatsApp Commerciale :",
        "admin_title": "## 📥 Panneau de Gestion Admin",
        "admin_desc": "Entrez le mot de passe de sécurité pour accéder aux champs d'ajout.",
        "pass_label": "Entrez le mot de passe :",
        "pass_success": "Accès autorisé. Formulaire déverrouillé.",
        "pass_error": "Mot de passe administratif incorrect.",
        "p_name": "Nom du Produit Chimique :",
        "p_cat": "Catégorie Chimique :",
        "p_price": "Prix (ex: USD ou HTG) :",
        "p_desc": "Spécifications du Produit & Description :",
        "p_img": "Prendre une Photo ou Choisir depuis la Galerie",
        "btn_publish": "Publier le Produit sur la Vitrine",
        "msg_success": "a été publié avec succès !",
        "msg_error": "Le nom du produit et le prix sont strictement requis.",
        "catalog_title": "## 🛍️ Catalogue des Produits Chimiques Actifs",
        "catalog_empty": "Le catalogue est actuellement vide. Utilisez le panneau d'administration pour ajouter des articles.",
        "no_img": "ℹ️ Aucun visuel importé pour ce produit.",
        "comments": "💬 Commentaires",
        "post_comment": "Publier le commentaire",
        "your_name": "Votre nom (optionnel)",
        "your_comment": "Votre commentaire",
        "reply": "Répondre",
        "like": "👍 J'aime"
    },
    "Haitian Creole": {
        "subtitle": "Sistèm Avanse pou Jere Pwodwi Chimik ak Envantè Boutik la",
        "top_contact": "🏢 Liy WhatsApp Biznis la:",
        "admin_title": "## 📥 Panèl Administratè pou Chaje Pwodwi",
        "admin_desc": "Mete kòd sekirite a pou ou ka jwenn aksè nan fòm lan.",
        "pass_label": "Mete Kòd Sekirite a:",
        "pass_success": "Aksè otorize. Panèl la louvri.",
        "pass_error": "Kòd sekirite administratif la pa kòrèk.",
        "p_name": "Non Pwodwi Chimik la:",
        "p_cat": "Kategori Pwodwi a:",
        "p_price": "Pri (pa egzanp: USD oswa HTG):",
        "p_desc": "Espesifikasyon ak Deskripsyon Pwodwi a:",
        "p_img": "Pran yon Foto oswa Chwazi nan Galri a",
        "btn_publish": "Pibliye Pwodwi a nan Boutik la",
        "msg_success": "pibliye avèk siksè!",
        "msg_error": "Non Pwodwi a ak Pri a obligatwa nèt.",
        "catalog_title": "## 🛍️ Katalòg Pwodwi Chimik ki Disponib",
        "catalog_empty": "Katalòg la vid pou kounye a. Sèvi ak panèl administratè a pou chaje pwodwi.",
        "no_img": "ℹ️ Pa gen okenn foto ki chaje pou pwodwi sa a.",
        "comments": "💬 Kòmantè",
        "post_comment": "Pibliye Kòmantè",
        "your_name": "Non ou (si ou vle)",
        "your_comment": "Kòmantè ou",
        "reply": "Reponn",
        "like": "👍 Renmen"
    }
}

# ================== Supabase Comment Functions ==================
def get_comments(product_key):
    """Retrieve all comments for a given product (top-level and replies)."""
    try:
        response = supabase.table("comments").select("*").eq("project_key", product_key).order("timestamp", desc=False).execute()
        return response.data
    except Exception as e:
        st.error(f"Error loading comments: {e}")
        return []

def add_comment(product_key, username, comment, parent_id=0, reply_to_username=""):
    """Insert a new comment (public – no login required)."""
    safe_comment = comment.strip()
    safe_username = username.strip() if username else "Anonymous"
    if not safe_comment:
        return False
    try:
        supabase.table("comments").insert({
            "project_key": product_key,
            "username": safe_username,
            "comment": safe_comment,
            "timestamp": datetime.now().isoformat(),
            "likes": 0,
            "parent_id": parent_id,
            "reply_to_username": reply_to_username
        }).execute()
        return True
    except Exception as e:
        st.error(f"Error adding comment: {e}")
        return False

def add_like(comment_id):
    """Increment the like count for a comment."""
    try:
        current = supabase.table("comments").select("likes").eq("id", comment_id).execute()
        if current.data:
            new_likes = current.data[0]["likes"] + 1
            supabase.table("comments").update({"likes": new_likes}).eq("id", comment_id).execute()
    except Exception as e:
        st.warning(f"Could not update like: {e}")

# ================== Sidebar Language Engine ==================
st.sidebar.markdown("## 🌐 Language Localization Layer")
selected_lang = st.sidebar.selectbox("", ["English", "French", "Haitian Creole"], index=0)
txt = translations[selected_lang]

st.sidebar.markdown("---")

# ================== Session State Mock Database ==================
if "products" not in st.session_state:
    st.session_state.products = [
        {
            "name": "Industrial Grade Ethanol 95%",
            "category": "Solvents",
            "price": "15,500 HTG",
            "desc": "High purity raw chemical solvent optimized for industrial processing, sanitization, and compounding.",
            "image": None,
            "product_key": "product_0"
        },
        {
            "name": "Concentrated Caustic Soda Pearls",
            "category": "Raw Materials",
            "price": "8,200 HTG",
            "desc": "Sodium Hydroxide (NaOH) crystals. Widely utilized for commercial soap manufacturing and heavy-duty industrial drainage cleaning.",
            "image": None,
            "product_key": "product_1"
        }
    ]

# ================== Top Contact Header (WhatsApp) ==================
whatsapp_number = "50944108261"
whatsapp_url = f"https://wa.me/{whatsapp_number}"

st.markdown(
    f"""
    <div class="client-header-bar">
        <div style="font-weight: 700; font-size: 1.05rem; color: #00ebc7 !important;">
            📩 Business Support: <a href="mailto:Jamesonbonard97@gmail.com" style="color: #00ebc7; text-decoration: none;">Jamesonbonard97@gmail.com</a>
        </div>
        <div style="font-weight: 700; font-size: 1.05rem; color: #ffffff !important;">
            {txt['top_contact']} 
            <a href="{whatsapp_url}" target="_blank" style="color: #25D366; text-decoration: none; font-weight: bold;">
                📱 +509 44 10 8261 (Click to WhatsApp)
            </a>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ================== Application Header ==================
st.title("BONARDENTERPRISE Website")
st.markdown(f"### <span class='neon-text'>{txt['subtitle']}</span>", unsafe_allow_html=True)
st.markdown("---")

# ================== Admin Sidebar Panel ==================
st.sidebar.markdown(txt['admin_title'])
st.sidebar.markdown(txt['admin_desc'])

entered_password = st.sidebar.text_input(txt['pass_label'], type="password")

if entered_password == ADMIN_PASSWORD:
    st.sidebar.success(f"🔓 {txt['pass_success']}")
    
    with st.sidebar.form(key="upload_form", clear_on_submit=True):
        new_name = st.text_input(txt['p_name'])
        new_cat = st.selectbox(txt['p_cat'], ["Solvents", "Raw Materials", "Acids & Bases", "Agricultural Chemicals", "Detergents / Surfactants", "Other"])
        new_price = st.text_input(txt['p_price'])
        new_desc = st.text_area(txt['p_desc'])
        new_img = st.file_uploader(txt['p_img'], type=["jpg", "jpeg", "png", "webp"])
        submit_product = st.form_submit_button(txt['btn_publish'])
    
    if submit_product:
        if new_name and new_price:
            img_bytes = new_img.read() if new_img is not None else None
            new_product_key = f"product_{len(st.session_state.products)}"
            st.session_state.products.insert(0, {
                "name": new_name,
                "category": new_cat,
                "price": new_price,
                "desc": new_desc,
                "image": img_bytes,
                "product_key": new_product_key
            })
            st.sidebar.success(f"⚡ {new_name} {txt['msg_success']}")
        else:
            st.sidebar.error(txt['msg_error'])
elif entered_password:
    st.sidebar.error(f"❌ {txt['pass_error']}")

# ================== Product Catalog + Comment Section ==================
st.markdown(txt['catalog_title'])

if not st.session_state.products:
    st.info(txt['catalog_empty'])
else:
    # Display products in a 3‑column grid
    cols = st.columns(3)
    for idx, prod in enumerate(st.session_state.products):
        col = cols[idx % 3]
        with col:
            st.markdown(f"""
            <div class='product-card'>
                <span class='category-badge'>{prod['category']}</span>
                <h4 style='margin-top:0; color:#00ebc7 !important;'>{prod['name']}</h4>
                <p style='font-size:1.1rem; font-weight:700; color:#ff007f !important;'>{prod['price']}</p>
                <p style='font-size:0.9rem; opacity:0.8; min-height:60px;'>{prod['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if prod['image'] is not None:
                st.image(prod['image'], use_container_width=True)
            else:
                st.caption(txt['no_img'])
            
            # ----- Comment Section for this product -----
            product_key = prod['product_key']
            comments = get_comments(product_key)
            
            with st.expander(f"{txt['comments']} ({len([c for c in comments if c.get('parent_id') == 0])})"):
                # Display existing comments (top-level only, then replies recursively)
                def display_comment(comment, level=0):
                    st.markdown(f"""
                    <div class="comment-box" style="margin-left: {level*20}px;">
                        <div class="comment-meta">
                            <strong>{comment['username']}</strong> · {comment['timestamp'][:16]} · 👍 {comment['likes']}
                        </div>
                        <p style="margin: 0 0 0.2rem 0;">{comment['comment']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        if st.button(f"❤️ {comment['likes']}", key=f"like_{comment['id']}"):
                            add_like(comment['id'])
                            st.rerun()
                    with col2:
                        with st.popover("💬 Reply", use_container_width=False):
                            reply_name = st.text_input(txt['your_name'], key=f"reply_name_{comment['id']}", placeholder="Anonymous")
                            reply_text = st.text_area(txt['your_comment'], key=f"reply_text_{comment['id']}", height=68)
                            if st.button(txt['post_comment'], key=f"reply_btn_{comment['id']}"):
                                if reply_text.strip():
                                    add_comment(product_key, reply_name, reply_text, parent_id=comment['id'], reply_to_username=comment['username'])
                                    st.rerun()
                                else:
                                    st.warning("Please enter a reply.")
                    # Show replies
                    replies = [c for c in comments if c.get("parent_id") == comment['id']]
                    for reply in replies:
                        display_comment(reply, level + 1)
                
                # Show all top-level comments
                top_comments = [c for c in comments if c.get("parent_id") == 0]
                for comment in top_comments:
                    display_comment(comment)
                
                # Form to add a new top‑level comment
                st.markdown("---")
                with st.form(key=f"new_comment_{product_key}"):
                    name = st.text_input(txt['your_name'], key=f"name_{product_key}", placeholder="Anonymous")
                    comment_text = st.text_area(txt['your_comment'], key=f"text_{product_key}", height=100)
                    if st.form_submit_button(txt['post_comment']):
                        if comment_text.strip():
                            add_comment(product_key, name, comment_text)
                            st.rerun()
                        else:
                            st.warning("Please write a comment.")

# ================== Footer ==================
st.markdown(
    f"""
    <div class="footer-container">
        <h4 style="margin-bottom: 5px;">BONARDENTERPRISE Website</h4>
        <p style="font-size: 0.95rem; opacity: 0.8; margin-bottom: 15px;">
            Engineered, programmed, and optimized by <strong>GlobalInternet.py</strong>
        </p>
        <p style="font-size: 0.9rem; color: #00ebc7 !important; font-weight: 600;">
            📧 Contact Engineering: <a href="mailto:deslandes78@gmail.com" style="color: #00ebc7; text-decoration: none;">deslandes78@gmail.com</a>
            &nbsp;&nbsp;|&nbsp;&nbsp; 
            📞 Client WhatsApp: <a href="{whatsapp_url}" target="_blank" style="color: #25D366; text-decoration: none;">+509 44 10 8261 (Click to chat)</a>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

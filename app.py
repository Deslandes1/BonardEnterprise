import streamlit as st
import pandas as pd
from datetime import datetime

# ================== Page Config ==================
st.set_page_config(
    page_title="BONARDENTERPRISE SOFTWARE",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================== Security Configuration ==================
# Change this variable to update your client's administrative password
ADMIN_PASSWORD = "BonardAdmin2026"

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
    
    /* Clean up default sidebar borders for a fully seamless appearance */
    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    /* Text styling overrides */
    h1, h2, h3, h4, p, label, .stMarkdown, .stSelectbox label {
        color: #ffffff !important;
    }
    
    /* Top Contact Bar Header styling */
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
    
    /* Custom Badges */
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
    
    /* Footer Styling */
    .footer-container {
        text-align: center;
        margin-top: 70px;
        padding: 30px;
        background: rgba(15, 23, 42, 0.6);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px 20px 0 0;
    }
    
    /* Fix form inputs text and background contrast elements */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: rgba(255, 255, 255, 0.07) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ================== Localization Dictionary Matrix ==================
translations = {
    "English": {
        "subtitle": "Advanced Chemical Product Management & Storefront Inventory Layer",
        "top_contact": "🏢 Business Operations Line:",
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
        "no_img": "ℹ️ No visual asset uploaded for this product layer."
    },
    "French": {
        "subtitle": "Gestion Avancée des Produits Chimiques & Inventaire de la Vitrine",
        "top_contact": "🏢 Ligne des Opérations Commerciales :",
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
        "no_img": "ℹ️ Aucun visuel importé pour ce produit."
    },
    "Haitian Creole": {
        "subtitle": "Sistèm Avanse pou Jere Pwodwi Chimik ak Envantè Boutik la",
        "top_contact": "🏢 Liy Operasyon Biznis la:",
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
        "no_img": "ℹ️ Pa gen okenn foto ki chaje pou pwodwi sa a."
    }
}

# ================== Sidebar Language Engine Trigger ==================
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
            "image": None
        },
        {
            "name": "Concentrated Caustic Soda Pearls",
            "category": "Raw Materials",
            "price": "8,200 HTG",
            "desc": "Sodium Hydroxide (NaOH) crystals. Widely utilized for commercial soap manufacturing and heavy-duty industrial drainage cleaning.",
            "image": None
        }
    ]

# ================== Top Contact Corporate Infrastructure Header ==================
st.markdown(
    f"""
    <div class="client-header-bar">
        <div style="font-weight: 700; font-size: 1.05rem; color: #00ebc7 !important;">
            📩 Business Support: <a href="mailto:Jamesonbonard97@gmail.com" style="color: #00ebc7; text-decoration: none;">Jamesonbonard97@gmail.com</a>
        </div>
        <div style="font-weight: 700; font-size: 1.05rem; color: #ffffff !important;">
            {txt['top_contact']} <a href="tel:+50944108261" style="color: #ffffff; text-decoration: none;">+509 44 10 8261</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ================== Application Header Architecture ==================
st.title("🧪 BONARDENTERPRISE SOFTWARE")
st.markdown(f"### <span class='neon-text'>{txt['subtitle']}</span>", unsafe_allow_html=True)
st.markdown("---")

# ================== Sidebar Form Components & Security Shield ==================
st.sidebar.markdown(txt['admin_title'])
st.sidebar.markdown(txt['admin_desc'])

# Password gateway input line
entered_password = st.sidebar.text_input(txt['pass_label'], type="password")

if entered_password:
    if entered_password == ADMIN_PASSWORD:
        st.sidebar.success(f"🔓 {txt['pass_success']}")
        
        # Only render the form elements if password matches securely
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
                
                st.session_state.products.insert(0, {
                    "name": new_name,
                    "category": new_cat,
                    "price": new_price,
                    "desc": new_desc,
                    "image": img_bytes
                })
                st.sidebar.success(f"⚡ {new_name} {txt['msg_success']}")
            else:
                st.sidebar.error(txt['msg_error'])
    else:
        st.sidebar.error(f"❌ {txt['pass_error']}")

# ================== Main Window Marketplace Display Grid ==================
st.markdown(txt['catalog_title'])

if not st.session_state.products:
    st.info(txt['catalog_empty'])
else:
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

# ================== Developer Footer Core Layers ==================
st.markdown(
    """
    <div class="footer-container">
        <h4 style="margin-bottom: 5px;">BONARDENTERPRISE SOFTWARE</h4>
        <p style="font-size: 0.95rem; opacity: 0.8; margin-bottom: 15px;">
            Engineered, programmed, and optimized by <strong>GlobalInternet.py</strong>
        </p>
        <p style="font-size: 0.9rem; color: #00ebc7 !important; font-weight: 600;">
            📧 Contact Engineering: <a href="mailto:deslandes78@gmail.com" style="color: #00ebc7; text-decoration: none;">deslandes78@gmail.com</a>
            &nbsp;&nbsp;|&nbsp;&nbsp; 
            📞 Core Infrastructure Line: <a href="tel:+50947385663" style="color: #00ebc7; text-decoration: none;">(509)-47385663</a>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

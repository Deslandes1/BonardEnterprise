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
    h1, h2, h3, h4, p, label, .stMarkdown {
        color: #ffffff !important;
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
    
    /* Fix file uploader and input text colors for dark background */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: rgba(255, 255, 255, 0.07) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ================== Session State Management ==================
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

# ================== Header Architecture ==================
st.title("🧪 BONARDENTERPRISE SOFTWARE")
st.markdown("### <span class='neon-text'>Advanced Chemical Product Management & Storefront Inventory Layer</span>", unsafe_allow_html=True)
st.markdown("---")

# ================== Sidebar: Real-Time Mobile Upload Control ==================
st.sidebar.markdown("## 📥 Admin Upload Panel")
st.sidebar.markdown("Use this panel on your **Computer** or **Phone Gallery** to add stock live.")

with st.sidebar.form(key="upload_form", clear_on_submit=True):
    new_name = st.text_input("Chemical Product Name:")
    new_cat = st.selectbox("Chemical Category:", ["Solvents", "Raw Materials", "Acids & Bases", "Agricultural Chemicals", "Detergents / Surfactants", "Other"])
    new_price = st.text_input("Price (e.g., USD or HTG):")
    new_desc = st.text_area("Product Specifications & Description:")
    
    new_img = st.file_uploader("Capture Photo or Choose from Gallery", type=["jpg", "jpeg", "png", "webp"])
    
    submit_product = st.form_submit_button("Publish Product to Storefront")

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
        st.sidebar.success(f"⚡ {new_name} has been published successfully!")
    else:
        st.sidebar.error("Product Name and Price fields are strictly required.")

# ================== Main Body: Grid Layout Marketplace ==================
st.markdown("## 🛍️ Active Chemical Catalog")

if not st.session_state.products:
    st.info("The catalog is currently empty. Use the sidebar panel to upload your inventory items.")
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
                st.caption("ℹ️ No visual asset uploaded for this product layer.")

# ================== Professional Footer Layout ==================
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

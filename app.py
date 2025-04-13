import streamlit as st
from backend import generate_landing_page
import time

def set_page_config():
    """Configure page settings"""
    st.set_page_config(
        page_title="AI Brand Page Generator",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def image_uploader_main():
    """Handles image upload in main area"""
    with st.container():
        st.subheader("Product Images")
        col1, col2 = st.columns([3, 1])
        
        with col1:
            uploaded_files = st.file_uploader(
                "Drag & drop product images (max 5)",
                type=["png", "jpg", "jpeg"],
                accept_multiple_files=True,
                label_visibility="collapsed"
            )
            
        with col2:
            image_layout = st.selectbox(
                "Layout Style",
                ["Hero + Grid", "Carousel", "Equal Grid"],
                index=0
            )
            
        if uploaded_files:
            st.write(f"Selected images: {len(uploaded_files)}/5")
            cols = st.columns(min(4, len(uploaded_files)))
            for idx, img_file in enumerate(uploaded_files):
                with cols[idx % 4]:
                    st.image(img_file, use_column_width=True)
    
    return uploaded_files

def sidebar_controls():
    """Collect inputs in sidebar"""
    with st.sidebar:
        st.header("Configuration Panel")
        
        # Brand Guidelines
        st.subheader("Brand Colors")
        primary_color = st.color_picker("Primary Color", "#4A90E2")
        secondary_color = st.color_picker("Secondary Color", "#FF6B6B")
        accent_color = st.color_picker("Accent Color", "#FFD700")
        font_family = st.selectbox("Font Family", ["Inter", "Poppins", "Roboto", "Open Sans"])
        
        # Product Details
        st.subheader("Product Information")
        product_name = st.text_input("Product Name", "Your Product")
        product_desc = st.text_area("Product Description", placeholder="Describe your product in detail...")
        product_price = st.number_input("Product Price ($)", min_value=0.0, value=49.99)
        price_display = st.radio("Price Format", ["$X.XX", "Starting at $X", "Contact for Pricing"])
        
        # Content Settings
        st.subheader("Content Settings")
        content_priority = st.slider("Visual/Text Balance", 1, 5, 3)
        num_features = st.slider("Number of Features", 1, 5, 2)

    return {
        "primary_color": primary_color,
        "secondary_color": secondary_color,
        "accent_color": accent_color,
        "font_family": font_family,
        "product_name": product_name,
        "product_desc": product_desc,
        "product_price": product_price,
        "price_display": price_display,
        "content_priority": content_priority,
        "num_features": num_features,
    }

def main():
    set_page_config()
    st.title("UI Generator")
    
    # Image upload in main area
    uploaded_files = image_uploader_main()
    
    # Sidebar controls
    inputs = sidebar_controls()
    
    if st.button("✨ Generate Landing Page"):
        if not inputs['product_desc']:
            st.error("Please provide a product description")
            return
            
        with st.spinner("Generating your custom page..."):
            try:
                start_time = time.time()
                
                # Generate the landing page
                result = generate_landing_page(inputs, uploaded_files)
                
                # Display live preview of generated HTML
                st.subheader("Live Preview")
                with st.container():
                    st.components.v1.html(result["html"], height=600, scrolling=True)
                
                # Download Button for HTML file
                st.download_button(
                    label="📥 Download HTML",
                    data=result["html"],
                    file_name="landing_page.html",
                    mime="text/html"
                )
                
                # Debugging: Show embedded images (optional)
                if result["images"]:
                    st.subheader("Embedded Images (Base64)")
                    for img in result["images"]:
                        st.code(img[:100] + "...")  # Show first 100 characters
                
                st.success(f"Generated in {time.time()-start_time:.1f}s")
                
            except Exception as e:
                st.error(f"Generation failed: {str(e)}")

if __name__ == "__main__":
    main()

import os
import requests
import re
import base64

TOGETHER_API_KEY = "YOUR_API_KEY"

def generate_landing_page(inputs, uploaded_files=[]):
    """Generate landing page HTML/CSS using Together AI."""

    # Convert uploaded images to Base64
    image_placeholders = {}
    for idx, file in enumerate(uploaded_files):
        file.seek(0)
        base64_image = base64.b64encode(file.read()).decode("utf-8")
        file_type = file.type.split('/')[-1] if hasattr(file, 'type') else 'jpeg'
        image_placeholders[f"IMAGE_{idx+1}"] = f"data:image/{file_type};base64,{base64_image}"

    # Enhanced CSS variables with fallbacks
    css_variables = f"""
    :root {{
        --primary-color: {inputs['primary_color']} !important;
        --secondary-color: {inputs['secondary_color']} !important;
        --accent-color: {inputs['accent_color']} !important;
        --font-family: {inputs['font_family']}, sans-serif !important;
    }}
    body {{
        background-color: {inputs['secondary_color']} !important;
        color: {inputs['primary_color']} !important;
    }}
    """

    # Create placeholders for the required number of feature images
    feature_placeholders = "\n".join(
        f'<div class="image-placeholder feature-image-placeholder"><!-- FEATURE_IMAGE_{i+1} --></div>'
        for i in range(inputs['num_features'])
    )

    prompt_template = f"""
Generate modern HTML/CSS for a dark-themed product landing page with these specifications:

## Design Requirements
- Use CSS variables from this :root selector:
{css_variables}
- Create a DARK MODE design with dark backgrounds and light text
- Background should use var(--bg-color)
- Text should use var(--text-color)
- Card/section backgrounds should use var(--card-bg-color)
- All accent colors MUST use the CSS variables (--primary-color, --secondary-color, --accent-color)
- All fonts MUST use --font-family

## Content
- Product Description: "{inputs['product_desc']}"
- Product Price: "{inputs['product_price']}"
- Price Display Format: "{inputs['price_display']}"
- Include {len(uploaded_files)} product images using these exact placeholder tags:
  <div class="image-placeholder hero-image-placeholder"><!-- HERO_IMAGE --></div> (for hero section)
  {feature_placeholders}

## Required Sections
1. Hero Section with hero image
2. Features Section with feature images 
3. Pricing Section
4. Footer


Return ONLY valid HTML/CSS code using these requirements.
"""

    url = "https://api.together.xyz/v1/completions"
    headers = {'Authorization': f'Bearer {TOGETHER_API_KEY}', 'Content-Type': 'application/json'}
    data = {
        "model": "deepseek-ai/DeepSeek-V3",
        "prompt": prompt_template,
        "max_tokens": 4096,
        "temperature": 0.7,
        "top_p": 0.9,
        "stop": ["<|im_end|>"]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        generated_html = response.json().get('choices', [{}])[0].get('text', '').strip()
        if generated_html.startswith("```html"):
            generated_html = re.sub(r"^```html\s*|\s*```$", "", generated_html, flags=re.DOTALL).strip()

        # Replace placeholders with Base64 images
        generated_html = generated_html.replace(
            "<!-- HERO_IMAGE -->",
            f'<img src="{image_placeholders.get("IMAGE_1", "")}" alt="Hero Image" class="hero-image">'
        )

        for i in range(inputs['num_features']):
            generated_html = generated_html.replace(
                f"<!-- FEATURE_IMAGE_{i+1} -->",
                f'<img src="{image_placeholders.get(f"IMAGE_{i+2}", "")}" alt="Feature Image {i+1}" class="feature-image">'
            )

        return {
            "html": generated_html,
            "images": list(image_placeholders.values()),
            "generated_content": {
                "headline": "Auto-generated in HTML",
                "subheadline": "Auto-generated in HTML",
                "cta_text": "Auto-generated in HTML",
                "features": "Auto-generated in HTML"
            }
        }
    else:
        raise ValueError(f"API Error: {response.status_code}, {response.text}")

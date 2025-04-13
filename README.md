# Project Overview

- This project is an AI-powered tool designed to generate professional, brand-specific landing pages quickly and efficiently. It allows users to input their brand guidelines, product details, and images to create visually appealing, responsive web pages. Built with Python and Streamlit, the project leverages Together AI to generate HTML/CSS code dynamically.
---

## Features

- **AI-Generated HTML/CSS**: Automatically create modern, responsive landing pages based on user inputs.
- **Customizable Design**: Tailor pages with your brand’s colors, fonts, and layout preferences.
- **Image Integration**: Seamlessly embed uploaded product images using Base64 encoding.
- **Dark Mode Support**: Generate designs optimized for dark mode with custom color schemes.
- **Downloadable Output**: Save the generated HTML file for deployment or further customization.

---

## Technologies Used

### Frontend
- [Streamlit](https://streamlit.io): Interactive UI for collecting user inputs and live previewing results.

### Backend
- [Together AI](https://together.xyz): API for generating HTML/CSS code based on prompts.
- Python Libraries:
  - `requests`: For API communication.
  - `base64`: For encoding uploaded images.
  - `re`: For placeholder replacements.

---

## Setup Instructions

### 1. Clone the Repository
### 2. Install Dependencies
  - `requests`: For API communication.
  - `base64`: For encoding uploaded images.
  - `re`: For placeholder replacements.
### 3. Add Your API Key
### 4. Run the Application
  - streamlit run app.py
### 5. Steps to Generate a Landing Page
  - Upload product images (up to 5).
  - Select brand colors, font family, and other design preferences.
  - Provide product details (name, description, price).
  - Click "Generate Landing Page" to see the live preview.
  - Download the generated HTML file for deployment or further customization.


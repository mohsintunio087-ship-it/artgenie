import streamlit as st
import io
import random
from PIL import Image
from huggingface_hub import InferenceClient

icon = Image.open("icon.png")
st.set_page_config(page_title="ArtGenie Pro", page_icon=icon, layout="centered")

# ---------- CUSTOM THEME / CSS ----------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1e1b4b 0%, #4c1d95 50%, #7e22ce 100%);
    }
    .main .block-container {
        padding-top: 2rem;
    }
    h1 {
        color: #ffffff !important;
        text-align: center;
        font-weight: 800 !important;
        text-shadow: 0px 0px 20px rgba(168, 85, 247, 0.6);
    }
    p, label, .stMarkdown {
        color: #e9d5ff !important;
    }
    .stTextArea textarea, .stTextInput input {
        background-color: rgba(255, 255, 255, 0.08) !important;
        color: #000000 !important;
        border: 1px solid rgba(168, 85, 247, 0.5) !important;
        border-radius: 12px !important;
    }
    .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
    }
    .stButton button {
        background: linear-gradient(90deg, #a855f7, #ec4899) !important;
        color: white !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.6rem 2rem !important;
        box-shadow: 0px 4px 15px rgba(236, 72, 153, 0.5) !important;
        transition: 0.3s !important;
    }
    .stButton button:hover {
        transform: scale(1.05);
        box-shadow: 0px 6px 20px rgba(236, 72, 153, 0.8) !important;
    }
    .stDownloadButton button {
        background: linear-gradient(90deg, #22c55e, #16a34a) !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
    }
    div[data-testid="stImage"] img {
        border-radius: 15px;
        box-shadow: 0px 8px 25px rgba(0,0,0,0.4);
    }
</style>
""", unsafe_allow_html=True)

if 'history' not in st.session_state:
    st.session_state.history = []

st.title("🧞 ArtGenie Pro")
st.write("✨ Apna prompt likhein aur AI se stunning images generate karein!")

prompt = st.text_area(
    "📝 Prompt likhen (Aap kya banana chahte hain?):",
    placeholder="e.g., a rural mud house with mountains in the background, heavy rainy day, wet mud ground"
)

negative_prompt = st.text_input(
    "🚫 Negative Prompt (optional - jo cheez NAHI chahiye):",
    placeholder="e.g., blurry, low quality, distorted, text, watermark"
)

STYLE_PRESETS = {
    "Koi Style Nahi (Default)": "",
    "Photorealistic": ", photorealistic, highly detailed, 8k, professional photography",
    "Anime": ", anime style, vibrant colors, Studio Ghibli inspired, cel shaded",
    "3D Render": ", 3D render, octane render, ultra detailed, cinematic lighting",
    "Digital Art": ", digital art, concept art, trending on artstation, detailed illustration",
    "Watercolor Painting": ", watercolor painting, soft brush strokes, artistic, pastel colors",
    "Sketch / Pencil Drawing": ", pencil sketch, hand-drawn, black and white, detailed linework",
    "Cyberpunk": ", cyberpunk style, neon lights, futuristic, dark atmosphere, sci-fi",
    "Fantasy Art": ", fantasy art style, magical, ethereal lighting, epic composition"
}

ASPECT_RATIOS = {
    "Square (1:1)": (1024, 1024),
    "Landscape (16:9)": (1344, 768),
    "Portrait (9:16)": (768, 1344),
    "Standard Photo (4:3)": (1152, 896),
    "Wide (21:9)": (1536, 640)
}

QUALITY_MODES = {
    "⚡ Fast (kam detail, tez)": "black-forest-labs/FLUX.1-schnell",
    "💎 High Quality (zyada detail, thoda slow)": "black-forest-labs/FLUX.1-dev"
}

col1, col2 = st.columns(2)
with col1:
    selected_style = st.selectbox("🎨 Style Preset:", list(STYLE_PRESETS.keys()))
    selected_ratio = st.selectbox("📐 Image Size/Ratio:", list(ASPECT_RATIOS.keys()))
with col2:
    selected_quality = st.selectbox("⚙️ Quality Mode:", list(QUALITY_MODES.keys()))
    num_images = st.selectbox("🖼️ Kitni Images chahiye:", [1, 2, 3, 4])

col3, col4 = st.columns([3, 1])
with col3:
    seed_input = st.number_input("🎲 Seed (0 = random har baar):", min_value=0, max_value=999999, value=0)
with col4:
    st.write("")
    st.write("")
    randomize = st.checkbox("Random", value=True)

import urllib.parse

if st.button("🚀 Generate"):
    if not prompt:
        st.warning("⚠️ Pehle prompt likhen (Aap kya banana chahte hain)!")
    else:
        final_prompt = f"{prompt}{STYLE_PRESETS[selected_style]}"
        width, height = ASPECT_RATIOS[selected_ratio]

        with st.spinner("✨ AI aapki image generate kar raha hai... thoda time lag sakta hai"):
            try:
                generated_images = []

                for i in range(num_images):
                    current_seed = random.randint(0, 999999) if randomize else seed_input + i

                    encoded_prompt = urllib.parse.quote(final_prompt)
                    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&seed={current_seed}&nologo=true"

                    if negative_prompt:
                        url += f"&negative_prompt={urllib.parse.quote(negative_prompt)}"

                    import requests
                    response = requests.get(url, timeout=60)

                    if response.status_code == 200:
                        result_image = Image.open(io.BytesIO(response.content))
                        generated_images.append(result_image)
                        st.session_state.history.append(result_image)
                    else:
                        st.error(f"⚠️ Error: Response code {response.status_code}")

                if generated_images:
                    st.markdown("### ✨ Generated Images")
                    cols = st.columns(min(len(generated_images), 2))
                    for idx, img in enumerate(generated_images):
                        with cols[idx % len(cols)]:
                            st.image(img, caption=f"ArtGenie Output {idx+1}", use_container_width=True)
                            buf = io.BytesIO()
                            img.save(buf, format="PNG")
                            st.download_button(
                                label=f"⬇️ Download {idx+1}",
                                data=buf.getvalue(),
                                file_name=f"generated_image_{idx+1}.png",
                                mime="image/png",
                                key=f"download_{idx}"
                            )

            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}. Ek dafa aur try karein ya thodi der wait karein.")

if len(st.session_state.history) > 1:
    st.markdown("---")
    st.subheader("📜 Pichli Changes")
    cols = st.columns(3)
    for i, img in enumerate(reversed(st.session_state.history[:-1])):
        if i >= 6:
            break
        with cols[i % 3]:
            st.image(img, use_container_width=True)
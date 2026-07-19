import streamlit as st
import io
from PIL import Image
from huggingface_hub import InferenceClient

icon = Image.open("icon.png")
st.set_page_config(page_title="ArtGenie Pro", page_icon=icon, layout="centered")

if 'history' not in st.session_state:
    st.session_state.history = []

st.title("🧞 ArtGenie Pro")
st.write("Apna prompt likhein aur AI se image generate karein! (Free Hugging Face engine)")
st.info("ℹ️ Note: Ye tool poori scene text se generate karta hai — uploaded image ko directly modify nahi karta. Isliye prompt mein poori scene describe karein (jo bhi image mein dikhna chahiye).")

uploaded_file = st.file_uploader("📁 Reference ke liye pic upload karen (optional - JPG/PNG):", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    input_image = Image.open(uploaded_file)
    input_image = input_image.resize((512, 512))
    st.image(input_image, caption="Aap ki Reference Image", width=250)

prompt = st.text_area(
    "Prompt likhen (Poori scene describe karein jo image mein dikhni chahiye):",
    placeholder="e.g., a rural mud house with mountains in the background, heavy rainy day, wet mud ground, dark clouds, no people visible, photorealistic"
)

if st.button("🚀 Generate"):
    if not prompt:
        st.warning("⚠️ Pehle prompt likhen (Aap kya banana chahte hain)!")
    else:
        with st.spinner("Hugging Face AI image generate kar raha hai... thoda time lag sakta hai"):
            try:
                client = InferenceClient(api_key=st.secrets["HF_TOKEN"])

                generated_image = client.text_to_image(
                    f"{prompt}, photorealistic, highly detailed",
                    model="black-forest-labs/FLUX.1-schnell"
                )

                st.session_state.history.append(generated_image)

                st.markdown("### ✨ Generated Image")
                st.image(generated_image, caption="ArtGenie Output", use_container_width=True)

                buf = io.BytesIO()
                generated_image.save(buf, format="PNG")
                byte_data = buf.getvalue()

                st.download_button(
                    label="⬇️ Download Image",
                    data=byte_data,
                    file_name="generated_image.png",
                    mime="image/png"
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
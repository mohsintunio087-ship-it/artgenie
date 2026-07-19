import streamlit as st
import io
import requests
from PIL import Image
import random

icon = Image.open("icon.png")
st.set_page_config(page_title="ArtGenie Pro", page_icon=icon, layout="centered")

if 'history' not in st.session_state:
    st.session_state.history = []

st.title("🧞 ArtGenie Pro")
st.write("Apni image upload karen aur prompt likh kar use modify ya change karein!")

uploaded_file = st.file_uploader("📁 Apni pic yahan upload karen (JPG/PNG):", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    input_image = Image.open(uploaded_file)
    input_image = input_image.resize((512, 512))
    st.image(input_image, caption="Aap ki Uploaded Image", width=250)

prompt = st.text_area("Prompt likhen (Aap is image me kya change karna chahte hain?):",
                      placeholder="e.g., change image into a heavy rainy day, wet mud floor, dark clouds, rain drops")

if st.button("🚀 Modify Image"):
    if uploaded_file is None:
        st.warning("⚠️ Pehle koi image upload karen!")
    elif not prompt:
        st.warning("⚠️ Pehle batayein ke image me kya change karna hai (Prompt likhen)!")
    else:
        with st.spinner("AI aapki image ko modify kar raha hai..."):
            try:
                if input_image.mode == 'RGBA':
                    background = Image.new("RGB", input_image.size, (255, 255, 255))
                    background.paste(input_image, mask=input_image.split()[3])
                    processed_image = background
                else:
                    processed_image = input_image.convert('RGB')

                img_byte_arr = io.BytesIO()
                processed_image.save(img_byte_arr, format='JPEG', quality=85)
                img_bytes = img_byte_arr.getvalue()

                if "CLIPDROP_API_KEY" not in st.secrets:
                    st.error("⚠️ CLIPDROP_API_KEY secrets mein missing hai. Settings mein add karein.")
                else:
                    response = requests.post(
                        "https://clipdrop-api.co/v1/image-to-image",
                        headers={"x-api-key": st.secrets["CLIPDROP_API_KEY"]},
                        files={"image": img_bytes},
                        data={"prompt": f"rural mud house and mountain scenery completely transformed into a heavy rainy day, {prompt}"}
                    )

                    if response.status_code == 200:
                        modified_image = Image.open(io.BytesIO(response.content))
                        st.session_state.history.append(modified_image)

                        st.markdown("### ✨ Modified AI Image")
                        st.image(modified_image, caption="ArtGenie Output", use_container_width=True)

                        buf = io.BytesIO()
                        modified_image.save(buf, format="PNG")
                        byte_data = buf.getvalue()

                        st.download_button(
                            label="⬇️ Download Modified Image",
                            data=byte_data,
                            file_name="modified_image.png",
                            mime="image/png"
                        )
                    else:
                        st.error(f"⚠️ AI Engine error. Response code: {response.status_code}. Ek dafa aur try karein.")

            except Exception as e:
                st.error(f"⚠️ Connection error: {str(e)}. Page refresh karke check karein.")

if len(st.session_state.history) > 1:
    st.markdown("---")
    st.subheader("📜 Pichli Changes")
    cols = st.columns(3)
    for i, img in enumerate(reversed(st.session_state.history[:-1])):
        if i >= 6: break
        with cols[i % 3]:
            st.image(img, use_container_width=True)
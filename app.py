import streamlit as st
import io
from PIL import Image
from huggingface_hub import InferenceClient

icon = Image.open("icon.png")
st.set_page_config(page_title="ArtGenie Pro", page_icon=icon, layout="centered")

if 'history' not in st.session_state:
    st.session_state.history = []

st.title("🧞 ArtGenie Pro")
st.write("Apni image upload karen (optional) aur prompt likh kar image generate ya modify karein!")

uploaded_file = st.file_uploader("📁 Apni pic yahan upload karen (optional - JPG/PNG):", type=["jpg", "jpeg", "png"])

input_image = None
if uploaded_file is not None:
    input_image = Image.open(uploaded_file)
    input_image = input_image.resize((512, 512))
    st.image(input_image, caption="Aap ki Uploaded Image", width=250)

prompt = st.text_area(
    "Prompt likhen (Aap kya banana ya change karna chahte hain?):",
    placeholder="e.g., change into heavy rainy weather, remove the people from the image"
)

if st.button("🚀 Generate"):
    if not prompt:
        st.warning("⚠️ Pehle prompt likhen (Aap kya banana chahte hain)!")
    else:
        with st.spinner("AI aapki image generate/modify kar raha hai... thoda time lag sakta hai"):
            try:
                client = InferenceClient(api_key=st.secrets["HF_TOKEN"])

                if input_image is not None:
                    # IMAGE-TO-IMAGE: uploaded image ko asal mein modify karega
                    result_image = client.image_to_image(
                        image=input_image,
                        prompt=prompt,
                        model="black-forest-labs/FLUX.1-Kontext-dev"
                    )
                else:
                    # TEXT-TO-IMAGE: sirf prompt se naya image banayega
                    result_image = client.text_to_image(
                        f"{prompt}, photorealistic, highly detailed",
                        model="black-forest-labs/FLUX.1-schnell"
                    )

                st.session_state.history.append(result_image)

                st.markdown("### ✨ Generated Image")
                st.image(result_image, caption="ArtGenie Output", use_container_width=True)

                buf = io.BytesIO()
                result_image.save(buf, format="PNG")
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
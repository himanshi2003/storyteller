import streamlit as st
from groq import Groq
import base64
import groq

# Initialize Groq client
client = Groq()
llava_model = 'llava-v1.5-7b-4096-preview'
llama31_model = 'llama-3.1-70b-versatile'

# Function to encode the image
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# Function to convert image to text
def image_to_text(client, model, base64_image, prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        model=model
    )
    return chat_completion.choices[0].message.content

# Function to generate short story
def short_story_generation(client, image_description):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a children's book author. Write a short story about the scene depicted in this image or images.",
            },
            {
                "role": "user",
                "content": image_description,
            }
        ],
        model=llama31_model
    )
    return chat_completion.choices[0].message.content

# Streamlit UI
st.title("Image to Story Generator")

# Image upload for single image processing
st.header("Process a Single Image")
uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    # Encode image
    base64_image = encode_image(uploaded_image)

    # Set the prompt for description
    prompt = "Describe this image in detail, including the appearance of the dog(s) and any notable actions or behaviors."
    
    # Get image description
    with st.spinner('Generating image description...'):
        image_description = image_to_text(client, llava_model, base64_image, prompt)
        st.write("### Image Description:")
        st.write(image_description)
    
    # Generate short story
    with st.spinner('Generating short story...'):
        short_story = short_story_generation(client, image_description)
        st.write("### Short Story:")
        st.write(short_story)

# Image upload for multiple image processing
st.header("Process Multiple Images")
uploaded_images = st.file_uploader("Upload multiple images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_images:
    image_descriptions = []
    for image in uploaded_images:
        base64_image = encode_image(image)
        description = image_to_text(client, llava_model, base64_image, prompt)
        image_descriptions.append(description)
        st.write(f"### Image Description for {image.name}:")
        st.write(description)

    # Combine descriptions for short story
    combined_image_description = "\n\n".join(image_descriptions)

    with st.spinner('Generating combined short story...'):
        combined_story = short_story_generation(client, combined_image_description)
        st.write("### Combined Short Story for Multiple Images:")
        st.write(combined_story)

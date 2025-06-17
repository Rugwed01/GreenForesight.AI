import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import io
from PIL import Image

# === Image Generation via Hugging Face Diffusers ===
from diffusers import StableDiffusionPipeline
import torch

# === Line Chart: Green Score Over Years ===
def plot_green_score_line(projection_dict, return_bytes=False):
    years = list(projection_dict.keys())
    scores = list(projection_dict.values())

    fig, ax = plt.subplots()
    sns.lineplot(x=years, y=scores, marker="o", ax=ax)
    ax.set_title("Green Score Projection Over Years")
    ax.set_ylabel("Green Score")
    ax.set_xlabel("Year")
    ax.grid(True)

    if return_bytes:
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        return buf.read()
    else:
        st.pyplot(fig)

def plot_impact_bar(breakdown_dict, return_bytes=False):
    categories = list(breakdown_dict.keys())
    values = list(breakdown_dict.values())

    fig, ax = plt.subplots()
    sns.barplot(x=values, y=categories, palette="Greens_r", ax=ax)
    ax.set_title("Carbon Emission Breakdown by Category")
    ax.set_xlabel("Emissions (kg)")
    ax.set_ylabel("Category")

    if return_bytes:
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        return buf.read()
    else:
        st.pyplot(fig)

# === Load Diffusion Model (cached for performance) ===
@st.cache_resource
def load_diffusion_pipeline():
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    )
    pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")
    return pipe

# === Generate Future Visual with Stable Diffusion ===
def generate_future_image(prompt="Futuristic green city in 2100 with renewable energy"):
    st.info("🔄 Generating AI-powered future image... (Stable Diffusion)")
    pipe = load_diffusion_pipeline()
    image: Image.Image = pipe(prompt).images[0]
    st.image(image, caption=prompt, use_column_width=True)

    # Save image to session state for later use (e.g. PDF)
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.session_state.generated_image_bytes = byte_im
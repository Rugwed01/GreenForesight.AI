import streamlit as st
from backend.simulation_engine import simulate_impact
from weasyprint import HTML
import tempfile
from visuals.graph_plotter import plot_green_score_line, plot_impact_bar, generate_future_image
import base64

# ================= Page Config =================
st.set_page_config(page_title="GreenForesight.AI", layout="centered")

# ========== Custom Styles ==========
def inject_css():
    st.markdown("""
    <style>
    body {
        font-family: 'Georgia', serif;
        background-color: #f4f1ec;
    }
    .headline {
        font-size: 24px;
        font-weight: bold;
        margin-top: 20px;
        color: #2e2e2e;
        border-left: 5px solid #2e8b57;
        padding-left: 10px;
    }
    .date-tag {
        font-size: 16px;
        color: #6c757d;
        font-style: italic;
    }
    .section {
        background-color: #ffffff;
        padding: 25px;
        margin: 15px 0;
        border-radius: 12px;
        box-shadow: 0px 3px 10px rgba(0,0,0,0.1);
    }
    .quote {
        font-size: 18px;
        color: #555;
        margin: 20px 0;
        padding-left: 15px;
        border-left: 3px solid #2e8b57;
    }
    </style>
    """, unsafe_allow_html=True)

inject_css()

# ========== Header ==========
st.title("🌿 GreenForesight.AI")
st.subheader("AI-Powered Time Machine for Your Sustainability Choices")
st.markdown("Choose your daily habits to simulate your environmental future 🌍")

# ========== User Form ==========
with st.form("user_choices"):
    meat = st.selectbox("🍔 Do you eat meat daily?", ["Yes", "No", "Occasionally"])
    transport = st.selectbox("🚗 How do you commute daily?", ["Car", "Public Transport", "Bike/Walk", "Electric Vehicle"])
    plastic = st.selectbox("🧴 Do you use single-use plastic?", ["Frequently", "Rarely", "Never"])
    energy = st.selectbox("🔌 Your household energy source?", ["Coal-based", "Mixed", "Solar/Renewable"])
    flights = st.selectbox("✈️ How often do you fly?", ["Frequent", "Occasional", "Never"])
    water = st.selectbox("🚿 Your water usage level?", ["High", "Moderate", "Low"])
    shopping = st.selectbox("📦 How often do you shop online?", ["Often", "Sometimes", "Never"])
    submitted = st.form_submit_button("🔮 Simulate My Future")

# ====================== STATE MANAGEMENT ======================
if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "result" not in st.session_state:
    st.session_state.result = None

if submitted:
    st.session_state.submitted = True
    result = simulate_impact(meat, transport, plastic, energy, flights, water, shopping)
    st.session_state.result = result

# ====================== MAIN RESULT SECTION ======================
if st.session_state.submitted and st.session_state.result:
    result = st.session_state.result
    total_emissions = result["total_emissions"]
    breakdown = result["breakdown"]
    projection = result["projection"]
    green_score = result["green_score"]

    st.success("Simulation complete ✅ Generating your climate story...")

    # Color-coded green score
    if green_score >= 75:
        score_color = "green"
    elif green_score >= 40:
        score_color = "orange"
    else:
        score_color = "red"

    st.markdown(f"""
    <div class='section'>
        <div class='headline'>[ 🧮 Green Score ]</div>
        <p style='font-size: 20px; color: {score_color};'>
            Your Green Score: <strong>{green_score}</strong> (0 = worst, 100 = best)
        </p>
    </div>
    """, unsafe_allow_html=True)

    opening_paragraph = f"""
    The relentlessness of climate change is etched into every sunrise and sweeping across every landscape of our lives. Yet, some choose to remain oblivious, forging onward in their carbon-fueled quest for convenience at the cost of an inhabitable Earth. This is the story of John, whose annual carbon footprint of <b>{total_emissions} kg</b> echoed through decades, leaving ruined landscapes in its wake.
    """
    projection_headlines = {
        2035: "🌡️ Global Temperature Rise Hits Critical Threshold",
        2050: "🌪️ Catastrophic Impacts: Extreme Weather Era Begins",
        2075: "🚨 The Legacy of Choices: Desperate Days Ahead"
    }
    human_story = """
    At the heart of this narrative lies John — a mere mortal whose everyday choices contributed to this unfolding climate crisis. As a child, he played in the woods and loved nature. But over the years, his choices created an invisible trail of carbon — one that now defines humanity's uncertain future.
    """

    st.markdown(f"<div class='headline'>[ Opening Paragraph ]</div>", unsafe_allow_html=True)
    st.write(opening_paragraph, unsafe_allow_html=True)

    st.markdown(f"<div class='headline'>[ Emissions Breakdown ]</div>", unsafe_allow_html=True)
    for k, v in breakdown.items():
        st.markdown(f"• **{k}**: {v} kg")

    st.markdown(f"<div class='headline'>[ Projected Future Headlines ]</div>", unsafe_allow_html=True)
    for year, headline in projection_headlines.items():
        st.markdown(f"<p class='date-tag'>{year}</p><p class='quote'>{headline}</p>", unsafe_allow_html=True)

    st.markdown(f"<div class='headline'>[ The Human Story ]</div>", unsafe_allow_html=True)
    st.write(human_story, unsafe_allow_html=True)

    st.markdown(f"<div class='headline'>[ 📈 Green Score Over Time ]</div>", unsafe_allow_html=True)
    plot_green_score_line(projection)

    st.markdown(f"<div class='headline'>[ 🌍 Emissions Breakdown by Category ]</div>", unsafe_allow_html=True)
    plot_impact_bar(breakdown)

    st.markdown(f"<div class='headline'>[ 🧠 AI-Powered Future Vision ]</div>", unsafe_allow_html=True)
    prompt = st.text_input("Enter your vision prompt:", "Futuristic green city in 2100 with renewable energy and vertical farms")

    if "image_generated" not in st.session_state:
        st.session_state.image_generated = False

    if st.button("🎨 Generate Future Image"):
        st.session_state.image_generated = True

    if st.session_state.image_generated:
        generate_future_image(prompt)

    from visuals.graph_plotter import plot_green_score_line, plot_impact_bar

    line_chart_bytes = plot_green_score_line(projection, return_bytes=True)
    bar_chart_bytes = plot_impact_bar(breakdown, return_bytes=True)

    line_chart_b64 = base64.b64encode(line_chart_bytes).decode("utf-8")
    bar_chart_b64 = base64.b64encode(bar_chart_bytes).decode("utf-8")

    charts_html = f"""
    <h3>📈 Green Score Over Time</h3>
    <img src="data:image/png;base64,{line_chart_b64}" style="width:100%; max-width:600px;" />
    <h3>🌍 Emissions Breakdown by Category</h3>
    <img src="data:image/png;base64,{bar_chart_b64}" style="width:100%; max-width:600px;" />
    """

    image_html = ""
    if "generated_image_bytes" in st.session_state:
        encoded_image = base64.b64encode(st.session_state.generated_image_bytes).decode("utf-8")
        image_html = f'<h3>AI-Generated Future Vision</h3><img src="data:image/png;base64,{encoded_image}" style="width:100%; max-width:600px;" />'

    html_content = f"""
    <html>
    <head><meta charset="utf-8"><style>
    body {{ font-family: 'Georgia', serif; padding: 30px; }}
    h1 {{ color: #2e8b57; }} h3 {{ margin-top: 30px; color: #2e2e2e; }}
    ul {{ padding-left: 20px; }}</style></head><body>
    <h3>Green Score</h3>
    <p style='color:{score_color}; font-size:18px;'>Your Green Score: <strong>{green_score}</strong></p>
    <h1>GreenForesight Climate Chronicle</h1>
    <h3>Opening Paragraph</h3><p>{opening_paragraph}</p>
    <h3>Emissions Breakdown</h3><ul>
    """
    for k, v in breakdown.items():
        html_content += f"<li><b>{k}</b>: {v} kg</li>"
    html_content += "</ul><h3>Projected Future Headlines</h3>"
    for year, headline in projection_headlines.items():
        html_content += f"<p><i>{year}</i>: {headline}</p>"
    html_content += f"<h3>The Human Story</h3><p>{human_story}</p>{image_html}" + charts_html + "</body></html>"

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        HTML(string=html_content).write_pdf(tmp_pdf.name)
        with open(tmp_pdf.name, "rb") as f:
            pdf_data = f.read()

    st.download_button(
        label="📄 Download Climate Story as PDF",
        data=pdf_data,
        file_name="greenforesight_climate_story.pdf",
        mime="application/pdf"
    )
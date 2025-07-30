import streamlit as st
import requests
import os
import time
import asyncio

# Set page config
st.set_page_config(page_title="ME/CFS & Depression App", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigate Menu")
menu = st.sidebar.radio(
    "Navigate to:",
    ("Home", "App", "About Model", "Team Members", "FAQ")
)

# --- Home ---
if menu == "Home":
    st.title("ME/CFS & Depression Screening Tool")

    # Image paths (built relative to script location)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    images = [
        os.path.join(base_dir, 'static', 'images', 'img1.jpeg'),
        os.path.join(base_dir, 'static', 'images', 'img2.jpeg'),
        os.path.join(base_dir, 'static', 'images', 'img3.png'),
    ]

    # Initialize session state
    if "img_index" not in st.session_state:
        st.session_state.img_index = 0
    if "auto_slide" not in st.session_state:
        st.session_state.auto_slide = True

    # Image display
    st.image(images[st.session_state.img_index])

    # Manual controls
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("◀️ Previous"):
            st.session_state.img_index = (st.session_state.img_index - 1) % len(images)
            st.session_state.auto_slide = False
    with col2:
        if st.button("▶️ Next"):
            st.session_state.img_index = (st.session_state.img_index + 1) % len(images)
            st.session_state.auto_slide = False
    with col3:
        toggle = st.toggle("🔁 Auto Slide", value=st.session_state.auto_slide)
        st.session_state.auto_slide = toggle

    # Auto slide logic
    async def auto_rotate():
        await asyncio.sleep(5)
        if st.session_state.auto_slide:
            st.session_state.img_index = (st.session_state.img_index + 1) % len(images)
            st.rerun()

    if st.session_state.auto_slide:
        asyncio.run(auto_rotate())

# --- App ---
elif menu == "App":
    st.title("Predict Diagnosis")
    
    st.write("Please enter the required information below:")

    depression_score = st.number_input("Depression Score (0–27)", min_value=0, max_value=27, help="Enter your PHQ-9 score.")
    pem_present = st.selectbox("Post-Exertional Malaise Present?", ["Yes", "No"], help="Do you experience PEM after physical or mental exertion?")

    if st.button("Predict"):
        input_data = {
            "depression_score": depression_score,
            "post_exertional_malaise": pem_present
        }

        try:
            response = requests.post("http://127.0.0.1:8000/predict", json=input_data)
            if response.status_code == 200:
                prediction = response.json().get("prediction")
                st.error(f"Prediction: {prediction}")
                st.info("Note: This is a research-based tool and **not a substitute for medical diagnosis**.")
            else:
                st.error("Error in prediction. Please try again later.")
        except requests.exceptions.RequestException as e:
            st.error("Could not connect to the prediction API.")

    st.markdown("---")
    st.header("How to Use This App")
    st.markdown("""
        - **Depression Score** is based on the **PHQ-9** questionnaire.
        - **Post-Exertional Malaise (PEM)** refers to worsening symptoms after exertion.
        - Click **Predict** to classify your condition as **Depression**, **ME/CFS**, or **Both**.
    """)
    st.warning("This app is for educational use only. Please consult a medical professional.")

# --- About Model ---
elif menu == "About Model":
    st.title("About the Machine Learning Model")
    st.success("Model: Support Vector Classifier (SVC)")
    st.info("🔧 Tuned using Grid SearchCV and Optuna for optimal hyperparameters.")
    st.warning("SMOTE applied to balance class distribution.")
    st.success("Accuracy: 99.67%")
    st.success("F1 Score: 0.9967")
    st.markdown("---")
    st.markdown("""
    ### Notes:
    - The model distinguishes between **ME/CFS**, **Depression**, or **Both**.
    - Evaluation metrics are based on a held-out test dataset.
    """)

# --- Team Members ---
elif menu == "Team Members":
    st.title("Team Members - Group 12")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = lambda filename: os.path.join(base_dir, 'static', 'images', filename)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(image_path("member3.jpg"), width=150)
        st.markdown("**Maheesha Sewmini**  \n*Data Scientist*")
        st.caption("Maheesha specializes in data analytics and visualization.")

    with col2:
        st.image(image_path("HemalMewantha.jpg"), width=150)
        st.markdown("**Hemal Mewantha**  \n*Backend Developer*")
        st.caption("Hemal focuses on API development and scalable backend systems.")

    with col3:
        st.image(image_path("member1.jpg"), width=150)
        st.markdown("**Sanjana Fernando**  \n*ML Engineer*")
        st.caption("Sanjana builds ML models focused on real-time prediction.")

# --- FAQ ---
elif menu == "FAQ":
    st.title("Frequently Asked Questions")

    st.markdown("""
If you have any questions or need further clarification about this tool, our team is here to help.

Patients, researchers, or medical professionals are encouraged to reach out to us.

Use the contact form below, and we will get back to you as soon as possible.
""")

    st.markdown("---")
    st.subheader("Contact Us")

    with st.form("contact_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        message = st.text_area("Message")

        submitted = st.form_submit_button("Send")
        if submitted:
            st.success("Thank you! Your message has been received.")

    st.markdown("""
    **Phone:** +94 765 436 732  
    **Email:** mewanmuna2000@gmail.com  
    **Website:** [www.group12research.org](https://www.group12research.org)
    """)

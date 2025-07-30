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
    
    # List of image paths (put your real image paths here)
    image_folder = "..\\static\\images"
    images = [
        os.path.join(os.path.dirname(__file__), '..', 'static', 'images', 'img1.jpeg'),
        os.path.join(os.path.dirname(__file__), '..', 'static', 'images', 'img2.jpeg'),
        os.path.join(os.path.dirname(__file__), '..', 'static', 'images', 'img3.png'),
    ]


    # Initialize session state
    if "img_index" not in st.session_state:
        st.session_state.img_index = 0
    if "auto_slide" not in st.session_state:
        st.session_state.auto_slide = True

    # Image display
    st.image(images[st.session_state.img_index], use_container_width=True)

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

    # Auto slide logic (simulated refresh)
    async def auto_rotate():
        await asyncio.sleep(5)
        if st.session_state.auto_slide:
            st.session_state.img_index = (st.session_state.img_index + 1) % len(images)
            st.rerun()

    # Run async auto slider
    if st.session_state.auto_slide:
        asyncio.run(auto_rotate())

# --- App ---
elif menu == "App":
    st.title("Predict Diagnosis")
    
    st.write("Please enter the required information below:")

    # Input form
    depression_score = st.number_input("Depression Score (0–27)", min_value=0, max_value=27, help="Enter your PHQ-9 score.")
    pem_present = st.selectbox("Post-Exertional Malaise Present?", ["Yes", "No"], help="Do you experience PEM after physical or mental exertion?")

    if st.button("Predict"):
        # Replace this with actual model inference logic
        input_data={
            "depression_score":depression_score,
            "post_exertional_malaise": pem_present
        }

        ##make a POST request to the backend API
        response=requests.post("http://127.0.0.1:8000/predict",json=input_data)

        ##check if the response is successful
        if response.status_code==200:
            prediction = response.json().get("prediction")
            st.error("Prediction: {prediction}".format(prediction=prediction))
            st.info("Note: This is a research-based tool and **not a substitute for medical diagnosis**.")
        else:
            st.error("Error in prediction. Please try again later.")
    st.markdown("---")
    # Description and usage guidelines
    st.markdown("---")
    st.header("How to Use This App")
    st.markdown("""
        - **Depression Score** is based on the **PHQ-9** questionnaire. Scores typically range:
            - `0–4`: Minimal or no depression  
            - `5–9`: Mild depression  
            - `10–14`: Moderate  
            - `15–27`: Severe  
        - **Post-Exertional Malaise (PEM)** refers to worsening symptoms after exertion and is a key marker for **ME/CFS**.
        - Click **Predict** to classify your condition as likely **Depression**, **ME/CFS**, or **Both** based on input.
        """)
    st.warning("This app is for educational use only. Please consult a medical professional for a real diagnosis.")

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
    ###  Notes:
    - The model is trained to distinguish between **ME/CFS**, **Depression**, or **Both** conditions.
    - Evaluation metrics are based on a held-out test dataset.
    - **Support Vector Classifier** was selected after benchmarking multiple models.
    """)

# --- Team Members ---
elif menu == "Team Members":
    st.title("Team Members-Group 12")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("../static/images/member3.jpg", width=150)
        st.markdown("**Maheesha Sewmini**  \n*Data Scientist*")
        st.caption("Maheesha specializes in data analytics and visualization, delivering insights from complex datasets.")

    with col2:
        st.image("../static/images/HemalMewantha.jpg", width=150)
        st.markdown("**Hemal Mewantha**  \n*Backend Developer*")
        st.caption("Hemal focuses on robust backend systems and API development with expertise in scalable architectures.")

    with col3:
        st.image("../static/images/member1.jpg", width=150)
        st.markdown("**Sanjana Fernando**  \n*ML Engineer*")
        st.caption("Sanjana builds and deploys machine learning models with a focus on real-time prediction systems.")
# --- FAQ ---
elif menu == "FAQ":
    st.title("Frequently Asked Questions")

    st.markdown("""
If you have any questions, concerns, or need further clarification about this tool, our team is here to help.

Patients, researchers, or medical professionals are encouraged to reach out to us for more information or support.  
Feel free to use the contact form below to send us your inquiries, and we will get back to you as soon as possible.
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

import streamlit as st
import time
import pandas as pd
from streamlit_lottie import st_lottie
import google.generativeai as genai
from PIL import Image
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
with open("Animation - 1740761871146.json", "r") as f:
    data_animation = json.load(f)

# Custom Styling
st.markdown("""
    <style>
    .stApp {background-color: #e3f2fd;}
    .stButton button {background-color: #0277bd !important; color: white !important; font-size: 16px;}
    h1, h2, h3 {color: #0277bd;}
    .chat-message {background-color: #f8f9fa; padding: 10px; border-radius: 8px;}
    </style>
""", unsafe_allow_html=True)

# Initialize session state for navigation if not already set
if 'page' not in st.session_state:
    st.session_state.page = "Home"

def navigate_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# ------------------- Home Page -------------------
if st.session_state.page == "Home":
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/3456/3456426.png", width=80)
    with col2:
        st.title("NutriGen: AI-Powered Nutrition Guide")
    
    st.subheader("Welcome to NutriGen 🍏")
    st.write("""Analyze your food intake and receive AI-powered nutritional guidance.
    Click below to explore different features!
    """)
    
    if data_animation:
        st_lottie(data_animation, speed=1, height=300)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📸 Upload Image"):
            navigate_to("Upload Image")
    with col2:
        if st.button("💬 Chatbot"):
            navigate_to("Chatbot")
    with col3:
        if st.button("🍽 Personalized Meal Plan"):
            navigate_to("Personalized Meal Plan")

# ------------------- Image Upload & Analysis -------------------
elif st.session_state.page == "Upload Image":
    st.subheader("📸 Upload a Food Image for Nutrition Analysis")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="📷 Uploaded Image", use_container_width=True)

        if st.button("🔍 Analyze Nutrition"):
            with st.spinner("Analyzing food image... 🍎"):
                try:
                    model = genai.GenerativeModel("gemini-1.5-pro")
                    identify_food_prompt = "Identify the food item in the image."
                    response = model.generate_content([image, identify_food_prompt])
                    
                    if response and response.text:
                        food_name = response.text.strip()
                        st.subheader(f"🍽 Detected Food: {food_name}")

                        nutrition_prompt = f"""
                            Provide a detailed nutritional breakdown per 100g for {food_name}, 
                            categorizing macronutrients (Calories, Carbohydrates, Proteins, Fats) 
                            and micronutrients (Fiber, Vitamins, Minerals).
                        """
                        nutrition_response = model.generate_content(nutrition_prompt)

                        st.subheader("🍎 Nutritional Breakdown")
                        st.markdown(nutrition_response.text if nutrition_response else "⚠ No response received.")
                    else:
                        st.error("⚠ Unable to identify the food item.")
                except Exception as e:
                    st.error(f"⚠ Error analyzing image: {e}")
    if st.button("🔙 Back to Home"):
        navigate_to("Home")

# ------------------- AI Chatbot -------------------
elif st.session_state.page == "Chatbot":
    st.subheader("💬 Ask the Nutrition Chatbot")
    user_question = st.text_input("Type your question about nutrition and diet:")
    model = genai.GenerativeModel("gemini-1.5-pro")
    if user_question:
        chatbot_prompt = f"Please provide a helpful answer to this nutrition-related question: {user_question}"
        chatbot_response = model.generate_content(chatbot_prompt)
        st.write(chatbot_response.text)
    if st.button("🔙 Back to Home"):
        navigate_to("Home")

# ------------------- Personalized Meal Plan -------------------
elif st.session_state.page == "Personalized Meal Plan":
    st.subheader("🍽 Personalized Meal Plan Generator")
    model = genai.GenerativeModel("gemini-1.5-pro")
    
    st.header("👤 User Information")
    age = st.number_input("Enter your age:", min_value=1, max_value=120, value=25)
    activity_level = st.selectbox("Select your activity level:", ["Sedentary", "Lightly active", "Moderately active", "Very active"])
    
    st.header("🍽 Dietary Preferences")
    diet = st.selectbox("Choose your diet:", ["Vegan", "Keto", "Gluten-Free", "Balanced", "Vegetarian"])
    cuisine = st.selectbox("Choose your preferred cuisine:", ["Indian", "Continental", "Mediterranean", "Asian", "Mexican", "American"])
    preferences = st.text_input("Foods you like (comma-separated):")
    allergies = st.text_input("List your allergies (comma-separated):")
    diseases = st.text_input("Enter any diseases/medical conditions (comma-separated):")
    calories = st.slider("🔥 Desired daily calorie intake:", 1000, 5000, 2000, step=100)
    show_procedure = st.checkbox("📚 Show cooking procedure for meals?")
    plan_duration = st.selectbox("Select meal plan duration:", ["1 day", "1 week"])

    if st.button("🍏 Generate Personalized Meal Plan"):
        
        if plan_duration == "1 week":
            prompt = f"""
Create a structured {diet} meal plan with {cuisine} cuisine preferences for a {age}-year-old person with {activity_level} activity level,
consuming around {calories} calories per day.

Include preferred foods {preferences} and exclude foods containing {allergies}. Also, consider dietary restrictions for medical conditions: {diseases}.

For each meal (Breakfast, Lunch, Dinner, Snacks), provide:
- *Macronutrient Breakdown*: Calories, Carbohydrates, Proteins, Fats  
- *Micronutrient Breakdown*: Fiber, Vitamins, Minerals  
- *Reasoning*: Explain why each food is recommended or avoided based on medical conditions.

### *Weekly Meal Plan (Monday-Sunday)*
Provide the response in a *tabular format* with columns for each day (Monday-Sunday) and rows for Breakfast, Lunch, Dinner, and Snack.

| Meal Type  | Monday        | Tuesday       | Wednesday     | Thursday      | Friday        | Saturday      | Sunday        |
|------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|
| Breakfast | Meal & Calories | Meal & Calories | Meal & Calories | Meal & Calories | Meal & Calories | Meal & Calories | Meal & Calories |
| Lunch     | Meal & Calories | Meal & Calories | Meal & Calories | Meal & Calories | Meal & Calories | Meal & Calories | Meal & Calories |
| Dinner    | Meal & Calories | Meal & Calories | Meal & Calories | Meal & Calories | Meal & Calories | Meal & Calories | Meal & Calories |
| Snack     | Meal & Calories | Meal & Calories | Meal & Calories | Meal & Calories | Meal & Calories | Meal & Calories | Meal & Calories |

"""
        elif plan_duration == "1 day":
            prompt = f"""
Create a structured {diet} meal plan with {cuisine} cuisine preferences for a {age}-year-old person with {activity_level} activity level,
consuming around {calories} calories per day.

Include preferred foods {preferences} and exclude foods containing {allergies}. Also, consider dietary restrictions for medical conditions: {diseases}.

For each meal (Breakfast, Lunch, Dinner, Snacks), provide:
- *Macronutrient Breakdown*: Calories, Carbohydrates, Proteins, Fats  
- *Micronutrient Breakdown*: Fiber, Vitamins, Minerals  
- *Reasoning*: Explain why each food is recommended or avoided based on medical conditions.

### *Meal Plan for One Day*
Provide detailed information for each meal, including macronutrients, micronutrients, and reasoning.

*Breakfast:* Meal Name (Calories: X kcal)  
- *Macronutrients:* Carbs: Xg, Proteins: Xg, Fats: Xg  
- *Micronutrients:* Fiber: Xg, Vitamins: X, Minerals: X  
- *Reasoning:* Explanation of why this meal is chosen  

*Lunch:* Meal Name (Calories: X kcal)  
- *Macronutrients:* Carbs: Xg, Proteins: Xg, Fats: Xg  
- *Micronutrients:* Fiber: Xg, Vitamins: X, Minerals: X  
- *Reasoning:* Explanation of why this meal is chosen  

*Dinner:* Meal Name (Calories: X kcal)  
- *Macronutrients:* Carbs: Xg, Proteins: Xg, Fats: Xg  
- *Micronutrients:* Fiber: Xg, Vitamins: X, Minerals: X  
- *Reasoning:* Explanation of why this meal is included  

*Snack:* Meal Name (Calories: X kcal)  
- *Macronutrients:* Carbs: Xg, Proteins: Xg, Fats: Xg  
- *Micronutrients:* Fiber: Xg, Vitamins: X, Minerals: X  
- *Reasoning:* Explanation of why this snack is included  

"""
        if show_procedure:
            prompt += "\nProvide cooking procedures for each meal."

        response = model.generate_content(prompt)
        st.subheader("🍽 Your Personalized Meal Plan")
        st.markdown(response.text if response else "⚠ No response received.", unsafe_allow_html=True)
    if st.button("🔙 Back to Home"):
        navigate_to("Home")

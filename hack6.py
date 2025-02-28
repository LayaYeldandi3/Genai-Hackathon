import streamlit as st
import google.generativeai as genai

# Configure Gemini AI API
API_KEY = "AIzaSyA-bJoQ2OiLMZEshr_h3Cv4-SPrPbzelQQ"
genai.configure(api_key=API_KEY)

st.title("🥗 NutriGen: AI-Powered Nutrition Guide")

# User Inputs
st.header("👤 User Information")
age = st.number_input("Enter your age:", min_value=1, max_value=120, value=25)
activity_level = st.selectbox("Select your activity level:", ["Sedentary", "Lightly active", "Moderately active", "Very active"])

st.header("🍽 Dietary Preferences")
diet = st.selectbox("Choose your diet:", ["Vegan", "Keto", "Gluten-Free", "Balanced"])
cuisine = st.selectbox("Choose your preferred cuisine:", ["Indian", "Continental", "Mediterranean", "Asian", "Mexican", "American"])
preferences = st.text_input("Foods you like (comma-separated):")
ingredients_at_home = st.text_area("Ingredients available at home (comma-separated):")
allergies = st.text_input("List your allergies (comma-separated):")
meal_choice = st.selectbox("Select a specific meal to generate:", ["All", "Breakfast", "Lunch", "Dinner", "Snack"])
calories = st.slider("🔥 Desired daily calorie intake:", 1200, 3000, step=100)
show_procedure = st.checkbox("📖 Show cooking procedure for meals?")

model = genai.GenerativeModel("gemini-1.5-pro")

if st.button("🍏 Generate Personalized Meal Plan"):
    prompt = f"""
    Create a well-structured {diet} meal plan with {cuisine} cuisine preferences for a {age}-year-old person with {activity_level} activity level,
    consuming around {calories} calories per day. 
    The plan should be well-organized into sections for each meal and contain detailed nutritional information.
    Include the following preferred foods: {preferences}.
    Exclude foods containing {allergies}.
    If a preferred food doesn't fit the diet, suggest an alternative.
    Prioritize using the following ingredients available at home: {ingredients_at_home}.
    If certain ingredients are missing for a suggested meal, provide suitable alternatives.
    
    Only include the following meal in the response: {meal_choice} (if "All" is selected, provide all meals).
    
    *Meal Plan Structure:*
    ---
    ### {meal_choice} Meal Plan
    *Meal:* [meal details]
    *Ingredients:*
      - [ingredient 1]
      - [ingredient 2]
    *Calories:* [caloric breakdown]
    
    *Alternative Food Recommendations:*
    - If certain foods are not available or do not fit dietary preferences, provide alternatives.
    
    *Grocery List:*
    - Generate a grocery list based on missing ingredients for the meal plan.
    """
    
    if show_procedure:
        prompt += """
        
        *Cooking Procedure:*
        1. [Step details]
        2. [Step details]
        """
    
    response = model.generate_content(prompt)
    
    st.subheader("🍽 Your Personalized Meal Plan")
    st.markdown(response.text)

# Nutritional Guidance Chatbot
st.subheader("💬 Ask the Nutrition Chatbot")
user_question = st.text_input("Type your question about nutrition and diet:")
if user_question:
    chatbot_prompt = f"Please provide a polite and helpful answer to this nutrition-related question: {user_question}"
    chatbot_response = model.generate_content(chatbot_prompt)
    st.write(chatbot_response.text)
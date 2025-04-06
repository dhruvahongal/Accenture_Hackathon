import streamlit as st
from model import load_customer_data, load_product_data, RecommendationAgent

# Load the data
customer_df = load_customer_data('customer_data_collection.csv')
product_df = load_product_data('product_recommendation_data.csv')

# Create the recommendation engine
recommender = RecommendationAgent(customer_df, product_df)

# Select a customer
customer_ids = customer_df['Customer_ID'].tolist()
selected_id = st.selectbox("Select a Customer ID:", customer_ids)

# Show customer profile
customer = customer_df[customer_df['Customer_ID'] == selected_id].iloc[0]
st.write("### 👤 Customer Profile")
st.write(f"- **Age:** {customer['Age']}")
st.write(f"- **Gender:** {customer['Gender']}")
st.write(f"- **Location:** {customer['Location']}")
st.write(f"- **Browsing History:** {customer['Browsing_History']}")
st.write(f"- **Purchase History:** {customer['Purchase_History']}")

# Recommend products
if st.button("🎯 Get Recommendations"):
    interests = list(set(customer['Browsing_History'] + customer['Purchase_History']))
    st.write("### 🔍 Extracted Interests:")
    st.write(interests)

    recommendations = recommender.recommend_for_customer(selected_id)
    st.write("### 🛒 Recommended Products:")
    st.dataframe(recommendations)

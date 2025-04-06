import pandas as pd
import ast

# Safe literal evaluation function
def safe_literal_eval(val):
    if isinstance(val, str):
        try:
            return ast.literal_eval(val)
        except Exception:
            return val
    return val

# Load customer data
def load_customer_data(path='customer_data_collection.csv'):
    customer_df = pd.read_csv(path)
    
    # Drop unnecessary columns
    if 'Unnamed: 10' in customer_df.columns:
        customer_df.drop(columns=['Unnamed: 10'], inplace=True)

    # Convert stringified lists to actual lists
    customer_df['Browsing_History'] = customer_df['Browsing_History'].apply(safe_literal_eval)
    customer_df['Purchase_History'] = customer_df['Purchase_History'].apply(safe_literal_eval)

    return customer_df

# Load product data
def load_product_data(path='product_recommendation_data.csv'):
    product_df = pd.read_csv(path)

    # Drop unnecessary columns
    for col in ['Unnamed: 13', 'Unnamed: 14']:
        if col in product_df.columns:
            product_df.drop(columns=[col], inplace=True)

    # Convert stringified lists to actual lists
    product_df['Similar_Product_List'] = product_df['Similar_Product_List'].apply(safe_literal_eval)

    return product_df

# Customer agent
class CustomerAgent:
    def __init__(self, customer_row):
        self.customer_id = customer_row['Customer_ID']
        self.age = customer_row['Age']
        self.gender = customer_row['Gender']
        self.location = customer_row['Location']
        self.browsing_history = customer_row['Browsing_History']
        self.purchase_history = customer_row['Purchase_History']
        self.segment = customer_row['Customer_Segment']
        self.avg_order_value = float(customer_row['Avg_Order_Value'])
        self.season = customer_row['Season']
    
    def get_interests(self):
        return list(set(self.browsing_history + self.purchase_history))

# Product agent
class ProductAgent:
    def __init__(self, product_df):
        self.products = product_df

    def filter_by_interest(self, interests, top_n=5):
        filtered = self.products[
            (self.products['Category'].isin(interests)) |
            (self.products['Subcategory'].isin(interests))
        ]
        return filtered.sort_values(by='Probability_of_Recommendation', ascending=False).head(top_n)

# Recommendation agent
class RecommendationAgent:
    def __init__(self, customer_df, product_df):
        self.customer_df = customer_df
        self.product_agent = ProductAgent(product_df)
    
    def recommend_for_customer(self, customer_id, top_n=5):
        customer_row = self.customer_df[self.customer_df['Customer_ID'] == customer_id].iloc[0]
        customer_agent = CustomerAgent(customer_row)
        interests = customer_agent.get_interests()
        return self.product_agent.filter_by_interest(interests, top_n=top_n)

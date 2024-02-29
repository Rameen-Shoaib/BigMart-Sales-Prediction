import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import pickle
import warnings
warnings.filterwarnings('ignore')


def main():
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_csv("Train.csv")
    
    
    # Sidebar for User Input
    st.sidebar.header('User Input Parameters')

    input_features = {}
    
    item_weight_input = st.sidebar.text_input('Enter Item Weight:', value=None, key="item_weight")
    input_features['Item_Weight'] = format(float(item_weight_input), ".6f") if item_weight_input is not None else None
    
    fat_content_mapping = {'Low Fat': 0, 'Regular': 1}
    input_features['Item_Fat_Content'] = st.sidebar.selectbox('Select Item Fat Content:', [''] + list(fat_content_mapping.keys()))
    
    item_visibility_input = st.sidebar.text_input('Enter Item Visibility:', value=None, key="item_visibility")
    input_features['Item_Visibility'] = format(float(item_visibility_input), ".6f") if item_visibility_input is not None else None

    item_mrp_input = st.sidebar.text_input('Enter Item MRP:', value=None, key="item_mrp")
    input_features['Item_MRP'] = format(float(item_mrp_input), ".6f") if item_mrp_input is not None else None

    outlet_size_mapping = {'Small': 2, 'Medium': 1, 'High': 0}
    input_features['Outlet_Size'] = st.sidebar.selectbox('Select Outlet Size:', [''] + list(outlet_size_mapping.keys()))

    location_type_mapping = {'Tier 1': 0, 'Tier 2': 1, 'Tier 3': 2}
    input_features['Outlet_Location_Type'] = st.sidebar.selectbox('Select Outlet Location Type:', [''] + list(location_type_mapping.keys()))

    outlet_type_mapping = {'Grocery Store': 0, 'Supermarket Type1': 1, 'Supermarket Type2': 2, 'Supermarket Type3': 3}
    input_features['Outlet_Type'] = st.sidebar.selectbox('Select Outlet Type:', [''] + list(outlet_type_mapping.keys()))
       
    if all(input_features.values()) and all(input_features.values()):
        if st.button("Predict Sales"):
            try:
                # Convert selected values to their corresponding numerical values
                input_features['Item_Fat_Content'] = fat_content_mapping[input_features['Item_Fat_Content']]
                input_features['Outlet_Size'] = outlet_size_mapping[input_features['Outlet_Size']]
                input_features['Outlet_Location_Type'] = location_type_mapping[input_features['Outlet_Location_Type']]
                input_features['Outlet_Type'] = outlet_type_mapping[input_features['Outlet_Type']]

                # loading the saved model
                model = pickle.load(open('C:/Users/ramee/Documents/FYP/sales_predictor.pkl', 'rb'))
                
                # Arrange the input data as a tuple
                input_data = (
                    input_features['Item_Weight'],
                    input_features['Item_Fat_Content'],
                    input_features['Item_Visibility'],
                    input_features['Item_MRP'],
                    input_features['Outlet_Size'],
                    input_features['Outlet_Location_Type'],
                    input_features['Outlet_Type']
                )
                
                # Convert the input data to a numpy array
                input_data_as_numpy_array = np.asarray(input_data)
                # Reshape the array to be compatible with the model
                input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
                # Make a prediction using the model
                predicted_sales = model.predict(input_data_reshaped)[0]

                # Display the prediction result outside the sidebar
                st.success(f"The predicted Sales is: {predicted_sales:.2f}")
                
                visualize_data(df, input_features)
                
            except Exception as e:
                st.error(f"Error: {e}")
                st.error(f"Input features: {input_features}")
    else:
        st.warning("Please enter all the input features before predicting sales.")


def visualize_data(df, input_features):
    # Chart: Item Weight Distribution
    fig_weight = px.histogram(df, x='Item_Weight', title='Item Weight Distribution')
    st.plotly_chart(fig_weight)

    # Chart: Sales Distribution by Fat Content
    fig_fat_content = px.violin(df, x='Item_Fat_Content', y='Item_Outlet_Sales', title='Sales Distribution by Fat Content')
    st.plotly_chart(fig_fat_content)

    # Chart: Item Visibility Distribution
    fig_visibility = px.histogram(df, x='Item_Visibility', title='Item Visibility Distribution')
    st.plotly_chart(fig_visibility)

    # Chart: MRP vs Sales
    fig_mrp = px.scatter(df, x='Item_MRP', y='Item_Outlet_Sales', title='MRP vs. Sales')
    st.plotly_chart(fig_mrp)

    # Chart: Sales Distribution by Outlet Size
    fig_outlet_size = px.box(df, x='Outlet_Size', y='Item_Outlet_Sales', title='Sales Distribution by Outlet Size')
    st.plotly_chart(fig_outlet_size)

    # Chart: Count of Items by Location Type
    fig_location_type = px.histogram(df, x='Outlet_Location_Type', color='Outlet_Location_Type', title='Count of Items by Location Type')
    st.plotly_chart(fig_location_type)

    # Chart: Sales Distribution by Outlet Type
    fig_outlet_type = px.box(df, x='Outlet_Type', y='Item_Outlet_Sales', title='Sales Distribution by Outlet Type')
    st.plotly_chart(fig_outlet_type)


if __name__ == '__main__':
    main()
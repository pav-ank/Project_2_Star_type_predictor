import streamlit as st
import pandas as pd
from joblib import load
import io
from io import BytesIO
import requests

# Set page configuration for the Streamlit app
st.set_page_config(page_title="Star Type Prediction App", layout="wide")

# Define the base URL for the FastAPI backend
API_URL = "https://star-type-predictor-2wh8.onrender.com/"  # Replace with your actual API URL

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# Add custom CSS for styling, background, and footer
st.markdown(f"""
    <style>
        .stApp {{
            background-image: url("https://www.nasa.gov/wp-content/uploads/2024/05/hubble-hptau-wfc3-1-flat-finalok.jpg");
            background-size: cover;
            background-position: center;
            color: white; /* Set default text color to white */
            margin-bottom: 35px; /* Add margin to prevent overlap with footer */
        }}
        .top-button {{
            font-size: 14px !important;
            padding: 6px 12px !important;
            color: white !important;
            background-color: #4CAF50 !important;
            border: none;
            cursor: pointer;
            margin: 4px;
        }}
        .top-button:hover {{
            background-color: #45a049 !important;
            color: white !important;
            transition: 0.3s;
        }}
        .home-button {{
            font-size: 14px !important;
            padding: 6px 12px !important;
            color: white !important;
            background-color: #007bff !important;
            border: none;
            cursor: pointer;
            margin: 4px;
        }}
        .home-button:hover {{
            background-color: #0056b3 !important;
            color: white !important;
            transition: 0.3s;
        }}
        footer {{
            position: fixed;
            bottom: 0;
            left: 0; /* Align footer to the left */
            width: 100%; /* Cover entire width */
            text-align: left; /* Align text to the left */
            padding: 5px; /* Increase padding */
            font-size: 16px; /* Increase font size */
            color: #FFFF; /* Change text color to black or a lighter color */
            background-color: rgba(0, 0, 0, 0.3); /* Lighten background color */
            box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.3); /* Optional shadow for better separation */
        }}
    </style>
    <footer>
        <center>
            This project is developed by <strong>Pavankumar Megeri</strong> as part of the Machine Learning for Astronomy program by <strong>Spartificial</strong>.
        </center>
    </footer>
""", unsafe_allow_html=True)


# Define the home page content
def home_page():
    """
    Renders the home page of the application, providing an introduction to the project
    and instructions for use.
    """
    st.title("Star Type Prediction App")
    
    # Introduction section
    st.write(""" 
    ### Introduction to Project
This web application is designed to help you predict the type of stars based on their physical parameters. 
Using machine learning models, we analyze key attributes of stars, such as temperature, luminosity, radius, 
and absolute magnitude, to classify them into distinct types. These types include:

- **Brown Dwarfs**: Cool, faint stars that lack the mass to sustain nuclear fusion.
- **Red Dwarfs**: Small, cool stars that are among the most common in the galaxy.
- **White Dwarfs**: Dense remnants of stars that have exhausted their nuclear fuel.
- **Main Sequence Stars**: Stars that are in the main stage of their lifecycle, fusing hydrogen into helium.
- **Hypergiants and Supergiants**: Massive stars with high luminosities, often nearing the end of their lifespans.

Use this app to explore star types based on different physical characteristics!
""")

    # Instructions container
    st.markdown(f"""
    <div style="
        background-color: rgba(200, 200, 200, 0.7); 
        padding: 15px; 
        border-radius: 5px; 
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2); 
        margin-bottom: 20px;
        ">
        <h3 style='color: #000;'>Instructions:</h3>
        <p style='color: #000;'>- Use <strong>Single Prediction</strong> mode to predict the star type for a single set of features.</p>
        <p style='color: #000;'>- Use <strong>Bulk Prediction</strong> mode to upload a CSV file containing star features for batch prediction.</p>
        <p style='color: #000;'>- Make sure the CSV file for <strong>Bulk Prediction</strong> has the following columns:</p>
        <ul style='color: #000;'>
            <li>Temperature (K)</li>
            <li>Luminosity(L/Lo)</li>
            <li>Radius(R/Ro)</li>
            <li>Absolute magnitude(Mv)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


def single_prediction_page():
    """
    Renders the single prediction page, allowing users to input star features
    and receive a prediction on the star type.
    """
    st.title("Single Star Type Prediction")
    st.write("Enter star features to predict its type:")

    # Input fields for star features
    temperature = st.number_input("Temperature (K)", step=1, format="%d", placeholder="Enter temperature in Kelvin", value=None)
    luminosity = st.number_input("Luminosity (L/Lo)", step=0.1, placeholder="Enter luminosity", value=None)
    radius = st.number_input("Radius (R/Ro)", step=0.1, placeholder="Enter radius", value=None)
    absolute_magnitude = st.number_input("Absolute Magnitude (Mv)", step=0.1, placeholder="Enter absolute magnitude", value=None)

    if st.button("Predict"):
        # Ensure all fields are filled before making a prediction
        if None in [temperature, luminosity, radius, absolute_magnitude]:
            st.error("Please fill in all fields.")
            return
        
        # Prepare data for API request
        data = {
            "Temperature (K)": temperature,
            "Luminosity(L/Lo)": luminosity,
            "Radius(R/Ro)": radius,
            "Absolute magnitude(Mv)": absolute_magnitude
        }

        try:
            # Call the API for prediction
            response = requests.post(f"{API_URL}/predict", json=data)
            response.raise_for_status()
            result = response.json()
            
            # Display the prediction results
            st.write(f"**Predicted Star Type**: {result['predicted_type']}")
            st.write(f"**Prediction Probability**: {result['predicted_probability']:.2f}")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")

def bulk_prediction_page():
    """
    Renders the bulk prediction page, allowing users to upload a CSV file
    for batch predictions on star types.
    """
    st.title("Bulk Star Type Prediction")
    st.write("Upload a CSV file with star features to predict types in bulk.")
    st.write(""" 
    The CSV file should contain columns: `Temperature (K)`, `Luminosity(L/Lo)`, `Radius(R/Ro)`, `Absolute magnitude(Mv)`
    
    **In case you don't have the dataset, we provide a sample dataset to try it out.**
    """)
    
    # Button to download a sample dataset
    with open("Sample_dataset.csv", "rb") as sample_file:
        st.download_button(
            label="Download Sample Dataset",
            data=sample_file,
            file_name="Sample_dataset.csv",
            mime="text/csv"
        )
    
    # File upload for CSV
    uploaded_file = st.file_uploader("Upload CSV", type="csv")

    if uploaded_file:
        try:
            # Read the uploaded file to ensure it has the correct columns
            data = pd.read_csv(uploaded_file)
            required_columns = ['Temperature (K)', 'Luminosity(L/Lo)', 'Radius(R/Ro)', 'Absolute magnitude(Mv)']
            
            # Validate that all required columns are present
            if not all(col in data.columns for col in required_columns):
                st.error(f"CSV file must contain the following columns: {required_columns}")
                return
            
            # Prepare the file for the FastAPI request
            files = {"file": ("filename.csv", io.BytesIO(uploaded_file.getvalue()), "text/csv")}
            
            # Call the API for bulk predictions
            response = requests.post(f"{API_URL}/bulk_predict", files=files)
            response.raise_for_status()
            
            # Display predictions received from the API
            prediction_data = pd.read_csv(BytesIO(response.content))
            st.write("### Prediction Results")
            st.dataframe(prediction_data)

            # Provide a download button for the prediction results
            st.download_button(
                label="Download Predictions as CSV",
                data=response.content,
                file_name="predictions.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Top-left Home button and top-right navigation buttons
col1, col2, col3, col4 = st.columns([1, 6, 1, 1])  # Adjust column widths for alignment
with col1:
    if st.button("Home", key="home_button", on_click=lambda: st.session_state.update(page="Home")):
        st.session_state.page = "Home"
with col3:
    if st.button("Single Prediction", key="single_button", on_click=lambda: st.session_state.update(page="Single")):
        st.session_state.page = "Single"
with col4:
    if st.button("Bulk Prediction", key="bulk_button", on_click=lambda: st.session_state.update(page="Bulk")):
        st.session_state.page = "Bulk"

# Display the selected page based on the button click
if st.session_state.page == "Home":
    home_page()
elif st.session_state.page == "Single":
    single_prediction_page()
elif st.session_state.page == "Bulk":
    bulk_prediction_page()

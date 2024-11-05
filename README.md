# Star Type Predictor using Logistic Regression

## To acces the Web app:
click on this --> [Star_Type_Predictor](https://star-type.streamlit.app/)

- This web application allows you to predict the type of stars based on their physical parameters using Machine Learning. You can easily classify stars into different categories using two modes:

- Single Prediction Mode: Predict the type of a single star by inputting its features.
- Bulk Prediction Mode: Predict the types of multiple stars by uploading a CSV file containing star features.

### ⚙️ How to Set Up This Project on Your System
Follow these steps to set up the project locally:

1. Clone the Repository: You can clone the repository using the following command or download it as a ZIP file.
   ```
   git clone https://github.com/pav-ank/Project2-Star_Type_predictor.git
   ```
2. Create a Virtual Environment:
   ```
   python -m venv venv
   ```
3. Activate the Virtual Environment:
    ```
    venv\Scripts\activate
    ```
4. Install the Requirements:
    ```
    python -m pip install -r requirements.txt
    ```
5. Run the Backend: Start the FastAPI backend using Uvicorn:
    ```
    uvicorn backend:app --reload
    ```
6. Run the Frontend: Launch the Streamlit frontend:
    ```
    streamlit run frontend.py
    ```
7. streamlit run frontend.py
   `Open your web browser and go to [your local host server] to start using the application.`
   
### 🔧 Tools Used in This Project
- `FastAPI`: A modern web framework for building APIs with Python 3.6+ based on standard Python type hints. It is fast, efficient, and allows for easy creation of RESTful endpoints with automatic validation and documentation.
- `Streamlit`: An open-source app framework for Machine Learning and Data Science projects that enables you to create beautiful web applications with minimal effort. It allows for interactive visualizations and user input through a simple Python script.
- `Render`: A cloud platform for hosting web applications, including FastAPI apps. It provides easy deployment options, automatic scaling, and is designed to support a wide variety of programming languages and frameworks.
- `Scikit-Learn`: A powerful and user-friendly library for machine learning in Python. It provides simple and efficient tools for data mining and data analysis, including functions for classification, regression, clustering, and dimensionality reduction.
- `NumPy`: A fundamental package for numerical computing in Python, offering support for large, multi-dimensional arrays and matrices, along with a collection of mathematical functions to operate on these arrays.
- `Matplotlib`: A comprehensive library for creating static, animated, and interactive visualizations in Python. It is widely used for plotting data in various formats, allowing users to visualize patterns and trends effectively.
- `Pandas`: A versatile data manipulation and analysis library for Python that provides data structures like DataFrames for efficiently handling and analyzing large datasets. It offers a variety of functions for data cleaning, transformation, and export.

### 💖 Acknowledgments
A special thank you to the authors and contributors of the libraries and tools used in this project. Your work has made this application possible!

### 🚀 Future Enhancements
- Model Improvement: Explore advanced machine learning models to enhance prediction accuracy.
- User Authentication: Implement user accounts to save past predictions and settings.
- Mobile Responsiveness: Ensure the application is fully responsive for mobile users.
  

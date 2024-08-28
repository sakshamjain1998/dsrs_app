import streamlit as st
import json
import os
import time
from datetime import datetime
from PIL import Image

# Path to the logo image
logo_path = "/content/logo.png"  # Update this path to the location of your logo file

# Function to display the logo
def display_logo():
    if os.path.exists(logo_path):
        st.image(logo_path, use_column_width=False, width=120)  # Set width for smaller logo
    else:
        st.error(f"Logo file not found at {logo_path}")

# Function to display the video
def play_video(video_path):
    st.video(video_path)

# Define date range constraints
MIN_DATE = datetime.strptime("01-2014", "%m-%Y")
MAX_DATE = datetime.strptime("01-2024", "%m-%Y")

# Style Enhancements
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 12px;
        padding: 10px 24px;
        font-size: 16px;
    }
    .stTextInput>div>div>input {
        padding: 10px;
    }
    .stProgress>div>div>div {
        background-color: #4CAF50;
    }
    .stAlert {
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Page 1: Form Input
if 'page' not in st.session_state:
    st.session_state.page = 'input'

if st.session_state.page == 'input':
    # Display the logo at the top of the page
    display_logo()

    st.title("🛰️ DSRS: Analysis of Nighttime Satellite Images")

    st.write("Welcome to the DSRS tool! Please enter the required details below to analyze nighttime satellite images of a specific area over a given time period.")

    # Coordinate Input
    st.header("🌍 Enter the coordinates of the location")
    col1, col2 = st.columns(2)
    with col1:
        latitude = st.text_input("Latitude")
    with col2:
        longitude = st.text_input("Longitude")

    # Area Input
    st.header("📏 Enter the dimensions of the area to be extracted")
    col3, col4 = st.columns(2)
    with col3:
        length = st.text_input("Length")
    with col4:
        breadth = st.text_input("Breadth")

    # Time Period Input
    st.header("📅 Enter the time period")
    col5, col6 = st.columns(2)
    with col5:
        from_date = st.text_input("From (MM-YYYY)", placeholder="e.g., 12-2016")
    with col6:
        to_date = st.text_input("To (MM-YYYY)", placeholder="e.g., 08-2024")

    # Validate inputs
    valid_inputs = True
    input_data = {}
    
    # Coordinate Input Validation
    try:
        if latitude:
            latitude = float(latitude)
            if -90 <= latitude <= 90:
                input_data['latitude'] = latitude
            else:
                st.error("Latitude must be between -90 and 90.")
                valid_inputs = False
        if longitude:
            longitude = float(longitude)
            if -180 <= longitude <= 180:
                input_data['longitude'] = longitude
            else:
                st.error("Longitude must be between -180 and 180.")
                valid_inputs = False
    except ValueError:
        st.error("Latitude and Longitude must be numerical values.")
        valid_inputs = False

    # Area Input Validation
    try:
        if length:
            length = float(length)
            if length > 0:
                input_data['length'] = length
            else:
                st.error("Length must be a positive numerical value.")
                valid_inputs = False
        if breadth:
            breadth = float(breadth)
            if breadth > 0:
                input_data['breadth'] = breadth
            else:
                st.error("Breadth must be a positive numerical value.")
                valid_inputs = False
    except ValueError:
        st.error("Length and Breadth must be numerical values.")
        valid_inputs = False

    # Time Period Input Validation
    try:
        if from_date:
            from_date = datetime.strptime(from_date, "%m-%Y")
            if MIN_DATE <= from_date <= MAX_DATE:
                input_data['from_date'] = from_date.strftime("%m-%Y")
            else:
                st.error("From date must be between 01-2014 and 01-2024.")
                valid_inputs = False
        if to_date:
            to_date = datetime.strptime(to_date, "%m-%Y")
            if MIN_DATE <= to_date <= MAX_DATE:
                if from_date and to_date < from_date:
                    st.error("End date cannot be before the start date.")
                    valid_inputs = False
                input_data['to_date'] = to_date.strftime("%m-%Y")
            else:
                st.error("To date must be between 01-2014 and 01-2024.")
                valid_inputs = False
    except ValueError:
        st.error("Dates must be in the format MM-YYYY.")
        valid_inputs = False

    # Buttons for Submit and View Results
    col7, col8 = st.columns([1, 1])  # Adjust column widths if needed

    with col7:
        if valid_inputs:
            if st.button('Submit'):
                # Show a 35-second progress bar after submission
                progress_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.35)  # Simulate a 35-second delay with incremental updates
                    progress_bar.progress(percent_complete + 1)

                # Save JSON data to a file
                file_name = "user_data.json"
                with open(file_name, "w") as f:
                    json.dump(input_data, f, indent=4)
                st.success(f"Data saved to {file_name}")
    
    with col8:
        if valid_inputs:
            if st.button('View Results'):
                # Transition to results page
                st.session_state.page = 'results'


elif st.session_state.page == 'results':
    # Display the logo at the top of the page
    display_logo()

    st.title("📊 DSRS - Analysis Results")

    # Introduction to the results page
    st.write("Here are the results of your analysis. You can view the generated images and videos below.")

    # Display the image and video section with improved layout
  

    # Set dimensions for the image and video to ensure uniformity
    image_width = 700  # Define a fixed width for both the image and video
    image_height = 400  # Define a fixed height for both the image and video

    # Display the graph image
    image_path = "/content/graph.png"
    if os.path.exists(image_path):
        image = Image.open(image_path)
        st.image(image, width=image_width)
    else:
        st.error(f"Image file not found at {image_path}")

    # Display the video directly under the graph
    video_path = "/content/output_video.mp4"
    if os.path.exists(video_path):
        st.video(video_path, start_time=0)
    else:
        st.error(f"Video file not found at {video_path}")

    st.markdown("---")

    # Button to go back to the input page
    if st.button('🔙 Back to Input Page'):
        st.session_state.page = 'input'

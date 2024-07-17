import pandas as pd
from sklearn.preprocessing import LabelEncoder
import streamlit as st

# Load the model
model = pd.read_pickle("xgboost_model.pkl")  # Replace with your model filename

# Define features for prediction
features = [
    'Absolute_throttle_position',
    'Engine_speed',
    'Current_Gear',
    'Steering_wheel_angle',
    'Steering_wheel_speed',
    'Acceleration_speed_-_Longitudinal',
    'Calculated_LOAD_value',
    'Engine_coolant_temperature',
    'Activation_of_Air_compressor',
    'Intake_air_pressure',
    'Engine_torque',
    'Vehicle_speed',
    'Accelerator_Pedal_value',
    'Indication_of_brake_switch_ON/OFF'
]

# Create a title and sections for input fields
st.title("Fuel Consumption Prediction")
st.header("Enter Vehicle Parameters:")

with st.expander("Engine Parameters"):
    user_input = {}
    user_input['Engine_speed'] = st.slider('Engine Speed (RPM)', 0, 6206, value=None)
    user_input['Engine_coolant_temperature'] = st.slider('Engine Coolant Temperature (°C)', -40, 95, value=None)
    user_input['Engine_torque'] = st.slider('Engine Torque (Nm)', 0, 84, value=None)

with st.expander("Transmission Parameters"):
    user_input['Current_Gear'] = st.selectbox('Current Gear', range(15), index=None)
    user_input['Acceleration_speed_-_Longitudinal'] = st.slider('Acceleration Speed - Longitudinal (M/Sec2)', -10, 8, value=None)

with st.expander("Steering Parameters"):
    user_input['Steering_wheel_angle'] = st.slider('Steering Wheel Angle (Degree)', -517, 530, value=None)
    user_input['Steering_wheel_speed'] = st.slider('Steering Wheel Speed (Rad./sec)', 0, 632, value=None)

with st.expander("Other Parameters"):
    user_input['Absolute_throttle_position'] = st.slider('Absolute Throttle Position (MCC/sec)', 13, 84, value=None)
    user_input['Calculated_LOAD_value'] = st.slider('Calculated LOAD Value (Nm)', 0, 98, value=None)
    user_input['Activation_of_Air_compressor'] = st.selectbox('Activation of Air Compressor (0 for OFF, 1 for ON)', [0, 1], index=None)
    user_input['Intake_air_pressure'] = st.slider('Intake Air Pressure (mbar)', 0, 177, value=None)
    user_input['Vehicle_speed'] = st.slider('Vehicle Speed (Km/hr)', 0, 129, value=None)
    user_input['Accelerator_Pedal_value'] = st.slider('Accelerator Pedal Value', 0, 99, value=None)
    user_input['Indication_of_brake_switch_ON/OFF'] = st.selectbox('Indication of Brake Switch (0 for OFF, 1 for ON)', [0, 1], index=None)


# Create a button to predict fuel consumption
if st.button("Predict Fuel Consumption"):
    # Check if any of the input fields are empty
    if any(val is None for val in user_input.values()):
        st.warning("Please fill the input fields before making a prediction.")
    else:
        # Reorder the input data to match the feature names in the model
        input_data = [user_input[feature] for feature in features]

        # Create a Pandas DataFrame with the reordered input data
        df = pd.DataFrame([input_data], columns=features)

        # Make prediction
        prediction = model.predict(df)[0]

        # Display prediction
        st.header("Predicted Fuel Consumption:")
        st.write("Fuel Consumption in (Millilitres per Cylinder per Cycle):", prediction)


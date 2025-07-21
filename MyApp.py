import streamlit as st
import pandas as pd
import pickle

# Load trained model, label encoders, and feature columns
with open("laptop_model.pkl", "rb") as f:
    rf_model = pickle.load(f)
with open("label_encoders.pkl", "rb") as f:
    label_encoders = pickle.load(f)
with open("feature_columns.pkl", "rb") as f:
    feature_columns = pickle.load(f)
with open("laptop_model_class.pkl", "rb") as f:
    class_model = pickle.load(f)
with open("label_encoders_class.pkl", "rb") as f:
    label_encoders_class = pickle.load(f)
with open("feature_columns_class.pkl", "rb") as f:
    feature_columns_class = pickle.load(f)
# Define categorical columns
categorical_cols = [
    'Company', 'TypeName', 'OpSys', 'Touchscreen', 
    'IPSpanel', 'RetinaDisplay', 'CPU_brand', 'PrimaryStorageType', 
    'SecondaryStorageType', 'GPU_company', 'Screen'
]

# Load the dataset
df = pd.read_csv("preprosseced.csv")

# Extract unique values for each form field
companies = sorted(df['Company'].unique().tolist())
types = sorted(df['TypeName'].unique().tolist())
rams = sorted(df['Ram'].unique().tolist())
opsys = sorted(df['OpSys'].unique().tolist())
touchscreens = sorted(df['Touchscreen'].unique().tolist())
ipspanels = sorted(df['IPSpanel'].unique().tolist())
retina_displays = sorted(df['RetinaDisplay'].unique().tolist())
screens = sorted(df['Screen'].unique().tolist())
cpu_brands = sorted(df['CPU_brand'].unique().tolist())
primary_storage_types = sorted(df['PrimaryStorageType'].unique().tolist())
secondary_storage_types = sorted(df['SecondaryStorageType'].unique().tolist())
gpu_companies = sorted(df['GPU_company'].unique().tolist())
def validate_specs(specs):
    warnings = []
    
    # Screen resolution vs description
    if specs.get('ScreenW') == 3840 and specs.get('ScreenH') == 2160 and specs.get('Screen') != '4K':
        warnings.append("⚠️ 3840x2160 is typically '4K' but screen description differs")
    elif specs.get('ScreenW') == 2560 and specs.get('ScreenH') == 1600 and specs.get('Screen') != 'Retina':
        warnings.append("⚠️ 2560x1600 is common for Retina displays but not marked as such")
    
    # Refresh rate sanity
    if specs.get('ScreenH') >= 1440 and specs.get('RefreshRate', 60) < 120:
        warnings.append("⚠️ High-resolution screens usually have 120Hz+ refresh rates")
    
    # ===== Brand-Specific Checks =====
    # Apple
    if specs.get('Company') == 'Apple':
        if specs.get('RetinaDisplay') != 'Yes':
            warnings.append("🍏 Apple devices almost always have Retina displays")
        if specs.get('OpSys') != 'macOS':  # Changed from checking for Windows
            warnings.append("🍏 Apple laptops should run macOS, not other operating systems")
        if specs.get('GPU_company') not in ['Apple', 'AMD']:
            warnings.append("🍏 Modern Apple devices use Apple/AMD GPUs (not Intel/NVIDIA)")
    
    # Gaming brands (Alienware, ASUS ROG, etc.)
    elif specs.get('Company') in ['Alienware', 'ASUS'] and 'ROG' in specs.get('TypeName', ''):
        if specs.get('GPU_company') == 'Intel':
            warnings.append("🎮 Gaming laptops typically use NVIDIA/AMD GPUs, not Intel")
        if specs.get('Weight', 0) < 2.0:
            warnings.append("🎮 Gaming laptops usually weigh >2kg due to cooling systems")
    
    # ===== CPU Validation =====
    if specs.get('CPU_brand') == 'Intel':
        if not specs.get('CPU_model_and_generation', '').lower().startswith(('i3','i5','i7','i9')):
            warnings.append("🔵 Intel CPUs should start with i3/i5/i7/i9")
        if specs.get('CPU_base_clock_speed', 0) < 1.0:
            warnings.append("🔵 Intel CPU clock speed unusually low (<1.0GHz)")
    
    elif specs.get('CPU_brand') == 'AMD':
        if not specs.get('CPU_model_and_generation', '').startswith(('Ryzen 3','Ryzen 5','Ryzen 7','Ryzen 9')):
            warnings.append("🔴 AMD CPUs should start with Ryzen 3/5/7/9")
        if specs.get('CPU_base_clock_speed', 0) < 2.0:
            warnings.append("🔴 AMD Ryzen base clock usually starts at 2.0GHz+")
    
    # ===== GPU Validation =====
    if specs.get('GPU_company') == 'Intel':
        if not specs.get('GPU_model', '').startswith(('UHD','Iris Xe')):
            warnings.append("🔷 Intel GPUs usually start with 'UHD' or 'Iris Xe'")
    
    elif specs.get('GPU_company') == 'NVIDIA':
        if not any(word in specs.get('GPU_model','') for word in ['RTX','GTX','MX']):
            warnings.append("🟢 NVIDIA GPUs typically include RTX/GTX/MX in model name")
        if 'RTX' in specs.get('GPU_model','') and specs.get('VRAM',0) < 4:
            warnings.append("🟢 RTX GPUs usually have 4GB+ VRAM")
    
    # ===== Storage Validation =====
    # SSD size sanity
    if specs.get('PrimaryStorageType') == 'SSD' and specs.get('PrimaryStorage',0) < 128:
        warnings.append("💾 SSDs below 128GB are uncommon in modern laptops")
    
    # HDD in premium laptops
    if specs.get('PrimaryStorageType') == 'HDD' and specs.get('Company') in ['Apple', 'Dell XPS']:
        warnings.append("💾 Premium laptops rarely use HDDs as primary storage")
    
    # Secondary storage conflicts
    if specs.get('SecondaryStorageType') == 'No' and specs.get('SecondaryStorage',0) > 0:
        warnings.append("💾 Secondary storage marked 'No' but size >0")
    elif specs.get('SecondaryStorageType') != 'No' and specs.get('SecondaryStorage',0) == 0:
        warnings.append("💾 Secondary storage type specified but size is 0")
    
    # ===== Physical Design Checks =====
    # Weight vs screen size
    if specs.get('Inches',0) >= 17 and specs.get('Weight',0) < 2.5:
        warnings.append("🏋️ Large screens (17+ inches) usually weigh more than 2.5kg")
    
    # Ultrabook light weight check
    if 'Ultrabook' in specs.get('TypeName','') and specs.get('Weight',0) > 1.5:
        warnings.append("📱 Ultrabooks typically weigh under 1.5kg")
    
    # Touchscreen without IPS
    if specs.get('Touchscreen') == 'Yes' and specs.get('IPSpanel') == 'No':
        warnings.append("🖱️ Touchscreens usually have IPS panels for better viewing angles")
    
    return warnings

def predict_laptop_price(model, specs, encoders, feature_cols):
    # Create input DataFrame
    input_df = pd.DataFrame([specs])
    
    # Encode categorical variables - ensure ALL categorical columns are encoded
    for col in categorical_cols:
        if col in input_df.columns and col in encoders:
            # Handle missing/unknown categories safely
            try:
                input_df[col] = encoders[col].transform([str(specs[col])])[0]
            except ValueError:
                # Use most frequent category as fallback
                fallback = encoders[col].classes_[0]
                st.warning(f"Unknown value '{specs[col]}' for '{col}'. Using '{fallback}' instead.")
                input_df[col] = encoders[col].transform([fallback])[0]
    
    # Ensure all model-expected features are present
    for col in feature_cols:
        if col not in input_df.columns and col not in ['Resolution', 'Unnamed: 0']:
            input_df[col] = 0  # Default value
    
    # Select only the columns the model expects
    model_features = [col for col in feature_cols if col not in ['Resolution', 'Unnamed: 0']]
    input_df = input_df[model_features]
    
    # Convert all columns to numeric (in case any strings slipped through)
    input_df = input_df.apply(pd.to_numeric, errors='coerce').fillna(0)
    
    return model.predict(input_df)[0]
# === Streamlit Interface ===
st.title("💻 Laptop Price Predictor")

with st.form("laptop_form"):
    st.subheader("Enter Laptop Specifications")

    col1, col2 = st.columns(2)
    with col1:
        Company = st.selectbox("Company", companies)
        TypeName = st.selectbox("Type", types)
        Inches = st.number_input("Screen Size (inches)", min_value=10.0, max_value=18.0, value=15.6)
        Ram = st.selectbox("RAM (GB)", rams)
        OpSys = st.selectbox("Operating System", opsys)
        Weight = st.number_input("Weight (kg)", min_value=0.5, max_value=5.0, value=2.0)
        Touchscreen = st.selectbox("Touchscreen", ['Yes', 'No'])
        IPSpanel = st.selectbox("IPS Panel", ['Yes', 'No'])
        RetinaDisplay = st.selectbox("Retina Display", ['Yes', 'No'])

    with col2:
        Screen = st.selectbox("Screen Description", screens)
        ScreenW = st.number_input("Screen Width", 800, 4000, 1920)
        ScreenH = st.number_input("Screen Height", 600, 3000, 1080)
        CPU_brand = st.selectbox("CPU Brand", cpu_brands)
        CPU_model_and_generation = st.text_input("CPU Model and Generation", 'i5 8th Gen')
        CPU_base_clock_speed = st.number_input("CPU Base Clock Speed (GHz)", 1.0, 5.0, 2.0)
        PrimaryStorage = st.number_input("Primary Storage (GB)", 0, 2048, 512)
        PrimaryStorageType = st.selectbox("Primary Storage Type", primary_storage_types)
        SecondaryStorage = st.number_input("Secondary Storage (GB)", 0, 2048, 0)
        SecondaryStorageType = st.selectbox("Secondary Storage Type", secondary_storage_types)
        GPU_company = st.selectbox("GPU Company", gpu_companies)
        GPU_model = st.text_input("GPU Model", 'UHD Graphics 620')

    submitted = st.form_submit_button("Predict")
if submitted:
    specs = {
        'Company': Company,
        'TypeName': TypeName,
        'Inches': Inches,
        'Ram': Ram,
        'OpSys': OpSys,
        'Weight': Weight,
        'Screen': Screen,
        'ScreenW': ScreenW,
        'ScreenH': ScreenH,
        'Touchscreen': Touchscreen,
        'IPSpanel': IPSpanel,
        'RetinaDisplay': RetinaDisplay,
        'CPU_brand': CPU_brand,
        'CPU_model_and_generation': CPU_model_and_generation,
        'CPU_base_clock_speed': CPU_base_clock_speed,
        'PrimaryStorage': PrimaryStorage,
        'PrimaryStorageType': PrimaryStorageType,
        'SecondaryStorage': SecondaryStorage,
        'SecondaryStorageType': SecondaryStorageType,
        'GPU_company': GPU_company,
        'GPU_model': GPU_model
    }

    warnings = validate_specs(specs)
    if warnings:
        st.warning("Some values seem unusual:")
        for w in warnings:
            st.write("•", w)

    try:
        # Predict price
        price = predict_laptop_price(rf_model, specs, label_encoders, feature_columns)

        # Predict class number
        class_num = predict_laptop_price(class_model, specs, label_encoders_class, feature_columns_class)

        # Map class numbers to names
        if class_num == 0:
            class_name = "Programming"
        elif class_num == 1:
            class_name = "School/University"
        else:
            class_name = "Business"

        # Display results
        st.success(f"💰 Estimated Price: €{price:.2f}")
        st.success(f"💰 Recommended Use: {class_name}")

    except Exception as e:
        st.error(f"Prediction failed: {str(e)}")

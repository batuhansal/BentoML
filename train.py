import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
import bentoml
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

# 1. Load Data
try:
    df = pd.read_csv('Social_Network_Ads.csv')
except FileNotFoundError:
    print("Error: Social_Network_Ads.csv not found. Please download it to this folder.")
    exit()

# 2. Manual Preprocessing
# Map Gender to 1 (Male) and 0 (Female)
df['Gender'] = df['Gender'].map({'Male': 1, 'Female': 0})

X = df[['Gender', 'Age', 'EstimatedSalary']].values.astype(np.float32)
y = df['Purchased'].values

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

# Scale
sc = StandardScaler()
X_train_scaled = sc.fit_transform(X_train)

# 3. Train Model
print("Training model...")
classifier = SVC(kernel='linear', random_state=0)
classifier.fit(X_train_scaled, y_train)

# 4. Convert to ONNX
print("Converting to ONNX...")
initial_type = [('float_input', FloatTensorType([None, 3]))]
onnx_model = convert_sklearn(classifier, initial_types=initial_type)

# 5. Save to BentoML
bentoml.onnx.save_model(
    "social_ads_onnx", 
    onnx_model,
    custom_objects={"scaler": sc} 
)

print("Success! Model saved to BentoML store.")
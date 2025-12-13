import bentoml
import numpy as np
import onnxruntime

# We use the new @bentoml.service decorator (Class-based API)
@bentoml.service(name="onnx_ads_service")
class AdsService:
    def __init__(self):
        # 1. Get the model from the BentoML store
        # We use standard 'bentoml.models.get' to avoid deprecation warnings
        self.model_ref = bentoml.models.get("social_ads_onnx:latest")
        
        # 2. Load the Scaler
        # We saved it as a custom object in train.py
        self.scaler = self.model_ref.custom_objects['scaler']
        
        # 3. Load the ONNX Runtime Session
        # We find the 'model.onnx' file inside the BentoML saved model folder
        model_path = self.model_ref.path_of("saved_model.onnx")
        self.session = onnxruntime.InferenceSession(model_path)

    # We define the API endpoint using the decorator
    @bentoml.api
    def predict(self, input_data: dict) -> dict:
        # Example Input: {"Gender": "Male", "Age": 30, "Salary": 87000}
        
        # A. Preprocessing
        gender_map = 1 if input_data.get("Gender") == "Male" else 0
        age = float(input_data.get("Age"))
        salary = float(input_data.get("Salary"))
        
        # Create vector [[1.0, 30.0, 87000.0]]
        raw_input = np.array([[gender_map, age, salary]], dtype=np.float32)
        
        # Scale it using the saved scaler
        scaled_input = self.scaler.transform(raw_input)
        
        # B. ONNX Inference
        # We run the session directly. 
        # The input name 'float_input' matches what we defined in train.py
        input_name = self.session.get_inputs()[0].name
        result = self.session.run(None, {input_name: scaled_input})
        
        prediction = int(result[0][0])
        
        # C. Response
        return {
            "prediction": prediction,
            "result": "Will Purchase" if prediction == 1 else "No Purchase",
            "backend": "ONNX Runtime (v1.4 Class-based)"
        }
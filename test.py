import joblib
bundle = joblib.load("model/deployment_gate_model.joblib")
print(type(bundle))
print(bundle)

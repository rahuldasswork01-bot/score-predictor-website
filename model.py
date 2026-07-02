import numpy as np
from sklearn.linear_model import LinearRegression
import pickle

# Our training data
hours_studied = np.array([1,2,3,4,5,6,7,8,9,10]).reshape(-1,1)
exam_scores = np.array([35,45,50,60,65,70,78,85,90,95])

# Train the model
model = LinearRegression()
model.fit(hours_studied, exam_scores)

# Save the model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model saved successfully!")
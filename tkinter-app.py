import tkinter as tk
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

# Load the model
model = load_model("model/")
# Load the tokenizer using pickle
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

labels = {'anger': 0,
          'hate': 6,
          'empty': 2,
          'sadness': 10,
          'neutral': 8,
          'worry': 12,
          'relief': 9,
          'happiness': 5,
          'surprise': 11,
          'boredom': 1,
          'enthusiasm': 3,
          'fun': 4,
          'love': 7}

def predict_emotion(sentence, model):
    maxlen = 178
    sequences = tokenizer.texts_to_sequences([sentence])
  
    padded = pad_sequences(sequences, maxlen=maxlen, padding='post', truncating='post')
    probabilities = model.predict(padded, verbose=0)
    predicted_class_index = np.argmax(probabilities)

    predicted_class_probability = probabilities[0][predicted_class_index]
    formatted_probability = "{:.2f}".format(predicted_class_probability*100)
    predicted_emotion = list(labels.keys())[list(labels.values()).index(predicted_class_index)]
  
    return predicted_emotion, formatted_probability

# Create a function to handle button click
def on_submit():
    sentence = entry.get()
    input_label.config(text="Entered Sentence: " + sentence, fg="blue")
    predicted_emotion, probability = predict_emotion(sentence, model)
    result_label.config(text="Predicted Emotion: " + predicted_emotion, font=("Arial", 14), fg="red")
    probability_label.config(text="Probability: " + probability + "%", font=("Arial", 14), fg="green")

# Create the main window
window = tk.Tk()
window.title("Emotion Predictor")
window.configure(bg="#1E1E1E")

# Description label
description_label = tk.Label(window, text="Enter a sentence to predict its emotion:", font=("Arial", 16), fg="#C5C5C5", bg="#1E1E1E")
description_label.pack(pady=10)

# Create and place widgets
entry_frame = tk.Frame(window, bg="#1E1E1E")
entry_frame.pack()
entry_label = tk.Label(entry_frame, text=">>", font=("Arial", 14), fg="#C5C5C5", bg="#1E1E1E")
entry_label.pack(side="left")
entry = tk.Entry(entry_frame, width=50, font=("Arial", 14), bg="#3A3A3A", fg="#C5C5C5")
entry.pack(side="left", padx=5)
submit_button = tk.Button(window, text="Predict", command=on_submit, font=("Arial", 14), bg="#3A3A3A", fg="#C5C5C5")
submit_button.pack(pady=5)
input_label = tk.Label(window, text="", font=("Arial", 12), fg="#C5C5C5", bg="#1E1E1E")
input_label.pack(pady=5)
result_label = tk.Label(window, text="", font=("Arial", 14), fg="#C5C5C5", bg="#1E1E1E")
result_label.pack(pady=5)
probability_label = tk.Label(window, text="", font=("Arial", 14), fg="#C5C5C5", bg="#1E1E1E")
probability_label.pack(pady=5)

# Start the GUI event loop
window.mainloop()
from flask import Flask, request, jsonify, render_template
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    sentence = data['sentence']
    predicted_emotion, probability = predict_emotion(sentence, model)
    return jsonify({"emotion": predicted_emotion, "probability": probability})

if __name__ == '__main__':
    app.run(debug=True)

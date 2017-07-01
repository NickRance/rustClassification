from keras.models import model_from_json, load_model
import json

MODEL_FILENAME = "my_model.h5"
#
# with open(MODEL_FILENAME) as data_file:
#     #data =json.load(data_file)
#     data = data_file.readlines()
# data_file.close()
# model = model_from_json(data)
model = load_model(MODEL_FILENAME)
print(model)
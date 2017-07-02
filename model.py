'''This script goes along the blog post
"Building powerful image classification models using very little data"
from blog.keras.io.
It uses data that can be downloaded at:
https://www.kaggle.com/c/dogs-vs-cats/data
In our setup, we:
- created a data/ folder
- created train/ and validation/ subfolders inside data/
- created cats/ and dogs/ subfolders inside train/ and validation/
- put the cat pictures index 0-999 in data/train/cats
- put the cat pictures index 1000-1400 in data/validation/cats
- put the dogs pictures index 12500-13499 in data/train/dogs
- put the dog pictures index 13500-13900 in data/validation/dogs
So that we have 1000 training examples for each class, and 400 validation examples for each class.
In summary, this is our directory structure:
```
data/
    train/
        dogs/
            dog001.jpg
            dog002.jpg
            ...
        cats/
            cat001.jpg
            cat002.jpg
            ...
    validation/
        dogs/
            dog001.jpg
            dog002.jpg
            ...
        cats/
            cat001.jpg
            cat002.jpg
            ...
```
'''

from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
import json, pprint, os

# dimensions of our images.
img_width, img_height = 150, 150

train_data_dir = 'data/train'
validation_data_dir = 'data/validation'
predict_data_dir = 'data/predict'
MODEL_FILENAME = "my_model.h5"

nb_train_samples = 1000
nb_validation_samples = 500
epochs = 10 #50 by default
batch_size = 32 #16 by default

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)



# this is the augmentation configuration we will use for training
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

# this is the augmentation configuration we will use for testing:
# only rescaling
test_datagen = ImageDataGenerator(rescale=1. / 255)

predict_generator = test_datagen.flow_from_directory(
		predict_data_dir,
		target_size=(img_width, img_height),
		batch_size=batch_size,
		class_mode='binary')

def retrain():
	model = Sequential()
	model.add(Conv2D(32, (3, 3), input_shape=input_shape))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))

	model.add(Conv2D(32, (3, 3)))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))

	model.add(Conv2D(64, (3, 3)))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))

	model.add(Flatten())
	model.add(Dense(64))
	model.add(Activation('relu'))
	model.add(Dropout(0.5))
	model.add(Dense(1))
	model.add(Activation('sigmoid'))

	model.compile(loss='binary_crossentropy',
				  optimizer='rmsprop',
				  metrics=['accuracy'])

	train_generator = train_datagen.flow_from_directory(
		train_data_dir,
		target_size=(img_width, img_height),
		batch_size=batch_size,
		class_mode='binary')


	validation_generator = test_datagen.flow_from_directory(
		validation_data_dir,
		target_size=(img_width, img_height),
		batch_size=batch_size,
		class_mode='binary')

	model.fit_generator(
		train_generator,
		steps_per_epoch=nb_train_samples // batch_size,
		epochs=epochs,
		validation_data=validation_generator,
		validation_steps=nb_validation_samples // batch_size)
	return (model)


def modelFromFile():
	model = load_model(MODEL_FILENAME)
	return(model)

def makePredictions(model):

	#print(predict_generator.filenames)

	#Steps is the number of iterations needed to generate output
	predictions = model.predict_generator(
		generator=predict_generator,
		steps=500,
		verbose=True
	)
	return(predictions)


def saveModel(model):
	model.save_weights('first_try.h5')
	model.save("my_model.h5")


model2 = modelFromFile()
# model2 = retrain()
# saveModel(model2)
predictions = makePredictions(model2)
#rounded = [round(x[0]) for x in predictions]
falseNegativeCount = 0
trueNegativeCount = 0
truePositiveCount=0
falsePositiveCount = 0
for x in range(0,len(predictions)):
	try:
		rounded = round(predictions[x][0])
		#print("Predictions[x]: " + str(rounded))
		# print("Predictions[x]: " + str(predictions[x]))
		#1 is rust, 0 is non-rust
		if rounded == 1 and "non-rust" in predict_generator.filenames[x]:
			print("False Positive: Filename: %s Prediction: %i "%(predict_generator.filenames[x],rounded))
			falsePositiveCount+=1
		elif rounded == 1 and "non-rust" not in predict_generator.filenames[x]:
			print("True Positive: Filename: %s Prediction: %i "%(predict_generator.filenames[x],rounded))
			truePositiveCount +=1
		elif rounded == 0 and "non-rust" not in predict_generator.filenames[x]:
			print("False Negative: Filename: %s Prediction: %i "%(predict_generator.filenames[x],rounded))
			falseNegativeCount +=1
		elif rounded == 0 and "non-rust" in predict_generator.filenames[x]:
			print("True Negative: Filename: %s Prediction: %i "%(predict_generator.filenames[x],rounded))
			trueNegativeCount +=1
	except IndexError:
		pass
NUMBER_OF_RUST_IMAGES = len(os.listdir('data/predict/rust'))
NUMBER_OF_NONRUST_IMAGES = len(os.listdir('data/predict/non-rust'))
#print(NUMBER_OF_NONRUST_IMAGES)
# print("Total False Negative: %.2f"% ((falseNegativeCount/NUMBER_OF_RUST_IMAGES)*100))
print("False Positive: %.2f"% ((falsePositiveCount/NUMBER_OF_NONRUST_IMAGES)*100))
print("True Positive: %.2f"% ((truePositiveCount/NUMBER_OF_RUST_IMAGES)*100))
print("False Negative: %.2f"% ((falseNegativeCount/NUMBER_OF_RUST_IMAGES)*100))
print("True Negative: %.2f"% ((trueNegativeCount/NUMBER_OF_NONRUST_IMAGES)*100))



#print(rounded)


# if __name__=="__main__":
# 	model = modelFromFile()
# 	#model = retrain()
# 	makePredictions(model)



# json_string = model.to_json()
# with open('model.json','w') as outputFile:
#     outputFile.write(json_string)
# outputFile.close()
    #json.dump(json_string,outputFile)
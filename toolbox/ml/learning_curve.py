""" Exploring learning curves for classification of handwritten digits
Robbie
 """

import matplotlib.pyplot as plt
import numpy
from sklearn.datasets import *
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression

data = load_digits()
print data.DESCR
num_trials = 10
train_percentages = range(5,95,5)
test_accuracies = numpy.zeros(len(train_percentages))

#Calculates results for each training percentage
for i in range(len(train_percentages)):
	score = 0
	#Trains the model num_trials of times
	for n in range(num_trials):
		x_train, x_test, y_train, y_test = train_test_split(data.data, data.target, train_size = train_percentages[i]/100.0)
		model = LogisticRegression(C = 1)
		model.fit(x_train, y_train)
		score += model.score(x_test, y_test)
	test_accuracies[i] = score/num_trials

fig = plt.figure()
plt.plot(train_percentages, test_accuracies)
plt.xlabel('Percentage of Data Used for Training')
plt.ylabel('Accuracy on Test Set')
plt.show()
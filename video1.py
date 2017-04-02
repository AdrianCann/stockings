import matplotlib.pyplot as plt

from sklearn import datasets
from sklearn import svm

digits = datasets.load_digits()

clf = svm.SVC(gamma=0.001, C=100)
# scikit learn can pick best version of gamma using machine learning

x,y = digits.data[:-1], digits.target[:-1]

clf.fit(x,y)

print('Prediction:', clf.predict(digits.data[-1]))

plt.imshow(digits.images[-1], cmap=plt.cm.gray_r, interpolation="nearest")
plt.show()

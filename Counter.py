import requests
import json
import time
import numpy as np
from sklearn import neighbors
from sklearn.lda import LDA
from sklearn.utils import shuffle
from sklearn.naive_bayes import BernoulliNB 
from sklearn.naive_bayes import MultinomialNB 
from sklearn.svm import LinearSVC 
from sklearn.linear_model import LogisticRegression 
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import sys
from sklearn.svm import NuSVC

def classifierError(truelabels,estimatedlabels):
    # Put your code here
    loss = 0
    for i in range(truelabels.size):
        if(truelabels[i]!=estimatedlabels[i]):
            loss+=1
    return loss/truelabels.size
    
    
# Lets train
s = np.array([[65,1,1,1,129,1,1,1],[87,1,1,1,129,1,1,1,],[145,17,145,33,203,225,225,65],[225,193,33,65,161,191,66,129],[33,189,193,1,65,129,193,1],[112,17,97,65,17,110,97,129],[69,17,101,160,33,17,225,65],[163,65,190,129,193,128,193,34]])


delta = 13
f = open('NonHumanSet.txt', 'r')
g = open('HumanSet.txt','r')

nonhumandata = f.readlines()
humandata = g.readlines()
i = 0

TrainingData = []
TrainingLabels = []
# label is 1
for i in humandata:
    #Z = np.fromstring(i,dtype=np.uint8, sep=',')
    Z = np.fromstring(i,dtype=np.uint8)[0:64]
    if(Z.size !=64):
        continue
    #Z = Z-s.reshape(64)
    #low_values_indices = Z < 0  # Where values are low
    #Z[low_values_indices] = 0
    TrainingData.append(Z)
    TrainingLabels.append(1)

# label is 0
for i in nonhumandata:
    Z = np.fromstring(i,dtype=np.uint8)[0:64]
    if(Z.size !=64):
        continue
    #Z = Z-s.reshape(64)
    #low_values_indices = Z < 0  # Where values are low
    #Z[low_values_indices] = 0
    TrainingData.append(Z)
    TrainingLabels.append(0)

NP_TrainingData = np.asarray(TrainingData)
NP_TrainingLabels = np.asarray(TrainingLabels)

NP_TrainingData, NP_TrainingLabels = shuffle(NP_TrainingData, NP_TrainingLabels, random_state=0)
#print NP_TrainingLabels

# At this point I have a set of data

num_elems = NP_TrainingData.shape[0]
ValidationData = NP_TrainingData[int(0.9*num_elems):num_elems]
ValidationLabels = NP_TrainingLabels[int(0.9*num_elems):num_elems]

TrainingData = NP_TrainingData[0:int(0.9*num_elems)]
TrainingLabels = NP_TrainingLabels[0:int(0.9*num_elems)]

# At this point we have training and validation data
#print TrainingData.shape
#print ValidationData.shape

# Following helps us test classifiers so we could choose one. The others should just be commented out.

#LDA#

#l = LDA()
#l.fit(TrainingData,TrainingLabels)
#labels = l.predict(ValidationData)
#print "Classifier error for validation data for LDA = " + str(classifierError(ValidationLabels,labels))
#
## 5-NN
#at = neighbors.KNeighborsClassifier(n_neighbors=5, weights='uniform', algorithm='auto')
#at.fit(TrainingData,TrainingLabels)
#labels = at.predict(ValidationData)
#
#print "Classifier error for validation data for KNN-5 = " + str(classifierError(ValidationLabels,labels))
#
## Bernoulli naive bayes
#Bern = BernoulliNB()
#Bern.fit(TrainingData,TrainingLabels)
#labels = Bern.predict(ValidationData)
#print "Classifier error for training data - BERNOULLI = " + str(classifierError(ValidationLabels,labels))
#
## Multinomial Naive Bayes
#Mul = MultinomialNB()
#Mul.fit(TrainingData,TrainingLabels)
#labels = Mul.predict(ValidationData)
#print "Classifier error for training data - Multinomial = " + str(classifierError(ValidationLabels,labels))
#
## Linear SVC
#Sup = LinearSVC()
#Sup.fit(TrainingData,TrainingLabels)
#labels = Sup.predict(ValidationData)
#print "Classifier error for training data - Linear SVC = " + str(classifierError(ValidationLabels,labels))
#
## Logistic Regression
#Logi = LogisticRegression()
#Logi.fit(TrainingData,TrainingLabels)
#labels = Logi.predict(ValidationData)
#print "Classifier error for training data - Logistic Regression = " + str(classifierError(ValidationLabels,labels))

#fig = plt.figure()
#Start real time prediction
#COUNTER = 0

#ChosenModel = neighbors.KNeighborsClassifier(n_neighbors=2, weights='uniform', algorithm='auto')
ChosenModel = LinearSVC()
ChosenModel.fit(TrainingData,TrainingLabels)
st = np.zeros((100,64))

fig = plt.figure(1)
#ir1 = False
#ir2 = False
#counterup = False
#counterdown = False
on = False
url = "http://sensormat.azurewebsites.net/api/SensorImages/GetLastSensorImage"
#plt.ion()
i = 0
while(1):
    #Check for new value every 10 ms
    time.sleep(0.001)
    myResponse = requests.get(url)
    if(myResponse.ok):
        jData = json.loads(myResponse.content)
    else:
        myResponse.raise_for_status()
        exit(1)
    instr_np = str(jData["SensorData"])
    
#    # Check if contains a #. If it does check if it contains a *. If yes and after, counterUp=true
#    # If yes and before, CounterDown = true. If no ir1 = true as long as ir2 = false, else counterDown
#    # else if contains *. ir2 = true as long as ir1 = false else counterUp
#    
#    instr_np = re.sub('[#*]','',instr)
    Z = np.fromstring(instr_np, dtype=np.uint8, sep=',')
    if(Z.size !=64):
        continue
    #plt.clf()
    #plt.figure(1)
    plt.imshow(Z.reshape(8,8),interpolation='None',cmap='jet')
    #plt.imshow(,interpolation='None',cmap='jet')
    #plt.show()
    #plt.clf()
    #X = np.arange(1, 9, 1)
    #X, Y = np.meshgrid(X, X)
    #plt.figure(2)
    #ax = fig.add_subplot(222, projection='3d')
    #surf = ax.plot_surface(X, Y, Z.reshape(8,8), cmap='jet',linewidth=0, antialiased=False)
    #ax.set_zlim(0, 256)
    #plt.show()
    plt.pause(0.01)
    #print Z.reshape(8,8)
    #Z = Z-s.reshape(64)
    #low_values_indices = Z < 0  # Where values are low
    #Z[low_values_indices] = 0
    m = np.mean(Z)
    #print m
    # Mean less than delta = Nothing crossing mat! Ignore!

    if(m<delta):
        sys.stdout.write(".")
        sys.stdout.flush()
        if(on == False):
            continue
    else:
        on = True
        if(i>99):
            continue
        st[i] = Z
        i = i+1
        continue
    # If we reach here, then something crossed the mat and it has been taken into the set!
    print st.shape
    Z = np.mean(st,axis=0)
    Z = Z.reshape(1,-1)
    print Z.shape
    label = ChosenModel.predict(Z)
    if(label == 1):
        print "Human detected"
    else:
        print "Object detected"
    st = np.zeros((100,64))
    on = False
    i = 0
    #plt.pause(0.01)

##    If IR1 < IR2 -> thing entered else exited
##       Therefore, counter++ or counter--
#
##    Update surface plot of what came in and display
##    Update contour plot of what came in and display
#    #X = np.arange(1,9,1)
#    #x, y = np.meshgrid(X, X)
#    #xi, yi = np.linspace(x.min(), x.max(), 1000), np.linspace(y.min(), y.max(), 1000)
#    #xi, yi = np.meshgrid(xi, yi)
#    #rbf = scipy.interpolate.Rbf(x, y, Z, function='linear')
#    #zi = rbf(xi, yi)
#    #plt.imshow(zi, vmin=0, vmax=256, origin='lower',extent=[x.min(), x.max(), y.min(), y.max()],cmap='jet')
#    #fig2 = plt.figure()
#    #ax = fig2.add_subplot(111, projection='3d')
#    #ax.plot_surface(xi, yi, zi)
#    plt.pause(0.05)
##while True:
##    plt.pause(0.05)
#    



![Python](https://img.shields.io/badge/SDK-Python-green) ![Android Studio](https://img.shields.io/badge/SDK-Android%20Studio-green) ![TensorFlow](https://img.shields.io/badge/ML-TensorFlow-red) ![scikit-learn](https://img.shields.io/badge/ML-scikit--learn-red) 

<div align="center">
  Artificial Conscience MobileHCI22 Student Design Competition
  
  <a href="mailto:jonas.keppel@uni-due.de">Jonas Keppel</a> |
  <a href="mailto:alper.oeztuerk@uni-due.de">Alper Öztürk</a> |
  <a href="mailto:jean-luc.herbst@stud.uni-due.de">Jean-Luc Herbst</a> |
  Stefan Lewin

</div>

<details open="open">
<summary>Table of Contents</summary>

- [About](#about)
- [Improvised Glasses](#improvised-glasses)
  - [Used parts](#used-parts)
  - [Concept](#concept)
  - [File descriptions](#file-descriptions)
- [Huawei Eyewear](#huawei-eyewear)
  - [About the Eyewear (used features for the project)](#about-the-eyewear-(used-features-for-the-project))
  - [Concept](#concept)
  - [File descriptions](#file-descriptions)
  - [Key features](#key-features)
    - [Android](#android)
    - [Python](#python)
  - [Implementation](#implementation)
    - [Android development](#android-development)
    - [Userinterface overview](#userinterface-overview)
    - [Python development](#python-development)
- [License](#license)
  
</details>


---

## About
What Is Artificial Conscience?

A modular system that supports users
to achieve a healthy lifestyle by
reminding of healthy behavior and
giving recommendations for everyday life.

The key features are:
- Suggesting context-dependent exercises
- Reminding oneself of personal goals
- Applying techniques to improve productivity

The basis for the recommendations are previously collected data, which have been processed with the help of machine learning algorithms. 

---

## Improvised Glasses

### Used parts:
- 1x Bluno Beetle - Product details: https://www.dfrobot.com/product-1259.html
- 1x GY-521 IMU
- Some jumper cables
- 1x (Regular) safty glasses
- Some cable ties

### Concept
Due to shipping problems with the Huawei eyewear (package got stuck in local customs), our team decided to design improvised glasses and work with those temporarily.
We decided to limit the features of the improvised goggles to IMU functions, since IMU data is a key component of our project.
The goal of the improvised glasses and our developed code is to get a first impression of how head movement data is formed. 

**Important!** The collected / received data is not applicable to the Huawei Eyewear due to different IMU modules and configurations.

### File descriptions
- The folder `improvised_glasses/arduino-firmware-improvised-glasses` includes the Firmware for the Bluno Beetle
- The folder `improvised_glasses/python-improvised-glasses-recorder` includes the python script for logging the IMU Data and converting it to a .csv file
  - additional required modules:
    - numpy
    - tk
    - pyserial
- `example_recording.csv` includes an example sensor recording file
- `improvised_glasses/improvised_glasses_wiring.pdf` includes the wiring of the both modules
- `improvised_glasses/training_model.ipynb` includes a jupyter notebook for preprocessing the data as well as training and saving a model
- `improvised_glasses/live_predictor` includes a python script to do live predictions by loading the saved model and using the IMU data to predict gestures

---

## Huawei Eyewear 

### About the Eyewear (used features for the project)
- 6 axis IMU (Accelerometer X, Y, Z and Gyroscope Yaw, Pitch, Roll)
- Private Speakers
- Wear Detection - not implemented
- Temperature sensor - not implemented
- More information about the device: https://consumer.huawei.com/en/wearables/huawei-eyewear/


### Concept
The goal was to create an artificial conscience using the sensor data and privacy speakers of the Huawei Eyewear. As a proof on concept, we implemented the working, drinking and neck exercises like rotate head (clockwise and counter-clockwise) or stretch head (left, right, and front). Since we were quite unlucky during the Competition (package stuck in local customs and probably a shipping damaged gyroscope sensor), we could not implement a full working demo system.

To demonstrate our concept, we produced and uploaded a video on YouTube: https://youtu.be/jAtU6x7G4BE

### File descriptions
- The file `python_huawei_eyewear_ML.ipynb` includes the python code for Shallow Classification and Deep Learning in a Jupyter Notebook file.
- `app-debug.apk` is a precompiled Android file, which can be used to install the software on your personal mobile phone.
- `example_overall_export.csv` is an example file to demonstrate the resulting file when selecting the option to export all sensor data to a .csv file.


### Key features
#### Android
- "On the fly" Conversation of the sensor data reporting from the Huawei Eyewear into a .csv file containing Accelerometer X, Y, Z and Gyroscope Yaw, Pitch, Roll
- Ability to export a full sensor data reporting of the Huawei Eyewear as a .csv
- The recorded .csv files will be saved in the downloads folder of your mobile
- Updated gradle to gradle-7.4.2 and added com.android.support:multidex:1.0.3 to make it compatible with Android 13
  - This application was succesfully tested with the following devices:
  - Pixel 6 (Android 13)
  - Pixel 6a (Android 13)
  - Xiaomi Mi 8 (Android 10 - MIUI 12.5)
- Added a Timer feature to auto-stop sensor recordings after a given time
- Added Google Offline TTS engine to announce the start of the recording
- All processes are working without an online connection (Data does not leave device)

#### Python
- Training of the collected activity data using multiple shallow classiifer using mostly default values (not-tweaked):
  - Method: Nearest Neighbors       Accuracity: 0.7272727272727273
  - Method: Linear SVM              Accuracity: 0.7727272727272727
  - Method: RBF SVM                 Accuracity: 0.7272727272727273
  - Method: Decision Tree           Accuracity: 0.6363636363636364
  - Method: Random Forest           Accuracity: 0.7272727272727273
  - Method: Neural Net              Accuracity: 0.5454545454545454
  - Method: Naive Bayes             Accuracity: 0.7727272727272727
  - Method: QDA                     Accuracity: 0.5454545454545454
  - Method: Gaussian Process        Accuracity: 0.7272727272727273
- Additionaly a tweaked variation of Random Forest (n_estimators=300, n_jobs=-1, random_state =1)
  - Method: Tweaked Random Forest   Accuracity: 0.77 
- Training of the collected activity data using Keras/Tensorflow

### Implementation Details
#### Android development:  
To implement this concept, we used the SDK Software by Huawei and modified it to implement a "on the fly" conversation of the reported sensor data, with some additional UI and "under the hood" changes as decribed in key features. It seems like the Huawei Eyewear, is transfering the Sensordata as multiple hex-values in a row to the SDK-Software and the Software "translates" it to a JSON-like structure:

Example raw data:
```
5a021e002b301600634201000f0000008f10000064001d0000010201000000000000000014bdf3ca0a2cfeb9f3cb0a34febff3c90a32fec5f3c20a2bfebff3bf0a2efec5f3c10a2efed1f3c80a2bfee0f3ce0a29feeef3d40a2ffef5f3d90a2dfef9f3dc0a30fefbf3df0a39fefdf3e10a3afef3f3e20a34fee8f3e00a35fedef3e20a31fee1f3dd0a29fee4f3da0a2cfee4f3db0a34fee0f3de0a36fe0000000000000000000000000000000000000000000000000000000000002018eb04000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006e0690000010000004609000000000000d004000000000000023e00006790000003f3ffff2c6700009b1e000050660000ebdb
```

example conversation by the SDK to (added line-breaks to make it more readable):
```
SensorData{
	serviceId=43, 
	commandId=48, 
	sensorType=22, 
	sensorTypes=[ACC, GYRO, PROX], 
	time=1443270, 
	packageNumber=119, 
	volt=4105, 
	chargeCurrent=0, 
	battPercent=91, 
	temperature=36, 
	hallData=0, 
	earSide=1, 
	roleState=2, 
	wearDetect=1, 
	knockDetect=0, 
	knockScore=0, 
	movementDetect=0, 
	touchEvent=[0, 0, 0, 0], 
	earSideDetect=0, 
	accelDataLen=20, 
	accelData=[Acc{x=-3526, y=-2200, z=600}, Acc{x=-3524, y=-2204, z=596}, Acc{x=-3519, y=-2203, z=600}, Acc{x=-3514, y=-2200, z=605}, Acc{x=-3516, y=-2198, z=601}, Acc{x=-3518, y=-2198, z=601}, Acc{x=-3520, y=-2194, z=604}, Acc{x=-3513, y=-2185, z=601}, Acc{x=-3517, y=-2181, z=602}, Acc{x=-3523, y=-2175, z=600}, Acc{x=-3531, y=-2169, z=599}, Acc{x=-3538, y=-2169, z=603}, Acc{x=-3543, y=-2167, z=600}, Acc{x=-3543, y=-2176, z=594}, Acc{x=-3546, y=-2174, z=597}, Acc{x=-3546, y=-2179, z=597}, Acc{x=-3540, y=-2181, z=595}, Acc{x=-3534, y=-2180, z=589}, Acc{x=-3534, y=-2179, z=582}, Acc{x=-3533, y=-2184, z=586}, Acc{x=0, y=0, z=0}, Acc{x=0, y=0, z=0}, Acc{x=0, y=0, z=0}, Acc{x=0, y=0, z=0}, Acc{x=0, y=0, z=0}],
	accTimeStamp=1443252000, 
	gyroDataLen=20, 
	gyroData=[Gyro{roll=1153, pitch=-262, yaw=-250}, Gyro{roll=1214, pitch=-384, yaw=-372}, Gyro{roll=1214, pitch=-445, yaw=-67}, Gyro{roll=1153, pitch=-384, yaw=-6}, Gyro{roll=1092, pitch=-384, yaw=-6}, Gyro{roll=1031, pitch=-384, yaw=116}, Gyro{roll=970, pitch=-323, yaw=116}, Gyro{roll=970, pitch=-262, yaw=299}, Gyro{roll=848, pitch=-201, yaw=299}, Gyro{roll=848, pitch=-262, yaw=238}, Gyro{roll=726, pitch=-201, yaw=299}, Gyro{roll=604, pitch=-79, yaw=421}, Gyro{roll=482, pitch=-201, yaw=421}, Gyro{roll=299, pitch=-201, yaw=360}, Gyro{roll=116, pitch=-18, yaw=299}, Gyro{roll=-189, pitch=-18, yaw=238}, Gyro{roll=-189, pitch=-18, yaw=177}, Gyro{roll=-311, pitch=-79, yaw=116}, Gyro{roll=-311, pitch=-18, yaw=238}, Gyro{roll=-250, pitch=-140, yaw=177}, Gyro{roll=0, pitch=0, yaw=0}, Gyro{roll=0, pitch=0, yaw=0}, Gyro{roll=0, pitch=0, yaw=0}, Gyro{roll=0, pitch=0, yaw=0}, Gyro{roll=0, pitch=0, yaw=0}], 
	capSensorDataLen=6, 
	capSensorData=[42584, 1, 993, 0, 611, 0], 
	capRawData=[29245, 16642, -1131, -3421, 19122, -184]
}
```

**Hint**: These two examples do not relate to each other and should be considered as two separate examples.

To reduce this dataset to the required sensor data (accelerometer and gyroscope) and then convert it to a .csv, regex statements are used to ensure good performance. The ability to export the entire dataset as a .csv is also included in the app, but we found that a small wait is required to ensure that the file creation process is complete when it is activated. 



##### Userinterface overview
![UI](https://user-images.githubusercontent.com/36895999/192547318-0e655bf9-78d0-44ef-a700-8ce74ece5eec.png)

#### Python development:
In order for the app to be able to recognize and correctly assign activities, we use machine learing. Two different approaches were tested for this purpose: Shallow classifier and deep learning.
  For the Shallow classifier the scikit-learn package (https://scikit-learn.org/stable/) was used, because this package contains many different classifiers and is compatible with the packages Numpy and mathplotlib.
For the deep learning training tensorflow / keras is used.

# License
This work is open-source under MIT-License.

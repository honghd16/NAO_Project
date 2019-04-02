# A NAO-based interactive project

## Requirement
1. PIL or pillow
2. Pynaoqi SDK for python2.7
3. openCV2
4. Tensorflow v1.1 or later

## Intro
### 操作方案
#### 待机
NAO开机后，在工程根目录（以下简称$ROOT）下执行命令：
```
python appGreeter.py
```
等待10s左右，NAO站起来后，即成功运行。之后，NAO将在地面进行随机的行走，此时的NAO处于待机状态。
同时，在检测到前方存在障碍物时，NAO将会左转或右转90度（根据障碍物的大体方位来选择）来避开障碍。
#### 唤醒
在待机状态下，用户能够通过两种方式对NAO进行唤醒：
1. 对NAO说“你好”。NAO能够自动检测用户的问候，以及发出问候的用户的大概方位。检测到问候后，NAO将自己的身体和面部转至大致朝向用户的方向，对用户发出同样的问候：“你好”，并伸出右手尝试与用户握手。当用户握住NAO的右手后，NAO将会摇动右手进行握手。
2. 站在NAO的面前。NAO能够自动检测视野中的人脸。当检测到人脸后，将会追踪人脸，使得人脸保持在自己的视野中心。之后，NAO将对用户发出问候：“你好”，并伸出右手尝试与用户握手。当用户握住NAO的右手后，NAO将会摇动右手进行握手。
#### 交互
在被用户唤醒后，NAO将与用户开始交互，用户能够通过说话来对NAO下达指令，现有对NAO的指令如下：
1. “这是什么”：NAO将会检测视野中的画面，将当前画面上传至服务器，服务器使用GPU将画面通过一个Resnet v2分类网络，获得分类结果，并传回给NAO。NAO将用语音播报分类结果，如“这是金鱼。”
2. 待补充...
3. “再见”：NAO将会停止对人脸的追踪，并回复“再见”，之后回到待机状态。
### 状态转移图
<img src="https://github.com/raxxerwan/NAO_Project/blob/master/doc/frame.png" />




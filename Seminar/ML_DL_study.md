< Sung Kim 딥러닝 강의 >
https://www.youtube.com/watch?v=Hax03rCn3UI&list=PLlMkM4tgfjnLSOjrEJN31gZATbcj_MpUm&index=4

-AI기술은 복잡한 의사결정을 정확하고 빠르게 해낼 수 있도록 도와줌 
-TensorFlow and Python 
-참고자료 reference 정보-> 1강 -09:00쯤 참고 

[머신러닝 개요]
* 머신러닝이 무엇인가? 
- Limitations of explicit programming 


ex) spam filter, automatic driving -> to many rules
(수많은 룰들이 존재하고 그 룰들을 프로그래밍 로직으로 정리하기 한계가 있음) 

-Authur Samuel(1959)
" Field of study that gives computers the ability to learn without being explicitly programmed" 
(일일이 프로그램을 하지말고 현상에서 자동적으로 배우면 안될까라는 생각에서 착안
개발자가 일일이 어떻게 하는 것인지 정하는 것이 아니라, 프로그램자체가 어떤 데이터를 학습해서 뭔가를 배우는 영역을 갖는 것이 머신러닝) 

* 학습하는 방법에 따라 지도학습(Supervised)/비지도학습(Unsupervised)으로 분류 
-지도학습 - learning with labeled examples 
-> Most common problem type in ML ex) Image labeling(learning from tagged images), Email spam filter(learning from labeled spam or ham email), Predicting exam score(learning from previous exam score and time spent)
비지도학습 - learning with un-labeled examples ex) google news grouping, word clustering

[TensorFlow 개요] 
- TensorFlow is an open source software library for numerical computation using data flow graphs
* what is data flow graph?
-Graph : 노드와 노드 사이에 엣지로 연결된 그림 
-Nodes in the graph represent mathmatical operations
-Edges represent the multidimensional data arrays(tensors) communicated between them. 


[Linear Regression] 

* 가설(Hypothesis)을 먼저 세우는 것 
H(x) = wx + b (-> 가장 간단한 단순회귀선형식) 
* linear regression 설계하기 위해 필요한 3가지 
- Hypothesis  ex) y(H(x1, x2, ...))= w1x1+w2x2+...+b(bias)
- Cost(loss) function 
- Gradient descnet algorithm (-cost fuction을 최적화하는 알고리즘)

->cost function의 cost를 작게하는 w를 구하는 것이 학습과정이다. 

* Gradient descent algorithm (경사하강법) 
- cost fucntion 만 정의한다면 minimize되는 cost fuction의 파라미터 값(w값 등)들은 기계적으로 찾아내는 것
-> Minimize cost function
-> Gradient descent is used many minimization problems
-> For a given cost functions, cost(W,b), it will find W, b to minimize cost
-> It can be applied to more general function: cost(w1, w2,...)
-How it works?
-> Start with initial guesses (Start at 0,0 (or any other value), Keeping changing W and b a little bit to try and reduce cost(W,b))
-> Each time you change the parameters, you select the gradient which reduces cost(W,b) the most possible
-> Repeat , Do so until you converage to a local minimum 
-> Has an interestign property - Where you start can determine which minimum you end up 

- 경사도를 구하기 위해서 '미분'을 이용 
-> cost function을 최소화하는 w를 구하는 방법 (Gradient descent algorithm의 핵심)

- Convex Function => 이러한 형태일 때 gradient descent algorithm이 최적의 답을 찾아준다는 것을 보장하게 됨 
-> Cost function을 설계할 때 형태가 convex fuction의 모양인지 확인을 해줘야 함!!


* Multi -variable 
-> 피처가 많아져서 수식이 너무 길어짐... => Matrix를 이용
-> Matrix multiplication - 행렬곱

- Hypothesis using matrix 
-> H(X) = XW (대문자 X의 의미가 matirx 의미)

- 레코드(인스턴스)가 많을 때 전체를 한 번에 연산가능한 점이 matrix의 큰 장점 

** TensorFlow 사용시, 대용량데이터 처리시(메모리에 한번에 올리기 어려움)  Queue runners를 사용하면 유용!
1. 파일들의 리스트를 만들어줌
filename_queue = tf.train.string_input_producer(['data01.csv', 'data02.csv', 'data03.csv', ...], shuffle=False, name='filename_queue')
2. 파일들을 읽어올 reader를 정의해줌 
reader = tf.TextLineReader()
key, value= reader.read(filename_queue)
3. 읽어온 value값을 어떻게 파싱할 것인지 
record_defaults = [[0.], [0.], [0.], [0.]]
xy = tf.decode_csv(value, record_defualts = record_defaults)
4. 배치생성 
train_x_batch, train_y_batch = tf.train.batch([xy[0:-1], xy[-1:]], batch_size=10)
sess = tf.Session()
coord = tf.train.Coordinator()
threads = tf.train.start_queue_runners(sess=sess, coord=coord)
for step in range(2001):
	x_batch, y_batch = sess.run([trian_x_batch, train_y_batch]) 
coord.request_stop()
coord.join(threads)

[Logistic Regression -lec 5] 
- Logistic Hypothesis -> 시그모이드함수식
- hypothesis를 변경했기 때문에 cost function도 변경해야 함
(liner regression에 사용하 는 cost function으로 사용한다면 gradient descent 방식으로 최적화가 되지 않음 - local minimum을 global minimum으로 착각하게 됨)

# Hypothesis using sigmoid 
hypothesis = tf.sigmoid(tf.matmul(X, W)+ b) 
(cf. sigmoid함수 구현 -> tf.div(1. , 1. + tf.exp(tf.matmul(X, W) + b) -- 그냥 tf.sigmoid 쓰면 됨..ㅎ) 
# cost function -- Cross-entropy
cost = -tf.reduce_mean(tf.reduce_sum(Y*tf.log(hypothesis)+ (1-Y)*tf.log(1-hypothesis)))
train = =tf.train.GradientDescentOptimizer(learning_rate=0.01).minmize(cost)
(train을 풀어서 쓰면) 
# Minimize 
a = tf.Variable(0.01) # Learning rate, alpha
optimizaer = tf.train.GradientDescentOptimizaer(a)
train = optimizer.minimize(cost))

# Accuracy computation
# True if hypothesis > 0.5 else False
predicted = tf.cast(hypothesis > 0.5, dtype = tf.float32) # tf.cast함수(floa32로 지정)는 True=1, False=0으로 변경해줌
accuracy = tf.reduce_mean(tf.cast(tf.equal(predicted, Y), dtype=tf.float32)) # 예측한값과 실제값(Y)이 같으면 True, 다르면 False로 뱉는데 그걸 tf.cast로 처리해줘서 예측을 잘했을 시(True), 1 틀렸을 시(False) 0으로 변경, 그리고 그 값을 평균구하면 정확도가 되는 것!!

# Train the model 
# Launch graph
with tf.Session() as sess: 
	sess.run(tf.global_variables_initializer())
	for step in range(10001): 
		cost_val, _ = sess.run([cost, train]), feed_dict={X: x_data, Y: y_data})
		if step % 200 == 0: # 200번 스텝마다 step, cost_val값을 출력하라는 의미 
			print((step, cost_val)
	
	# Accuracy report
	h, c, a = see.run([hypothesis, predicted, accuracy], feed_dict={X: x_data, Y: y_data})
	print("\nHypothesis : ", h, "\nCorrect (Y): ", c, "\nAccuracy: ", a)
	
[Softmax -lec 6] - Multinomial classification
- hypothesis - softmax함수 
- cost function(예측값과 실제값의 차이 함수) -- Cross-entropy 
cost = -tf.reduce_sum(Y * tf.log(hypothesis))

-cost function의 형태는 convex한 형태이고, 이 비용함수도 마찬가지로 Gradient Desent 알고리즘을 사용하여 최적화해줌 
cost function을 제일 작게하는 경사면 즉 기울기를 구해야 하므로, cost function을 미분해야 하는데 비용함수식이 복잡해졌으므로 미분의 과정도 굉장히 복잡해짐
그러므로, Gradient Descent 알고리즘 함수를 활용하여 컴퓨터가 계산하도록 하면 됨
(cost function을 미분해주고 그 미분해준 갓에 learning rate를 곱해준 다음 마이너스해준 값을 기존 W에 업데이트를 minimze 되도록 계속 해주는) 

두 함수가 같은 이유는 두개의 예측 및 결과만 있기에  -시그마(Li * log(Si) = -(L1*log(S1))-(L2*log(S2)) 입니다. 
실제 값 L1,L2은 1과 0, 그리고 서로 반대의 값을 지닐수밖에 없기 때문에 L2 = 1-L1 일 수밖에 없습니다. (0 또는 1, 1또는 0) 
S1, S2은 예측값이기 때문에 1,0 만 나오는 것은 아니지만 둘의 합은 1이 될 수밖에 없습니다. (0.3, 0.7 등 그러나 어쨌든 1-L0 = L1)
따라서 -L1*log(S1)-(1-L1)*log(1-S1) 가 됩니다. 
L1 = y, S1 = H(x) 로 바꾸면 -y*log(H(x))-(1-y)*log(1-H(x))가 되는 것입니다.

* Tesorflow 구현 실습
scores -> softmax function ->  probabilities (-> one-hot encoding)
# 실습코드 https://github.com/hunkim/DeepLearningZeroToAll/blob/master/tf2/tf2-06-1-softmax_classifier.py
import tensorflow as tf
import numpy as np

hypothesis = tf.nn.softmax(tf.matmul(X,W)+b)
# Minimize error using cross entropy
learning_rate = 0.001
cost = tf.reduce_mean(-tf.reduce_sum(Y * tf.log(hypothesis), axis  =1)) # Cross entropy
optimizer = tf.train.GradientDesentOptimizer(learning_rate).minimize(cost) # Gradient Descent

[lec7. Learning rate, Preprocessing, Overfitting, Regulrization(일반화), Training/Testing dataset]
* Learning rate(알파)
-learning rate를 너무 크게하면, overshooting 문제
-learning rate를 너무 작게하면, 시간이 너무 걸리고 local minimum에서 학습이 멈출 수 있음 
-> 몇 번을 시도해봐야 함 (보통 0.01로 시작) -cost function 값을 확인 

* Preprocessing 
Data X preprocessing for gradient descent 
X들간의 값의 단위가 달라 서로 너무 차이가 크면 gradient descent 에서 문제가 생김 (gloabl minimum으로 가지 않고 튕겨나갈 수 있음)
-> nomalize 할 필요가 있음 (여러 방법이 있음 - zero-centered data/ nomalized data 등)
-> 방법: Standardization(평균, 분산 사용하여 정규화)

* Overfitting
- 학습데이터만 딱 맞는 모델을 생성 
-> 학습데이터에서는 성능이 잘 나올 수 있으나, 실제 데이터에서는 성능이 잘 나오지 않음
-> 문제해결: 학습데이터를 많이 가질 수록, 피처의 개수를 줄이는(중복피처들 제거), 일반화(Regularization) 등

* Regularization
- Let's not have too big numbers in the weight 
-> cost function에 regularization term을(Lamda*sum(W element 제곱)  -- lambda : regularizatino strength)더해줌
-> ex) l2reg = 0.001 * tf.reduce_sum(tf.square(W)) -- W는 element w의 matrix

* Training/Testing Dataset
- Training/Validation/Testing Dataset

* Online learning
- 학습데이터가 너무 많을 때 학습데이터를 한 번에 학습시키는 것이 아니라, 쪼개서 학습시킨다는 것 

[lec8. 딥러닝의 기본개념 ]
-We need to use MLP, multilayer perceptrons (multilayer neural nets) 
-"No one on earth had found viable way to train" -Marvin Minsky, 1969
-Backpropagation(1974, 1982 by Paul Werbos, 1986 by Hinton)
-CNN(Convolutional Neural Networks), nerual-network
-Backpropagation just did not work well for normal neural nets with many layers(복잡한 문제에는 여러 개의 레이어가 필요할텐데 backpropagation 알고리즘은 레이어가 많아지면 잘 동작을 못했음)
-Other rising machine learning algorithms: SVM, RandomForest, etc.
-1995 "Comparison of Learning Algorithms For Handwritten Digit Recognition" by LeCun et al. found that this new approach worked better
-> nerual network의 2번째 침체기 

-CIFAR(Canadian Institute for Advanced Research)단체가 뉴럴넷에 대한 연국 적극적으로 지원
-Breakthrough (in 2006 and 2007 by Hinton and Bengio
-Neural networks with many layers really could be trained well, if the weights are initialized in a clever way rather than randomly. 
-Deep machine learning methods are more efficient for difficult problems than shallow methods
-Rebranding to Deep Nets, Deep Learning
-> 다시 신경망에 관심을 갖고 연구 시작
-IMAGENET 챌린지 (Large Scale Visual Recognition Chall enge) -> 신경망이 주목을 받게 된 주요 계기 
-The Image Classification Challenge: 1000 object classes 1,431,167 images
-Vision Deep CNN, Language Generating RNN, Deep API Learning (API 자동예측: 자연어로 시스템에게 말하면 어떤 api를 써야 하는지, 어떤 순서대로 api를 써야 하는지 나열해줌 -- 딥러닝사용하여 정확도 20%->60%로 증가) 

(이전에 신경망이 왜 잘 안되었을까 하는 Hinton의 회고)
* Geoffrey Hinton's summary of findings up to today 
-Our labeled datasets were thousands of times too small. 
-Our computers were millions of times too slow. 
-We initialized the weights in a stupid way. 
-We used the wrong type of non-linearity. 

[lab.8 Tensor Manipulation]
- Shape, Rank, Axis 
- matmul, broadcasting
- reshape, squeeze, expand_dims
- argmax, cast, stack
- reduce_mean, reduce_sum 
- ones_like, zeros_like, zip 

[lec9. 딥러닝 - XOR문제 딥러닝으로풀기, 미분, 딥넷트웍 학습 ]
* XOR문제 딥러닝으로풀기
-One logistic regression unit cannot separate XOR 
-> 3개의 시그모이드 유닛으로 연결하면 해결 가능 
(실습코드)
# NN -- 2개의 뉴럴넷 유닛으로 해결 
K = tf.sigmoid(tf.matmul(X, W1) + b1)
hypothesis = tf.sigmoid(tf.matmul(K, W2)+b2) 

* 미분
-Basic derivative
-Partial derivative(편미분) - consider other variables as constants(다른 변수는 상수로 취급)
-체인룰(chain rule)
 
* XOR문제를 NN으로 풀었던 예제에서는 W와 B가 주어졌지만, 실제에는 어떻게 자동적으로 학습해서 구할 수 있을까?
(How can we learn W1, W2, B1, B2 from training data?)
-> Gradient Descnet 알고리즘으로 해결 가능 
그런데, NN의 구조는 미분으로 계산하기가 너무 복잡... (노드도 많고, Layer도 많고 중간중간 시그모이드함수같은 것도 섞여 있고..)

* Back Propagation(chain rule)
-> f = wx+b, g = wx, f = g+b
1)forward (예시: w=-2, x=5, b=3, 학습데이터로부터 값을 가져오기) 
2)backward로 실제 미분의 값을 계산
아무리 복잡한 것들이 있더라도 그것을 미분하는데 필요한 것은 간단한 형들이 있으면 되고, 
어떤 복잡한 형태의 수식이라도 미분 가능

(NN for XOR)
x_data = np.array([0,0], [0,1], [1,0], [1,1]], dtype=np.float32)
y_data = np.array([[0], [1], [1] ,[0]], dtype=np.float32) 
X = tf.placeholder(tf.float32)  
Y = tf.placeholder(tf.float32) 
W1 = tf.Variable(tf.random_normal([2,2]), name = 'weight1')
b1 = tf.Variable(tf.random_normal([2]), name = 'bias1') 
layer1 = tf.sigmoid(tf.matmul(X, W1) + b1
W2 = tf.Variable(tf.random_normal([2,1]) name='weight2')
b2 = tf.Variable(tf.random_normal([1]), name='bias2')
hypothesis = tf.sigmoid(tf.matmul(layer1,  W2)+ b2)
# cost function 
cost = -tf.reduce_mean(Y*tf.log(hypothesis) + (1-Y)*tf.log(1-hypothesis))
train = tf.train.GradientDescentOptimizer(learning_rate=0.1).minimize(cost)
# Accuracy computation
# True if hypothesis>0.5 else False
predicted = tf.cast(hypothesis > 0.5 , dtype = tf.float32)
accuracy = tf.reduce_mean(tf.equal(predicted, Y), dtype=tf.float32))
(Wide NN for XOR) ouput 더 많이 
(Deep NN for XOR) layer 더 많이 

* 텐서보드 - 진행상황 시각화, Plot quantitative metrics, Show additional data 

[lec10. Sigmoid보다 ReLU, Weight의 초기값 설정중요, Dropout과 앙상블, NN lego play] 

* Vanishing Gradient (NN winter2: 1986-2006  --이 문제로 2006년도까지 다시 뉴럴넷 분야는 빙하기 접어들음) 
-layer가 많아질 수록 활성함수로 sigmoid 사용시, "Vanishing Gradient"(경사가 사라지는) 문제 발생 
-> input데이터의 영향도가 output함수 f에 영향이 0.0000~~으로 가게 되기 때문 (시그모이드 함수를 통해 1보다 작은 값들을 계속 곱해나가니..)
=> Geoffrey Hinton 교수가 시그모이드함수를 잘못 썼다는 걸 발견 (We used the wrong type of non-linearity.)
* ReLU : Rectified Linear Unit
-> hidden layer상에서는 relu 사용 (출력값은 binary로 받기위해서는 마지막 ouput layer에서는 sigmoid 사용해야 함)
* Activation Functions 종류
-Sigmoid (잘 사용하지 않음)
-tanh -sigmoid를 조금 변형시켜서 -1 ~ 1사이의 값이 나오도록 하는 함수 (가끔 사용)
-ReLU - max(0, x)
-Leaky ReLU - ReLU에서 0보다 작은 값이 들어가면 모두 0으로 만드는 것을 보완하기 위해 나온 것  -- max(0.1x, x) 
-Maxout
-ELU


(Initialize weights in a smart way)
* Geoffrey Hinton 교수 - We initialized the weights in a stupid way.
* Need to set the initial weight values wisely 
- Not all 0's (- chain rule로 인해 w의 초기값을 0으로 다 주면 학습이 전혀 되지 않음) 
- Challenging issue
- Hinton et al.(2006) "A Fast Learning Algorithm for Deep Belief Nets" -Restricted Boatman Machine(RBM)
(RBM을 활용하여 초기값을 설정하면 학습이 잘된다는 것) 
(-> RBM이 근데 너무 복잡) 
-No need to use complicated RBM for weight initializations
-Simple methods are OK
-> Xavier initialization (2010)
-> He's initialization (2015)- Makes sure the weights are 'just right' not too small, not too big, Using number of input(fan_in) and output(fan_out)
(코드)
# Xavier initialization -- 코드 찾으려면 'xacier initialization tensorflow' 구글링해보면 잘 나옴
ex) W = tf.get_variable("W", shape=[784,256], initializer = tf.contrib.layers.xavier_initializer())
# Glorot et al. 2010
W = np.random.randn(fan_in, fan_out)/np.sqrt(fan_in)
# He et al. 2015
W = np.random.randn(fan_in, fan_out)/np.sqrt(fan_in/2)
* Still an active area of research(계속 연구되는 분야이기에 새로운 초기화 방법들이 나오고 있음. -데이터에 맞게 여러 가지 시도해보고 제일 잘 맞는 초기화방법을 사용하면 됨) 
-We don't know how to initialize perfect weight values, yet
-Many new algorithms 
-> Batch normalization
-> Layer sequential uniform variance 


(NN Dropout and model ensemble)
-딥러닝은 layer가 깊어질 수록(뉴럴네트워크를 깊게 만들수록) 오버피팅가능성이 크다. 
(오버피팅의 해결 3가지 : m ore training data/ reduce the number of features-딥러닝에서는 필요없는 문제/ regularization) 
-> Regularization 방법 - regularization strength 조절 / (딥러닝에서 추가되는 방법) Dropout
* Dropout(A simple way to prevent Neural Networks from overfitting - Srivastava et al. 2014)
"Randomlyu set some neurons to zero in the forward pass"
-> 학습할 때 레이어간의 연결을 임의적으로 끊어서 몇 개의 노드를 죽인다는 것
(tensorflow implementation)
dropout_rate = tf.placeholder("float")
_L1 = tf.nn.relu(tf.add(tf.matmul(X, W1), B1))
L1 = tf.nn.dropout(_L1, dropout_rate) -- dropout_rate로 0.5~0.7 보통 사용
(**주의: 학습 시에만 dropout을 사용)
# Train 
sess.run(optimizer, feed_dict={X: batch_xs, Y: batch_ys, dropout_rate: 0.7}) -- 30% 끊어내겠다는 의미 
# Evaluation 
print "Accuracy: ", accuracy.eval({X: mnist.test.images, Y: mnist.test.labels, dropout_rate: 1}) --test할 때에는 dropout을 안하겠다는 의미 (test시에는 반드시 1로 해야 함)

* 앙상블모델 -> 실제 2~5% 성능 향상 

(NN LEGO Play) -네트워크이므로 다양한 형태로 구성 가능 
* Feedforward neural network
* Fast Forward 
* Split & Merge
* Recurrent network(RNN)
-> The only limit is your imagination! (상상력을 발휘해서 다양하게 구성해봐라)

[lab10. NN, ReLu, Xavier, Dropout and Adam] 
* 코드 테스트 결과 
Softmax for MNIST -정확도90% -> NN for MNIST(layer 3단만 추가, Relu 적용, normal distribution으로 초기값설정) -정확도94% -> Xavier for MNIST (W 초기값 설정) -정확도97% -> Deep Neural Nets with Dropout for MNIST -정확도98%!!

* Optimizers도 종류가 여러가지 많음 (AdaGrad, RMSprop, SGDNesterov, AdaDelta, Adam 등) 
-Adam optimizer가 좋다고 함 (Kingma et al.2015 자료에서 제일 좋은 성능 보였음) --권장
-ADAM: a method for stochastic optimization 

* Batch Normalization (입력값을 nomalization하는 방법) 
https://github.com/hunkim/DeepLearningZeroToAll/blob/master/lab-10-6-mnist_nn_batchnorm.ipynb



[lec11-1. CNN(Convolutional Neural Networks) introduction]
- 고양이 실험에서 시작 
(고양이에게 어떤 형태의 그림을 보여줬더니, 그림을 읽어드리는 뇌의 뉴런들이 동시에 다 반응하는 것이 아니라 어느 부분만 반응 -그림에 따라) 
(-> 이 실험에서 착안한 것이 CNN -- 입력을 나눠서 넣어주는 방식을 착안)  
-전체 이미지를 하나의 입력으로 받지 않고 일부분 일부분 나누어서 입력을 받음 
-필터 : 전체 이미지는 일부분, 일부분으로 나누는 처리 
-32*32*3 image - > 5*5*3 filter -> one number (Wx+b 사용하여)
(filter크기는 사용자가 정의, filter는 한 값을 만들어 냄)

-Ouput size: (N-F)/stride + 1   -- (stride: 움직이는 칸 수)
ex) N - 32, F(filter) - 5
-> ouput size가 작아질 수록 정보를 잃어버린다는 의미 -> '패딩' 개념을 사용(0으로 값을 둔 테두리를 둠)
-> 모서리 부분을 알려줄 수 있음
-> output사이즈는 필터의 사이즈와 stride에 정해짐
-> ex) input 7*7 - 3*3 filter, applied with stride 1 - pad with 1 pixel boarder ->what is the output? 7*7 output! 
(패딩을 사용해서 input 이미지와 output이미지의 사이즈가 같아지도록 하는 것을 일반적으로 사용) 
-(F-1)/2 -- common to see CONV layers with stride 1, fillter of size F*F, and zero-padding with (F-1)/2 (will preserve size spatially)
ex) F=3 => zero pad with 1, F=5 => zero pad with 2, F=7 => zero pad with 3

-CONV(convolutional) layer의 깊이는 몇 개의 필터를 사용했느냐에 따라 정해짐

(블로그 참고 -https://blog.naver.com/PostView.nhn?blogId=intelliz&logNo=221709190464)
-CNN의 레이어는 크게 2가지
1) Convolution/Pooling 메커니즘 - 이미지를 형상으로 분할하고 분석
2) FC(Fully Connected Layer) - 이미지를 분류/설명하는 데 가장 적합하게 예측(CConvolution/Pooling프로레스의 결과를 취하여 이미지를 정의된 라벨로 분류하는데 사용 --단순분류 경우)
*FC(Fully connected layer) 
*FCN(Fully connected Neural Networks)
- Convolutional layer -"필터"는 이미지를 통과하여 한 번에 몇 번 pixel을 스캔하고 각 형상이 속하는 클래스를 예측하는 형상 맵을 만듦
- Pooling layer(downsampling) - 가장 중요한 정보를 유지하는 동시에, 각 피쳐의 정보량을 줄임(대개 여러 개의 회전이 있음)

[lec11-2. CNN introduction: Max pooling and others] 
* Pooling layer(sampling)
-CONV layer의 레이어를 하나씩 갖고와서 resize(sampling) 한 후 다시 쌓음

* Max Pooling(필터처리할 때 가장 큰 값을 가져오는)

* ConvNetJS demo : training on CIFAR-10
http://cs.stanford.edu/people/karpathy/convnetjs/demo/cifar10.html

[lec11-3. CNN case study] 
* Case Study 1: LeNet-5
- 가장처음 CNN 구상하신 분- LeCun 교수(et al.1998)
- Input 32*32/ C1 feature maps 6@28*28/ S2 f.maps 6@14*14 / C3 f.maps 16@10*10/ S4 f.maps 16@5*5 / C5: layer 120/ F6 : layer 84 / OUTPUT 10 
- Conv filters were 5*5, applied at stride 1 
- Subsampling(Pooling) layers were 2*2 applied at stride 2 
- i.e.architecture is [CONV-POOL-CONV-POOL-CONV-FC]

* Case Study 2: AlexNet [Krizhevsky et al. 2012] --이미지넷 경진대회에서 1등을 하면서 많은 사람들의 관심을 끌었던 (15%) -- 8개 레이어 사용 
-Input : 227*227*3 images
-First layer(CONV1) : 96개 11*11*3 filters applied at stride 4
-> output volume [55*55*96] -- parameters:(11*11*3)*96 = 35K (35개의 변수가 필요) -- 무 슨의미? 2:42  질문하기  
-Second layer(POOL1): 3*3 filters applied at stride 2 
-> output volume [27*27*96] -- parameters 0! (pooling 이니깐 특별한 변수는 필요 없음)

* Case Study 3 : GoogLeNet [Szegedy et al. 2014]
- Inception module  -- ILSVRC 2014 winner(6.7% top5 error)

* Case Study 4 :ResNet [He et al. 2015] -- 152개 레이어 사용
-- ILSVRC 2015 winner(3.6% top5 error)
- 152개 정도의 레이어를 사용하면 학습하기 어려움 (ReLU를 쓴다하더라도)
-> 어떻게 가능? Fast Forward 방법을 이용(레이어가 깊지 않은 느낌으로 학습하게 됨 --정확한 이유는 다들 모른다고 하심)
 
* CNN으로 이미지뿐만 아니타 텍스트에도 사용 
-> Convolutional Neural Networks for Sentence Classification [Yoon Kim, 2014] 

* Case Study Bonus : DeepMind's AlphaGo
-알파고도 CNN을 사용
-Nature 논문   

Feature engineering feature engineering 

[ lab11. CNN Class, Layers, Ensemble ]
* tf.layers 사용하면 복잡한 shape 신경쓰지 않아도 됨 


[lec12. RNN - Recurrent Neural Network ] 
-Sequence data ex)음성, 자연어 등
-We understand based on the previous words + this word.(time series)
-NN/CNN cannot do this
-We can process a sequence of vectors x by applying a recurrence formula at every time step 

* RNN applications (RNN 활용사례 다양)
- Language Modeling (연관검색어 기능)
- Speech Recognition 
- Machine Translation (기계번역 ex- 파파고 - seq of words -> seq of words)
- Conversation Modeling/Question Answering
- Image/Video Captioning (ex- image-> sequence of words / video classification on frame level-> seq of words)
- Image/Music/Dance Generation 
- Sentiment Classification (sequence of words -> sentiment)

=> RNN도 다양하게 구성 가능 

* Multi-Layer RNN (더 복잡한 학습이 가능)
- 그러나, RNN도 깊어지고 복잡해지면 학습시 어려워짐
- 이 문제를 극복하기 위한 Several advanced models 
-> LSTM(Long Short Term Memory) 모델 (더이상 RNN 자체를 쓰지 않음) 
-> GRU 모델 (by Cho et al.2014)


	
	
 

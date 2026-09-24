ENGG2112 MultiDisciplinary Engineering 

Semester 2, 2026 _Week 5_ 

**Professor T. J. Lim** 



# Motivation 

Why Neural Networks in Engineering? 

## Applications of Neural Networks in Engineering 

#### **Structural Health Monitoring** 

_Detecting cracks, fatigue and anomalies in bridges and aircraft from vibration and sensor signals_ 

**Automated Defect Detection** _Spotting defects on production lines from images; faster and more consistent than manual inspection_ 

**Predictive Maintenance** _Forecasting equipment failure from sensor data before it happens_ 

**Autonomous Control Systems** _Learning control policies for robots, drones, and self-driving vehicles directly from data_ 

The University of Sydney 

3 

NMKTSE | 2026 | USYD 

## What We’re Covering Today 

**01** 



### **MLPs** 

Neurons, layers, and activation functions — the building blocks. 

**02** 



**Training** How networks learn: stochastic gradient descent & backpropagation. 

**03** 



**CNNs** Convolutions for images and spatially structured engineering data. 

**04** 



**Code** Hands-on examples in scikit-learn and PyTorch. 

The University of Sydney 

Multi-Layer Perceptrons _The Building Block_ 

## Borrowing from Biology: The Artificial Neuron 



<!-- Start of picture text -->
B IOL OG ICA L NEUR O N<br>Dendrites<br>Axon<br>Cell body<br>Signals arrive at the dendrites, are combined in the cell<br>body, and — if strong enough — fire down the axon.<br><!-- End of picture text -->



Inputs are scaled by weights, summed, and passed through an activation function to produce an output 

The University of Sydney 

## The Perceptron 

The full computation performed by a neuron: 



where 𝜎 ⋅ is known as an activation function. It is usually non-linear, and hence the perceptron performs a non-linear operation. 

The weights 𝑤1, … , 𝑤𝐾 and bias 𝑏 are the parameters that need to be learned during training. 

The neuron inputs 𝑥1, … , 𝑥𝐾 are the input features in the first layer, and the outputs of a prior layer of neurons in the hidden layer. 

The neuron output is labelled ƶ𝑦 but is only the output of the NN at the output layer; at other layers, the neuron output is an input to another layer of neurons. 

The University of Sydney 

## Activation Functions 

Three common choices: 

**Sigmoid** **_σ(z) = 1 / (1 + e⁻ᶻ)_** Squashes to (0, 1) — classic choice for output probabilities. 



<!-- Start of picture text -->
Tanh<br><!-- End of picture text -->



**_tanh(z)_** Squashes to (−1, 1) — zerocentered, common in hidden layers. 



<!-- Start of picture text -->
ReLU<br><!-- End of picture text -->



**_max(0, z)_** Cheap and effective — the default for hidden layers today. 

The University of Sydney 

## Non-Linearity to Model Complex Systems 

- Without the activation function, even a complex multi-layered system will be linear and cannot model cognitive systems or other complex systems. 

- With activation functions to introduce non-linearity, increasing the complexity of the NN architecture allows us to successfully mimic cognitive functions such as image recognition. 

The University of Sydney 

Stacking Neurons: The Multilayer Perceptron 



**Hidden layer 1 Hidden layer 2 Output layer** _4 neurons 4 neurons 2 classes_ 

The University of Sydney 

## What is the Network Actually Learning? 

Complex non-linear decision boundaries can be synthesized by an MLP. 

The more layers and neurons, the more flexible the decision boundaries can be. 

• Both blessing and curse – if training data is sufficient, MLP can solve very complex classification problems it has not seen before. But if training is insufficient, model may overfit and not generalize well. 

- More on this later. 

##### **Multilayer perceptron — non-linear** 



The University of Sydney 

# Training and Back-Propagation 

Minimizing loss function iteratively 

## Loss Functions 

- In any supervised learning context, we want the ML model output ƶ𝑦 to be as close to the ground truth label 𝑦 as possible. 

   - But what does that mean precisely? 

   - In classification, perhaps we can maximize 𝑃 𝑦= ƶ𝑦 ? 

   - - In regression, perhaps we should minimize 𝐸 𝑦−ƶ𝑦<sup>2</sup> ? 

- In both cases, we need the probability distribution of the features and the label. 

   - Conceptually, we can learn this distribution to some degree using training data. Hence the more data we have, the better. 

- Whether regression or classification, we need to define a loss function to minimize over the model parameters 𝜃 . 

   - For regression, MSE (mean square error) is the natural choice. 

   - For classification, the probability of error is not suitable but we have a proxy called cross entropy. 

The University of Sydney 

## Mean Squared Error (MSE) 

- In regression, the model directly outputs an estimate of the continuous label, i.e. ƶ𝑦= 𝑓𝜃 𝑥 , as we saw earlier. 

   - For a given 𝑥 , ƶ𝑦 is a function of 𝜃 , hence 𝑦−ƶ𝑦<sup>2</sup> will also be a function of 𝜃 . 

   - Need to find the 𝜃 that minimizes 𝑦−ƶ𝑦<sup>2</sup> on average, where averaging is over the distribution of 𝑥 and 𝑦 . 

   - Since we only have training data but not exact distributions, we can approximate the desired average by averaging over all the training data, hence this loss function works: 

𝑁 1 𝐿 𝜃= 𝑦𝑖 −ƶ𝑦𝑖<sup>2</sup> 𝑁<sup>෍</sup> 𝑖=1 

- This is generally not a simple function of 𝜃 and hence we cannot minimize it in a closed-form expression. 

The University of Sydney 

## Cross Entropy 

- In a classification problem where 𝑦 has a sample space with L values, the ML model must output a probability distribution over those L values. 

   - We’ll see how in just a while. 

- In this case, we don’t only have a single “point” estimate of 𝑦 , as in regression. - Instead, the model outputs its confidence that 𝑦 takes each of its L possible values, i.e. it outputs 

𝐿 𝑝1, … , 𝑝𝐿 s.t. 𝑝𝑙 = 1 ෍ 𝑙=1 

   - We would naturally want max 𝑝1, … , 𝑝𝐿 = 𝑝𝑦 , where 𝑦 is the ground truth label, for all training samples. 

   - But this problem statement does not afford us any way to find the optimal 𝜃 . 

- Hence, we need to bring in the concept of entropy. 

The University of Sydney 

## Cross Entropy 

- In general, the cross entropy of two distributions P and Q over the same discrete sample space 𝒮 is 

   - 𝐻 𝑃 𝑥log2 𝑄 𝑥 𝑃, 𝑄= −෍ 𝑥∈𝒮 

- It is minimal when P = Q, i.e. the two distributions are identical. In that sense, it’s a form of distance between two distributions. 

- Now recall that our ML model outputs a probability distribution over the sample space of 𝑦 , and that we have the ground truth value of 𝑦 . 

- Suppose 𝒮𝑦 = 1,2,3,4 , and the true value of 𝑦= 2 . Then the true distribution is 𝑝1 = 𝑝3 = 𝑝4 = 0 and 𝑝2 = 1 . 

- The ML model will estimate a different distribution from the true one, let’s call this distribution ƶ𝑝𝑙, 𝑙= 1,2,3,4 . 

The University of Sydney 

## Cross Entropy 



- This is an incredibly elegant result! Since ƶ𝑝𝑦 is the 𝑦 -th output of the ML model, its relationship to the parameter vector 𝜃 is explicit. 



where 𝑦𝑖 denotes the ground truth label of the i-th data sample. 

The University of Sydney 

Optimization of Loss Function _Training Using Gradient Descent_ 

## Method of Steepest Descent 

- Both MSE and cross-entropy loss functions are differentiable with respect to 𝜃 , as we’ll see soon. But still we can’t solve 

𝑑𝐿 𝜃 𝛻𝐿 𝜃= = 0 𝑑𝜃 

- A simple numerical method for approximately solving this equation is to “descend” towards the nearest minimum through a sequence of steps taken in the direction of steepest descent. 

   - The direction of steepest ascent is given by 𝛻𝐿 𝜃 , hence the direction of steepest <u>descent is the negative of that.</u> 

   - Denoting the step size or learning rate by 𝜇 , we have the SD iteration 𝜃𝑡+1 = 𝜃𝑡 −𝜇𝛻𝐿 𝜃𝑡 

   - The iterations continue until a “stopping criterion” is met, e.g. 𝜃 changes by less than a threshold from one iteration to the next, or a maximum number of iterations is reached. 

The University of Sydney 

## Batch, Mini-Batch and Stochastic Gradient Descent (SGD) 

- Recall that our two loss functions are averages over the **<u>entire</u>** set of training samples. - The size of this data set is normally very large (at least in the thousands). 

- - The computational complexity and time of gradient calculation both scale linearly with N, the size of the training data. 

   - Using all training samples (known as **batch** processing) for gradient descent optimization will therefore consume a lot of resources and be very slow. 



where 𝑁𝑏 ≪𝑁 is the mini-batch size, and 𝑙𝑖 𝜃 is either squared error or cross entropy for the i-th training sample. 

The University of Sydney 

## Batch, Mini-Batch and Stochastic Gradient Descent (SGD) 

- The mini-batch size 𝑁𝑏 can be anything from 1 to N. Generally accepted terminology is: 

   - Batch GD: 𝑁𝑏 = 𝑁 (i.e. use all training samples per iteration) 

   - Mini-Batch GD: 2 ≤𝑁𝑏 < 𝑁 (i.e. use more than 1 but fewer than all training samples per iteration) 

   - Stochastic GD: 𝑁𝑏 = 1 (i.e. use only one sample per iteration) 

- Unfortunately, SGD is also often used to refer to mini-batch GD. Putting aside terminology, the main idea here is: 

   - Use 𝑁𝑏 as a trade-off variable – smaller 𝑁𝑏 ⇒ noisier but faster and less complex updates. 

   - Default in sklearn is 𝑁𝑏 = 200 . It can be reset using the `batch_size` input parameter. 

The University of Sydney 

## Epochs and Batches 

- As we proceed through the batches, we eventually pass all the training data through the SGD solver. 

- - Each complete pass through the training data is known as a training epoch. 

- - The number of epochs we use for training is arbitrary – it depends on how much time and computational resources we have. 

Mini-batches Train (Weights over updated once several using GD per epochs mini- batch) 

The University of Sydney 

## Choice of Step Size/Learning Rate 

**Too Small** 



Crawls toward the minimum — training takes far longer than necessary. 

**Just Right** 



Converges quickly and smoothly toward the minimum. 



<!-- Start of picture text -->
Too Large<br><!-- End of picture text -->



Overshoots the minimum — can oscillate or even diverge. 

No need to pick step size manually. Optimizers like Adam adapt the step size automatically. 

The University of Sydney 

## Overfitting and Regularization 

- If we have more parameters than training data, e.g. we have an MLP having 1000 weights and 500 training samples, then we can drive the loss function to a value that matches every input feature perfectly with its class. This is an extreme case of the **overfitting** phenomenon. 

   - Can visualize it as in the figures below. 

   - Generalization performance will be poor. 



The University of Sydney 

## Overfitting and Regularization 

- Avoiding over-fitting by ensuring that number of training samples exceeds number of model parameters is obviously something we can do. 

- However over-fitting is not necessarily due to such an easily detected scenario. It is usually because the underlying model is simpler than what we’ve assumed – but we don’t know the underlying model! 

   - All we can do is to try to drive the smallish weights (which are essentially redundant) down to zero. 

   - The usual way to do this is to penalize the norm of the parameter vector, i.e. we add a term that drives the norm towards zero. 

The University of Sydney 

## Backpropagation 

- In SGD, we need to compute gradients of the loss function with respect to each and every one of the weights in the NN. 

- To do this we use the chain rule of differentiation, starting from the output layer and progressing backwards. 

- To illustrate, consider one of the output layer weights: 

   - ƶ𝑦= 𝜎 𝑤1𝑥1 + ⋯ = 𝜎 𝑧 

- We use the Chain Rule to write 𝑑𝐿 𝑑𝐿 𝑑ƶ𝑦 𝑑𝐿 = = 𝑧𝑥1 

- 𝑑𝑤1 𝑑ƶ𝑦<sup>⋅</sup> 𝑑𝑤1 𝑑ƶ𝑦<sup>𝜎’</sup> 

- All the terms on the RHS can be calculated. 

- In the lecture, we will demonstrate finding the derivative with respect to one of the hidden layer weights. 

The University of Sydney 

Convolutional Neural Networks (CNNs) _Automatic Feature Extraction on 2D Inputs_ 

## Why Images Are Problematic for MLPs 

- MLPs assume that features are just a flat list: if we swap two features in the order that they are fed into the MLP, the result will be unchanged. 

   - In other words, adjacency carries no information as the ordering of features are arbitrary. 

- If an image were to be fed into an MLP, we would ”flatten” the pixels, i.e. turn the matrix of 2D pixel values into a 1D vector. This presents the first problem, complexity or “parameter explosion” 

   - A 128 x 128 grayscale image turns into 16,384 features at the input layer. 

   - If the first hidden layer only has 128 neurons, we already need over 2 million weights in that first layer. 

- The second problem is that any detail (a face, a sign, etc.) when shifted even by one pixel will not be recognized as being the same thing. 

   - The MLP has no built-in notion that something is the “same pattern but moved”. 

The University of Sydney 

## Convolution or Filtering to Reveal Features 

- Convolution or linear filtering is nothing new. A filter for a 2D image can change the image so that certain colours are amplified or edges are sharpened – digital image processing has been doing this for years. 

   - The effect of filtering depends critically on the filter kernel 𝑤𝐽,𝑘, where the total number of weights in the kernel is user-defined. The filter output is 

- 𝑤𝑗,𝑘 𝑥𝑚−𝑗,𝑛−𝑘 

- 𝑦𝑚,𝑛 = ෍ ෍ 𝑗 𝑘 

- - Depicted pictorially this is much less obtuse than this equation! See next page. 

The University of Sydney 

## Convolution Illustration 



This kernel is a vertical edge detector – if the image in the window has a vertical edge, say a value of 10 for the first two columns and 0 in the third column, what’s the filter output? 

The University of Sydney 

## Feature Maps: What a Filter Detects 



<!-- Start of picture text -->
Original<br><!-- End of picture text -->



<!-- Start of picture text -->
Vertical edges<br><!-- End of picture text -->



<!-- Start of picture text -->
Horizontal edges<br><!-- End of picture text -->



<!-- Start of picture text -->
Blur<br><!-- End of picture text -->

The University of Sydney 

## CNN Convolutional Layer 

- A CNN starts with a convolutional layer where the kernels are not hand-designed but are learned from the data. 

- In other words, instead of manually deciding what features to extract for a given image processing task, we let the learning algorithm decide from the data. 

   - If the task is deciding whether a picture contains a furry animal or not, ”furriness” could be a more important feature than “vertical edge”. 

- This automatic feature extraction step is the key to solving the 2<sup>nd</sup> problem of the MLP, its inability to recognise a feature that’s been shifted. 

- But it doesn’t solve the complexity issue, which is where “max pooling” comes in. 

The University of Sydney 

## CNN Pooling 

- An image carries redundancy – an edge will carry over multiple pixels, so will a single colour or a texture. 

   - This translates also into the feature map. 

- It is therefore sufficient to collapse a small region of a feature map into just one number, e.g. within a 2 x 2 pixel square, retain only the largest value to represent the presence of that feature within the region. 

- This operation is known as max-pooling, and solves the 1<sup>st</sup> MLP problem of parameter explosion. 

- We can also have average-pooling, which retains the average of the feature map in a region. 

The University of Sydney 

## Illustration of Max Pooling 

- We just reduced the number of inputs to the next layer by a factor of 4 without losing (much) information. 



<!-- Start of picture text -->
-<br><!-- End of picture text -->

- Max pooling keeps only the strongest activation in each region, i.e. the clearest indication that the feature was found in that region. 

   - That’s all the information that the next layer needs for e.g. face recognition or anomaly detection. 

The University of Sydney 

## LeNet-5: Pioneering CNN 



The University of Sydney 

## LeNet-5: Pioneering CNN 



The University of Sydney 

## Softmax Output Layer 

The University of Sydney 

## Creating Probabilities Using Softmax 

- Recall: in a classification problem where the label space has L values, an ML model should produce probability values 𝑝1, … , 𝑝𝐿 where 𝑝𝑙 quantifies the confidence that the model has that the true label is 𝑙 . 

- The forward propagation through a NN (or any ML model) is designed to result in L values, but there is no way that those L values will sum to 1 without normalization. 

   - This normalization operation is known as softmax. 

- There are obviously many ways in which we can transform L raw numbers into a probability distribution, but softmax makes the most sense: 

𝑒<sup>𝑧𝑖</sup> softmax𝑖 𝑧1, … , 𝑧𝐿 = σ𝐿𝑙=1 𝑒<sup>𝑧𝑙</sup> 

- It allows the raw input to be any real value (negative or positive); the exponentiation magnifies the gap between the largest and smallest values; most importantly, it has a simple derivative with respect to any 𝑧𝑖 . 

The University of Sydney 

## Creating Probabilities Using Softmax 

- Example 1: The task is classifying an image as “dog”, “cat” or “airplane”. If the raw NN outputs are (2.0, 1.0, 0.1), the softmax outputs are (0.659, 0.242, 0.099). Instead of a factor of two between the top two choices, now the ratio is 2.72. 

- Example 2: Same task as above. If the raw NN outputs are (1, 2, 8), the model is more confident in the most likely label than above. The softmax function accentuates that certainty and outputs probabilities of (0.001, 0.002, 0.997). 

The University of Sydney 

## Recap 

- Neural Networks attempt to mimic the structure of the brain 

- Basic building block is the neuron or perceptron 

- Most straightforward NN is the multi-layer perceptron (MLP), which is a feedforward NN 

- Described MSE and cross-entropy loss functions and how to minimize them using training data and SGD 

- Described Convolutional NN as an ML model naturally able to handle 2D (image) inputs. 

- Ended with a discussion of the softmax function. 

The University of Sydney 

See you next week! 



**Survey on this lecture** 


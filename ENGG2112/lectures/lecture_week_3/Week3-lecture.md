ENGG2112 MultiDisciplinary Engineering Semester 2, 2026 _Week 3_ 

**Professor T. J. Lim** 



## What We’re Covering Today 

- What’s a model in the engineering context? 

- How are engineering models described? How did/do we learn the best model for a given system? 

- What do we mean by “AI model”? How do AI models differ from non-AI models? 

- What are the main concepts in machine learning or artificial intelligence? 

### Model in a General Sense 

##### **Dictionary definition** : 

1. A three-dimensional representation of a person or thing or of a proposed structure, typically on a smaller scale than the original. E.g. “a model of St Paul’s Cathedral”. 

2. A thing used as an example to follow or imitate. E.g. “the project became a model for other schemes”. 







The University of Sydney 

### Engineering Models 

- These are closer to the first definition, i.e. **a representation of a thing** . 

- This representation must be useful in engineering design. 

- What are some examples you can think of? 

- Probably model cars, buildings, and digital twins, all of which enable visualisation and some limited amount of design refinement and experimentation. 

The University of Sydney 

### Engineering System Models 

- Apart from models that represent a whole complex “thing” (e.g. a car, a building, a manufacturing process), engineers rely on models of **sub-systems** within that complex thing. 

- These **models allow us to design** those sub-systems through computer simulations, mathematical analysis, lab experiments, etc. and ensure they work. 

- Such models are necessarily mathematical: 

   - A model for the human auditory system would be a filter that suppresses frequencies outside our hearing range and emphasizes and de-emphasizes some frequencies within that range. 

   - A model for how flow rate into a hose impacts the force of water at the other end will account for the diameter of the nozzle. 

The University of Sydney 

### Input-Output Systems 

- In engineering, a **system** takes in one or more **inputs** and produces one or more **outputs** in response to those inputs. 

- A **deterministic system** always responds in the same way to a given input, whereas a random or **stochastic system** does not necessarily give the same output in response to a given input. 

- What examples can you think of for deterministic and stochastic systems? 

- Deterministic: Weighing scale or other measuring device, audio amplifier in a TV, car engine in response to gas pedal. 

- Stochastic: Natural systems with inherent randomness, LLMs and other engineered systems that mimic natural randomness. 



<!-- Start of picture text -->
Input/excitation Output/response<br>System<br><!-- End of picture text -->

The University of Sydney 

### Input-Output Systems – General Mathematical Model 

- From the first lecture, we already saw this model 



<!-- Start of picture text -->
Model<br>inputs 𝑦= 𝑓𝜃 𝑥 outputs<br><!-- End of picture text -->

f𝜃 𝑥 is a function (examples later) – x is usually multi-dimensional, the output of the model y may also be multi-D. 

We need to find the best parameter 𝜃 for the system we’re modelling – this is “training”. 

The University of Sydney 



<!-- Start of picture text -->
Example 1: Discrete-Time Feedforward Model<br>•<br>•<br>frequencies.<br>•<br>output system.<br>2<br>𝑛= 𝑤 𝑥 𝑛−𝑘<br>𝑦 𝑘<br>෍<br><!-- End of picture text -->

### Example 1: Discrete-Time Feedforward Model 

- In this model, x[n] is a sequence of samples of a signal (e.g. audio sampled at 44.1 kHz); y[n] are the samples of the output signal. 

- We can design the weights 𝑤0, 𝑤1 , 𝑤2 to accomplish various functions, e.g. suppressing high frequencies. 

- We can also use it to model an unknown inputoutput system. 

2 **What is θ in this** 𝑛= 𝑤 𝑥 𝑛−𝑘 𝑦 𝑘 ෍ 𝑘=0 **case?** 

The University of Sydney 

### Example 2: Non-Linear Model 



Let’s model a memory-less power amplifier using a hyperbolic tangent function: 𝑦 𝑛= 𝐴⋅tanh 𝑔⋅𝑥 𝑛 

We don’t know the characteristics of this power amplifier but we have the device and can control its input and measure the corresponding output. 

**What are the parameters of the model that we need to learn?** 

_(There’s an interactive demo in HTML that is available on Canvas.)_ 

The University of Sydney 

### Example 3: Neural Network Model 

What are the parameters of the model in this case? How would we make the model more powerful? How do we find the best weights in a given problem? 

Simplest NN model, a multi-layer perceptron (MLP) 

The University of Sydney 

### How Do LLMs Fit in the Above Picture? 

Let’s first watch this video together: Large Language Models explained briefly 

As you’re watching, jot down the terms/concepts that you don’t totally understand. Enter them into this Menti: 



The University of Sydney 

## Basic Terminology 

Data sets 

### Datasets 

- Previously, we had introduced the model 𝑦= 𝑓𝜃 𝑥 , where in the training phase the objective is to find the best value of 𝜃 using the training data available. 

- Training data is organized into rows of 𝑥1, … , 𝑥𝐾, 𝑦 data, assuming 𝐾 scalar inputs (features) and one scalar output (response or label). These are often organized into CSV or Excel files, e.g. 



The University of Sydney 

### Datasets 

- Each row is a **data record** or a **sample** . 

- Depending on the problem some of the columns are **features** , and some are **responses** (or **labels** ). 

- Basically, we’re interested in the machine **estimating** or **predicting** the label from the features. 

- **Inference** is another word for estimation and prediction. 

The University of Sydney 

### Labelled Data for Supervised Learning 

- In supervised learning, the ML model is trained on labelled data, i.e. each training data record has a true y value corresponding to the x values in that record. 

- This true y value is known as the **ground truth** label. 

- The x values are fed into the ML model – these are also known as **features** or **observations.** 



<!-- Start of picture text -->
Features<br>ML Model Label<br>𝑦<br>𝑥1, 𝑥2, … , 𝑥𝑁<br><!-- End of picture text -->

The University of Sydney 

## The AI/ML Pipeline 

End-to-end AI/ML data processing and deployment 



### Overview of the Pipeline 

- AI/ML applications are often described in terms of a “pipeline” of functions, one leading into another. 

- With the monitoring/feedback function, it’s more of a cycle. We’ll explain each part of the cycle next. 

The University of Sydney 

### Data Preparation 

- **Data Collection** : Need to collect the right data for the application. Remember “Garbage In, Garbage Out”. 

   - In this unit, you probably won’t run experiments to collect your own data so you will rely on publicly available data sets. 

   - Be sure to read the overview, description, etc. of the data set you’re downloading. 

   - Academic papers often also provide their data sets freely. In that case, read the paper to understand what the authors did with the data. 

- **Cleaning and Preprocessing** : Data may be missing, corrupted, in the wrong format, noisy, etc. 

   - Usually need to do something to “clean up” the data before using it for training and testing. 

   - More on this later. 

- **Feature Engineering** : Either manually or automatically (through the AI architecture) extract the relevant attributes of the data for processing. 

The University of Sydney 

### Data Split 

- Think of a dataset as a spreadsheet with N rows and K columns 

   - Each row is a sample; each column is a feature or a label. 

   - E.g. in an image application, each sample represents one image in the dataset; the k-th column may be a pixel value corresponding to some position in the image; the final column may be a label such as “dog”, “car”, ”bicycle”. 

- **Training** requires some samples of data but not all. 

   - If we use all samples for training, we have none left for **validation** – this is for deciding whether the current model is good or should be changed. 

   - We also need some for **testing** – this is the final step where the final model is assessed on some other unseen data to see how well it generalizes. 

- If we reuse data in training, validation or testing, there will be “leakage” from the validation and test sets into training, yielding better-than-normal results. 

- Therefore, we split the available data into training/validation/test sets, e.g. 80/10/10. 

The University of Sydney 

### Training & Evaluation 

- Training an ML model is conceptually easy to understand, but mathematically intricate! 

- Define a **loss function** that captures statistically how well the model is predicting the labels. 

   - In regression, some variant of a **mean squared error (MSE)** function works; 

   - In classification, need a **cross-entropy** function. 

- The loss function must be differentiable with respect to the model parameters, θ. 

- We then use some variant of **gradient descent** to minimize the loss function with respect to θ. 

   - Loss function is defined in terms of statistical expectation, i.e. E[…] but this is not knowable with precision. 

   - Therefore, we use averages over the training samples as an approximation, leading to **stochastic gradient descent (SGD)** . 

- _(See Appendix for some technical details, ask AI or your tutor to explain further if you’re interested.)_ 

The University of Sydney 

### Training & Evaluation 

- **Training set** : To adjust parameters for a given model and hyper-parameter setting. 

- **Validation set** : To adjust hyper-parameter settings. 

- **Testing set** : To evaluate performance of final model and settings; if unacceptable, need to re-design from the start, e.g. choose a different model or re-evaluate ML task. 

- How do we evaluate performance in all of the above? We’ll talk about that in a minute. 

   - Accuracy, precision, recall, F1, etc. 

The University of Sydney 

### Deployment & Monitoring 

- AI application needs to be deployed 

   - API, app on a phone, firmware on a microcontroller or DSP chip, etc. 

- **Different constraints** from training/validation/testing in software 

   - Memory, processing speed, real-time requirements 

- **Mismatch** between training and deployment environments, e.g. sensors used in deployment may be noisier than those used in the lab for testing. 

- Hence, **monitoring** of performance is critical after deployment. 

- If it doesn’t work, we need to go back to the first step to re-design the system. 

- - Footnote: Contrary to popular belief, AI systems generally do not learn on-the-fly. The model is static after training and is re-trained periodically. 

The University of Sydney 

## Classification, Regression, Performance Measures 

How do we evaluate performance? Does it depend on the ML task? 

### Classification Versus Regression 

- There are two basic types of problems in ML: **Classification** and **Regression** . 

- In classification, the set of all possible outputs, 𝒮𝓎 , is finite. 

   - Problem is to decide which of a **finite set of classes** the observed features belong to, e.g. whether sensor readings indicate a problem, whether proximity sensors in a car indicate it should brake, whether a robot arm should pick up an object, etc. 

- In regression, the set of possible outputs 𝒮𝓎 is uncountable (and therefore infinite). 

   - Problem is to **estimate the value** of the response to the inputs/features. E.g., predicting amount of rainfall tomorrow based on weather conditions today, estimating the traffic volume at 5pm given various related measurements at 4pm, estimating someone’s age based on a photo, etc. 

- In both cases, the model 𝑦= 𝑓𝜃 𝑥 applies. We note here that classification and regression machines are often capable of producing the output **probability distribution** . 

   - This distribution is very useful – not just one output ( _point estimate_ ) but a range of outputs with probabilities ( _soft estimate_ ). 

The University of Sydney 

### Observation Space and Decision Regions 

- We can visualize input vectors as lying in a geometrical observation space. 

- Think of a 2D slice of that multi-dimensional space and you get something like this → 

- The classification task here is to **decide** which of three classes an observation belongs in. 

- An ML model or any classifier will divide up the observation space into three nonoverlapping decision regions, as illustrated here. 



The University of Sydney 

### Classification Errors 

- Classifiers can make errors – how often does your phone fail to recognize your face? 

- Suppose the crosses belong in the blue class and the stars in the yellow class. 



- Let the slanted line in the middle be the **decision boundary** , i.e. all points to the right are classified as “blue” and all to the left as “yellow”. 

- Because the classifier is not perfect (perhaps it can only create decision boundaries that are straight lines) there will be errors in classification. 

- In this example, 1 out of 6 crosses are incorrectly labelled as yellow, and 1 out of 7 stars as blue. 

- How would we **quantify** the performance of this classifier? 

The University of Sydney 

### Confusion Matrix and Performance Metrics 



The University of Sydney 

### Example 1: Accuracy High But… 

- Here’s a classifier that does a bad job but appears from its accuracy to do a terrific job – 94.5% accuracy! 

- ▪ But precision = 33% means only 1/3 of those it predicted to be positive were actually positive. 

- Recall = 10% means only 1 in 10 truly positive cases were detected. 

- Problem is dataset is heavily skewed towards negative -- classifier can then output “negative” almost all the time, regardless of the input, and still achieve high accuracy. 

The University of Sydney 

### Relative Cost of False Negative and False Positive 

- In many cases, FN does not have the same cost as FP. 

   - Medical diagnosis – FN means patient doesn’t receive timely treatment; FP means patient goes for additional tests ➔ FN is more costly in terms of risk to patient. 

   - Intrusion detection – FN means a security breach is undetected and there may be major costs; FP means human experts are called in for further tests ➔ FN is more costly. 

   - Facial detection for phone unlocking – FN means you have to try again; FP means an unauthorized user is allowed to unlock your phone ➔ FP is more costly. 

- Therefore, depending on application, designer needs to look at the right performance metric. 

- The F1 score is a harmonic mean of Recall and Precision, and balances the two. It can only be high if both are high. 

The University of Sydney 

### Example 2: All Metrics Agree But… 



<!-- Start of picture text -->
•<br>•<br>•<br>•<br>•<br><!-- End of picture text -->

- Now consider a case of balanced data, 500 positive and 500 negative. 

- Classifier correctly identifies positive cases and negative cases at a 70% rate. 

- • Recall, precision, accuracy, F1 are all 0.70. 

- Is this good enough? Depends on application! 

- This is an example of a classifier that is mediocre in both directions. Good candidate for re-design! 

The University of Sydney 

### More Than Two Classes 

#### Predicted Class 

||**A**|**B**|**C**|**D**|
|---|---|---|---|---|
|**A**|85|2|10|3|
|**B**|1|95|1|3|
|**C**|12|1|82|5|
|**D**|2|2|3|93|



In non-binary classification, confusion matrix has this form. 

Accuracy is defined as proportion of correct decisions (green). 

Recall, precision and F1 are now defined on class-by-class basis, or “onevs-rest”. 

The University of Sydney 

### Regression Errors 

- Unlike classification, errors in regression occur with probability one because the output of the ML model and the ground truth label are both continuous, so there is zero probability of the two being identical. 

- Denoting the true label as 𝑦0 and the model output as 𝑦 , the error is 𝑒= 𝑦−𝑦0 . Since we would like the error to be minimized, our goal is often to select the model and the corresponding 𝜃 to minimize the **mean squared error (MSE)** : 

   - 𝜁= 𝐸[ 𝑦−𝑦0<sup>2</sup> ] 

- Here, 𝐸[⋅] denotes the statistical mean operator. Just think of this as the average/mean that you already know. 

- Unlike the classification task, regression tasks generally use only the MSE as a performance measure. 

The University of Sydney 

## What’s Coming Up? _Next Week’s Class_ 

### Week 4 Preview 

- Data pre-processing including one-hot encoding 

- “Classical” ML models 

   - Linear Regression 

   - Naïve Bayes, Random Forest, Logistic Regression, etc. 

   - How to implement them in Python 

- Softmax function 

The University of Sydney 

# See you next week! 


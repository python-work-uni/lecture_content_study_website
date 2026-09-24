ENGG2112 MultiDisciplinary Engineering 

Semester 2, 2026 _Week 4_ 

**Professor T. J. Lim** 



# What We’re Covering Today 

_Data Pre-Processing or Cleaning Stochastic Gradient Descent Classical Machine Learning Methods_ – K nearest neighbours, random forest, naïve Bayes 

- Training 

- Parameters versus Hyper-Parameters 

- Python implementation 

# Data Pre-Processing 

Let’s keep it clean! 

## Importing Data 

- Recall that we have a table of data… 

- Some items might be missing… 

- What do we do? 

Features or labels (K) 



The University of Sydney 

4 

NMKTSE | 2026 | USYD 

## Dealing with Missing Data 

- When analysing real data, we very often encounter missing data, i.e. some cells are blank because the data was not recorded properly. E.g. 



What to do with these cells? 

The University of Sydney 

## Pandas tools for data pre-processing 

- Any missing data is converted to NaN (Not a Number) when loading a file using pandas. 



- NaN is frequently treated as zero, e.g. summing, averaging, etc. 

- This may or may not be sensible of course. 

- • If we want to ignore rows that have any missing data, we use the dropna function: 



The University of Sydney 

6 

## Pandas tools for data pre-processing 

- To find the missing entries in a data frame, we use the isna function. The opposite of this is notna. 





The University of Sydney 

7 

## Pandas tools for data pre-processing 

- We can even fill in the NaN values using a variety of methods through the fillna function. 

- Ref: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.fillna.html#pandas.DataFrame.fillna 



<!-- Start of picture text -->
FoFo r ward ward fill<br>Fill<br><!-- End of picture text -->



<mark>NaN values in the Power(kW) column filled with 200</mark> 

The University of Sydney 

8 

## Other forms of data pre-processing 

- Engineering data often comes in the form of signals measured at regular intervals of time. 

- Important information is often in the frequency domain, with the main differences between two classes appearing as frequency artefacts. 

- Common to “transform” : timedomain → frequency domain, using the Fourier transform (or some other transform). 



The University of Sydney 

## Other forms of data pre-processing 

- Break a long sequence of measurements into short, appropriately sized “windows”. 

Extracting dominant features from signals to differentiate classes is more an art than a science. Using the entire signal can be inefficient and we can often reduce dimensionality through feature engineering. 

- **Feature engineering** is often the step that takes the most time in an ML project. 

   - Feature Selection (picking the best inputs) – looking for the highest correlation with the output 

   - Variance threshold (remove nearly-constant features) 

   - In training separation using Decision Tree or Random Forest ML methods first 

   - Using PCA (Principal Component Analysis) -> captures maximum variance 

   - Manual feature engineering using human insights into data 

The University of Sydney 

## Imbalanced Datasets 

Sometimes, one class is much more prevalent than others, skewing ML training. **This is called imbalanced data.** 

**The trained model will be optimised for finding the majority case** 

E.g. if 95% of the data is “blue” and the performance metric is accuracy, then the model may output “blue” independent of the input and maximize performance. 

Therefore, we need to prevent that. 



The University of Sydney 

## Resampling of Imbalanced Data 

#### **Resampling methods:** 

- Oversampling minority class (e.g., SMOTE – **S** ynthetic **M** inority **O** versampling **TE** chnique). 

- Undersampling the majority class. 

Replicate minority- 

class samples 

The University of Sydney 

## Other Ways to Handle Imbalanced Data 

#### **Cost-Sensitive Learning** 

- Assign higher penalties to costly errors during training. 

- Define a new loss function that reflects the relative costs of FP and FN. 

- ML model adapts by **shifting decision boundary** to reduce the more expensive error. 

- Goal: **Minimise overall cost** , not just improve accuracy. 

**Data augmentation:** Create synthetic but realistic minority class data. 



The University of Sydney 

## One-Hot Encoding of Categorical Variables 

- Features may not be numerical, e.g. airport names, airlines over on the right. 

- Most ML algorithms expect numerical inputs though (otherwise you can’t multiply, etc.) 

- The most basic method for converting such categorical variables into a numeric representation is “one-hot encoding”. 

- We first look at how many values the categorical variable can take, say 𝑀 . 

- Then we create 𝑀 −1 new “dummy” 0/1 variables, with a 1 in the position corresponding to the category. 



The University of Sydney 

## One-Hot Encoding of Categorical Variables 

- Example: Suppose Gender is one of the features, and the allowable values are Male/Female/Not Given. The problem is to estimate the amount spent in a given shop based on gender (as one of the features). 

- - Then we generate two dummy variables, 𝑥 _1 and 𝑥 _2 to represent Male and Female respectively. Note that there’s no need for a 3rd dummy variable because 𝑥 _1= 𝑥 _2= 0 means Gender is in the 3rd category. 

- In the following table, customers 1 and 2 are male, 3 and 4 are female, and 5 is unknown. 



The University of Sydney 

## One-Hot Encoding of Categorical Variables 

- With this, we can now perform regression or classification using the new dummy variables. 

- **Question** : Could we have simply assigned say 0 to Male, 1 to Female and 2 to Unknown? What impact would that have had? 

   - Answer: No, that would be risky and imply an ordinal relationship between the genders, i.e. Male < Female < Unknown. 

The University of Sydney 

## One-Hot Encoding in Python 

- This is the sklearn implementation using the function OneHotEncoder 

- - Returns results in a numpy array, which can be converted into a pandas dataframe if necessary. 



The University of Sydney 

## One-Hot Encoding in Python 

- This implementation uses pandas to create a dataframe with one-hot encoded columns. 



The University of Sydney 

# Classical Machine Learning 

Everything but neural networks 

## Mathematical Foundations of Classification and Regression 

- Assume we don’t know the relationship between x and y (or else the model is already known!). 

- For a given input x, there is some chance that the output y takes a certain value. - E.g. Consider that x encodes the words “The quick brown fox” and y is the next word in the sentence. We might have probabilities 

   - P[y = “jumps” | x] = 0.4; P[y = “walks” | x] = 0.1; P[y = “is” | x] = 0.05, etc. 

   - - If we knew these conditional probabilities, then which output y would we choose if forced to choose only one? 

- Clearly, a detector that knows P[y | x] can output the y that maximizes this function. 

   - In detection theory, this is known as the _maximum a posteriori_ (MAP) detector. 

   - For discrete y (classification), MAP minimizes the probability of making a decision error, i.e. it **maximizes accuracy** . 

- However, how do we find the conditional distribution P[y | x]? 

The University of Sydney 

## Mathematical Foundations of Classification and Regression 

- Either it needs to be learned from training data, or it is derived mathematically from knowledge or assumptions about the system being modelled. 

   - Consider the transmission of a bit over a noisy channel. The bit value is either 0 or 1, and it is received as either 0 or 1, but there is a probability of bit error p, i.e. - P[0 received | 1 transmitted] = P[1 received | 0 transmitted] = p 

   - - If p is known through measurements, then we have the required conditional distribution. 

- In other cases, there isn’t such a simple model that would adequately match reality. - In many applications, especially those involving the mimicking of human cognitive ability, we don’t have sufficient understanding of the underlying process to design a simple accurate model. 

   - That’s why we have general AI/ML models that (sort of) works in many scenarios. 

- We will examine some of the simpler ones next. 

The University of Sydney 

## Did Probabilistic Foundations Influence AI Model Design? 

- The short answer is YES. 

- Explicitly applied in the Naïve Bayes model, which is basically computing the MAP decision with several major simplifying assumptions. 

- Indirectly manifested in the ”soft” outputs created by the softmax function (more on this later). 

- The long answer is more nuanced. 

   - AI/ML has also been developed from the computer science algorithms angle, as we will see when we discuss random forest and K-nearest neighbours (KNN). 

   - However, they still have been designed to output probabilities. 

The University of Sydney 

## Naïve Bayes Model 

- Assume K features 𝑥1, … , 𝑥𝐾 and one discrete feature 𝑦 . This is a classification problem. 

- Bayes rule applied here says 



- For a given vector of observed features 𝑥1, … , 𝑥𝐾 , we want to calculate the distribution of the label 𝑦 using the RHS, then pick the value of 𝑦 that maximizes this distribution. 

- The denominator is irrelevant (just a normalizing constant). 

- 𝑝 𝑦 can be found from training data. 

- But 𝑝 𝑥1, … , 𝑥𝐾|𝑦 is hard to figure out. This is the joint distribution of the features given the label. Given training data, we would in theory have to estimate the relative frequency of each possible 𝑝 𝑥1, … , 𝑥𝐾|𝑦 : 

   - If the features are binary, there will be 2<sup>𝐾</sup> such relative frequencies – there is usually not enough data to get good estimates of the required probabilities. 

The University of Sydney 

Gaussian Naïve Bayes Model – Independence and Gaussian Assumptions 

- The key to progressing to a general inference model are two simplifying assumptions: (a) that all the features are conditionally independent and (b) all the individual conditional feature distributions are Gaussian. 

- Assumption (a) allows us to write 



<!-- Start of picture text -->
Gaussian<br>𝐾<br>𝑝 𝑝 𝑥𝑖|𝑦<br>𝑥1, … , 𝑥𝐾|𝑦= ෑ<br>𝑖=1<br><!-- End of picture text -->

- While Assumption (b) means finding the mean and variance of each feature conditioned on y gives us its distribution. 



<!-- Start of picture text -->
2<br>𝑝 𝑥𝑖|𝑦= 𝐾⋅exp − 𝑥𝑖 − 2𝜇𝑖,𝑦<br>𝜎𝑖,𝑦<br><!-- End of picture text -->

The University of Sydney 

## Gaussian NB 

- For each class 𝑦∈𝒮𝑦 , find mean and variance of each corresponding feature. E.g. if 𝑦 ∈ 0,1 , we may have: 



<!-- Start of picture text -->
𝑦 𝑥1 𝑥2<br>0 0.2 0.9<br>0 -0.6 1.2<br>1 2.4 -1.0<br>1 3.1 -0.6<br>1 2.8 -1.4<br><!-- End of picture text -->

𝜇1,0 = −0.2 𝜇2,0 = 1.05 𝜇1,1 = 2.77 𝜇2,1 = −1.0 Conditional variances can be estimated from the data too. Thus, we have the Gaussian distributions needed. 

The University of Sydney 

## Gaussian NB in Python 

```
From sklearn.naive_bayes import GaussianNB
```

```
nb = GaussianNB() # Give the model a name
```

```
nb.fit(X_train, y_train) # Train the model on training data
y_pred = nb.predict(X_test) # Generate predictions from test
data
```

That’s it really! In scikit-learn, almost all ML models are trained using `<xyz>.fit` and inference using the model invokes `<xyz>.predict` , where `<xyz>` is the name of your model. 

Upon first definition, `<xyz>` needs to be given the right hyper-parameter values (in GNB, there happen to be none). 

The University of Sydney 

## Gaussian NB Parameters 

- From the training data, we estimate the conditional means and variances of every feature conditioned on each class label. 

- These are the **parameters** of the Gaussian NB model. 

- There are no hyper-parameters as the structure of the Gaussian NB model is entirely determined by the number of features and the number of classes the label can take. 

The University of Sydney 

## Random Forest – Decision Tree Concept 

- Unlike the Gaussian NB, the random forest is a model derived from a computer science perspective. 

- Based on concept of a decision tree, e.g. 

- At each level of a tree, we ask a question that splits 

- the data into two parts 

- For a given data sample, traversing the whole 

- tree from top (root) to bottom (leaf) yields 

- the final decision at the leaf node. 

- In a random forest, we run in parallel 

- a number of trees, then take a 

- majority decision. 

The University of Sydney 

## Random Forest – Specifications 

- For each decision tree, the following are the key hyper-parameters set by us humans: a. The maximum depth (levels) of the tree ( `max_depth` ); 

   - b. How many features to choose from at each node ( `max_features` ); 

   - c. The quality measure used in splitting ( `criterion` ). 

- In the training phase the following parameters are optimized by the machine: a. Which feature to split on at each node; 

   - b. Threshold value to use for the split at each node. 

- The main idea is that at each node, ideal split of data results in only one class label per branch – in that case, no further splitting is needed. We just need to find: 

   - Which feature to use at each node, and what threshold to use, that would bring us as “close” to that ideal as possible. 

   - - The measure of closeness is the `criterion` hyper-parameter – either a Gini impurity or entropy. 

- We will illustrate this in class with a worked example. 

The University of Sydney 

## Random Forest – Randomization is Key 

- Problem with relying on a single tree is that it may overfit the training data, i.e. perform very well on the training data but not generalize. 

- In a random forest, we avoid this problem by using many decision trees, each one randomized (and so different from each other) in the following ways: 

   - **Bagging (bootstrap sampling),** i.e. each tree trains on a different resampled dataset. 

   - **Random feature subsets** at each split, i.e. every node is allowed to only investigate m out of p features, chosen randomly and independently. 

- The randomization prevents different trees turning out the same as each other and defeating the purpose of introducing multiple trees. 

   - Rather clever! 

The University of Sydney 

## Random Forests and Python ☺ 

```
from sklearn.ensemble import RandomForestClassifier
```

- `# Create Random Forest model with chosen hyper-parameters RF = RandomForestClassifier(n_estimators = 100, max_depth = 5)` 

- `# Train with training data RF.fit(X_train, y_train)` 

- `# Infer labels in test data Y_pred = RF.predict(X_test)` 

- `# Compute performance, plot charts, etc.` 

The University of Sydney 

## Supervised Machine learning: K Nearest Neighbour 

- We have **N training samples** (xi, yi)  i = 1 … N. 

- yi are **class labels** : they take on a limited number of possible values. 

- _In the example, each point belongs to a category such as “bee,” “cat,” or “dragonfly.”_ 

- Xi are **feature vectors** : in this case, each has **two dimensions** , so we can represent them on a 2D Cartesian plane. 



https://medium.com/swlh/k-nearest-neighbor-ca2593d7a3c4 

The University of Sydney 

### Supervised Machine learning: K Nearest Neighbour 

1. Set parameter 𝐾 to an odd value, say 5. 

2. Denote training feature vectors by 𝐱𝑖𝑚 , where 𝑚∈ ℳ is the class label (or category) and 𝑖 the sample index. 

3. For a new feature vector 𝐱 , compute the 𝑁 distances where 𝑁 is the number of training data records: 

2 𝑚 𝑑𝑖 𝐱= 𝐱−𝐱𝑖 , 𝑖= 1, … , 𝑁 

4. Sort from smallest to largest, and note the 𝐾 smallest values and their class labels. 

5. Classifier output is the class label with highest count. 



The University of Sydney 

### Supervised Machine learning: K Nearest Neighbour 

- In an illustrated example, when K=3, the, classifier output is “triangle”. 

- But when 𝐾 = 5 , classifier output is “square”. 

- Choice of K is important but there is no formulaic way to choose it well for any given data set. 

   - -Note that K does not impact **computational complexity** – we always have to compute all N distances. It does impact **classifier accuracy** . 

   - -As complexity grows with N, best not to use “too many” training samples. 



- Distance measure need not be 𝐿2 (Euclidean). May also be Hamming (= no. of positions where two vectors differ), 𝐿1 , etc. 

The University of Sydney 

## KNN: Imbalanced Data 

- We can have an imbalanced data problem, i.e. one class dominates the training set, e.g. 90% of the training data are of class 0, only 10% of class 1. _(See example on right)_ 

- Suppose test feature is the <mark>yellow triangle.</mark> Though visually it looks like it’s in the orange class, KNN may return an output of blue because there are more blue neighbours! 

- Solution: Give nearer neighbours higher “weight” in the count. 



The University of Sydney 

## Weighted Nearest Neighbour 

To be precise: 

1. Find the K training points closest to the test point and their distances to the test point, 𝑑𝑖 𝐱 , 𝑖∈ℐ𝐾 𝐱 , where ℐ𝐾 𝐱 is the set of K training indices having smallest distance to 𝐱 . 

1 

2. Group those K points according to class. For class n, compute 𝑁𝑛 = σ𝑖 𝑑𝑖 𝐱<sup>,</sup> 

where we’re only summing over the points in class n. 

3. Classifier output is the value of n that maximizes 𝑁𝑛 . 

The University of Sydney 

## Weighted Nearest Neighbour 

𝑁0 = 4.5 





<!-- Start of picture text -->
𝑁1 = 2.92<br><!-- End of picture text -->

- Example: Suppose K = 5, and we have the following distances from the test point to the 5 nearest neighbours: 

|**Point**|**1**|**2**|**Triangle**|**3**|**4**|**5**|
|---|---|---|---|---|---|---|
|Class|**0**|**0**|**?**|**1**|**1**|**1**|
|Distance|0.5|0.4|-|1.0|0.8|1.5|
|Inverse of dist.|1|1|-|1|1|1|
||0.5|0.4||1|0.8|1.5|
|WNN count|2|2.5|?|1|1.25|0.67|



- KNN: 𝑁0 = 2 ; 𝑁1 = 3 ∴ output class = 1 

- WNN: max sum 𝑁0 = 2 + 2.5 = 4.5 ; 𝑁1 = 1 + 1.25 + 0.67 = 2.92 , ∴ output class = 0 

The University of Sydney 

## KNN and WNN: Probabilities 

- We’re also interested in knowing the probability that a given input belongs in each possible class. More formally, it would be nice to know 𝑃[𝐶𝑖|𝐱] , where 𝐶𝑖 denotes the i-th class and 𝐱 is the vector of input features. 

- This expression is read **_:_** 

   - _“The probability of the correct class being_ 𝐶𝑖 **_<u>given</u>_** _that the observed features are_ 𝑥 _”._ 

- It is what’s called a **conditional probability** . 

- In both KNN and WNN, we can argue that 

𝑁𝑖 𝑃[𝐶𝑖|𝐱] = σ𝑘 𝑁𝑘 

where 𝑁𝑖 is either the weighted or unweighted count of the nearest neighbours in class 𝐶𝑖 . 

The University of Sydney 

## KNN and WNN: Probabilities 

- To continue with the last example, the WNN estimate of the probabilities of the two classes are: 

4.5 2.92 𝑃 𝐶0 𝒙= 4.5+2.92<sup>=0.606AND𝑃</sup> 𝐶1 𝒙= 4.5+2.92<sup>=0.394</sup> 

- The KNN estimates of the probabilities of the same events are: 

2 3 𝑃𝑘𝑛𝑛 𝐶0 𝒙= 5<sup>=0.4AND𝑃𝑘𝑛𝑛</sup> 𝐶1 𝒙= 5<sup>=0.6</sup> 

- If we use some other classifier, the estimated probabilities will be different again. Hard to argue that one result is more accurate than another. 

The University of Sydney 

## Normalisation 

- Another problem is that the dynamic range of one feature may be vastly different from that of another. E.g. 

   1. Engine capacity (in cc) versus model year; 

   2. Age (in years) versus height (in cm); 

   3. Bit rate (in bps) versus transmitted power (in mW); etc. 

So we should normalise to a standard scale, e.g. min-max normalisation: 



This maps the original values to a new range, usually between 0 and 1. 

The function `preprocessing.sklearnnormalize` implements this normalisation algorithm. 

The University of Sydney 

## KNN and WNN in Python 

In **sklearn** , we can easily execute KNN and WNN using the **KneighborsClassifier** function. 

Import required libraries: 



Define classifier objects: 



Fit the model using training data, and test it using test data 



The University of Sydney 

## Scikit-Learn for Supervised Learning 

- In almost all supervised ML functions in `sklearn` , we take the following steps: 1. Create an object for the desired ML algorithm using the appropriate class; 2. Use the `fit` method to train the model; 

   3. Use the `predict` method to estimate the class of the test data samples; 4. Use the `predict_proba` method to estimate the probability of each class given the input features; 

   5. Test the accuracy of the algorithm using one or more of the `metrics` . 

The University of Sydney 

## KNN/WNN in the General ML Model 

- Remember that we said an ML model is a function 𝑓𝜃(𝑥) that outputs the class label corresponding to the input variables x, where 𝜃 is the parameter vector. 

- In KNN and WNN, there are no obvious parameters to optimise; instead the training data is used to create decision regions. 

- We can consider the decision boundaries (i.e. borders between adjacent decision regions) to be the “parameters”. 

- The parameter _K_ (no. of nearest neighbours) is a **<u>hyperparameter</u>** that determines the exact form of the model. 

- Hyperparameters are not learned or updated during the optimisation process. They are set before training begins. They are fixed values that determine the overall architecture and behaviour of the model. 

The University of Sydney 

More on Validation and Testing 

## Training, Validation and Testing Split 



The University of Sydney 

## Validation 

- In this step, labelled data that has not been used in training is used to determine how good the current model is. 

   - Hyper-parameters of the model, and even the model itself, are adjusted and iterated in a training-validation cycle until the designer is satisfied. 

- Often, validation is not done just once for each setting but instead performance is averaged over multiple validation steps, called **cross-validation** . 

   - Most commonly, we use K-fold cross-validation. 

   - See five-fold cross-validation illustration on next page. 

   - Implemented using 

```
from sklearn.model_selection import StratifiedKFold
cv = StratifiedKFold(n_splits = 5)
```

The University of Sydney 



The University of Sydney 

## Testing After Validation 

- Once the right model is chosen after validation, the final step is to test it on the final set of data that has not been used, the test set. 

- The performance of the trained and validated model on the test dataset is what should be reported. 

   - This is the performance we expect after deployment, when data that has not been seen in training or validation is presented to the model. 

The University of Sydney 

What’s Coming Up? _Next Week’s Class_ 

## Week 4 Preview 

- Focus is on neural networks, the most important class of AI/ML model in use today 

   - Basic concepts 

   - Different sorts of NNs 

   - Why differentiability is key 

   - Example applications 

The University of Sydney 

See you next week! 



**Survey on this lecture** 


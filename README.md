# S2-graph-based-Active-Learning
S2: An efficient graph based active learning algorithm with application to nonparametric classification

This is an implementation of the algorithm described in the paper: 
[S2: An efficient graph based active learning algorithm with application to nonparametric classification](http://proceedings.mlr.press/v40/Dasarathy15.pdf)

Here is a trial run of the algorithm when both classes have almost equal number of elements. A Low budget is provided where its not possible to "zip" through the whole decision boundary. After S2 is run, the obtained boundary is then passed onto a label completeion algorithm as described in the paper.  

![](gif1.gif)

Here is the trial run of the algorithm when one class has more number of elements compared to the other and you are given a high budget. Here the algorithm has high enough budget to "zip" through the whole decision boundary. 

![](gif2.gif)

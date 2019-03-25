# S2-graph-based-Active-Learning
S2: An efficient graph based active learning algorithm with application to nonparametric classification

This is an implementation of the algorithm described in the paper: 
[S2: An efficient graph based active learning algorithm with application to nonparametric classification](http://proceedings.mlr.press/v40/Dasarathy15.pdf)

Here is a trial run of the algorithm when both classes have almost equal number of elements. A Low budget is provided where its not possible to "zip" through the whole decision boundary. After S2 is run, the obtained boundary is then passed onto a label completeion algorithm as described in the paper.  

![](gif1.gif)

Here is the trial run of the algorithm when one class has more number of elements compared to the other and you are given a high budget. Here the algorithm has high enough budget to "zip" through the whole decision boundary. 

![](gif2.gif)

# Coarsened version of S2

When the graph is very big, S2 algorithm does not get a complete picture of the decision boundary as it can tend it to be very myopic. This is illustrated by performing S2 on a graph and feeding it to a label-completeion algorithm such as the [ZLG](http://mlg.eng.cam.ac.uk/zoubin/papers/zgl.pdf). We can notice that the prediction of labels tends to be very uneven:

![](S2_ZLG.png) 
The series of blue dots indicate the queried points when S2 is performed. 

The ground truth labelling is as below: 
![](S2_gt.png)

However, when we coarsened the graph by 3 levels in this case, we observe that the the labels output by ZLG is much closer to the ground-truth and consequently captures the decision boundary in a better fashion. Coarsening is a very useful strategy when the budget is very less. It helps to get a "broader" picture of the decision boundary:

![](coarsened_S2_ZLG.png)

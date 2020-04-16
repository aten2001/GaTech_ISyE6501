#################### data prep #################### 

# import libraries for knn
install.packages("kknn")
library(kknn)

set.seed(123) # set seeds for reproducibility
data <- read.delim("credit_card_data-headers.txt", header=TRUE) # read data

#################### KNN #################### 
# generating knn function with arg for number of neighbors
# the algorithm loops over each data point by excluding itself from the computation
# data are scaled
# generating predictions and calculating %correct

knn = function(kn){
pred <- rep(0,(nrow(data)))
for (i in 1:nrow(data)){
model = kknn(R1~., data[-i,], data[i,], k=kn, scale = TRUE)
pred[i] <- as.integer(fitted(model)+0.5)
}
correct = sum(pred == data[,11]) / nrow(data)
return(correct)
}

# using the knn function to try values of neighbors in [0,20]
correct=rep(0,20)
for (val in 1:20){
correct[val] = knn(val)
}

# finding max fit and corresponding number of neighbors
# the max is reached at 12 with a fit of 85.32%
pred_best <- max(correct)
nn_best <- which.max(correct)
print(pred_best)
print(nn_best)
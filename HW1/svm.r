#################### data prep #################### 

# import libraries for ksvm
install.packages("kernlab")
library(kernlab)


set.seed(123) # set seeds for reproducibility
data <- read.delim("credit_card_data-headers.txt", header=TRUE) # read data

#################### SVM #################### 
# generating a function for a SVM with args for lambda, kernel type
# lambda is the weight on the margin
# larger values of lambda emphasize margin-max over error error-min

## analysis ##
# we tried out four kernel types, linear (vanilladot) and nonlinear (anovadot, rbfdot, polydot)
# for each kernel type, we specified values of lambda in powers of 10
# for the linear kernel, lambda = 1, 10, 100 all give 86.39% correct guesses
# for lambda = 1000=10000, perc. correct guesses decreases slightly to 86.23% with a much more SVs
# for anovadot, lambda=10000 yields 90.83% correct guesses (max perc. correct for powers of 10)
# in general, nonlinear kernels display higher predictive performance as expectated

svm <- function(type, lambda){

# the SVM model is scaled
model <- ksvm(as.matrix(data[,1:10]), as.factor(data[,11]), type="C-svc", kernel=type, C=lambda, scaled=TRUE)

# calculating coefficients and intercept
a <- colSums(model@xmatrix[[1]]*model@coef[[1]]) 
a0 <- -model@b 

# calculating model predictions
pred <- predict(model,data[,1:10])

# calculating percent correct guesses
correct = sum(pred == data[,11]) / nrow(data)

# printing results
print(model)
print(a)
print(a0)
print(pred)
print(correct)
}
# iterative fibbonacci
# example from https://www.youtube.com/watch?v=Igh-vBI2LXc
# adapted to be first N instead of infinite
var_0 = 0
var_1 = 1
print("Input a Number:")
N_ITER = input()
while (N_ITER > 0):
    print(var_0)
    var_2 = (var_0) + (var_1)
    var_0 = var_1
    var_1 = var_2
    print(" ")
    N_ITER = (N_ITER) - (1)

print('\\nHello, World!\\n')
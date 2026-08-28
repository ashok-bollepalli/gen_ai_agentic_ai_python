import numpy as np

arr1 = np.array([10, 20, 30])

arr2 = np.array([
    [10, 20, 30],
    [40, 50, 60]
])

arr3 = np.array([
    [[10, 20], [30, 40]],
    [[50, 60], [70, 80]]
])

print(arr1.ndim)
print(arr2.ndim)
print(arr3.ndim)

print(arr2.shape)
print(arr2.size)
print(arr2.dtype)

arr4 = np.array([10, 20, 30, 40, 50, 60], dtype=float)
print(arr4)

print(arr4[0])
print(arr4[-1])

print(arr2[0, 0])

print(arr4[0:4])

arr = np.zeros(5)
print(arr)

arr = np.zeros((2, 3))
print(arr)

arr = np.ones(5)
print(arr)

arr = np.ones((2, 3))
print(arr)

arr = np.full(5, 10)
print(arr)

arr = np.full((2, 3), 8)
print(arr)

arr = np.arange(1, 11)
print(arr)

arr = np.arange(1, 11, 2)
print(arr)

arr = np.arange(1, 13, 2)
arr = arr.reshape(2, 3)
print(arr)

arr = np.random.randint(1, 9, 5)
print(arr)

arr = np.random.rand(5)
print(arr)

arr = np.array([
    [10, 20, 30],
    [40, 50, 60]
])

arr = arr.flatten()
print(arr)

######################

arr = np.array([10, 20, 30])
print(arr + 5)
print(arr - 5)
print(arr * 2)
print(arr / 2)

a = np.array([10, 20, 30])
b = np.array([1, 2, 3])

print(a + b)
print(a - b)
print(a * b)
print(a / b)

arr = np.array([10, 20, 30, 40, 50])

print(np.sum(arr))
print(np.mean(arr))
print(np.median(arr))
print(np.min(arr))
print(np.max(arr))
print(np.std(arr))
print(np.var(arr))

classA = np.array([48, 49, 50, 51, 52])  # mean is 50
classB = np.array([20, 40, 50, 60, 80])  # mean is 50

print(np.mean(classA))
print(np.mean(classB))

print(np.std(classA))
print(np.std(classB))

# Both classes have the same average (50).
# Class A students performed consistently.
# Class B students' performance varies a lot.


p1_stock_returns = [10, 11, 9, 10, 10]
p2_stock_returns = [2, 20, -5, 25, 8]

print(np.mean(p1_stock_returns))
print(np.mean(p2_stock_returns))

print(np.std(p1_stock_returns))
print(np.std(p2_stock_returns))

arr1 = np.array([10, 20, 30])
arr2 = arr1.copy()

arr2[0] = 100
print(arr1)
print(arr2)

arr1 = np.array([10, 20, 30])
arr2 = arr1.view()

arr2[0] = 300

print(arr1)
print(arr2)

arr = np.array([10, 20, 30, 40, 50])
result = arr[arr > 25]
print(result)

arr = np.array([1, 2, 3, 4, 5, 6])
even_numbers = arr[arr % 2 == 0]
print(even_numbers)

arr = np.array([40, 10, 30, 20])
result = np.sort(arr)
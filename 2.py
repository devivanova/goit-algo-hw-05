def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    iterations = 0
    upper_bound = None

    while left <= right:
        iterations += 1
        mid = (left + right) // 2

        if arr[mid] == target:
            return (iterations, arr[mid])

        elif arr[mid] < target:
            left = mid + 1
        else:
            upper_bound = arr[mid]
            right = mid - 1

    return (iterations, upper_bound)


sorted_array = [0.5, 1.2, 1.5, 2.3, 3.8, 5.0, 6.7]
target = 2.0

result = binary_search(sorted_array, target)
print(f"Кількість ітерацій: {result[0]}, Верхня межа: {result[1]}")

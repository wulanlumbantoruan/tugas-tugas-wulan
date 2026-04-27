# Nomor 3
def hybrid_search(arr, target):
    # tidak terurut 
    i = 0
    while i < len(arr) and (i == 0 or arr[i] >= arr[i - 1]):
        if arr[i] == target:
            return i
        i += 1

    # terurut 
    left, right = i, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1

# terurut
print('Pada data terurut, indeks data 28 adalah:',hybrid_search([5, 3, 1, 2, 10, 12, 15, 20, 25, 28, 30], 28))
# tidak terurut
print('Pada data tidak terurut, indeks data 28 adalah:',hybrid_search([90, 12, 18, 11, 55, 28, 12, 72, 9, 11, 7], 28))
# Nomor 4
def modified_binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        
        if arr[left] <= arr[mid]:
            if arr[left] <= target < arr[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            if arr[mid] < target <= arr[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1

# ditemukan
print('Ditemukan: ',modified_binary_search([10, 15, 1, 5, 7, 12], 5))
# tidak ditemukan
print('Tidak ditemukan: ',modified_binary_search([10, 15, 1, 5, 7, 12], 20))

"""
Mencari indeks pertama dan terakhir dari suatu angka dalam array menggunakan algoritma Binary Search. Array harus dalam keadaan terurut.
"""
# Nomor 1
def find_first_and_last(arr, target):
    def find_first(arr, target):
        left, right = 0, len(arr) - 1
        first_index = -1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == target:
                first_index = mid
                right = mid - 1  # kiri
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return first_index

    def find_last(arr, target):
        left, right = 0, len(arr) - 1
        last_index = -1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == target:
                last_index = mid
                left = mid + 1  # kanan
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return last_index

    first = find_first(arr, target)
    last = find_last(arr, target)
    
    return (first, last)

# misal
arr = [1, 2, 2, 2, 2, 3, 4, 4, 5]
target = 4
print(find_first_and_last(arr, target)) 
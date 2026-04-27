
# Kasus 1: Mengeluarkan Output "I am Data Scientist" 10 Kali
# Program menggunakan for:
for i in range(10):
    print("I am Data Scientist")


# Program menggunakan while:
i = 0
while i < 10:
    print("I am Data Scientist")
    i += 1


# Kasus 2: Menghitung Banyaknya Digit Angka
# Program menggunakan while:
number = int(input("Input: "))
count = 0
while number > 0:
    number //= 10
    count += 1
print("Output:", count)


# Program menggunakan for:
number = input("Input: ")
count = 0
for digit in number:
    count += 1
print("Output:", count)


# Kasus 3: Menghitung Penjumlahan Digit Angka
# Program menggunakan while:
number = int(input("Input: "))
total_sum = 0
while number > 0:
    total_sum += number % 10
    number //= 10
print("Output:", total_sum)


# Program menggunakan for:
number = input("Input: ")
total_sum = 0
for digit in number:
    total_sum += int(digit)
print("Output:", total_sum)


# Kasus 4: Menghitung Nilai Faktorial
# Program menggunakan while:
number = int(input("Input: "))
factorial = 1
i = 1
while i <= number:
    factorial *= i
    i += 1
print("Output:", factorial)


# Program menggunakan for:
number = int(input("Input: "))
factorial = 1
for i in range(1, number + 1):
    factorial *= i
print("Output:", factorial)


# Kasus 5: Menghitung Pangkat (nth) dari Sebuah Bilangan
# Program menggunakan while:
base = int(input("Input 1: "))
exponent = int(input("Input 2: "))
result = 1
count = 0
while count < exponent:
    result *= base
    count += 1
print("Output:", result)


# Program menggunakan for:
base = int(input("Input 1: "))
exponent = int(input("Input 2: "))
result = 1
for i in range(exponent):
    result *= base
print("Output:", result)

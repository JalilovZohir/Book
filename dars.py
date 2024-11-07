def main(numbers):
  a = 1
  i = 0
  while i < len(numbers):
    a *= numbers[i]
    i += 1
  result = [0]
  i = 0
  while i < len(numbers):
    result[i] = a // numbers[i]
    i += 1
  return result
print(main([3,27,4,2]))
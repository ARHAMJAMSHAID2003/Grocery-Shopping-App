t = int(input())
result = []
for x in range(t):
    n = int(input())
    arr = list(map(int,input().split()))
    arr.sort(reverse=True)
    arr2 = []
    sum = 0
    for y in range(n):
        arr2.append(arr[y])
        sum+=max(arr2)
    result.append(sum)
    
for x in range(t):
    print(result[x])
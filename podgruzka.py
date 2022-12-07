a, b, c = map(int, input().split())
a_h, b_h, c_h = map(int, input().split())
k = 0
s = a_h + b_h + c_h
a_values = [a_h]
b_values = [b_h]


for i in range(int((c_h // (c / a)))+1):
    for j in range(int(b_h // (b / a))+1):
        a_values.append(a_h + (c_h - c*i) + (b_h - b*j))

for i in a_values:
    for j in range(int(c_h // (c / b))+1):
        b_values.append(b_h + (c_h - c*i) + a)

a_values = list(set(a_values))
b_values = list(set(b_values))
print(len(a_values)+len(b_values))
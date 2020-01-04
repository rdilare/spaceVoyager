


a = list(range(10))
i = 0
while i!=len(a):
	print(i)
	if a[i]%2==0:
		e = a[i]
		a.remove(e)
	else:
		i+=1

print(a)

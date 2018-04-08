def mergesort(a,left,right)
	if left==right return end
	mid = (left+right)/2
	mergesort(a,left,mid)
	mergesort(a,mid,right)
	return
end
cc=Array(2)
cc[0]=1
cc[1]=2
mergesort(cc,0,2)
ee=cc[0]
print(ee)
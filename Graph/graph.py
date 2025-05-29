import random
fin1= open("graph.in","w")
fout= open("graph.out","w")
values=[0,1]
n=random.randint(5,10)
a=[[values[random.randint(0,1)]if(i!=j) else 0 for i in range(n)  ]for j in range(n)]
# Generating a random graph, with 0's on the main diagonal
print("s a generat")
def ScriereMinFile(a,n):
    for i in range(n):
        for j in range(n):
            print(a[i][j], file=fin1, end=" ")
        print("", file=fin1)
    fin1.close()
ScriereMinFile(a,n)
fin=open("graph.in","r")
lines = fin.readlines()
ct=1
for line in lines:
     numbers=[int(i) for i in line.split()]
     for i in range(n):
         if numbers[i]:
             print(f"{ct}-{i+1}", file=fout)
     ct+=1


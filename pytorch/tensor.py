import torch

x = torch.Tensor([5,3])
y = torch.Tensor([2,1])

print("x = ",x ,"\n")

print("y = ",y ,"\n")

print("x*y = ",x*y,"\n")

z = torch.zeros([2,5])

print("z = ",z,"\n")

print("z shape = ",z.shape,"\n") 

b = torch.rand([2,5])

print(" b = torch.rand([2,5]) = ",b,"\n")

print("b.view([1,10]) = ")

print("b = ",b,"\n")

a = b.view([1,10])

print("a = b.view([1,10])")

print("a = ",a)

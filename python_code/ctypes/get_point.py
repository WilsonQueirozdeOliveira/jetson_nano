import ctypes

# Define the Point struct in Python
class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_float), ("y", ctypes.c_float)]

# Load the shared library
lib = ctypes.CDLL('./libpoint.so')

# Declare the function signature
get_point = lib.get_point
get_point.restype = Point
get_point.argtypes = []

# Call the function and convert the result to a Python tuple
p = get_point()
result = (p.x, p.y)

# Print the result
print(result)

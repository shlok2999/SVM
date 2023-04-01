import multiprocessing
import time
import numpy as np

# def my_function(x):
#     # Your code for the function
#     # print(type(x))
#     y = int(x)
#     print(y*y, type(y))
#     print(x)
#     return x


def my_function(n, m):
	# n1 = int(n)
	matrix1 = np.random.rand(n, m)
	matrix2 = np.random.rand(m, n)
	result = np.dot(matrix1, matrix2)
	print(result)
	return result


if __name__ == '__main__':
    
    start_time = time.time()

    my_function(3,6)
    my_function(6,9)
    my_function(9, 12)
    my_function(12, 15)

    # p1 = multiprocessing.Process(target=my_function, args=(3,6))
    # p2 = multiprocessing.Process(target=my_function, args=(6,9))
    # p3 = multiprocessing.Process(target=my_function, args=(9,12))
    # p4 = multiprocessing.Process(target=my_function, args=(12,15))

    

    
    # p1.start()
    # p2.start()
    # p3.start()
    # p4.start()

    
    # p1.join()
    # p2.join()
    # p3.join()
    # p4.join()

    
    end_time = time.time()

    
    print(f"Execution time: {end_time - start_time} seconds")

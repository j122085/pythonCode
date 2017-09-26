import numpy as np
import tensorflow as tf
tensor_1d=np.array([1.3,1,4.0,23.99])
tf_tensor=tf.convert_to_tensor(tensor_1d,dtype=tf.float64)
with tf.Session() as sess:
    print(sess.run(tf_tensor))
    print(sess.run(tf_tensor[0]))
    print(sess.run(tf_tensor[1]))
tensor_2d=np.array([(1,2,3,4),(5,6,7,8),(9,10,11,12),(13,14,15,16)])
print(tensor_2d)
print(tensor_2d[3][3])
print(tensor_2d[0:2,0:2])

matrix1=np.array([(2,2,2),(2,2,2),(2,2,2)])
matrix2=np.array([(1,1,1),(1,1,1),(1,1,1)])
print(matrix1)
print(matrix2)
matrix1=tf.constant(matrix1)
matrix2=tf.constant(matrix2)



#矩陣相乘
matrix_product=tf.matmul(matrix1,matrix2)
#矩陣相家
matrix_sum=tf.add(matrix1,matrix2)
matrix_3=np.array([(2,7,2),(1,4,2),(9,0,2)],dtype='float32')
print(matrix_3)
#determinant 矩陣行列式
matrix_det=tf.matrix_determinant(matrix_3)
with tf.Session() as sess:
    result1=sess.run(matrix_product)
    result2=sess.run(matrix_sum)
    result3=sess.run(matrix_det)
    print(result1)
    print(result2)
    print(result3)
tensor_3d=np.array([[[1,2],[3,4]],[[5,6],[7,8]]])
print(tensor_3d)
#tensor_3d[plane,row,col]

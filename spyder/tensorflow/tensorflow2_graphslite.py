import matplotlib.image as mp_image
filename=r'D:\Data\GraphData\circle\35331817_p0_master1200.jpg'
input_image=mp_image.imread(filename)
print('input dim={}',format(imput_image.ndim))
print('input shape={}',format(input_image.shape))
import matplotlib.pyplot as plt
plt.imshow(input_image)
plt.show()


#切割 高切50-250 寬沒切(-1)
import tensorflow as tf
my_image=tf.placeholder('uint8',[None,None,3])
slice=tf.slice(my_image,[50,0,0],[250,-1,3])
with tf.Session() as session:
    result=session.run(slice,feed_dict={my_image:input_image})
    print(result.shape)
plt.imshow(result)
plt.show()

#轉向 (1跟0交換)
x=tf.Variable(input_image,name='x')
model=tf.initialize_all_variables()
with tf.Session() as session:
    x=tf.transpose(x,perm=[1,0,2])
    session.run(model)
    result=session.run(x)
plt.imshow(result)
plt.show()



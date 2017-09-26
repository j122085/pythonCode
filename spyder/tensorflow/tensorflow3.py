#=x=complex(5,4)   1j=根號-1 4j=根號-4
x=5.+4j
print(x)
print(x.real)
print(x.imag)
import tensorflow as tf
import numpy as np
Y,X =np.mgrid[-1.3:1.3:0.005,-2:1:0.005]
Z=X+1j*Y
c=tf.constant(Z.astype(np.complex64))

zs=tf.Variable(c)
ns=tf.Variable(tf.zeros_like(c,tf.float32))
sess=tf.InteractiveSession()
tf.initialize_all_variables().run()
zs_=zs*zs+c
not_diverged=tf.abs(zs_)<4
step=tf.group(zs.assign(zs_),\
              ns.assign_add(tf.cast(not_diverged,tf.float32)))

for i in range(200) :step.run()
plt.imshow(ns.eval())
plt.show()


Y,X=np.mgrid[-2:2:0.005,-2:2:0.005]
Z=X+1j*Y
Z=tf.constant(Z.astype('complex64'))
zs=tf.Variable(Z)
ns=tf.Variable(tf.zeros_like(Z,'float32'))
sess=tf.InteractiveSession()
tf.initialize_all_variables().run()
c=complex(0.0,0.75)
zs_=zs*zs-c
not_diverged=tf.abs(zs_)<4
step=tf.group(zs.assign(zs_),\
              ns.assign_add(tf.cast(not_diverged,"float32")))
for i in range(200):step.run()
plt.imshow(ns.eval())
plt.show()
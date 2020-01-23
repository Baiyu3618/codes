#############################################################################
# backpropagation example problem solved using python                       #
# source:                                                                   #
# https://mattmazur.com/2015/03/17/a-step-by-step-backpropagation-example/  #
# developed using numpy module                                              #
#                                                                           #
# NOTE: This script will be a bit comprehensive as it is my first machine   #
#       learning script using neural networks                               #
#############################################################################

########################################
# Neural Network schematic diagram     #
#                                      #
# ip1 -----------> h1 -----------> op1 #
#     \_        _/   \_        _/      #
#       \_    _/       \_    _/        #
#         \__/           \__/          #
#          _\_            _\_          #
#        _/   \_        _/   \_        #
#      _/       \_    _/       \_      #
#     /           \  /           \     #
# ip2 -----------> h2 -----------> op2 #
########################################


import numpy as np

# functions definition----------------------------------------------------------
sigmoid = lambda x: 1.0/(1.0 + np.exp(-x)) # activation function

# inputs and outputs definition ------------------------------------------------
ip = np.array([0.05, 0.10])
op = np.array([0.1, 0.5])

# neural network parameters-----------------------------------------------------
n_hidden_layers = 1             # no of hidden layers
n_Ni = n_Nh = n_No = 2          # no of neurons in input, output and hide

w = np.zeros(8)                 # weights and its initial values
w[0] = 0.15; w[1] = 0.2
w[2] = 0.25; w[3] = 0.3

w[4] = 0.4;  w[5] = 0.45
w[6] = 0.5;  w[7] = 0.55

b = np.array([0.35, 0.60])      # bias values,(common for each layer, so only 2)

eta = 0.5                       # learning rate
iteration = 10000                # no of iterations

# training section--------------------------------------------------------------
for itr in range(iteration):
    # feed forward with existing weights
    # node h1:
    net_h1 = w[0]*ip[0] + w[1]*ip[1] + b[0] # net total input value to neuron h1
    out_h1 = sigmoid(net_h1)                # output value of neuron h1
    
    # node h2:
    net_h2 = w[2]*ip[0] + w[3]*ip[1] + b[0] # net total input value to neuron h2
    out_h2 = sigmoid(net_h2)                # output value of neuron h2

    # node o1
    net_o1 = w[4]*out_h1 + w[5]*out_h2 + b[1] # net total input of o1
    out_o1 = sigmoid(net_o1)                  # output value of neuron o1
    
    # node o2
    net_o2 = w[6]*out_h1 + w[7]*out_h2 + b[1] # net total input of o2
    out_o2 = sigmoid(net_o2)                  # output value of neuron o2
    
    # total error calculation
    Et = 0.5*((op[0] - out_o1)**2 + (op[1] - out_o2)**2)
    
    # derivative computations for back propagation
    # output layer - hidden lauer
    d_Et_out_o1 = -(op[0] - out_o1) # these derivatives are hand-calculated
    d_out_o1_net_o1 = out_o1*(1 - out_o1)
    d_net_o1_w5 = out_h1
    d_net_o1_w6 = out_h2
    
    d_Et_w5 = d_Et_out_o1 * d_out_o1_net_o1 * d_net_o1_w5
    d_Et_w6 = d_Et_out_o1 * d_out_o1_net_o1 * d_net_o1_w6
    
    d_Et_out_o2 = -(op[1] - out_o2)
    d_out_o2_net_o2 = out_o2*(1 - out_o2)
    d_net_o2_w7 = out_h1
    d_net_o2_w8 = out_h2
    
    d_Et_w7 = d_Et_out_o2 * d_out_o2_net_o2 * d_net_o2_w7
    d_Et_w8 = d_Et_out_o2 * d_out_o2_net_o2 * d_net_o2_w8
    
    # hidden layer - input layer
    d_net_o1_out_h1 = w[4]
    d_net_o2_out_h1 = w[6]
    d_net_o1_out_h2 = w[5]
    d_net_o2_out_h2 = w[7]
    d_out_h1_net_h1 = out_h1*(1 - out_h1)
    d_out_h2_net_h2 = out_h2*(1 - out_h2)
    d_net_h1_w1 = ip[0]
    d_net_h1_w2 = ip[1]
    d_net_h2_w3 = ip[0]
    d_net_h2_w4 = ip[1]
    
    d_Et_w1 = (d_Et_out_o1*d_out_o1_net_o1*d_net_o1_out_h1 +
               d_Et_out_o2*d_out_o2_net_o2*d_net_o2_out_h1) \
               * d_out_h1_net_h1*d_net_h1_w1
    
    d_Et_w2 = d_Et_w1 / d_net_h1_w1 * d_net_h1_w2 # they are quite similar
    
    d_Et_w3 = (d_Et_out_o1*d_out_o1_net_o1*d_net_o1_out_h2 +
               d_Et_out_o2*d_out_o2_net_o2*d_net_o2_out_h2) \
               * d_out_h2_net_h2*d_net_h2_w3
    
    d_Et_w4 = d_Et_w3/d_net_h2_w3 * d_net_h2_w4
    
    # new weights computation
    eta = 0.5                       # learning rate
    w[0] -= eta * d_Et_w1
    w[1] -= eta * d_Et_w2
    w[2] -= eta * d_Et_w3
    w[3] -= eta * d_Et_w4
    w[4] -= eta * d_Et_w5
    w[5] -= eta * d_Et_w6
    w[6] -= eta * d_Et_w7
    w[7] -= eta * d_Et_w8

    print(itr,Et)
#

print("The output from neural network is : ",out_o1," and ", out_o2)

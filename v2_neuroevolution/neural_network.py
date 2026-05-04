import numpy as np


class NeuralNetwork:

    def __init__(self,input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        #He Initialization
        self.W1 = np.random.randn(self.input_size, self.hidden_size) * np.sqrt(2.0 / self.input_size)
        self.b1 = np.zeros(self.hidden_size)
        self.W2 = np.random.randn(self.hidden_size, self.output_size) * np.sqrt(2.0 / self.hidden_size)
        self.b2 = np.zeros(self.output_size)


    def relu(self, x):
        return np.maximum(0, x)

    def forward(self, input):

        z1 = (input @ self.W1) + self.b1
        a1 = self.relu(z1)

        z2 = (a1 @ self.W2) + self.b2
        return z2

    def get_parameters(self):
        return np.concatenate([self.W1.flatten(),
                               self.b1.flatten(),
                               self.W2.flatten(),
                               self.b2.flatten()])

    def set_parameters(self, parameters):
        w1_end = self.input_size * self.hidden_size
        b1_end = w1_end + self.hidden_size
        w2_end = b1_end + (self.hidden_size * self.output_size)

        self.W1 = parameters[:w1_end].reshape((self.input_size, self.hidden_size))
        self.b1 = parameters[w1_end:b1_end]
        self.W2 = parameters[b1_end:w2_end].reshape((self.hidden_size, self.output_size))
        self.b2 = parameters[w2_end:]
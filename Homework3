import numpy as np
import matplotlib.pyplot as plt
import os

g = 9.8

class mov_sim:
    def __init__(self, vx0, vy0, t):
        self.t = np.linspace(0,t,t+1)
        self.vx = vx0 - g * self.t
        self.vy = vy0
        self.x = vx0 * self.t -  0.5 * g * self.t ** 2
        self.y = vy0 * self.t

    def save_res(self):
        self.mov_data = pd.DataFrame({'t' : self.t,  'x' : self.x, 'y': self.y, 
                    'vx': self.vx, 'vy': self.vy})
        self.mov_data.to_csv('movement_data.csv')
        
    def plot_res(self):
        plt.plot(self.y, self.x)
        plt.xlabel('y')
        plt.ylabel('x')
        plt.title('Movement Simulation')
        plt.show()


if __name__ == '__main__':
    vx, vy, t = input('Input Vertical speed, Horizontal speed and Simulation time, split by space').split(' ')
    vx = int(vx)
    vy = int(vy)
    t = int(t)
    sim =  mov_sim(vx, vy, t)
    sim.save_res()
    sim.plot_res()

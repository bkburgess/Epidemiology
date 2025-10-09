from random import random, seed
import matplotlib.pyplot as plt 
from math import exp

# seed = 398759832

class SIRDCity():
    def __init__(self, susceptible=100, infected=20, recovered=0, dead=0):
        self.susceptible = [susceptible]
        self.infected = [infected]
        self.recovered = [recovered]
        self.dead = [dead]
    
    def infect(self, susceptible, infected):
        new_infected = min(random()*(susceptible/4)*(1-exp(-infected/10)), susceptible)
        susceptible -= new_infected
        infected += new_infected
        return susceptible, infected

    def recover(self, infected, recovered):
        new_recovered = min(random()*(infected/5), infected)
        infected -= new_recovered
        recovered += new_recovered
        return infected, recovered

    def die(self, infected, dead):
        died = min(random()*(infected/10), infected)
        infected -= died
        dead += died
        return infected, dead

    def plot(self, susceptible, infected, recovered, dead):
        fig, ax = plt.subplots()
        ax.plot(susceptible)
        ax.plot(infected)
        ax.plot(recovered)
        ax.plot(dead)
        ax.legend(("susceptible", "infected", "recovered", "dead"))
        plt.show()


    def run(self):
        for _ in range(100):
            s, i = self.infect(self.susceptible[-1], self.infected[-1])
            i, r = self.recover(i, self.recovered[-1])
            i, d = self.die(i, self.dead[-1])
            self.susceptible.append(s)
            self.infected.append(i)
            self.recovered.append(r)
            self.dead.append(d)
        
        self.plot(self.susceptible, self.infected, self.recovered, self.dead)


if __name__ == "__main__":
    city = SIRDCity()
    city.run()
    
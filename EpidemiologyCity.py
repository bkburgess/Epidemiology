from random import random
import networkx as nx
from time import sleep
import matplotlib.pyplot as plt
from math import erf
import logging
# logging.basicConfig(level=logging.DEBUG)


class Disease():
    """
    a disease that can infect people in a population
    """
    def __init__(self, _name: str = 'A', _inf_prob: float = 0.01, _death_prob: float = 0.01, _rec_prob: float = 0.01, _rein_prob: float = 0.001):
        self.name           = _name
        self.infect_prob    = _inf_prob 
        self.death_prob     = _death_prob
        self.recover_prob   = _rec_prob
        self.reinfect_prob  = _rein_prob
        self.research_progress = 0

class Box():
    """
    A status or potential status for a person
    """
    types = ['uninfected', 'infected', 'dead', 'recovered']
    def __init__(self, n: int, _type: str ='uninfected') -> None:
        self.n = n
        self.type = _type

    def transfer_people(self, n_change: int, box: 'Box') -> int:
        """
        n_change: number of people to transfer
        box: a box to transfer people to
        """
        n_change = min(self.n, n_change)
        n_change = max(n_change, 0)
        self.n -= n_change
        box.n += n_change
        
        return n_change


class Population():
    """
    A large collection of people, mix of statuses, potentially infected by disease
    """
    def __init__(self,  total: int, name: str) -> None:
        self.total = total
        self.name = "Esterpool"
        self.diseases = {}

    def load_disease_info(self, disease_name: str, n_unf: int, n_inf: int, n_rec: int = 0, n_dead: int = 0, research_rate: float=0.001):
        if n_unf + n_inf + n_rec + n_dead != self.total: 
            raise ValueError("The total number of people must equal the population total")

        self.diseases[disease_name] = {
            'uninfected': Box(n_unf, _type='uninfected'),
            'infected': Box(n_inf, _type='infected'),
            'recovered': Box(n_rec, _type='recovered'),
            'dead': Box(n_dead, _type='dead'),
            'research_rate': research_rate
        }
    
    def __str__(self) -> str:
        return "Population: " + self.name

    def update_population_status(self, disease: Disease) -> None:
        """
        disease: disease that affects the population
        """
        self.infect(disease.infect_prob, disease.reinfect_prob)
        self.recover(disease.recover_prob)
        self.die(disease.death_prob)
        # self.research(disease)
        # self.impact = (self.dead.n + self.infected.n) / (self.dead.n + self.infected.n + self.uninfected.n + self.recovered.n)
        assert self.uninfected.n + self.infected.n + self.dead.n + self.recovered.n == self.total

    def infect(self, infect_prob: float, reinfect_prob: float, prob_fn: str = "simple") -> None:
        """
        disease: a disease that can infect people in a population
        prob_fn: how to calculate the rate of infection (ratio, erf)
        """
        # [ ] TODO include option to be dependent upon number dead
        # [ ] TODO adjust infected/reinfected per disease instead of total
        if prob_fn == 'simple':
            new_infected = infect_prob   * self.uninfected.n
            reinfected   = reinfect_prob * self.recovered.n
        elif prob_fn == "ratio":
            new_infected = infect_prob   * self.uninfected.n * self.infected.n / (self.uninfected.n + self.infected.n)
            reinfected   = reinfect_prob * self.recovered.n  * self.infected.n / (self.recovered.n  + self.infected.n) 
        elif prob_fn == "erf": 
            new_infected = infect_prob   * self.uninfected.n * erf(self.infected.n/self.uninfected.n)
            reinfected   = reinfect_prob * self.recovered.n  * erf(self.infected.n/self.recovered.n)

        new_infected = round(new_infected)
        reinfected = round(reinfected)
        self.uninfected.transfer_people(new_infected, self.infected)
        self.recovered.transfer_people(reinfected, self.infected)

    def recover(self, recover_prob: float) -> int:
        """
        disease: a disease that people will recover from
        """
        new_recovered = recover_prob * self.infected.n
        new_recovered = round(new_recovered)
        return self.infected.transfer_people(new_recovered, self.recovered)
        

    def die(self, death_prob: float) -> int:
        """
        disease: a disease that people will die of
        """
        died = death_prob * self.infected.n
        died = round(died)
        return self.infected.transfer_people(died, self.dead)

    def research(self, research_progress: float) -> int:
        """
        disease: a disease that cities can research
        """
        research_progress += self.research_rate
        return research_progress
        
    def print_population_status(self, disease: Disease) -> None:
        print(f"uninfected: {self.uninfected.n}")
        print(f"infected: {self.infected.n}")
        print(f"recovered: {self.recovered.n}")
        print(f"dead: {self.dead.n}")
        # print(f"research for disease: {disease.research_progress}")
        print()

def make_graph():
    G = nx.DiGraph()
    positions = {}
    locations = [(-10, 0), (0,0), (0,-10), (10, 0)]
    for i, type in enumerate(Box.types):
        G.add_node(type)
        positions[type] = locations[i]
    print(positions)
    print(G.nodes())
    G.add_edge('uninfected', 'infected')
    G.add_edge('infected', 'recovered')
    G.add_edge('recovered', 'infected')
    G.add_edge('infected', 'dead')
    print(G.edges())

    nx.draw_networkx(G, pos=positions, node_size=1000, with_labels=True)
    plt.axis('equal')
    plt.show()

def draw_plot(record: dict):
    fig, ax = plt.subplots()
    ax.plot(record['uninfected'])
    ax.plot(record['infected'])
    ax.plot(record['recovered'])
    ax.plot(record['dead'])
    ax.legend(record.keys())
    plt.show()


if __name__ == "__main__":

    init_uninfected = 1000
    init_infected = 10
    disease = Disease('andromeda')
    pop = Population(init_infected + init_uninfected)
    pop.load_disease_info(disease, init_uninfected, init_infected)
    record = {'uninfected': [init_uninfected], 'infected': [init_infected], 'dead': [], 'recovered': []}
    duration = 300
    for i in range(duration):
        pop.update_population_status(disease)
        record['dead'].append(pop.dead.n)
        record['infected'].append(pop.infected.n)
        record['recovered'].append(pop.recovered.n)
        record['uninfected'].append(pop.uninfected.n)

    draw_plot(record)
    # make_graph()
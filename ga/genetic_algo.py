import numpy as np

"""
A population is a set of individuals.
A individual is a set of characteristics - alleles.
Each characteristic comes from a pool of possible characteristics - genes.



"""


class BaseIndividual():

    def __init__(self, chromosome=None, alleles=None):
        self.chromosome = np.array(chromosome)
        self.size = self.chromosome.size

        self.alleles = np.array(alleles)
        self.alleles_size = self.alleles.size
    
    
    
    def __repr__(self):
        return ''.join(self.chromosome)
    
    
    def mate(self, other):
        """For each chromosome position, picks a """
        picks = np.random.randint(2, size=self.size).astype(bool)

        child1 = np.choose(picks, choices=[self.chromosome, other.chromosome])
        child2 = np.choose(~picks, choices=[self.chromosome, other.chromosome])

        return np.array((self.__class__(child1), self.__class__(child2)))
    
    def mutate(self, mutate_prob):
        # sequence of bernoulli's
        chromosome_picks = np.random.binomial(1, p=mutate_prob, size=self.size).astype(bool)
        n_mutations = np.sum(chromosome_picks)

        new_chromosome = self.chromosome.copy()

        if n_mutations>0:
            alleles_picks = np.random.randint(self.alleles_size, size=n_mutations)
            new_chromosome[chromosome_picks] = self.alleles[alleles_picks]

        return self.__class__(new_chromosome)




class Population():
    

    def __init__(self, pop=None):
        if pop is not None:
            pass
        else:
            raise ValueError("One of pop or size should not be None.")
        self.pop = np.array(pop)
        self.size = len(pop)

        self.fitness_scores = None
        self.fittests_ranks = None

    def calc_fitness_scores(self, objective, *args, **kwargs):
        fitness_scores = np.array(objective(x, *args, **kwargs) for x in self.pop)
        self.fitness_scores = fitness_scores
        return fitness_scores

    def calc_fittests_rank(self):
        if not self.fitness_scores:
            raise ValueError("No fitness scores.")
        scores = self.fitness_scores
        fittests_rank = np.argsort(-scores)
        #handle score ties
        #rnd = np.random.random(scores.size)
        #self.fittests_rank = np.array(np.lexsort((rnd, scores)))
        self.fittests_ranks = fittests_rank
        return fittests_rank
    
    def select_top_fittests(self, p: float = None, n: int = None):
        if not (p or n): raise ValueError("One of p or n arguments should be provided.")
        elif p: n = int(p * self.size)
        idx_top_fittest = self.fittests_ranks[:n]
        return self.__class__(self.pop[idx_top_fittest].copy())
    

    def mate_randomly(self, new_pop_size):
        #new_pop_size = self.size
        n_pairs = np.ceil(new_pop_size/2).astype(int)
        parents1, parents2 = np.random.choice(self.pop, size=(2,n_pairs))
        
        offspring = np.array([x.mate(y) for x, y in zip(parents1, parents2)]).flatten()[:new_pop_size].copy()
        
        return self.__class__(offspring)

    def mutate(self, mutate_prob):
        return self.__class__([x.mutate(mutate_prob=mutate_prob) for x in self.pop])
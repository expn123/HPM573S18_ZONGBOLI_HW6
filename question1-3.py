import numpy as np
import scipy.stats as stato
import scr.StatisticalClasses as Stat


class Game:
    def __init__(self,id):
        self.id=id
        self.rnd=np.random
        self.rnd.seed(self.id)
        self.rarray = np.random.random(size=20)
        self.game_list = list(self.rarray)
    def simulation(self):
        for k in range(0, 20):
            if self.rarray[k] > 0.5:
                self.game_list[k] = 'H'
            else:
                self.game_list[k] = 'T'
        m = 0
        for j in range(0, len(self.game_list) - 2):
            if self.game_list[j] == 'T' and self.game_list[j + 1] == 'T' and self.game_list[j + 2] == 'H':
                m += 1
                j = j + 3
            else:
                m += 0
                j = j + 1
        total_result = 100 * m - 250
        return total_result

class Cohort:
    def __init__(self,id,pop_size):

        self.gamelist=[]
        self.catotal_score=[]
        self._sumSTAT=\
            Stat.SummaryStat('Gamblers total score', self.catotal_score)
        n=1
        while n<=pop_size:
            gameunit=Game(id*pop_size+n)
            self.gamelist.append(gameunit)
            n+=1

    def simulatecohort(self):
        for game in self.gamelist:
            value=float(game.simulation())
            self.catotal_score.append(value)

    def get_expected_score(self):
        return sum(self.catotal_score)/len(self.catotal_score)

    def get_CI(self,alpha):
        return self._sumSTAT.get_t_CI(alpha)

class MultiCohort:
    def __init__(self,ids,pop_sizes):
        self._ids=ids
        self._popsizes=pop_sizes
        self._getallexprewards=[]
    def simulate(self):
        for i in range(len(self._ids)):
            cohort=Cohort(i,self._popsizes)
            cohort.simulatecohort()
            self._getallexprewards.append(cohort.get_expected_score())

def get_proportion_CI(p,n,alpha):
    CIP=[0,0]
    std_dev = pow(p*(1-p),0.5)/pow(n,0.5)
    half_length=stato.t.ppf(1-alpha/2,n)*std_dev
    CIP[0]=p-half_length
    CIP[1]=p+half_length
    return CIP



#Give alpha and do the simulation
alphax=0.05
cohorttest=Cohort(2,1000)
cohorttest.simulatecohort()

#Caculate the CI of expected reward
sum_stat = Stat.SummaryStat("dsa",cohorttest.catotal_score)
CI_of_Expected=sum_stat.get_t_CI(alphax)

#Print the CI of expected reward
print("95 % Confidence Interval of Expeceted Reward is",CI_of_Expected)

#Caculate the CI of probability
count=0
for i in range(0,len(cohorttest.catotal_score)):
    if cohorttest.catotal_score[i]<0:
        count+=1
    else:
        count+=0
probability=count/float(len(cohorttest.catotal_score))
CI_of_Prob= get_proportion_CI(probability,len(cohorttest.catotal_score),alphax)

#Print the CI of probability
print("95 % CI of probability is", CI_of_Prob)

#Answer of question 2:
print("Here is answer of question 2: \n \
    95% CI of expected rewards means that if we simulate many times of 1000 games and get a confidence interval in each time, 95% of\
    these intervals will cover true mean.\n\
     95% CI of probability means that if we simulate multiple times of 1000 games and get a confidence interval of probability in each time, 95% of  these intervals will cover true probability of losing.")

#Answer of question3:
print("Here is answer of question 3")
print("1.As a casino owner, you should pay attention to the profit of your casino in long time running instead of the profit of a specific game. So you may worry about the true expected reward of the game. So I recommand confidence interval of rewards and probability.")
print("95 % Confidence Interval of Expeceted Reward is",CI_of_Expected,"95% CI of expected rewards means that if we simulate many times of 1000 games and get a confidence interval in each time, 95% of\
    these intervals will cover true mean.")
print("95 % CI of probability is", CI_of_Prob, "95% CI of probability means that if we simulate multiple times of 1000 games and get a confidence interval of probability in each time, 95% of  these intervals will cover true probability of losing (you get profit!).")
print("2.As a gambler, you only pay attention to how much you will get in the next 10 games. So you may worry about the expected reward of the next 10 games and how likley I will get certain range of score in the next 10 games?OK,here comese the prediction interval.")
print("Now let's simulate 1000 times 10-time game and get 95% prediction value:")
numbersimu=1000
gamblermulti=MultiCohort(range(numbersimu),10)
gamblermulti.simulate()
sum_statpi=Stat.SummaryStat
PI_gambler=sum_stat.get_PI(alphax)
print(PI_gambler)
print("This means that there are 95% probability that your expected reward in next 10-game lies in [-250,150].")

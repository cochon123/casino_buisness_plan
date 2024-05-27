import numpy as np
import random
import matplotlib.pyplot as plt
from tqdm import tqdm

#0 = facile, 1=moyen, 2=dificile

#persone0 = argent non récupérable, person1 = type de partie, person2 = argentRetirable

#créer la population de joueur
nb_joueur = 1000
pop = np.zeros((nb_joueur,3))

sum_trans = 0

gain_casino = 0

gain_casino1 = []
reste1 = []

#créer les espaces de jeu
facile = np.array([])
moyen = np.array([])
dificile = np.array([])

def init ():
    global pop

    for person in pop :
        #argent non récupérable
        person[0] += 10
        global sum_trans
        sum_trans += 10

        if person[0]+person[2] >= 50 :
            niveau = random.randint(0,1000)
            if niveau >= 50:
                if person[0] < 50:
                    argent = 50 - person[0]
                    person[2] -= argent
                    person[0] += argent
                person[1] = 2
            elif niveau >= 10:
                if person[0] < 20:
                    argent = 20 - person[0]
                    person[2] -= argent
                    person[0] += argent
                person[1] = 0
            else:
                person[1] = 0
        elif person[0]+person[2] >= 20 :
            niveau = random.randint(0,50)
            if niveau > 30:
                if person[0] < 20:
                    argent = 20 - person[0]
                    person[2] -= argent
                    person[0] += argent
                person[1] = 1
            else:
                person[1] = 0
        else :
            person[1] = 0


def repartition(person):
    global sum_trans
    try :
        argent_retrait = random.randint(0, person[2])
    except : 
        argent_retrait = 0
    person[2] -= argent_retrait
    sum_trans += argent_retrait

def jeu ():
    global gain_casino
    global pop
    global facile
    global moyen
    global dificile
    facile = np.array([])
    moyen = np.array([])
    dificile = np.array([])

    for person in pop :
        # prendre trois personne qui ont choisi facile
        if person[1] == 0:
            facile = np.append(facile, person)
        elif person[1] == 1:
            moyen = np.append(moyen, person)
        else:
            dificile = np.append(dificile, person)

    a = True
    while(a):
        try :
            facile = np.reshape(facile, (-1, 3, 3))
            a = False
        except:
            facile = np.delete(facile, -1)
    
    b = True
    while(b):
        try :
            moyen = np.reshape(moyen, (-1, 6, 3))
            b = False
        except:
            moyen = np.delete(moyen, -1)
    
    c = True
    while(c):
        try :
            dificile = np.reshape(dificile, (-1, 10, 3))
            c = False
        except:
            dificile = np.delete(dificile, -1)

    #facile partie
    for partie in facile:
        for i in range(2): #vider la mise des joueurs
            partie[i][0] -= 10

        j = random.randint(0,2) #choisir le gagnant
        partie[j][2] += 25

        gain_casino += 5

    #moyen partie
    for partie in moyen:
        for i in range(5): #vider la mise des joueurs
            partie[i][0] -= 20

        j = random.randint(0,5) #choisir le gagnant
        partie[j][2] += 100

        gain_casino += 20
        
    #dificile partie
    for partie in dificile:
        for i in range(9): #vider la mise des joueurs
            partie[i][0] -= 50

        j = random.randint(0,9) #choisir le gagnant
        partie[j][2] += 400

        gain_casino += 100
    
    gain_casino1.append(gain_casino)


    pop = np.array([])
    pop = np.concatenate((facile,moyen,dificile), axis = None)
    (a,) = pop.shape
    a = 3*nb_joueur - a
    pop = np.concatenate((pop, np.zeros((a,))))

    c = True
    while(c):
        try :
            pop = np.reshape(pop, (-1, 3))
            c = False
        except:
            pop = np.delete(pop, -1)

    for person in pop:
        repartition(person)

    init()


init () #initialiser la population
for i in tqdm(range(100)):
    jeu ()
    frais = sum_trans * 2.5 / 100
    reste = gain_casino - frais
    reste1.append(reste)
for person in pop:
    print(person)
print("facile : ",facile.shape," \n moyen : ",moyen.shape,"\n difficile : ",dificile.shape)
print(pop.shape,"\ngain_casino", gain_casino,"\n", "somme des transactions",sum_trans,"\n", "ce qu'il nous reste", reste)

plt.plot(gain_casino1, label = 'gain_casino')

plt.plot(reste1, label = 'gain avec les frais')

plt.ylabel("dollars")
plt.xlabel("itération")
plt.legend()
plt.show()
#Raphaels förslag för lösningen:

import numpy as np
from ast import literal_eval
import matplotlib
import matplotlib.pyplot as plt
import re

#hoppa över första råden i datafile

def get_data():
    data = []
    with open ("Data/datapoints.txt") as file:
        data = file.readlines ()[1:]

    arr= []
    for line in data:
        x, y, c = line.split(sep=', ')
        arr.append([float(x), float(y), int(c)])
        
    return np.array(arr)

def get_test():
    testp = []
    with open ("Data/testpoints.txt") as file:
        rstr = r"(\(.+, .+\))"
        test = file.read()
        for tupl in re.findall(rstr, test):
            testp += [literal_eval(tupl)]
    return np.array(testp)

def l2_norm(*terms):
    return np.sqrt(np.sum(np.square(np.array(terms))))

def eucd(a, b):
    return l2_norm(np.array(a)-np.array(b))

def classify(P, k, data=get_data()):
    dists = sorted([(eucd(P, (x, y)), c) for x, y, c in data]) [:k]
    #returns false for Pichu and True for Pikachu
    return len([c for _, c in dists if c ==0]) < len([c for _, c in dists if c ==1])

def run_tests():
    tests = get_test()
    for x, y in tests:
        pikachu = classify(P=(x,y), k=1)
        print (f"x,y: {x, y}", end=" ")
        if pikachu:
            print("Pickachu")
        else:
            print("Pichu")
            
def query():
    loop= True
    while loop:
        try:
            inp = input("Input length and width (x, y): ")
            x, y =literal_eval(inp)
            if x < 0 or y < 0:
                raise ValueError()
            pikachu = classify (P=(x,y), k=1)
            print(f"Point {x, y} classifies as {'Pikachu' if pikachu else 'Pichu'}.")
            loop = False
        except (TypeError, SyntaxError, ValueError):
            print("Wrong input should have form '<positiv number>, <positiv number>'")
            
def main():
    data = get_data()
    accs = []
    for _ in range(10):
        np.random.shuffle(data)
        pichus = [(x, y, c) for x, y, c in data if c==0]
        pikachus = [(x, y, c) for x, y, c in data if c==1]
        train = pichus[:50] + pikachus[50:]
        test = pichus[50:75] + pikachus[50:75]
        result = [(r, c) for x, y, c in test
                          for r in [classify(P=(x,y), k=10, data =train)]
                    if c== r]
        accs += [len(result)/len(test)]
        
    print(f"Medelnoggranhet {np.average(accs)}")
    plt.plot(range(1, 11), accs)
    plt.xlabel("n")
    plt.ylabel("accuracy")
    plt.show()

if __name__ == '__main__':
    run_tests()         
    #query()
    #main()
    
    
            


from GrandConseil import AlgorithmeGrandConseil

E2017 = {"Gauche" : 110639, "ADC": 58212, "UDC" : 64517, "PLR" : 111117 }
for a,s in E2017.items():
    if s/sum(E2017.values())<0.05: E2017[a] = 0
r = AlgorithmeGrandConseil(E2017,19,True)

E2022 = {"UDC/PLR" : 151495, "Gauche": 99644, "PVL" : 46682, "Libres" : 12184, 'Centre' : 11192, 'Pirates': 4156, 'Libertes': 3160 }
for a,s in E2022.items():
    if s/sum(E2022.values())<0.05: E2022[a] = 0
r = AlgorithmeGrandConseil(E2022,19,True)


from gurobipy import GRB, Model, quicksum

m = Model()
m.setParam('TimeLimit', 120)

#### CONJUNTOS #####

# Los datos indicados a continuación hacen referencia a los datos presentes en el excel adjuntado.
articulos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
camiones = [1, 2, 3]
motos = [1, 2]
coolers = [1, 2, 3]
cajas = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
clientes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
pedidos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
periodos = [1, 2, 3, 4]

congelados = []
no_congelados = []

productos_para_mayores = []
productos_para_todos = []

clientes_mayores = []
clientes_no_mayores = []


#### PARAMETROS ######
Vc = {1: [30, 0.2], 2: [13, 0.1]}  # Diccionario de las cajas en {peso, volumen}

Vcc = {1: [15, 0.016]} # Diccionario de las coolers en {peso, volumen}

Vk = {1: [6, 24990], 2: [8, 29990], 3: [10,39990]} # Variables vehiculos. Diccionario de camiones que indica {volumen, costo}

Vm = {1: [0.2, 7000], 2: [0.2, 7000]} # Variables vehiculos. Diccionario de motos que indica {volumen, costo}

Vp = {1: [1, 1.11 * 0.01, 0, 0], 2: [1, 1.075 * 0.01, 0, 0], 3: [0.5, 1 * 0.01, 1, 0], 4: [1.8, 0.75 * 0.001, 0, 1], 5: [3, 3 * 0.001, 0, 0], 6: [1, 1 * 0.001, 0, 0]
    , 7: [1, 8 * 0.001, 0, 0], 8: [1, 1 * 0.001, 0, 0], 9: [1, 0.08 * 0.001, 0, 0], 10: [0.5, 0.7 * 0.001, 1, 0], 11: [0.43, 0.5 * 0.001, 0, 0], 12: [1.2, 1.5 * 0.001, 0, 0]
        , 13: [0.4, 0.5 * 0.001, 0, 0], 14: [2.3, 2 * 0.001, 0, 0], 15: [5, 4.43 * 0.001, 0, 0], 16: [1, 1.8 * 0.001, 0, 0], 17: [0.5, 0.5 * 0.001, 0, 0]
            , 18: [0.7, 3.5 * 0.001, 0, 0], 19: [0.38, 4.2 * 0.001, 0, 0], 20: [0.39, 0.5 * 0.001, 0, 0], 21: [1, 1.6 * 0.001, 0, 0], 22: [1, 1 * 0.001, 0, 0]
               , 23: [0.4, 0.5 * 0.001, 0, 0], 24: [1, 1 * 0.001, 0, 0], 25: [0.5, 0.5 * 0.001, 0, 0]}
                
### Variables productos. Diccionario que indica las cualidades de cada uno de los productos en el orden {peso, volumen, binaria congelado, binaria destilado} ###

P = {1: [1, 3, 4, 0, 10, 12, 0, 0, 2, 3, 1, 1, 2, 0, 0, 0, 3, 0, 1, 1, 0, 0, 2, 0, 0], 2: [1, 1, 1, 0, 0, 2, 0, 0, 2, 2, 1, 1, 2, 0, 0, 0, 3, 0, 4, 1, 0, 0, 2, 0, 0], 3: [1, 2, 4, 0, 1, 2, 4, 0, 2, 3, 2, 1, 2, 1, 1, 0, 3, 0, 1, 1, 0, 0, 2, 0, 0],
    4: [0, 3, 2, 0, 1, 0, 0, 0, 2, 3, 1, 2, 2, 0, 0, 0, 1, 0, 1, 1, 0, 0, 2, 0, 0], 5: [4, 1, 1, 0, 1, 0, 2, 0, 2, 3, 1, 2, 1, 0, 0, 1, 1, 0, 1, 2, 0, 0, 2, 0, 0], 6: [0, 1, 1, 8, 1, 0, 5, 0, 2, 3, 1, 2, 2, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0],
        7: [0, 0, 1, 0, 1, 0, 0, 0, 4, 3, 1, 2, 5, 0, 0, 0, 1, 0, 1, 5, 0, 0, 2, 9, 0], 8: [2, 4, 2, 5, 1, 0, 0, 9, 2, 3, 11, 2, 2, 0, 0, 10, 1, 0, 1, 1, 0, 0, 2, 0, 0], 9: [1, 6, 1, 0, 1, 3, 0, 0, 2, 3, 1, 2, 2, 6, 0, 0, 1, 0, 1, 1, 0, 0, 2, 0, 0],
            10: [2, 4, 2, 0, 1, 0, 2, 1, 2, 3, 1, 2, 1, 0, 1, 0, 1, 0, 1, 5, 0, 0, 2, 0, 0], 11: [4, 2, 2, 0, 1, 1, 0, 0, 2, 7, 1, 2, 2, 9, 0, 0, 1, 0, 1, 10, 0, 0, 2, 0, 0], 12: [9, 0, 0, 0, 1, 0, 0, 0, 2, 1, 1, 2, 2, 0, 0, 0, 1, 0, 2, 1, 0, 0, 2, 0, 0],
                13: [1, 2, 8, 0, 1, 0, 1, 0, 2, 3, 5, 2, 2, 0, 6, 0, 1, 2, 1, 1, 0, 1, 2, 0, 0], 14: [3, 3, 3, 3, 2, 1, 0, 0, 2, 3, 1, 5, 2, 0, 8, 0, 1, 0, 1, 1, 0, 2, 2, 0, 0], 15: [1, 4, 2, 2, 1, 6, 7, 0, 2, 3, 1, 2, 2, 0, 0, 0, 1, 0, 1, 1, 0, 0, 2, 0, 0]}
# Pedidos. Pedidos modelo en el orden {indice_pedido: [cantidad p1, p2, p3, p4, p5, p6]}

C = {1: {"Nombre": "Juan", "Pedido": 1, "Mayor": 1}, 2: {"Nombre": "Pedro", "Pedido": 2, "Mayor": 0}, 3: {"Nombre": "Pepita", "Pedido": 3, "Mayor": 1}, 4: {"Nombre": "Mauriz", "Pedido": 4, "Mayor": 0}, 5: {"Nombre": "Yenny", "Pedido": 5, "Mayor": 1}\
    , 6: {"Nombre": "Josh", "Pedido": 6, "Mayor": 0}, 7: {"Nombre": "Diego", "Pedido": 7, "Mayor": 1}, 8: {"Nombre": "Feña", "Pedido": 8, "Mayor": 0}, 9: {"Nombre": "Ignacio", "Pedido": 9, "Mayor": 1}, 10: {"Nombre": "Ignacia", "Pedido": 10, "Mayor": 0}\
        , 11: {"Nombre": "Alberto", "Pedido": 11, "Mayor": 1}, 12: {"Nombre": "Emilia", "Pedido": 12, "Mayor": 0}, 13: {"Nombre": "Alicia", "Pedido": 13, "Mayor": 1}, 14: {"Nombre": "Agustin", "Pedido": 14, "Mayor": 0}\
            , 15: {"Nombre": "Kayle", "Pedido": 15, "Mayor": 0}}
# Diccionario de clientes: si es mayor de edad, "Mayor" : 1, sino "Mayor" : 0

for u in articulos:
    if Vp[u][2] == 1:
        congelados.append(u)
    else:
        no_congelados.append(u)

for u in articulos:
    if Vp[u][3] == 1:
        productos_para_mayores.append(u)
    else:
        productos_para_todos.append(u)

for u in clientes:
    if C[u]["Mayor"] == 1:
        clientes_mayores.append(u)
    else:
        clientes_no_mayores.append(u)

M = 10000000000


##### VARIABLES #######
x1 = m.addVars(articulos, pedidos, cajas, periodos, vtype=GRB.BINARY, name="x1")
x2 = m.addVars(articulos, pedidos, coolers, periodos, vtype=GRB.BINARY, name="x2")
# Resumimos las variables x en solo x1 y x2 por recomendacion de la ayudante
y1 = m.addVars(cajas, camiones, periodos, vtype=GRB.BINARY, name="y1")
y2 = m.addVars(coolers, camiones, periodos, vtype=GRB.BINARY, name="y2")
y3 = m.addVars(cajas, motos, periodos, vtype=GRB.BINARY, name="y3")
z1 = m.addVars(camiones, periodos, vtype=GRB.BINARY, name="z1")
z2 = m.addVars(motos, periodos, vtype=GRB.INTEGER, name="z2", lb=0, ub = 4)


m.update()


######### RESTRICCIONES #############

### Cada producto i no congelado del pedido p debe ser cargado en una caja c en el periodo t: ###
m.addConstrs((quicksum(quicksum(x1[u,p,c,t] for p in pedidos ) for c in cajas) == 1 for t in periodos for u in articulos if u in no_congelados), name = "R1" )

### Cada producto i congelado del pedido p debe ser cargado en un cooler en el periodo t: ###
m.addConstrs((quicksum(quicksum(x2[n,p,q,t] for p in pedidos) for q in coolers) == 1  for t in periodos for n in articulos if n in congelados), name = "R2" )

### Solo las cajas con productos se suben a los camiones: ###
m.addConstrs((quicksum(quicksum(x1[u,p,c,t] for u in articulos if u in no_congelados) for t in periodos) >= y1[c,k,t] for k in camiones for p in pedidos for c in cajas for t in periodos), name = "R3" )

### Cada cooler q es cargado en un camion k en el periodo t: ###
m.addConstrs((quicksum(y2[q,k,t] for k in camiones) == 1  for t in periodos for q in coolers), name = "R4" )

### Cada caja c es cargada a lo mas en una moto m en el periodo t: ###
m.addConstrs((quicksum(y3[c,m,t] for m in motos) <= 1  for t in periodos for c in cajas), name = "R5" )

### Analisis de sensibilidad cambiando el lado derecho de R5: El modelo se vuelve infactible al realizar este cambio ###
#m.addConstrs(quicksum(y3[c,m,t] for m in motos) == 1  for t in periodos for c in cajas)

### Respetar la capacidad de volumen de las cajas c, tanto en los camiones k como en las motos m en el periodo t: ###
m.addConstrs((quicksum(Vp[i][1] * x1[i,p,c,t] for i in articulos) <= Vc[1][1] * (quicksum(y1[c,k,t] for k in camiones)) for c in cajas for t in periodos for p in pedidos), name = "R6" )
m.addConstrs((quicksum(Vp[i][1] * x1[i,p,c,t] for i in articulos) <= Vc[1][1] * (quicksum(y3[c,m,t] for m in motos)) for c in cajas for t in periodos for p in pedidos), name = "R7" )

### Analisis de sensibilidad cambiando el lado derecho de R6: no hay cambio en la FO###
#m.addConstrs((quicksum(Vp[i][1] * x1[i,p,c,t] for i in articulos) <= (2*Vc[1][1]) * (quicksum(y1[c,k,t] for k in camiones)) for c in cajas for t in periodos for p in pedidos), name = "R6" )

### Analisis de sensibilidad cambiando el lado derecho de R7: no hay cambio en la FO###
#m.addConstrs((quicksum(Vp[i][1] * x1[i,p,c,t] for i in articulos) <= (2*Vc[1][1]) * (quicksum(y3[c,m,t] for m in motos)) for c in cajas for t in periodos for p in pedidos), name = "R7" )


### Respetar la capacidad de volumen de los coolers q, tanto en los camiones k como en las motos m en el periodo t:###
m.addConstrs((quicksum(Vp[i][1] * x2[i,p,q,t] for i in articulos) <= Vcc[1][1] * (quicksum(y2[q,k,t] for k in camiones)) for q in coolers for t in periodos for p in pedidos), name = "R8" )

### Respetar la capacidad de peso de las cajas c, tanto en los camiones k como en las motos m en el periodo t: ###
m.addConstrs(((quicksum(Vp[i][0] * x1[i,p,c,t] for i in articulos)) <= Vc[1][0] * (quicksum(y1[c,k,t] for k in camiones)) for c in cajas for t in periodos for p in pedidos), name = "R9" )
m.addConstrs(((quicksum(Vp[i][0] * x1[i,p,c,t] for i in articulos)) <= Vc[1][0] * (quicksum(y3[c,m,t] for m in motos)) for c in cajas for t in periodos for p in pedidos), name = "R10" )

### Analisis de sensibilidad cambiando el lado derecho de R9: no hay cambio en la FO###
#m.addConstrs(((quicksum(Vp[i][0] * x1[i,p,c,t] for i in articulos)) <= (2*Vc[1][0]) * (quicksum(y1[c,k,t] for k in camiones)) for c in cajas for t in periodos for p in pedidos), name = "R9" )


### Respetar la capacidad de peso de los coolers q en los camiones k en el periodo t: ###
m.addConstrs(((quicksum(Vp[i][0] * x2[i,p,q,t] for i in articulos)) <= Vcc[1][0] * (quicksum(y2[q,k,t] for k in camiones)) for q in coolers for t in periodos for p in pedidos), name = "R11" )

### Respetar la capacidad (volumen) de los camiones en el periodo t: ###
m.addConstrs(((Vc[1][1] * quicksum(y1[c,k,t] for c in cajas)) + (Vcc[1][1] * (quicksum(y2[q,k,t] for q in coolers)))  <= Vk[k][0] * z1[k,t] for k in camiones for t in periodos), name = "R12" )

## Las motos solo pueden llevar una caja de productos en el periodo t: ##
m.addConstrs((Vc[1][1] * quicksum(y3[c,m,t] for c in cajas) <= Vm[1][0] * z2[m,t] for m in motos for t in periodos), name = "R13" )

### Los camiones pueden realizar como maximo 1 entrega por periodo: ###
m.addConstrs((z1[k,t] <= 1 for k in camiones for t in periodos), name = "R14" )

### Las motos pueden realizar como maximo 4 entregas por periodo: ###
m.addConstrs((z2[m,t] <= 4 for m in motos for t in periodos), name = "R15" )


obj = quicksum(quicksum(Vk[k][1] * z1[k,t] for k in camiones) +  (quicksum(Vm[1][1] *z2[m,t] for m in motos)) for t in periodos)
m.setObjective(obj, GRB.MINIMIZE)

m.optimize()
m.printAttr("X")
m.write("G42.sol")

# El sieguente codigo sirve para calcular las holguras, ya que al tener tantas restricciones activas como en nuestro problema, el codigo que retorna no alcanza a tomar todas las holguras. solo las ultimas.

contador1 = 0
contador2 = 0
contador3 = 0
contador4 = 0
contador5 = 0
contador6 = 0
contador7 = 0
contador8 = 0
contador9 = 0
contador10 = 0
contador11 = 0
contador12 = 0
contador13 = 0
contador14 = 0

for constr in m.getConstrs():
    if constr.getAttr("slack") == 0 and constr.ConstrName[:2] == "R1" and contador1 == 0 :
        print(constr, constr.getAttr("slack"))
        contador1 += 1

    elif constr.getAttr("slack") == 0 and constr.ConstrName[:2] == "R2" and contador2 == 0 :
        print(constr, constr.getAttr("slack"))
        contador2 += 1

    elif constr.getAttr("slack") == 0 and constr.ConstrName[:2] == "R3" and contador3 == 0 :
        print(constr, constr.getAttr("slack"))
        contador3 += 1

    elif constr.getAttr("slack") == 0 and constr.ConstrName[:2] == "R4" and contador4 == 0 :
        print(constr, constr.getAttr("slack"))
        contador4 += 1

    elif constr.getAttr("slack") == 0 and constr.ConstrName[:2] == "R5" and contador5 == 0 :
        print(constr, constr.getAttr("slack"))
        contador5 += 1

    elif constr.getAttr("slack") == 0 and constr.ConstrName[:2] == "R6" and contador6 == 0 :
        print(constr, constr.getAttr("slack"))
        contador6 += 1

    elif constr.getAttr("slack") == 0 and constr.ConstrName[:2] == "R7" and contador7 == 0 :
        print(constr, constr.getAttr("slack"))
        contador7 += 1

    elif constr.getAttr("slack") == 0 and constr.ConstrName[:2] == "R8" and contador8 == 0 :
        print(constr, constr.getAttr("slack"))
        contador8 += 1

    elif constr.getAttr("slack") == 0 and constr.ConstrName[:2] == "R9" and contador9 == 0 :
        print(constr, constr.getAttr("slack"))
        contador9 += 1

    elif constr.getAttr("slack") == 0 and constr.ConstrName[:2] == "R10" and contador10 == 0 :
        print(constr, constr.getAttr("slack"))
        contador10 += 1

    elif constr.getAttr("slack") == 0 and constr.ConstrName[:2] == "R11" and contador11 == 0 :
        print(constr, constr.getAttr("slack"))
        contador11 += 1

    elif constr.getAttr("slack") == 0 and constr.ConstrName[:2] == "R12" and contador12 == 0 :
        print(constr, constr.getAttr("slack"))
        contador12 += 1

    elif constr.getAttr("slack") == 0 and constr.ConstrName[:2] == "R13" and contador13 == 0 :
        print(constr, constr.getAttr("slack"))
        contador13 += 1
    
    elif constr.getAttr("slack") == 0 and constr.ConstrName[:2] == "R14" and contador14 == 0 :
        print(constr, constr.getAttr("slack"))
        contador14 += 1

# El siguiente codigo muestra que pasa si se tratan de ver todas las holguras, no se alcanza a imprimir todos los resultados.

# print("\n-------------\n")
# for constr in m.getConstrs():
#  print(constr, constr.getAttr("slack"))
    


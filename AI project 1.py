import pickle
import time
import math

with open("mapasgraph.pickle", "rb") as fp:   #Unpickling
    U = pickle.load(fp)[1]
    
with open("coords.pickle", "rb") as fp:
    coords = pickle.load(fp)

class SearchProblem:
    def __init__(self, goal, model = U, auxheir = coords):
        self.goal = goal
        self.model = model
        self.auxheir = auxheir
        
    def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf], anyorder = False):
        if len(init) == 1:
            a = self.alinea2(init, limitexp, limitdepth, tickets)
            return a
        elif len(init) == 3:
            if anyorder:
                a = self.alinea5(init, limitexp, limitdepth, tickets)
                return a
            else:
                a = self.aux2(init, self.goal ,limitexp, limitdepth, tickets)
                return a
        else:
            return "init tem que ter comprimento 1 ou 3."
        
    def alinea5(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf]):
        start = time.time()
        #z = distancias_individuais
        z = []
        #este ciclo calculas as distancias individuais com as combinacoies possiveis. no final, esta lista
        #vai ter 3 elementos, cada uma delas uma lista com 3 elementos, cada um dele o tamanho do caminho do
        #i-ésimo agente até ao j-ésimo objetivo.
        for i in range(3):
            z1 = []
            for j in range(3):
                z2 = self.aux7([init[i]], self.goal[j])
                z1 += [z2]
            z += [z1]
        
        tamanho1 = max([min([a[0] for a in z]),min([a[1] for a in z]),min([a[2] for a in z])]) + 1
        tamanho2 = max(min(z[0]), min(z[1]), min(z[2])) + 1
        tamanho = max([tamanho1,tamanho2])
        #existem 6 possiveis escolhas para os objetivos de cada agente, cada elemento representa para onde
        #cada agente vai. por exemplo: o caso [2,0,1] é o primeiro agente ir para o terceiro objetivo,
        #o segundo agente ir para o primeiro objetivo e o terceiro agente ir para o segundo objetivo.
        #possiveis_escolhas :
        p = [[0,1,2],[1,2,0],[2,0,1],[0,2,1],[1,0,2],[2,1,0]]
        #vamos agora ordenar estas possiveis escolhas de forma a cada agente ir para o objetivo mais proximo.
        i = 0
        while i < 5:
            if z[0][p[i][0]] + z[1][p[i][1]] + z[2][p[i][2]] <= z[0][p[i+1][0]] + z[1][p[i+1][1]] + z[2][p[i+1][2]]:
                i += 1
            else:
                p[i],p[i+1] = p[i+1],p[i]
                i = 0
        
        w = True
        i = 0
        a = [0,0,0,0,0,0]
        b = 20
        j = 0
        while w and i < 6:
            new_goal = [self.goal[p[i][0]], self.goal[p[i][1]], self.goal[p[i][2]]]
            if len(self.aux1(init, new_goal)) - 1 < b:
                a[i] = self.aux2(init, new_goal, tickets = tickets)
                if len(a[i]) < b:
                    b = len(a[i])
                    j = i
                if len(a[i]) == tamanho:
                    w = False
                else:
                    i += 1
            else:
                i += 1
                
        if not w:
            return a[i]
        else:
            return a[j]
        
        
        
        
        
    def aux2(self, init, goal,limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf]):
        #alinea 4
        a = self.aux1(init, goal) #usar a função usada na alínea 3 para calcular um caminho sem restrições de tickets
        
        
        b = [0,0,0] #b calcula quantos tickets foram usados nesse caminho.
        for i in range(1, len(a)):
            for j in range(3):
                if a[i][0][j] == 0:
                    b[0] += 1
                elif a[i][0][j] == 1:
                    b[1] += 1
                else:
                    b[2] += 1
                    
        r = True
        for i in range(3):
            if b[i] > tickets[i]:
                r = False
        if r:
            return a
        
        else:#aqui começa o programa a sério.
            #cada nó é [lista com as posições dos agentes, caminhos de cada agente, tickets gastos, heurística]
            
            
            
            def expand(no, lista, expansions, g = goal):
                if expansions < limitexp and len(no[1]) - 1 < limitdepth:
                    lista = lista[1:]
                    
                    
                    todasligacoes = [ligacoes(i) for i in no[0]]
                    for i in todasligacoes[0]:
                        for j in todasligacoes[1]:
                            for k in todasligacoes[2]:
                                
                                if i[1] != j[1] and j[1] != k[1] and i[1] != k[1]:
                                
                                    f = True
                                    
                                    e = [no[2][0],no[2][1],no[2][2]]
                                    d = [i,j,k]
                                    for n in range(3): #ciclo para criar os bilhetes do nó filho.
                                        if d[n][0] == 0:
                                            e[0] += 1
                                        elif d[n][0] == 1:
                                            e[1] += 1
                                        else:
                                            e[2] += 1
                                    for m in range(3):
                                        if e[m] > tickets[m]:
                                            f = False
                                    
                                    if f: #f é falso se os bilhetes do nó filho excederem os bilhetes existentes, e nesse caso
                                        #não se gera esse nó.
                                        if i[1] == g[0] and j[1] == g[1] and k[1] ==g[2]:
                                            filho = [ [i[1],j[1],k[1]], no[1] + [[ [i[0],j[0],k[0]] , [i[1],j[1],k[1]] ]], e, 0]
                                            lista = [filho] + lista
                                            return lista, expansions + 1
                                        
                                    
                                        h = self.heuristica([i[1],j[1],k[1]], goal)
                                        filho = [ [i[1],j[1],k[1]], no[1] + [[ [i[0],j[0],k[0]] , [i[1],j[1],k[1]] ]], e, h]
                                        
                                        h1 = len(no[1]) + h #h1 é f(n), ou seja, o custo até ao nó filho mais a sua heurística.
                                        a = 0
                                        b = True
                                        c = len(lista)
                                        while a < c and b: #ciclo para colocar o filho na lista
                                            if len(lista[a][1]) - 1 + lista[a][3] < h1:
                                                a += 1
                                            else:
                                                b = False
                                                lista = lista[:a] + [filho] + lista[a:]
    
                    return lista, expansions + 1
                else:
                    return lista[1:], expansions
            
            por_expandir = [[ init,[ [[],init] ], [0,0,0], len(a) - 1], [ init,[ [[],init] ], [0,0,0], 20]]
            a = True
            b = 0
            while a and len(por_expandir) > 1:
                por_expandir,b = expand(por_expandir[0], por_expandir, b)
                if por_expandir[0][0] == goal:
                     a = False
            if a:
                return "Não há solução possível com limitdepth: " + str(limitdepth) + " e limite de expansoes: " + str(limitexp) + " e com bilhetes: " + str(tickets)
            else:
                return por_expandir[0][1]
                
            
    def heuristica(self,init, goal):
        a = self.aux7([init[0]], goal[0])
        b = self.aux7([init[1]], goal[1])
        c = self.aux7([init[2]], goal[2])
        return max([a,b,c])
    
            
    def aux1(self, init, goal, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf]): 
        #alinea 3
        caminhos, tamanhos, indice = self.aux3(init, goal)
        #caminhos contem 3 caminhos dos agentes individualmente, podem sobrepoer-se, e podem nao ter o mesmo tamanho
        #tamanhos, é uma lista com o comprimento desses caminhos individuais
        #e indice é o indice do maior caminho, pode ser 0,1 ou 2
        indices = [a for a in range(3) if a != indice]
        
        if indices[1] > indices[0]: #vamos primeiro procurar o caminho para o seguundo mais longe, para o 
                                    #nao ser restringido pelo caminho menor.
            indices[1],indices[0] = indices[0],indices[1]
            
        #indices é a lista com os indices onde ainda falta encontrar um caminho.
        i = 0
        w = True
        caminhos_ja_percorridos = []
        while w: 
        #entramos num ciclo que encontra os caminhos para os 3 agentes, de tamanho igual e sem se sobreporem
        #quando para um certo comprimento não é possível... procura com o próximo comprimento.
            
            caminhos[indice] = self.aux5([init[indice]], goal[indice], tamanhos[indice] + i, caminhos = caminhos_ja_percorridos)
            
            if caminhos[indice] == 0:
                caminhos[indice] = self.aux8([init[indice]], goal[indice], tamanhos[indice] + i, caminhos = caminhos_ja_percorridos)
                
            if caminhos[indice] == 0:
                caminhos_ja_percorridos = []
                i += 1
            
            else:
            
                a = self.aux4([init[indices[0]]], goal[indices[0]], tamanhos[indice] + i, caminho1 = caminhos[indice])
                #a é o caminho para o proximo agente, com tamanho iual ao maior caminho e sem se sobrepor a esse
                caminhos[indices[0]] = a
                if a == 0:
                    a = self.aux6([init[indices[0]]], goal[indices[0]], tamanhos[indice] + i, caminho1 = caminhos[indice])
                
                if a == 0:
                    caminhos_ja_percorridos += [caminhos[indice]]
                    #i += 1
                    
                else: 
                    b = self.aux4([init[indices[1]]], goal[indices[1]], tamanhos[indice] + i, caminho1 = caminhos[indice], caminho2 = a)
                    #b é o caminho para o ultimo agente, com tamanho igual aos outros, e sem se sobrepor a nenhum
                    caminhos[indices[1]] = b
                    if b == 0:
                        b = self.aux6([init[indices[0]]], goal[indices[0]], tamanhos[indice] + i, caminho1 = caminhos[indice], caminho2 = a)
                    
                    if b == 0:
                        
                        caminhos_ja_percorridos += [caminhos[indice]]
                        print(str(caminhos_ja_percorridos) + " " + str(len(caminhos_ja_percorridos)))
                        
                        if len(caminhos_ja_percorridos) > 10:
                            caminhos_ja_percorridos = []
                            i += 1
                    else:
                            w = False          
        
        
        if not coincideQ([caminhos[indice],a,b]):
            
            r = [0,0,0]
            r[indice] = caminhos[indice]
            r[indices[0]] = a
            r[indices[1]] = b
            return apresentacao(r)
        else:
            return 4
        
        
    def aux3(self, init, goal, limitexp = 10000, limitdepth = 15, tickets = [math.inf,math.inf,math.inf]):#nó é uma lista [posiçao do no, caminho ate ao no]
    #função que rapidamente calcula o menor caminho de um ponto para outro. para os 3 agentes.
    #ideia:
    #calcula-se qual dos 3 policias esta mais longe do seu objetivo
    #e depois calcula-se um caminho com esse tamanha para os outros polícias.
        
        def expand3(no, lista, expansions, lista2, g = goal[0]):
            if expansions < limitexp and len(no[1]) - 1 < limitdepth and not(no[0] in lista2):
                lista = lista[1:]
                for i in ligacoes(no[0])[::-1]:
                    if i[1] == g:
                        lista = [[i[1] ,no[1] + [[[i[0]],[i[1]]]]]] + lista
                    else:
                        lista = lista + [[i[1] ,no[1] + [[[i[0]],[i[1]]]]]]  
                lista2 += [no[0]]
                return lista, expansions + 1, lista2
            else:
                return lista[1:], expansions, lista2
        r = []
        r1 = []
        for i in range(3):
            por_expandir = [[init[i],[[[],[init[i]]]]], [init[i],[[[],[init[i]]]]]]
            ja_expandidos = []
            a = True
            b = 0
            while a and len(por_expandir) > 0:
                por_expandir, b, ja_expandidos = expand3(por_expandir[0], por_expandir, b, ja_expandidos, g = goal[i])
                if por_expandir[0][0] == goal[i]:
                     a = False
                     
            r += [por_expandir[0][1]]
            r1 += [len(por_expandir[0][1]) - 1]
        r2 = 0
        for i in range(3):
            if r1[i] > r1[r2]:
                r2 = i
        return r, r1, r2
    
    def aux4(self, init, goal, n,limitexp = 100000, limitdepth = 15, tickets = [math.inf,math.inf,math.inf], caminho1 = [[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]]], caminho2 = [[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]]]):        
        #nó é uma lista [posiçao do no, caminho ate ao no]
        
    #função que rapidamente calcula um caminho com n passos, de um ponto para outro. nunca coincidindo
    #com caminhos dados.
    #ideia:
    #calcular o caminho do primeiro policia, depois calcular o caminho do segundo policia que nao coincida 
    #com esse, e finalmente calcular o caminho do terceiro policia sem coicidir com nenhum dos anteriores.

        def expand4(no, lista, m, lista2, g = goal):
            if not(no[0] in lista2):
                lista = lista[1:]
                for i in ligacoes(no[0])[::-1]:
                    a = True
                    if caminho1[len(no[1])][1][0] == i[1] or caminho2[len(no[1])][1][0] == i[1]:
                        a = False
                        
                        
                    if a:       
                        if len(no[1]) <= m:
                            if i[1] == g and len(no[1]) == m:
                                lista = [[i[1] ,no[1] + [[[i[0]],[i[1]]]]]] + lista
                            elif len(no[1]) == m:
                                pass
                            else:
                                lista = lista[:-1] + [[i[1] ,no[1] + [[[i[0]],[i[1]]]]]] + [lista[-1]]
                if no[0] != g and not(no[0] in [a[1] for a in ligacoes(g)]):
                    lista2 += [no[0]]
                return lista, lista2
            else:
                return lista[1:], lista2
        

            
        por_expandir = [[init[0],[[[],init]]], [init[0],[[[],init]]]]
        ja_expandidos = [0]
        a = True
        while a and len(por_expandir) > 1:
            if len(por_expandir) > 8000:          
                por_expandir = por_expandir[:100] 
            por_expandir, ja_expandidos = expand4(por_expandir[0], por_expandir, n, ja_expandidos)
            if por_expandir[0][0] == goal and len(por_expandir[0][1]) -1 == n:
                 a = False

        if a:
            return 0
        else:
            return por_expandir[0][1]
        
    def aux5(self, init, goal, n,limitexp = 100000, limitdepth = 15, tickets = [math.inf,math.inf,math.inf], caminhos = []):        
        #nó é uma lista [posiçao do no, caminho ate ao no]
        
    #função que rapidamente calcula um caminho com n passos, de um ponto para outro. nunca coincidindo
    #com caminhos dados.
    #ideia:
    #calcular o caminho do primeiro policia, depois calcular o caminho do segundo policia que nao coincida 
    #com esse, e finalmente calcular o caminho do terceiro policia sem coicidir com nenhum dos anteriores.

        def expand(no, lista, m, lista2, g = goal):
            if not(no[0] in lista2):
                lista = lista[1:]
                for i in ligacoes(no[0])[::-1]:
                    a = True
                    
                    if no[1] + [ [[i[0]],[i[1]] ] ] in caminhos:
                        a = False
                        
                        
                    if a:       
                        if len(no[1]) <= m:
                            if i[1] == g and len(no[1]) == m:
                                lista = [[i[1] ,no[1] + [[ [i[0]],[i[1]] ]]]] + lista
                            elif len(no[1]) == m:
                                pass
                            else:
                                lista = lista[:-1] + [[i[1] ,no[1] + [[[i[0]],[i[1]]]]]] + [lista[-1]]
                if no[0] != g and not(no[0] in [a[1] for a in ligacoes(g)]):
                    lista2 += [no[0]]
                return lista, lista2
            else:
                return lista[1:], lista2
        

            
        por_expandir = [[init[0],[[[],init]]], [init[0],[[[],init]]]]
        ja_expandidos = [0]
        a = True
        while a and len(por_expandir) > 1:
            if len(por_expandir) > 8000:          
                por_expandir = por_expandir[:100] 
            por_expandir, ja_expandidos = expand(por_expandir[0], por_expandir, n, ja_expandidos)
            if por_expandir[0][0] == goal and len(por_expandir[0][1]) -1 == n:
                 a = False

        if a:
            return 0
        else:
            return por_expandir[0][1]
        
    def aux6(self, init, goal, n,limitexp = 100000, limitdepth = 15, tickets = [math.inf,math.inf,math.inf], caminho1 = [[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]]], caminho2 = [[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]],[0,[0]]]):        
                #nó é uma lista [posiçao do no, caminho ate ao no]
        
    #função que lentamente calcula um caminho com n passos, de um ponto para outro. nunca coincidindo
    #com caminhos dados.
    #ideia:
    #se a rápida não der... usamos esta.

        def expand6(no, lista, m, g = goal):
            lista = lista[1:]
            for i in ligacoes(no[0])[::-1]:
                a = True
                if caminho1[len(no[1])][1][0] == i[1] or caminho2[len(no[1])][1][0] == i[1]:
                    a = False
                    
                if a:       
                    if len(no[1]) <= m:
                        if i[1] == g and len(no[1]) == m:
                            lista = [[i[1] ,no[1] + [[[i[0]],[i[1]]]]]] + lista
                        elif len(no[1]) == m:
                            pass
                        else:
                            lista = lista + [[i[1] ,no[1] + [[[i[0]],[i[1]]]]]]
            return lista

        

            
        por_expandir = [[init[0],[[[],init]]], [init[0],[[[],init]]]]
        a = True
        while a and len(por_expandir) > 1:
            if len(por_expandir) > 8000:          
                por_expandir = por_expandir[:100]
            por_expandir = expand6(por_expandir[0], por_expandir, n)
            if por_expandir[0][0] == goal and len(por_expandir[0][1]) -1 == n:
                 a = False

        if a:
            return 0
        else:
            return por_expandir[0][1]
        
        
    def aux7(self, init, goal): #nó é uma lista [posiçao do no, caminho ate ao no]
        #alínea 1
        def expand7(no, lista, expansions, lista2, g = goal):
            if not(no[0] in lista2):
                lista = lista[1:]
                for i in ligacoes(no[0])[::-1]:
                    if i[1] == g:
                        lista = [[i[1] ,no[1] + [[[i[0]],[i[1]]]]]] + lista
                    else:
                        lista = lista + [[i[1] ,no[1] + [[[i[0]],[i[1]]]]]]  
                lista2 += [no[0]]
                return lista, expansions + 1, lista2
            else:
                return lista[1:], expansions, lista2
            
        por_expandir = [[init[0],[[[],init]]], [init[0],[[[],init]]]]
        ja_expandidos = []
        a = True
        b = 0
        while a and len(por_expandir) > 0:
            por_expandir, b, ja_expandidos = expand7(por_expandir[0], por_expandir, b, ja_expandidos)
            if por_expandir[0][0] == goal:
                 a = False
        if a:
            return "Não há solução possível com limitdepth: " + str(limitdepth) + " e limite de expansoes: " + str(limitexp)
        else:
            return len(por_expandir[0][1]) - 1  
        
        
    def aux8(self, init, goal, n,limitexp = 100000, limitdepth = 15, tickets = [math.inf,math.inf,math.inf], caminhos = []):        
                #nó é uma lista [posiçao do no, caminho ate ao no]
        
    #função que lentamente calcula um caminho com n passos, de um ponto para outro. nunca coincidindo
    #com caminhos dados.
    #ideia:
    #se a rápida não der... usamos esta.

        def expand8(no, lista, m, g = goal):
            lista = lista[1:]
            for i in ligacoes(no[0])[::-1]:
                a = True
                
                if no[1] + [ [[i[0]],[i[1]] ] ] in caminhos:
                    a = False

                    
                if a:       
                    if len(no[1]) <= m:
                        if i[1] == g and len(no[1]) == m:
                            lista = [[i[1] ,no[1] + [[[i[0]],[i[1]]]]]] + lista
                        elif len(no[1]) == m:
                            pass
                        else:
                            lista = lista + [[i[1] ,no[1] + [[[i[0]],[i[1]]]]]]
            return lista

        

            
        por_expandir = [[init[0],[[[],init]]], [init[0],[[[],init]]]]
        a = True
        while a and len(por_expandir) > 1:
            if len(por_expandir) > 8000:          
                por_expandir = por_expandir[:100] 
            por_expandir = expand8(por_expandir[0], por_expandir, n)
            if por_expandir[0][0] == goal and len(por_expandir[0][1]) -1 == n:
                 a = False

        if a:
            return 0
        else:
            return por_expandir[0][1]
        
    def alinea2(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf]): 
        #nó é uma lista [posiçao do no, caminho ate ao no, bilhetes ate ao no, heuristica do no]
        #a heurística é o tamanho do caminho calculado sem a restrição dos tickets. que é admissível.
        def expand(no, lista, expansions, g = self.goal[0]):
            if expansions < limitexp and len(no[1]) - 1 < limitdepth:
                lista = lista[1:]
                for i in ligacoes(no[0])[::-1]:
                    
                    f = True
                    e = [0,0,0]
                    for n in range(3): #ciclo para criar os bilhetes do nó filho.
                        if i[0] == n:
                            e[n] = no[2][n] + 1
                            if e[n] > tickets[n]:
                                f = False
                        else:
                            e[n] = no[2][n] + 0
                            
                    if f: #f é falso se os bilhetes do nó filho excederem os bilhetes existentes, e nesse caso
                        #não se gera esse nó.
                        h = self.heuristica2([i[1]])
                        h1 = len(no[1]) + h #h1 é f(n), ou seja, o custo até ao nó filho mais a sua heurística.
                        
                        a = 0
                        b = True
                        while a < len(lista) and b: #ciclo para colocar o filho na lista
                            if len(lista[a][1]) - 1 + lista[a][3] < h1:
                                a += 1
                            else:
                                b = False
                                lista = lista[:a] + [[ i[1], no[1] + [[[i[0]],[i[1]]]], e, h]] + lista[a:]
                return lista, expansions + 1
            else:
                return lista[1:], expansions
            
        por_expandir = [[init[0],[[[],init]], [0,0,0], self.heuristica2(init)],[init[0],[[[],init]], [0,0,0],10000]]
        a = True
        b = 0
        while a and len(por_expandir) > 1:
            
            por_expandir,b = expand(por_expandir[0], por_expandir, b)
            if por_expandir[0][0] == self.goal[0]:
                 a = False
        if a:
            return "Não há solução possível com limitdepth: " + str(limitdepth) + " e limite de expansoes: " + str(limitexp) + " e com bilhetes: " + str(tickets)
        else:
            return por_expandir[0][1]
        
    def heuristica2(self, init):
        #calcula o tamanho do caminho calculado na primeira alínea do projeto.
        def expand(no, lista, lista2, g = self.goal[0]):
            if not(no[0] in lista2):
                lista = lista[1:]
                for i in ligacoes(no[0])[::-1]:
                    if i[1] == g:
                        lista = [[i[1] ,no[1] + [[[i[0]],[i[1]]]]]] + lista
                    else:
                        lista = lista + [[i[1] ,no[1] + [[[i[0]],[i[1]]]]]]  
                lista2 += [no[0]]
                return lista, lista2
            else:
                return lista[1:], lista2
            
        por_expandir = [[init[0],[[[],init]]], [init[0],[[[],init]]]]
        ja_expandidos = []
        a = True
        while a and len(por_expandir) > 0:
            por_expandir, ja_expandidos = expand(por_expandir[0], por_expandir, ja_expandidos)
            if por_expandir[0][0] == self.goal[0]:
                 a = False
        if a:
            return "Não há solução possível com limitdepth: " + str(limitdepth) + " e limite de expansoes: " + str(limitexp)
        else:
            return len(por_expandir[0][1]) - 1
    
def coincideQ(lista):
    c1 = lista[0]
    c2 = lista[1]  
    c3 = lista[2]
    if len(c1) == len(c2) and len(c2) == len(c3):
        r = False
        for i in range(len(c1)):
            if c1[i][1] == c2[i][1] or c1[i][1] == c3[i][1] or c2[i][1] == c3[i][1]:
                r = True
        return r
    else:
        return True
    
    
def apresentacao(lista):
    c1 = lista[0]
    c2 = lista[1]  
    c3 = lista[2]
    r = []
    for i in range(len(c1)):
        a = c1[i][0]+c2[i][0]+c3[i][0]
        b = c1[i][1]+c2[i][1]+c3[i][1]
        r += [[a,b]]
    return r
 
    
def coordenadas(n):
    return coords[n-1]
                
    
def distancia(n1, n2):
    c1 = coordenadas(n1)
    c2 = coordenadas(n2)
    return math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)

def ligacoes(n):
    return U[n]
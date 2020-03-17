import math 

#region Classes de Modelos
class IDF:
    def __init__( self ):
        self.idf = 0
        self.palavra = ""
    def Create(self, idf, palavra):
        self.idf = idf
        self.palavra = palavra
        return self

class TF:
    def __init__( self ):
        self.documento = 0
        self.palavra = ""
        self.valor = 0
    def Create(self, documento, palavra, valor):
        self.documento = documento
        self.palavra = palavra
        self.valor = valor
        return self

class Resultado:
    def __init__( self ):
        self.documento = 0
        self.valor = 0
    def Create(self, documento, valor):
        self.documento = documento
        self.valor = valor
        return self
#endregion

#region Importação arquivo
f = open("artigos.txt", "r")
if f.mode == "r":
	contents = f.read()

artigos = contents.replace(',', '').split("#")
qtd_artigos = len(artigos)
#endregion

#region Leitura da pesquisa
pesquisa = input("Digite o que você deseja pesquisar: ")
palavras_pesquisadas = pesquisa.replace(',', '').split()
#endregion 

for x in artigos:
    print(x)
print('---------')

#region Calculo de IDF
list_idf = []

palavras_documento = []
for val_artigo in artigos:
    palavras_documento = palavras_documento + val_artigo.split()

palavras_documento = list(dict.fromkeys(palavras_documento))

for x in palavras_documento:
    print(x)
print('---------')

for index in range(len(palavras_documento)):
    count = 0
    palavra = palavras_documento[index]
    for val_artigo in artigos:    
        is_exist = False
        for x in val_artigo.split():
            if x.strip().lower() == palavra.strip().lower():
                is_exist = True
        if is_exist:
            count = count + 1
    if count == 0:
        count = 1
    item = IDF().Create(math.log(len(artigos)/count), palavra)
    list_idf.insert(index, item)
#endregion

#region Calculo de IDF Não Consultado

for x in list_idf:
    print(x.palavra, x.idf)
print('---------')

#region TF-IDF
list_tf = []
count_insert = 0
for index in range(qtd_artigos):
    for val_idf in list_idf:
        count = 0
        for x in artigos[index].split():
            if x.strip().lower() == val_idf.palavra.strip().lower():
                count = count + 1
        item = TF().Create(index, val_idf.palavra, val_idf.idf * count)
        list_tf.insert(count_insert, item)
        count_insert = count_insert + 1
#endregion

for x in list_tf:
    print(x.documento, x.palavra, x.valor)
print('---------')

#region Cálculo de Similaridade
list_resultado = []
for index in range(qtd_artigos):
    soma = 0
    nr_documento = 0
    for value_tf in list_tf:
        if value_tf.documento == index:
            idf = 0
            for value_idf in list_idf:
                exist = False
                for x in palavras_pesquisadas:
                    if x.strip().lower() == value_idf.palavra.strip().lower():
                        exist = True
                if value_idf.palavra.strip().lower() == value_tf.palavra.strip().lower() and exist:
                    idf = value_idf.idf
            soma = soma + value_tf.valor * idf
            nr_documento = nr_documento + (value_tf.valor ** 2)
    if nr_documento == 0:
        nr_documento = 1        
    item = Resultado().Create(index, soma / (nr_documento ** (1/2)))
    list_resultado.insert(index, item)
#endregion

list_resultado.sort(key=lambda x: x.valor, reverse = True)
for x in list_resultado:
   print(x.documento, x.valor)
print('---------')

for x in list_resultado:
   print('D' + str(x.documento + 1), artigos[x.documento])
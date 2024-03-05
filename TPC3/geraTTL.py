import json
import random

with open("mapa-virtual.json") as f:
    bd = json.load(f)


ttl="""@prefix : <http://rpcw.di.uminho.pt/2024/mapa#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://rpcw.di.uminho.pt/2024/mapa> .

<http://rpcw.di.uminho.pt/2024/mapa> rdf:type owl:Ontology .

#################################################################
#    Object Properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/mapa#destino
:destino rdf:type owl:ObjectProperty ;
         rdfs:domain :Ligação ;
         rdfs:range :Cidade .


###  http://rpcw.di.uminho.pt/2024/mapa#emDistrito
:emDistrito rdf:type owl:ObjectProperty ;
            rdfs:domain :Cidade ;
            rdfs:range :Distrito .


###  http://rpcw.di.uminho.pt/2024/mapa#origem
:origem rdf:type owl:ObjectProperty ;
        rdfs:domain :Ligação ;
        rdfs:range :Cidade .


#################################################################
#    Data properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/mapa#descricao_cidade
:descricao_cidade rdf:type owl:DatatypeProperty ;
                  rdfs:domain :Cidade ;
                  rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/mapa#distancia_ligacao
:distancia_ligacao rdf:type owl:DatatypeProperty ;
                   rdfs:domain :Ligação ;
                   rdfs:range xsd:float .


###  http://rpcw.di.uminho.pt/2024/mapa#id_cidade
:id_cidade rdf:type owl:DatatypeProperty ;
           rdfs:domain :Cidade ;
           rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/mapa#id_ligacao
:id_ligacao rdf:type owl:DatatypeProperty ;
            rdfs:domain :Ligação ;
            rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/mapa#nome_cidade
:nome_cidade rdf:type owl:DatatypeProperty ;
             rdfs:domain :Cidade ;
             rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/mapa#nome_distrito
:nome_distrito rdf:type owl:DatatypeProperty ;
               rdfs:domain :Distrito ;
               rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/mapa#populacao_cidade
:populacao_cidade rdf:type owl:DatatypeProperty ;
                  rdfs:domain :Cidade ;
                  rdfs:range xsd:string .


#################################################################
#    Classes
#################################################################

###  http://rpcw.di.uminho.pt/2024/mapa#Cidade
:Cidade rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/mapa#Distrito
:Distrito rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/mapa#Ligação
:Ligação rdf:type owl:Class .


#################################################################
#    General axioms
#################################################################

[ rdf:type owl:AllDisjointClasses ;
  owl:members ( :Cidade
                :Distrito
                :Ligação
              )
] .

"""

cidades = set()
distritos = set()

for linha in bd["cidades"]:

    cidades.add(linha["id"])
    linha["distrito"]= linha["distrito"].replace(" ","_")
    
    if linha["distrito"] not in distritos:
        distritos.add(linha["distrito"])
        ttl+=f"""###  http://rpcw.di.uminho.pt/2024/mapa#{linha["distrito"]}
<http://rpcw.di.uminho.pt/2024/mapa#{linha["distrito"]}> rdf:type owl:NamedIndividual ,
    :Distrito ;
    :nome_distrito "{linha["distrito"]}"^^xsd:string .
    
"""

    ttl+=f"""###  http://rpcw.di.uminho.pt/2024/mapa#{linha["id"]}
<http://rpcw.di.uminho.pt/2024/mapa#{linha["id"]}> rdf:type owl:NamedIndividual ,
    :Cidade ;
    :id_cidade "{linha["id"]}"^^xsd:string ;
    :nome_cidade "{linha["nome"]}"^^xsd:string ;
    :populacao_cidade "{linha["população"]}"^^xsd:string ;
    :descricao_cidade "{linha["descrição"]}"^^xsd:string ;
    :emDistrito <http://rpcw.di.uminho.pt/2024/mapa#{linha["distrito"]}> .
    
"""



for linha in bd["ligacoes"]:
    if (linha["destino"] in cidades) and (linha["origem"] in cidades):
        ttl+=f"""###  http://rpcw.di.uminho.pt/2024/mapa#{linha["id"]}
<http://rpcw.di.uminho.pt/2024/mapa#{linha["id"]}> rdf:type owl:NamedIndividual ,
    :Ligação ;
  :id_ligacao "{linha["id"]}"^^xsd:string ;
  :distancia_ligacao "{linha["distância"]}"^^xsd:float ;
  :origem <http://rpcw.di.uminho.pt/2024/mapa#{linha["origem"]}> ;
  :destino <http://rpcw.di.uminho.pt/2024/mapa#{linha["destino"]}> .
  
"""


with open("mapa.ttl","w") as file:
    file.write(ttl)

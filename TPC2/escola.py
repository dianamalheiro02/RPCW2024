import json

f = open("db.json")
bd = json.load(f)
f.close()

ttl = '''@prefix : <http://rpcw.di.uminho.pt/2024/2024/3/musica_correct/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://rpcw.di.uminho.pt/2024/2024/3/musica_correct/> .

<http://rpcw.di.uminho.pt/2024/2024/3/musica_correct> rdf:type owl:Ontology .

#################################################################
#    Object Properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/2024/3/musica_correct#ensina
:ensina rdf:type owl:ObjectProperty ;
        rdfs:domain :Curso ;
        rdfs:range :Instrumento .


###  http://rpcw.di.uminho.pt/2024/2024/3/musica_correct#estuda
:estuda rdf:type owl:ObjectProperty ;
        rdfs:domain :Aluno ;
        rdfs:range :Curso .


#################################################################
#    Data properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/2024/3/musica_correct#anoCurso
:anoCurso rdf:type owl:DatatypeProperty ;
          rdfs:domain :Aluno ;
          rdfs:range xsd:int .


###  http://rpcw.di.uminho.pt/2024/2024/3/musica_correct#dataNascimento
:dataNascimento rdf:type owl:DatatypeProperty ;
                rdfs:domain :Aluno ;
                rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/2024/3/musica_correct#designação
:designação rdf:type owl:DatatypeProperty ;
            rdfs:domain :Curso ;
            rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/2024/3/musica_correct#duração
:duração rdf:type owl:DatatypeProperty ;
         rdfs:domain :Curso ;
         rdfs:range xsd:int .


###  http://rpcw.di.uminho.pt/2024/2024/3/musica_correct#nome_Aluno
:nome_Aluno rdf:type owl:DatatypeProperty ;
            rdfs:domain :Aluno ;
            rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/2024/3/musica_correct#nome_Instrumento
:nome_Instrumento rdf:type owl:DatatypeProperty ;
                  rdfs:domain :Instrumento ;
                  rdfs:range xsd:string .


#################################################################
#    Classes
#################################################################

###  http://rpcw.di.uminho.pt/2024/2024/3/musica_correct#Aluno
:Aluno rdf:type owl:Class ;
       rdfs:subClassOf [ rdf:type owl:Restriction ;
                         owl:onProperty :estuda ;
                         owl:someValuesFrom :Curso
                       ] .


###  http://rpcw.di.uminho.pt/2024/2024/3/musica_correct#Curso
:Curso rdf:type owl:Class ;
       rdfs:subClassOf [ rdf:type owl:Restriction ;
                         owl:onProperty :ensina ;
                         owl:someValuesFrom :Instrumento
                       ] .


###  http://rpcw.di.uminho.pt/2024/2024/3/musica_correct#Instrumento
:Instrumento rdf:type owl:Class .


#################################################################
#    General axioms
#################################################################

[ rdf:type owl:AllDisjointClasses ;
  owl:members ( :Aluno
                :Curso
                :Instrumento
              )
] .


###  Generated by the OWL API (version 4.5.26.2023-07-17T20:34:13Z) https://github.com/owlcs/owlapi

'''

for aluno in bd["alunos"]:
    ttl += f'''###  http://rpcw.di.uminho.pt/2024/2024/3/musica_correct#{aluno["id"]}
:{aluno["id"]} rdf:type owl:NamedIndividual ,
                 :Aluno ;
        :estuda :{aluno["curso"]} ;
        :anoCurso "{aluno["anoCurso"]}"^^xsd:int ;
        :dataNascimento "{aluno["dataNasc"]}" ;
        :nome_Aluno "{aluno["nome"]}" .

        
'''
    
for curso in bd["cursos"]:
    ttl+=f'''###  http://rpcw.di.uminho.pt/2024/2024/3/musica_correct#{curso["id"]}
:{curso["id"]} rdf:type owl:NamedIndividual ,
              :Curso ;
     :ensina :{curso["instrumento"]["id"]} ;
     :designação "{curso["designacao"]}" ;
     :duração {curso["duracao"]} .


'''
    
for instrumento in bd["instrumentos"]:
    ttl += f'''###  http://rpcw.di.uminho.pt/2024/2024/3/musica_correct#{instrumento["id"]}
:{instrumento["id"]} rdf:type owl:NamedIndividual ,
              :Instrumento ;
     :nome_Instrumento "{instrumento["#text"]}" .

'''


f = open("musica_correct.ttl", "w")
f.write(ttl)
f.close()

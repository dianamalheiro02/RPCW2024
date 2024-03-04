import json

f= open("db.json")
bd=json.load(f)
f.close()

individuals = set()

def format_space(ppt):
    return ppt.replace(" ", "_")

ttl=""

for corredor in bd["alunos"]:
    
    ttl += f"""
###  http://rpcw.di.uminho.pt/2024/escola#708{corredor['id']}
<http://rpcw.di.uminho.pt/2024/escola#{corredor['id']}> rdf:type owl:Aluno ,
                                                      :Aluno ;
                                             :hasNome :"{format_space(corredor['nome'])}" ;
                                             :hasDataNasc :"{format_space(corredor['dataNasc'])}" ;
                                             :hasCurso :{format_space(corredor['curso'])} ;
                                             :hasAnoCurso :"{format_space(str(corredor['anoCurso']))}" ;
                                             :hasInstrumento :{format_space(corredor['instrumento'])} .
"""
    properties = {
        #'Nome': corredor['nome'],
        #'DataNascimento': corredor['dataNasc'],
        'Curso': corredor['curso'],
        #'AnoCurso': str(corredor['anoCurso']),
        'Instrumento': corredor['instrumento']
    }
    
    for prop, value in properties.items():
        if value:
            prop_value = value.replace(" ","_")
            prop_name = prop.replace(" ", "_")
            if prop_value not in individuals:
                ttl += f"""
###  http://rpcw.di.uminho.pt/2024/escola#{prop_value}
:{prop_value} rdf:type owl:Aluno ,
              :{prop_name} .
"""
                individuals.add(prop_value)
                
                
#for element in individuals:
#    print(element)

#print(dif)
print(ttl)


# Open the file for reading and writing
with open('out.ttl', 'w') as file:
    # Write to the file (this will overwrite existing content)
    file.write(ttl)


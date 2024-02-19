import json

f= open("plantas.json")
bd=json.load(f)
f.close()

individuals = set()

def format_space(ppt):
    return ppt.replace(" ", "_")

ttl=""

for corredor in bd:
    properties = {
        'Código de rua': str(corredor['Código de rua']),
        'Rua': corredor['Rua'],
        'Local': corredor['Local'],
        'Freguesia': corredor['Freguesia'],
        'Espécie': corredor['Espécie'],
        'Nome Científico': corredor['Nome Científico'],
        'Origem': corredor['Origem'],
        'Data de Plantação': corredor['Data de Plantação'],
        'Estado' :corredor['Estado'],
        'Caldeira': corredor['Caldeira'],
        'Tutor': corredor['Tutor'],
        'Implantação': corredor['Implantação'],
        'Gestor': corredor['Gestor'],
        'Data de actualização': corredor['Data de actualização'],
        'Número de intervenções': str(corredor['Número de intervenções']),
    }
    
    for prop, value in properties.items():
        if value:
            prop_value = value.replace(" ","_")
            prop_name = prop.replace(" ", "_")
            if prop_value not in individuals:
                ttl += f"""
###  http://rpcw.di.uminho.pt/2024/plantas#{prop_value}
:{prop_value} rdf:type owl:NamedIndividual ,
              :{prop_name} .
"""
                individuals.add(prop_value)
                
    
    ttl += f"""
###  http://rpcw.di.uminho.pt/2024/plantas#708{corredor['Id']}
<http://rpcw.di.uminho.pt/2024/plantas#{corredor['Id']}> rdf:type owl:NamedIndividual ,
                                                      :Corredor ;
                                             :temCodigoRua :{format_space(str(corredor['Código de rua']))} ;
                                             :temRua :{format_space(corredor['Rua'])} ;
                                             :temLocal :{format_space(corredor['Local'])};
                                             :temFreguesia :"{format_space(corredor['Freguesia'])}" ;
                                             :temEspecie :"{format_space(corredor['Espécie'])}" ;
                                             :temNomeCientifico :"{format_space(corredor['Nome Científico'])}" ;
                                             :temOrigem :"{format_space(corredor['Origem'])}" ;
                                             :temDataPlantacao :"{format_space(corredor['Data de Plantação'])}" ;
                                             :temEstado :"{format_space(corredor['Estado'])}" ;
                                             :temCaldeira :"{format_space(corredor['Caldeira'])}" ;
                                             :temTutor :"{format_space(corredor['Tutor'])}" ;
                                             :temImplantacao :"{format_space(corredor['Implantação'])}" ;
                                             :temGestor :"{format_space(corredor['Gestor'])}" ;
                                             :temDataActualizacao :"{format_space(corredor['Data de actualização'])}" ;
                                             :temIntervencoes :"{format_space(str(corredor['Número de intervenções']))}" .




"""

print(ttl)

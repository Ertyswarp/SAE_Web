# importations
import pandas as pd
import numpy as np



# Categories des domaines medicales
Cardiaques=['CARDIOLOGIE','CARDIAQUE','CARDIOVASCULAIRE','THORACIQUE','DIABETOLOGIE','VASCULAIRE','PNEUMOLOGIE',"GERIATRIE"]
Pyschiatriques=['DPD',"GERIATRIE",'sclérose en plaques','transfusion sanguine','gérontologie','NEUROCHIRURGIE','NEUROLOGIE','NEUROPEDIATRIE','NEUROPSYCHIATRIE','PEDIATRIE','PSYCHIATRIE']
Addictifs=['CSAPA','addictologie','toxicomanes']
Cancereux=["CANCEROLOGIE","ONCOLOGIE","GERIATRIE"]


def recupData(nomTxt):
    data=[]
    resc=open(nomTxt,'r')
    while True:
        line=resc.readline()
        col=line.split(';')
        for i in range(len(col)):
            s=col[i].strip()
            s=s.replace('"',"")
            col[i]=s.upper()
            
        
        data.append(col)
        if not line:
            break

        
    resc.close()
    return data



def recherche(mot,table,SearchIndice,RepIndice):
    CodePresc=[]
    for i in range(len(table)-1):
        s=table[i][SearchIndice]
        if((s.find((mot.upper())))!=-1):
            CodePresc.append(table[i][RepIndice])
    return CodePresc

def recupDataCateg(table,categ):
    CodePrescCateg=[]
    for elt in categ:
        t=recherche(elt,table,1,0)
        for code in t:
            CodePrescCateg.append(code)
    return CodePrescCateg



def recupCodeCisCateg(table,CodesCateg):
    CodeCisCateg=[]
    for elt in CodesCateg:
        t=recherche(elt,table,1,0)
        for code in t:
            CodeCisCateg.append(code)
    return CodeCisCateg


def ClasserAdministreCateg(C1,C2,C3,C4):
    xls=pd.ExcelFile('resultat.xlsx')
    df=pd.read_excel(xls,"Resultat sondage")
    #nomColumn=df.columns
    nbLigne=len(df.index)
    nbColumns=len(df.columns)
    pCardiques=[]
    pPyschiatriques=[]
    pAdddictifs=[]
    pCancereux=[]
    df.fillna(0)
    
    for i in range(nbLigne):
        ligne=list(df.iloc(0))[i]
        for j in range(8,nbColumns):
            info=[]
            #if(not np.isnan(ligne[j])):
                #print(str(int((ligne[j]))))
            if(not np.isnan(ligne[j])):
                if(str(int(ligne[j])) in C1):
#                     print('cardiaques')
                    for k in range(8):
                        info.append(ligne[k])
                    if(not info in pCardiques):
                        pCardiques.append(info)
                
                elif(str(int(ligne[j])) in C2):
#                     print('psy')
                    for k in range(8):
                        info.append(ligne[k])
                    if(not info in pPyschiatriques):
                        pPyschiatriques.append(info)
                
                elif(str(int(ligne[j])) in C3):
#                     print('addi')
                    for k in range(8):
                        info.append(ligne[k])
                    if(not info in pAdddictifs):
                        pAdddictifs.append(info)
                
                elif(str(int(ligne[j])) in C4):
                    #print("cancereux")
                    for k in range(8):
                        info.append(ligne[k])
                    if(not info in pCancereux):
                        pCancereux.append(info)
                
    
    return pCardiques,pPyschiatriques,pAdddictifs,pCancereux

def affichage(resultat,nbChamp):
    for i in range(4):
        if(i==0):
            
            print("Liste des administrés ayant des problemes Cardiaques : \n")
            
        elif(i==1):
            
            print("Liste des administrés ayant des problemes Psychiatriques : \n")
            
        
        elif(i==2):
            
            print("Liste des administrés ayant des problemes Addictifs : \n")
            
        else:
            
            print("Liste des administrés ayant des problemes Cancereux : \n")
            
        for elt in resultat[i]:
            s=""
            for k in range(nbChamp):
                if(k==nbChamp-1):
                    s=s+str(elt[k])+"\n"
                else:
                    s=s+str(elt[k])+" "
            print(s)
        print("---------------------------------------------------------------\n\n")
            
            
    
# Recuperation des code Prescription par catégorie
dPresc=recupData("prescription.txt")

CodePresc_psy=recupDataCateg(dPresc,Pyschiatriques)
CodePresc_cancer=recupDataCateg(dPresc,Cancereux)
CodePresc_card=recupDataCateg(dPresc,Cardiaques)
CodePresc_addi=recupDataCateg(dPresc,Addictifs)
# Recuperation des codes CIS

dCorresp=recupData("correspondance.txt")
CodeCis_psy=recupCodeCisCateg(dCorresp,CodePresc_psy)
CodeCis_cancer=recupCodeCisCateg(dCorresp,CodePresc_cancer)
CodeCis_card=recupCodeCisCateg(dCorresp,CodePresc_card)
CodeCis_addi=recupCodeCisCateg(dCorresp,CodePresc_addi)

resultat=ClasserAdministreCateg(CodeCis_card,CodeCis_psy,CodeCis_addi,CodeCis_cancer)
pathologie={}
pathologie["Cardiques"]=len(resultat[0])
pathologie["Psychiatriques"]=len(resultat[1])
pathologie["Addictifs"]=len(resultat[2])
pathologie["Cancereux"]=len(resultat[3])
for cle, valeur in pathologie.items():
        print("Nombre d'administre ayant des problèmes ", cle, ":", valeur)

#affichage(resultat,3)

#print('60524826' in CodeCis_cancer)
#print('60058008' in CodeCis_cancer)
#print('60797287' in CodeCis_psy)
# print(CodeCis_psy)
# print(CodeCis_cancer)
# print(CodeCis_card)
# print(CodeCis_addi)


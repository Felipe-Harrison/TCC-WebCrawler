

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

string1 = "É #FAKE que foto de corintianos foi feita em meio a atos de vandalismo bolsonarista em 2022 no DF"
string2 = "Ministério Público Militar do STM pede a prisão de Alexandre de Moraes #boato"

similarity_ratio = similar(string1, string2)
print(f"A similaridade entre as strings é: {similarity_ratio}")
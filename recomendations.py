class Recomendation:
    def __init__(self,rec,exp,org):
        self.recomendation = rec
        self.explanation = exp
        self.origin = org

def get_recomendations(dayclass,name,weekday):
    reclist = []
    if dayclass == 'Solenidade':
        reclist.append(Recomendation('Ir à missa.','É obrigatório para todos os católicos ir à missa em dias de Solenidade.','name'))
    if (weekday == 1) and (dayclass != 'Solenidade'):
        reclist.append(Recomendation('Ir à missa.','É obrigatório para todos os católicos ir à missa aos domingos.','weekday'))
    if (weekday == 6) and (dayclass != 'Solenidade'):
        reclist.append(Recomendation('Abster-se de carne.','É obrigatório para todos os católicos abster-se de carne (exceto peixe) em todas as sextas-feiras do ano (exceto solenidades).','weekday'))
    if (name == 'Quarta-feira de Cinzas') or (name == 'Sexta-feira da Paixão do Senhor'):
        reclist.append(Recomendation('Fazer jejum.','É obrigatório para todos os católicos fazer jejum na Quarta-feira de Cinzas e na Sexta-feira Santa.','name'))
    return reclist
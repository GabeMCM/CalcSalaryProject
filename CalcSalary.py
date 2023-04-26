print()
print('Olá, preciso que me informa algumas coisas para que te retorne o que deseja.')
print()

def verificacao_input(pergunta, valor_1, valor_2):
    resposta = int(input(pergunta))
    while resposta != valor_1 and resposta != valor_2:
        print('Não entendi sua resposta, por favor digite novamente')
        resposta = int(input(pergunta))
    return resposta

decisao_salario = (
    verificacao_input('Você deseja me passar seu salário bruto ou o valor que a loja vendeu? (1 - Salário | 2 - Vendas)\n->', 1, 2)
    )

if decisao_salario == 1:
    valor_inicial = float(input('Me informe quanto você recebeu.\n->'))
    
else:
    porcentagem_sobre_vendas = float(input('Me informe a porcentagem que você ganha sobre as vendas.\n->'))
    valor_vendido= float(input('Me informe quanto você veneu.\n->'))
    valor_inicial = valor_vendido * (porcentagem_sobre_vendas / 100)

decisao_vale_transporte = (
    verificacao_input('Você recebe Vale_transporte? (1 - Sim | 2 - Não)\n->', 1, 2)
    )
if decisao_vale_transporte == 1:
    recebe_vale_transporte = True
else:
    recebe_vale_transporte = False
    
decisao_dependentes = int(input('Você possui dependentes? Se SIM, quantos? Se NÃO, digite "0"(sem aspas).\n->'))

decisao_pensao = (
    verificacao_input('Você paga pensão alimentícia? (1 - Sim | 2 - Não)\n->', 1, 2)
    )

if decisao_pensao == 1:
    desconta_pensao = True
    metodo_pagamento_pensao = (verificacao_input('A pensao é descontada no seu salario bruto ou líquido?(1 - Bruto | 2 - Líquido)\n->', 1, 2))
    if metodo_pagamento_pensao == 1:
        forma_de_pagamento_pensao = (
            verificacao_input('A pensão é descontada logo no seu salário bruto. Nesse caso, você paga um valor fixo de pensão ou um valor percentual?(1 - Fixo | 2 - Percentual)\n->', 1, 2)
            )
        if forma_de_pagamento_pensao == 1:
            valor_pago_de_pensao = float(input('Digite aqui o valor que voce paga de pensão\n->'))
        else:
            valor_pago_de_pensao = float(input('Digite aqui a pocentagem que voce paga de pensão\n->'))
    else:
        forma_de_pagamento_pensao = (
            verificacao_input('Apensão é descontada no seu salário líquido. Nesse caso, você paga um valor fixo de pensão ou um valor percentual?(1 - Fixo | 2 - Percentual)\n->', 1, 2)
            )
        if forma_de_pagamento_pensao == 1:
            valor_pago_de_pensao = float(input('Digite aqui o valor que voce paga de pensão\n->'))
        else:
            valor_pago_de_pensao = float(input('Digite aqui a pocentagem que voce paga de pensão\n->'))    
else:
    desconta_pensao = False 
    metodo_pagamento_pensao = 0
    forma_de_pagamento_pensao = 0
    valor_pago_de_pensao = 0
        
class CalculoSalario:

    def __init__(
        self, salario_bruto: float=0, vale_transporte: bool=False,dependentes: int=0,
        paga_pensao: bool=False, #True = Paga pensão || False = Não paga pensão -> decisao_pensao
        momento_desc_pensao: int=0, # 1 = desconto do salário bruto || 2 = desconto do salário liquido -> metodo_pagamento_pensao
        desc_fixo_ou_percent: int=0, #1 = desconta valor fixo || 2 = desconta valor percentual -> forma_de_pagamento_pensão
        valor_desc_pensao: float=0 # -> valor_pago_de_pensao
        ) -> None:   

        self.salario_bruto = salario_bruto
        self.desconto_inss = [
            (1302.00, 7.5, 0.0),
            (2571.29, 9.0, 19.53),
            (3856.94, 12.0, 96.67),
            (7507.49, 14.0, 173.81)
        ]
        #self.desconto_inss = [
        #    (1212.00, 7.5, 0.0),
        #    (2427.35, 9.0, 18.18),      -> valores referentes a 2022 
        #    (3641.03, 12.0, 91.01),
        #    (7087.22, 14.0, 163.00)
        #]
        self.desconto_irrf = [
            (1903.98, 0, 0),
            (2826.65, 7.5, 142.80),
            (3751.05, 15, 354.80),
            (4664.68, 22.5, 636.13),
            (float("inf"), 27.5, 869.36)
        ]

        self.momento_desc_pensao = momento_desc_pensao
        self.vale_transporte = vale_transporte
        self.dependentes = dependentes
        self.paga_pensao = paga_pensao
        self.desc_fixo_ou_percent = desc_fixo_ou_percent
        self.valor_desc_pensao = valor_desc_pensao

    def desc_dependentes(self):		
        return self.dependentes * 189.59

    def desc_pensao_bruto(self):
        if self.paga_pensao:
            if self.momento_desc_pensao == 1: #desconto do salário bruto                
                if self.desc_fixo_ou_percent == 1: #desconta valor fixo
                    return self.valor_desc_pensao
                elif self.desc_fixo_ou_percent == 2: #desconta percentual
                    return self.salario_bruto * (self.valor_desc_pensao / 100)   
            else: #desconto do salário liquido
                return 0                   
        else:
            return 0
        
    def desc_inss(self):
        valor_a_ser_descontado_de_inss = 0
        calcuclo_inss = (self.salario_bruto - self.desc_pensao_bruto()) - self.desc_vale_transporte()
        for limit, percent, reducao in self.desconto_inss:
            if calcuclo_inss <= limit:
                valor_a_ser_descontado_de_inss = (self.salario_bruto * (percent / 100)) - reducao
                break
            else:
                valor_a_ser_descontado_de_inss = 877.24
        return valor_a_ser_descontado_de_inss
    
    def desc_irrf(self):
        valor_a_ser_descontado_de_irrf = 0
        salario_descontado_tudo = (self.salario_bruto - (self.desc_inss() + self.desc_pensao_bruto() + self.desc_dependentes()))
        for limit, percent, reducao in self.desconto_irrf:
            if salario_descontado_tudo <= limit:
                valor_a_ser_descontado_de_irrf = (salario_descontado_tudo * (percent / 100)) - reducao
                break
        return valor_a_ser_descontado_de_irrf

    def desc_vale_transporte(self):
        if self.vale_transporte:
            return self.salario_bruto * 0.06
        else:
            return 0
        
    def salario_liquido(self):
        salario_final = (self.salario_bruto - (self.desc_vale_transporte() + self.desc_inss() + self.desc_irrf() + self.desc_pensao_bruto()))
        return salario_final

calc = CalculoSalario(valor_inicial, recebe_vale_transporte, decisao_dependentes, desconta_pensao, metodo_pagamento_pensao, forma_de_pagamento_pensao, valor_pago_de_pensao)

if metodo_pagamento_pensao == 2:
    if forma_de_pagamento_pensao == 1:
        salario = calc.salario_liquido() - valor_pago_de_pensao
    else:
        pensao = calc.salario_liquido() * (valor_pago_de_pensao / 100)
        salario = calc.salario_liquido() - pensao
else:
    salario = calc.salario_liquido()
    pensao = calc.desc_pensao_bruto()

descontos = calc.desc_inss() + calc.desc_irrf() + pensao + calc.desc_vale_transporte()

def criarTabela():

    print('Descrição\t\t\t\tDesconto')
    print(68*'-')
    print(f'INSS:\t\t\t\t\tR$ {calc.desc_inss():.2f}')
    print(f'IRRF:\t\t\t\t\tR$ {calc.desc_irrf():.2f}')
    print(f'PENSÃO:\t\t\t\t\tR$ {pensao:.2f}')
    print(f'VALE-TRANSPORTE:\t\t\tR$ {calc.desc_vale_transporte():.2f}')
    print(68*'-')
    print(f'Salario Bruto: R$ {valor_inicial:.2f}\t\tTotal Descontos: R$ {descontos:.2f}')
    print(68*'-')
    print(f'SALARIO LÍQUIDO:\t\t\tR$ {salario:.2f}')
    print()

criarTabela()
# Win Wizard #

* Autor: Oriol Gómez, mantido atualmente por Lukasz Golonka
* Compatibilidade con NVDA: 2019.3 e versões posteriores
* Download [Versão extável][1]

Este addon permite que você execute algumas operações na janela com o
foco e o processo associado a ele. Ao matar um processo ou mostrar/ocultar
uma janela, um bipe de confirmação é tocado se a ação tiver
sucesso. Se você acha isso irritante, pode desativar os bipes no painel
Opções do WinWizard, disponíveis na caixa de diálogo Opções do NVDA.

## Atalhos de teclado:
Todos esses comandos podem ser modificados na caixa de diálogo Gestos de entrada,
na categoria Win Wizard.
### Ocultar ou exibir janelas:
* NVDA+windows+números de 1 a 0 - Oculta a janela que tem foco no slot correspondente ao número pressionado
* NVDA+windows+seta esquerda - Move para a pilha anterior de janelas ocultas.
* NVDA+windows+seta direita - Move para a próxima pilha de janelas ocultas.
* Windows+shift+h - Oculta a janela em foco no primeiro slot disponível
* NVDA+windows+h - Exibe a última janela ocultada
* Windows+shift+l - Mostra a lista de todas as janelas ocultas agrupadas em pilhas (observe que a última janela oculta está selecionada)

### Gestão de processos:
* Windows+f4 - Encerra o processo associado à janela que está em foco
* NVDA+windows+p - Abre uma caixa de diálogo que permite definir a prioridade do processo associado à janela em foco

### Outros atalhos:
* NVDA+windows+tab - Alterna entre as janelas de nível superior do programa atual (útil em foobar2000, Back4Sure, etc.)
* Ctrl+alt+t - Permite alterar o título do programa que está em foco

## Alterações:

### Alterações para 5.0.5:

* Compatibilidade con NVDA 2023.1
* Tradução para pt_BR
* Resolvido bug de codificação UTF-8 no arquivo manifest

### Alterações para 5.0.4:

* Compatibilidade con NVDA 2022.1
* Agora é possível desabilitar os bips de confirmação nas configurações
* Traduções atualizadas

### Alterações para 5.0.3:

* Compatibilidade con NVDA 2021.1

### Alterações para 5.0.2:

* Primeira versão disponível no site de complementos

[1]: https://addons.nvda-project.org/files/get.php?file=winwizard

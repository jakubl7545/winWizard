# Win Wizard #
[[!meta title="Win Wizard"]]

* Autor: Oriol Gómez, Łukasz Golonka, manutenção atual por Jakub Lukowicz
* Compatibilidade com NVDA: 2019.3 e posterior
* Download [versão estável][1]

Esse complemento permite que você execute algumas operações na janela
focalizada ou no processo associado a ela.  Ao eliminar um processo ou
exibir/ocultar uma janela, um bipe de confirmação é emitido quando a ação é
bem-sucedida.  Se você achar isso incômodo, poderá desativar esses bipes no
painel de configurações do Win Wizard, disponível na caixa de diálogo de
configurações do NVDA.

## Comandos de teclado:
Todos esses comandos podem ser remapeados na caixa de diálogo Gestos de
entrada na categoria Win Wizard.
### Ocultar e exibir janelas ocultas:
* NVDA+Windows+números de 1 a 0 - oculta a janela atualmente focalizada no
  slot correspondente ao número pressionado
* NVDA+Windows+seta para a esquerda - move para a pilha anterior de janelas
  ocultas.
* NVDA+Windows+seta para a direita - passa para a próxima pilha de janelas
  ocultas.
* Windows+Shift+h - oculta a janela atualmente focalizada no primeiro espaço
  disponível
* NVDA+Windows+h - mostra a última janela oculta
* Windows+Shift+l - mostra a lista de todas as janelas ocultas agrupadas por
  pilhas (observe que, por padrão, a última janela oculta é selecionada)

### Gerenciar processos:
* Windows+F4 - elimina o processo associado à janela focada no momento
* NVDA+Windows+p - abre uma caixa de diálogo que permite definir a
  prioridade do processo associado à janela focada no momento

### Comandos diversos:
* NVDA+Windows+TAB - alterna entre as janelas de nível superior do programa
  atual (útil em foobar2000, Back4Sure etc.)
* CTRL+ALT+T - permite que você altere o título do programa atualmente em
  foco

## Alterações:

### Alterações para a versão 5.0.6:

* Compatibilidade com o NVDA 2024.1
* Atualizar traduções

### Alterações para a versão 5.0.5:

* Compatibilidade com o NVDA 2023.2
* Atualizar traduções

### Alterações para a versão 5.0.4:

* Compatibilidade com o NVDA 2022.1
* Agora é possível desativar os bipes de confirmação no painel de
  configurações dos complementos
* Atualizar traduções

### Alterações para a versão 5.0.3:

* Compatibilidade com o NVDA 2021.1

### Alterações para a versão 5.0.2:

* Primeira versão disponível no site de complementos

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=winwizard

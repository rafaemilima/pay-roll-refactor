# Refatoração do sistema

## Descrição
O presente repositório concerne à refatoração do código presente em https://github.com/rafaemilima/folha-de-pagamento , que se refere  à um Sistema de Folha de Pagamento.
Nesse repositório serão identificados e corrigidos alguns code smells do sistema no arquivo classes.py. 

<br>

## Code Smells Detectados

|       Smell Detectado      | Fonte                                                                                                                                                                                                                                                                                                                                           | Padrões e estratégias de refatoração                                                                                                                                                                  |
|:--------------------------:|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Long Method**            | - Método **undoRedo** na classe **Actions** é bastante extenso em linhas, além de ter várias ifs e elses, bem como realizar ações que fogem do seu escopo inicial de ação e que são comuns à todas as decisões. <br><br>  - Métodos **update** e **getAttribute** da classe  **Employee** apresentam diversas tomadas de decisão  de if e else. | **Extract Method** para os passos comuns para cada decisão, seguida da aplicação do **Strategy Pattern**, transformando cada decisão em uma subclasse, aplicando conceitos de herança e polimorfismo. |
| **Código Duplicado**       | - Métodos **update** e **getAttribute** apresentam a mesma estrutura de tomadas de decisão, apenas  diferindo em um passo que toma.<br><br>  - Método **addEmployee** na classe **Employee** apresenta o código com notáveis similaridades com o construtor de classe.                                                                          | **Extract Method** para os passos comum aos métodos.                                                                                                                                                  |
| **Speculative generality** | - Método **addEmployee** na classe **Employee**  não está sendo usado em nenhum local da aplicação.                                                                                                                                                                                                                                             | **Remove Method**, como o método se faz  desnecessário, o removeremos do código em detrimento do construtor.                                                                                          |
| **Primitive obcession**    | - Atributo **address** na classe **Employee** está sendo tratado como uma string.                                                                                                                                                                                                                                                               | **Replace data value with object**, criar um objeto endereço associado à classe empregado  com todos os atributos necessários                                                                         |
| **Feature Envy**           | - Método **remove** na classe **Employee** usa mais atributos e métodos da classe Company.<br><br> - Método **getEmployeeByID** na classe **Employee** usa mais atributos e métodos da classe Company.<br><br> - Método **undoRedo** na classe **Actions** manipula mais atributos da classe Action.                                            | **Move Method** aplicado para levar  os métodos para as classes mais apropriadas.                                                                                                                     |

## Padrões a serem aplicados

* Na resolução da **duplicação de código**, farei uso do **extract method** juntamente com o **template method**. 
* Para solucionar os smells **Long Method**, farei uso de padrões que combinam hierarquia e polimorfismo, com o padrão Strategy.
* Para solucionar os smells de **primitive obcession**, usarei o padrão replace data value with object.
* Para solucinar o smell de Speculative generality, removerei o método que não está em uso.
* Para solucionar os smells de Feature Envy farei uso do padrão move method.
<br>

## Code Smells solucionados

### Padrões Complexos
* **Long Method no método undoRedo**: Apois ser deslocado para a classe Action usando o **Move Method**, para cada tomada de decisão principal desse método foi criada uma subclasse correspondente da classe Action. Cada subclasse fazia uso do método abstrato undoRedo de Action, concluindo a nossa aplicação do *Strategy Pattern*. 


### Padrões Simples
* **Speculative Generality e Código Duplicado na função addEmployee**: Após se certificar que o método, apesar de muito semelhante, era inferior em funcionalidades ao construtor da classe e que o mesmo não estava sendo usado em nenhuma parte do sistema, descartou-se o método mantendo apenas o construtor.
<br>

* **Feature Envy no método undoRedo**: Essa função usava mais métodos e atributos da classe Action ao invés da classe em que estava, sendo assim apliquei o **Move Method** nesse método e o desloquei da classe Actions para Action. 
<br>

* **Feature Envy no metodo remove**: A função remove da classe Employee, apresenta uma predominância de métodos e atributos da classe Company. Sendo assim, apliquei o **Move Method** e desloquei esse método para a classe mais adequada, nesse caso a classe Company.
<br>

* **Feature Envy no método getEmployeeByID**: A função anteriormente na classe Employee, apresenta uma predominância de métodos e atributos da classe Company. Sendo assim, apliquei o **Move Method** e desloquei esse método para a classe Company.
<br>

* **Long Method no método undoRedoControl**: Após o move method, esse método de controle que continuou na classe Actions, permaneceu com ações fora do escopo da sua proposta de funcionalidade, sendo assim performou-se o **Extract Method** e criou-se duas funções auxiliares para realizar essas funções, deixando o código mais limpo e auto explicativo.

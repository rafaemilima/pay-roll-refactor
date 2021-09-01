# Refatoração do sistema

## Descrição
O presente repositório concerne à refatoração do código presente em https://github.com/rafaemilima/folha-de-pagamento , que se refere  à um Sistema de Folha de Pagamento.
Nesse repositório serão identificados e corrigidos alguns code smells do sistema no arquivo classes.py. 

<br>

## Smells Detectados

* Long method: Na classe Actions, o método undoRedo() apresenta diversos ifs e elses, além de ser um método bastante extenso no número de linhas.
<br><br>![image](https://user-images.githubusercontent.com/53321503/131696213-0d433b1d-4268-4eb1-9e81-f092ac44652f.png)
<br>

* Long method: Na classe Payagenda, o método getNextPayday() apresenta diversos ifs.
<br><br>![image](https://user-images.githubusercontent.com/53321503/131696475-27303310-1895-47b3-8db7-df425cd54439.png)
<br>

* Long method e código duplicado: Na classe employee temos os métodos update e get attribute que apresentam a mesma estrutura semântica e que tem diveros ifs e elses.
<br><br> ![image](https://user-images.githubusercontent.com/53321503/131696610-f77358fe-9c69-4fc2-bcd6-a5f97421204e.png)
![image](https://user-images.githubusercontent.com/53321503/131696813-00587d8e-8582-4764-a5a2-eb3cd39c52cb.png)
<br>

* Speculative generality e código duplicado: Na classe Employee temos um método de adicionar employee que realiza a mesma função do construtor e não está sendo usado.
<br><br> ![image](https://user-images.githubusercontent.com/53321503/131696981-205e5719-7985-4ab0-8fcb-d3145a5fa83b.png)
<br>

* Primitive obcession: O atributo endereço da classe Employee está sendo tratada como uma string.
<br><br> ![image](https://user-images.githubusercontent.com/53321503/131697209-cc9e7eb3-b5e8-4597-b232-431de75e09c1.png)
<br>

* Primitive obcession: O atributo data nas vendas está sendo tratado como uma string.
<br><br>![image](https://user-images.githubusercontent.com/53321503/131697340-3143e7fc-ceae-4954-918c-84c91ba4bda1.png)
<br>

## Padrões a serem aplicados

* Na resolução da **duplicação de código**, farei uso do **extract method** juntamente com o **template method**. 
* Para solucionar os smells **Long Method**, farei uso dos padrões que combinam hierarquia e polimorfismo, mais necessariamente com os padrões strategy, command e interpreter.
* Para solucionar os smells de **primitive obcession**, usarei o padrão replace data value with object.
* Para solucinar o smell de Speculative generality, usou-se uma estratégia semelhante à de chain constructors.
<br>

## Smells em solução 
* Primitive obcession. Solucionando com o padrão replace data value with object.
<br>


## Smells solucionados

* Speculative generality e código duplicado na função addEmployee: Após se certificar que o método era inferior em funcionalidades ao construtor da classe e que o mesmo não estava sendo usado em nenhuma parte do sistema, descartou-se a função mantendo apenas o construtor. 

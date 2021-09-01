# Refatoração do sistema

## Descrição
O presente repositório concerne à refatoração do código presente em https://github.com/rafaemilima/folha-de-pagamento , que se refere  à um Sistema de Folha de Pagamento.
Nesse repositório serão identificados e corrigidos alguns code smells do sistema no arquivo classes.py. 

<br>

## Smells Detectados

* Long method: Na classe Actions, o método undoRedo() apresenta diversos ifs e elses, além de ser um método bastante extenso no número de linhas. Segue abaixo um overview da quantidade de decisões efetuadas no método:
<br>

``` python    
  def undoRedo(self, company, redo):
        action = None
        if not redo and len(self.undostack) > 0:
        if redo and len(self.redostack) > 0:

        if action:
            if action.type == "remove":
            
            elif action.type == "create":
            
            elif action.type == "update":
            
            elif action.type == "updatetype":
                if redo:
                else:
                
            elif action.type == "generaltaxes":
            elif action.type == "aditionaltaxes":
                if redo:

            elif action.type == "sale":
                if redo:
                else:

            elif action.type == "clockin":
                if redo:

            elif action.type == "clockout":
                if redo:
                else:
                    
            elif action.type == "paymentoday":
                if redo:
                else:

            if redo:
            else:

```

<br>

* Long method: Na classe Payagenda, o método getNextPayday() apresenta diversos ifs.
``` python
    def getNextPayday(self, month, today):
        d = dt.date(today[2], today[1], today[0])
        if self.type == "W":
            if len(self.nextpayday) == 0:
                while d.weekday() != self.day:
                    d += dt.timedelta(1)
            else:
                d += dt.timedelta(7)

            list = [d.day, d.month, d.year]
            self.nextpayday = list

        elif self.type == "M":
            list = []
            if self.period == "end":
                h = self.getLastBusinessDay(2021, month)
                list = [h, month, d.year]
            elif self.period == "middle":
                if d.day > 15:
                    month += 1
                list = [15, month, d.year]
            elif self.period == "beggining":
                if d.day > 1:
                    month += 1
                list = [1, month, d.year]

            self.nextpayday = list

        elif self.type == "B":
            if len(self.nextpayday) == 0:
                while d.weekday() != self.day:
                    d += dt.timedelta(1)
            else:
                d += dt.timedelta(14)
            list = [d.day, d.month, d.year]
            self.nextpayday = list
```

<br>

* Long method e código duplicado: Na classe employee temos os métodos update e get attribute que apresentam a mesma estrutura semântica e que tem diveros ifs e elses.
``` python
    def getAttribute(self, parameter):
        if parameter == "name":
            return self.name
        elif parameter == "salary":
            return self.salary
        elif parameter == "syndicate":
            return self.issyndicate
        elif parameter == "comission":
            return self.comission
        elif parameter == "address":
            return self.address
        elif parameter == "paymethod":
            return self.payment.paymethod
        elif parameter == "salary_h":
            return self.salary_h
        elif parameter == "comission":
            return self.comission

    def update(self, parameter, value):
        if parameter == "name":
            self.name = value
        elif parameter == "salary":
            self.salary = value
        elif parameter == "syndicate":
            self.issyndicate = value
        elif parameter == "comission":
            self.comission = value
        elif parameter == "address":
            self.address = value
        elif parameter == "paymethod":
            self.payment.paymethod = value
        elif parameter == "salary_h":
            self.salary_h = value
        elif parameter == "comission":
            self.comission = value
        return
```
<br>

* Speculative generality e código duplicado: Na classe Employee temos um método de adicionar employee que realiza a mesma função do construtor e não está sendo usado.
``` python
    def addEmployee(self, company, name, address, jobtype, salary, issyndicate, salary_h, comission, id = None):
        if self.id:
            self.id = id
        else:
            self.id = self.defineID(company)

        self.name = name
        self.address = address
        self.jobtype = jobtype
        self.salary = salary
        self.issyndicate = issyndicate
        self.salary_h = salary_h
        self.comission = comission
        company.employees.append(self)
```
<br>

* Primitive obcession: O atributo endereço da classe Employee está sendo tratada como uma string.
``` python
  endereco = input("Endereço: ")
```
<br>

* Primitive obcession: O atributo data nas vendas está sendo tratado como uma string.
``` python
  data = input("informe a data da venda: ")
```
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

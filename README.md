# Refatoração do sistema

## Descrição
O presente repositório concerne à refatoração do código presente em https://github.com/rafaemilima/folha-de-pagamento , que se refere  à um Sistema de Folha de Pagamento.
Nesse repositório serão identificados e corrigidos alguns code smells do sistema no arquivo classes.py. 

<br>

## Code Smells Detectados

|       Code Smell Detectado      | Fonte                                                                                                                                                                                                                                                                                                                                           | Padrões e estratégias de refatoração                                                                                                                                                                  |
|:--------------------------:|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Long Method**            | - Método **undoRedo** na classe **Actions** é bastante extenso em linhas, além de ter várias ifs e elses, bem como realizar ações que fogem do seu escopo inicial de ação e que são comuns à todas as decisões.<br><br> - Método **getNextPayday** na classe **Payagenda** apresenta diversas tomadas de decisão que podem ser submetidas ao strategy pattern.| **Extract Method** para os passos comuns para cada decisão, seguida da aplicação do **Strategy Pattern**, transformando cada decisão em uma subclasse, aplicando conceitos de herança e polimorfismo. |
| **Código Duplicado**       | - Método **addEmployee** na classe **Employee** apresenta o código com notáveis similaridades com o construtor de classe.                                                                          | **Extract Method** para os passos comum aos métodos.                                                                                                                                                  |
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

## Code Smells Solucionados

### Refatorados por Padrões Simples

Nos padrãos simples referentes ao método undoRedo é importante mencionar que devido à extensão do método foi apresentada apenas uma pequena amostragem para demonstrar os padrões adotados. Caso queira conferir o método refatorado completo, avance para os padrões complexos. Tirando essa exceção, o restante dos códigos à seguir demonstra os métodos completos.

* **Speculative Generality e Código Duplicado na função addEmployee**: Após se certificar que o método, apesar de muito semelhante, era inferior em funcionalidades ao construtor da classe e que o mesmo não estava sendo usado em nenhuma parte do sistema, descartou-se o método mantendo apenas o construtor.
<br>

* **Primitive Obcession no atributo address da super classe Employee**: A refatoração consistiu em aplicar o padrão replace data value with object e o atributo address deixou de ser tratado como string e se tornou objeto de uma classe Address que possui atributos referentes ao conjunto de informações comunmente presentes em um endereço. 

``` python
# APÓS O REPLACE DATA VALUE WITH OBJECT
class Address:
    def __init__(self, street, number, district, city, state):
        self.street = street
        self.number = number
        self.district = district
        self.city = city
        self.state = state
```

<br>

* **Feature Envy no método undoRedo**: Essa função usava mais métodos e atributos da classe Action ao invés da classe em que estava, sendo assim apliquei o **Move Method** nesse método e o desloquei da classe Actions para Action. 

``` python
# ANTES DO MOVE METHOD

class Actions:
    def undoRedo(self, company, redo):
        # Após o pop da stack apropriada, se manipulava todos os atributos 
        # de um objeto da classe Action dentro da classe Actions
        action = None
        if not redo and len(self.undostack) > 0:
            action = self.undostack.pop()
        if redo and len(self.redostack) > 0:
            action = self.redostack.pop()
        # Exemplo da feature envy nos ifs do método UndoRedo:
        if action.type == "create":
             action.attrvalue = company.getPayagendaIndex(action.ogemployee)
             action.ogemployee.remove(company, action.ogemployee.id)
             action.type = "remove"
             print("Funcionário removido do sistema!")
        elif action.type == "update":
             old = action.ogemployee.getAttribute(action.attribute)
             action.ogemployee.update(action.attribute, action.attrvalue)
             action.attrvalue = old
             print("Atributo resetado.")
```

``` python
# APÓS O MOVE METHOD

class Actions:
    def undoRedoControl(self, company, redo):
        action = None
        if not redo and len(self.undostack) > 0:
            action = self.undostack.pop()
        if redo and len(self.redostack) > 0:
            action = self.redostack.pop()
        action.undoRedo(company, redo)
        if redo:
            self.undostack.append(action)
            print(f"Ação refeita")
        else:
            self.redostack.append(action)
            print(f"Ação desfeita")

class Action:
    def undoRedo(self, company, redo):
        if self.type == "create":
            self.attrvalue = company.getPayagendaIndex(self.ogemployee)
            self.ogemployee.remove(company, self.ogemployee.id)
            self.type = "remove"
            print("Funcionário removido do sistema!")
        elif self.type == "update":
            old = self.ogemployee.getAttribute(self.attribute)
            self.ogemployee.update(self.attribute, self.attrvalue)
            self.attrvalue = old
            print("Atributo resetado.")
            # print(action.attrvalue)
    
```

<br>

* **Feature Envy no metodo remove**: A função remove da classe Employee, apresenta uma predominância de métodos e atributos da classe Company. Sendo assim, apliquei o **Move Method** e desloquei esse método para a classe mais adequada, nesse caso a classe Company.

``` python
# ANTES DO MOVE METHOD

class Employee:
    @staticmethod
    def remove(company, s_id):
        e = Employee.getEmployeeByID(company, s_id)
        for agenda in company.payagendas:
            if e in agenda.employees:
                agenda.employees.remove(e)
        for i in company.employees:
            if i.id == int(s_id):
                company.employees.remove(i)
                del(i)

        return
```

```python
# APÓS O MOVE METHOD

class Company:
    def remove(self, s_id):
        e = self.getEmployeeByID(s_id)
        for agenda in self.payagendas:
            if e in agenda.employees:
                agenda.employees.remove(e)
        for i in self.employees:
            if i.id == int(s_id):
                self.employees.remove(i)
                del(i)
        return
```
<br>

* **Feature Envy no método getEmployeeByID**: A função anteriormente na classe Employee, apresenta uma predominância de métodos e atributos da classe Company. Sendo assim, apliquei o **Move Method** e desloquei esse método para a classe Company.

``` python
# ANTES DO MOVE METHOD

class Employee:
    @staticmethod
    def getEmployeeByID(company, s_id):
        for i in company.employees:
            if i.id == int(s_id):
                return i
        return None
```

``` python
# APÓS O MOVE METHOD

class Company:
    def getEmployeeByID(self, s_id):
        for employee in self.employees:
            if employee.id == int(s_id):
                return employee
        return None
```
<br>

* **Long Method no método undoRedoControl**: Após o move method, esse método de controle que continuou na classe Actions, permaneceu com ações fora do escopo da sua proposta de funcionalidade, sendo assim performou-se o **Extract Method** e criou-se duas funções auxiliares para realizar essas funções, deixando o código mais limpo e auto explicativo.

```python
# ANTES DO EXTRACT METHOD

   def undoRedoControl(self, company, redo):
        action = None
        if not redo and len(self.undostack) > 0:
            action = self.undostack.pop()
        if redo and len(self.redostack) > 0:
            action = self.redostack.pop()
        action.undoRedo(company, redo)
        if redo:
            self.undostack.append(action)
            print(f"Ação refeita")
        else:
            self.redostack.append(action)
            print(f"Ação desfeita")
```

```python
# APÓS O EXTRACT METHOD
   
   def pushAction(self, action, redo):
        if redo:
            self.undostack.append(action)
            print(f"Ação refeita")
        else:
            self.redostack.append(action)
            print(f"Ação desfeita")

    def popAction(self, redo):
        if not redo and len(self.undostack) > 0:
            return self.undostack.pop()
        elif redo and len(self.redostack) > 0:
            return self.redostack.pop()

    def undoRedoControl(self, company, redo):
        action = self.popAction(redo)
        if action:
            action.undoRedo(company, redo)
            self.pushAction(action, redo)
   
```
<br>

### Refatorados por Padrões Complexos
* **Long Method no método undoRedo**: Apois ser deslocado para a classe Action usando o **Move Method**, para cada tomada de decisão principal desse método foi criada uma subclasse correspondente da classe Action. Cada subclasse fazia uso do método abstrato undoRedo de Action, concluindo a nossa aplicação do *Strategy Pattern*.

``` python
# ANTES DA APLICAÇÃO DO STRATEGY PATTERN

class Actions:
    def __init__(self):
        self.redostack = []
        self.undostack = []

    def undoRedo(self, company, redo):
        action = None
        if not redo and len(self.undostack) > 0:
            action = self.undostack.pop()
        if redo and len(self.redostack) > 0:
            action = self.redostack.pop()

        if action:
            if action.type == "remove":
                company.employees.append(action.ogemployee)
                company.payagendas[action.attrvalue].employees.append(action.ogemployee)
                print("Funcionário cadastrado no sistema!")
                action.type = "create"
                
            elif action.type == "create":
                action.attrvalue = company.getPayagendaIndex(action.ogemployee)
                action.ogemployee.remove(company, action.ogemployee.id)
                action.type = "remove"
                print("Funcionário removido do sistema!")
                
            elif action.type == "update":
                old = action.ogemployee.getAttribute(action.attribute)
                action.ogemployee.update(action.attribute, action.attrvalue)
                action.attrvalue = old
                print("Atributo resetado.")

            elif action.type == "updatetype":
                if redo:
                    aux = {"H": 0, "S": 2, "C": 1}
                    company.payagendas[aux[action.ogemployee.jobtype]].employees.append(action.ogemployee)
                    Employee.remove(company, action.attrvalue[0].id)
                    company.employees.append(action.ogemployee)
                else:
                    Employee.remove(company, action.ogemployee.id)
                    company.employees.append(action.attrvalue[0])
                    company.payagendas[action.attrvalue[1]].employees.append(action.attrvalue[0])
                    
            elif action.type == "generaltaxes":
                old = company.syndicate.taxes
                company.syndicate.taxes = action.attrvalue
                action.attrvalue = old

            elif action.type == "aditionaltaxes":
                new = action.attrvalue
                if redo:
                    new = new * (-1)
                action.ogemployee.aditional_taxes -= new
                print("Taxa adicional resetada")

            elif action.type == "sale":
                if redo:
                    action.ogemployee.addSale(action.attrvalue[0], action.attrvalue[1])
                    print(len(action.ogemployee.sales))
                else:
                    sale = action.ogemployee.sales.pop()
                    action.ogemployee.payment.value -= action.ogemployee.comission_amount
                    action.ogemployee.comission_amount -= (sale.value * action.ogemployee.comission_percent)
                    
            elif action.type == "clockin":
                new = action.attrvalue
                action.ogemployee.workstarthour = 0
                if redo:
                    action.ogemployee.workstarthour += new


            elif action.type == "clockout":
                employee = action.ogemployee
                if redo:
                    employee.punchTheClockOut(action.attrvalue[1], action.attrvalue[0])
                else:
                    employee.workendhour = int(action.attrvalue[1])
                    work_day = employee.workendhour - int(action.attrvalue[0])
                    employee.hours_amount -= work_day
                    employee.payment.value -= employee.calculateSalary(work_day)

            elif action.type == "paymentoday":
                d = dt.date.today()
                if redo:
                    print("Pagamentos do dia refeitos")
                    company.makePayments([d.day, d.month, d.year], company.syndicate.taxes)
                else:
                    print("Pagamentos do dia desfeitos")
                    for agenda in action.attrvalue:
                        agenda.nextpayday = [d.day, d.month, d.year]

            if redo:
                self.undostack.append(action)
                print(f"Ação refeita")
            else:
                self.redostack.append(action)
                print(f"Ação desfeita")
```

``` python
# APÓS A APLICAÇÃO DO STRATEGY PATTERN

class Action(ABC):
    def __init__(self, actions, employee, value=None, attribute=None):
        self.ogemployee = employee
        self.attribute = attribute
        self.attrvalue = value
        actions.undostack.append(self)
        if len(actions.redostack) > 0:
            actions.redostack = []

    @abstractmethod
    def undoRedo(self, company, redo):
        pass


class Create(Action):
    def undoRedo(self, company, redo):
        if redo:
            company.employees.append(self.ogemployee)
            company.payagendas[self.attrvalue].employees.append(self.ogemployee)
            print("Funcionário cadastrado no sistema!")
        else:
            self.attrvalue = company.getPayagendaIndex(self.ogemployee)
            company.remove(self.ogemployee.id)
            print("Funcionário removido do sistema!")


class Remove(Action):
    def undoRedo(self, company, redo):
        if redo:
            self.attrvalue = company.getPayagendaIndex(self.ogemployee)
            company.remove(self.ogemployee.id)
            print("Funcionário removido do sistema!")

        else:
            company.employees.append(self.ogemployee)
            company.payagendas[self.attrvalue].employees.append(self.ogemployee)
            print("Funcionário cadastrado no sistema!")


class Update(Action):
    def undoRedo(self, company, redo):
        old = self.ogemployee.getAttribute(self.attribute)
        self.ogemployee.update(self.attribute, self.attrvalue)
        self.attrvalue = old
        print("Atributo resetado.")
        # print(action.attrvalue)


class GeneralTaxes(Action):
    def undoRedo(self, company, redo):
        old = company.syndicate.taxes
        company.syndicate.taxes = self.attrvalue
        self.attrvalue = old
        print("Taxa geral resetada.")


class AditionalTaxes(Action):
    def undoRedo(self, company, redo):
        # print(action.ogemployee.aditional_taxes)
        new = self.attrvalue
        if redo:
            new = new * (-1)
        self.ogemployee.aditional_taxes -= new
        print("Taxa adicional resetada")
        # print(action.ogemployee.aditional_taxes)
        
class MakeSale(Action):
    def undoRedo(self, company, redo):
        if redo:
            self.ogemployee.addSale(self.attrvalue[0], self.attrvalue[1])
            print(len(self.ogemployee.sales))
        else:
            sale = self.ogemployee.sales.pop()
            self.ogemployee.payment.value -= self.ogemployee.comission_amount
            self.ogemployee.comission_amount -= (sale.value * self.ogemployee.comission_percent)
            print(len(self.ogemployee.sales))


class ClockIn(Action):
    def undoRedo(self, company, redo):
        new = self.attrvalue
        self.ogemployee.workstarthour = 0
        if redo:
            self.ogemployee.workstarthour += new
        print("Horário de início de expediente resetado")
        # print(action.ogemployee.workstarthour)


class ClockOut(Action):
    def undoRedo(self, company, redo):
        employee = self.ogemployee
        if redo:
            employee.punchTheClockOut(self.attrvalue[1], self.attrvalue[0])
        else:
            employee.workendhour = int(self.attrvalue[1])
            work_day = employee.workendhour - int(self.attrvalue[0])
            employee.hours_amount -= work_day
            employee.payment.value -= employee.calculateSalary(work_day)
        print("Horário de final de expediente resetado")
        # print(employee.hours_amount)
        # print(employee.payment.value)


class PaymentToday(Action):
    def undoRedo(self, company, redo):
        d = dt.date.today()
        if redo:
            print("Pagamentos do dia refeitos")
            company.makePayments([d.day, d.month, d.year], company.syndicate.taxes)
        else:
            print("Pagamentos do dia desfeitos")
            for agenda in self.attrvalue:
                agenda.nextpayday = [d.day, d.month, d.year]


```

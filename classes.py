from random import randint
from abc import ABC, abstractmethod
import calendar
import time
import datetime as dt


class Actions():
    def __init__(self):
        self.redostack = []
        self.undostack = []

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
        print(f"undostack: {len(self.undostack)} redostack: {len(self.redostack)}")


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


class CreateEmployee(Action):
    def undoRedo(self, company, redo):
        if redo:
            company.employees.append(self.ogemployee)
            company.payagendas[self.attrvalue].employees.append(self.ogemployee)
            print("Funcionário cadastrado no sistema!")
        else:
            self.attrvalue = company.getPayagendaIndex(self.ogemployee)
            company.remove(self.ogemployee.id)
            print("Funcionário removido do sistema!")


class RemoveEmployee(Action):
    def undoRedo(self, company, redo):
        if redo:
            self.attrvalue = company.getPayagendaIndex(self.ogemployee)
            company.remove(self.ogemployee.id)
            print("Funcionário removido do sistema!")

        else:
            company.employees.append(self.ogemployee)
            company.payagendas[self.attrvalue].employees.append(self.ogemployee)
            print("Funcionário cadastrado no sistema!")


class UpdateEmployee(Action):
    def undoRedo(self, company, redo):
        old = self.ogemployee.getAttribute(self.attribute)
        self.ogemployee.update(self.attribute, self.attrvalue)
        self.attrvalue = old
        print("Atributo resetado.")
        # print(action.attrvalue)


class UpdateEmployeeType(Action):
    def undoRedo(self, company, redo):
        if redo:
            aux = {"H": 0, "S": 2, "C": 1}
            company.payagendas[aux[self.ogemployee.jobtype]].employees.append(self.ogemployee)
            company.remove(self.attrvalue[0].id)
            company.employees.append(self.ogemployee)
        else:
            company.remove(self.ogemployee.id)
            company.employees.append(self.attrvalue[0])
            company.payagendas[self.attrvalue[1]].employees.append(self.attrvalue[0])


class ChangeGeneralTaxes(Action):
    def undoRedo(self, company, redo):
        old = company.syndicate.taxes
        company.syndicate.taxes = self.attrvalue
        self.attrvalue = old
        print("Taxa geral resetada.")


class ChangeAditionalTaxes(Action):
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


class MakePaymentToday(Action):
    def undoRedo(self, company, redo):
        d = dt.date.today()
        if redo:
            print("Pagamentos do dia refeitos")
            company.makePayments([d.day, d.month, d.year], company.syndicate.taxes)
        else:
            print("Pagamentos do dia desfeitos")
            for agenda in self.attrvalue:
                agenda.nextpayday = [d.day, d.month, d.year]


class Company:
    def __init__(self):
        self.employees = []
        self.payagendas = []
        self.standardPayagendas()
        self.actions = Actions()
        self.syndicate = Syindicate(0,  1)

    def getPayagendaIndex(self, employee):
        i = 0
        for payagenda in self.payagendas:
            if employee in payagenda.employees:
                return i
            i += 1
        return - 1


    def cleanStacks(self):
        self.actions.undostack = []
        self.actions.redostack = []

    def printEmployees(self):
        for employee in self.employees:
            print(f"Nome: {employee.name}\nID: {employee.id}")

    def standardPayagendas(self):
        date = time.localtime()
        month = int(time.strftime("%m", date))
        weekly = AgendaW(4, None)
        bimonthly = AgendaB(4, None)
        monthly = AgendaM(None, "end")
        self.payagendas.append(weekly)
        self.payagendas.append(bimonthly)
        self.payagendas.append(monthly)

    def getEmployeeByID(self, s_id):
        for employee in self.employees:
            if employee.id == int(s_id):
                return employee
        return None

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


    def returnPayagenda(self, searched_employee):
        for payagenda in self.payagendas:
            if searched_employee in payagenda.employees:
                return payagenda

    def printPayAgendas(self):
        for payagenda in self.payagendas:
            print(payagenda.nextpayday)

    def makePayments(self, today, general_taxes):
        for payagenda in self.payagendas:
            if today == payagenda.nextpayday:
                for employee in payagenda.employees:
                    employee.getSalary()
                    total = employee.payment.value
                    if employee.issyndicate:
                        total = employee.payment.value - general_taxes
                    print("\n-------------NEW PAYMENT-------------")
                    print("Employee Informations")
                    print("---------------------------------------")
                    print(f"ID: {employee.id}")
                    print(f"Name: {employee.name}")
                    print("---------------------------------------")
                    print("Payment Details")
                    print("---------------------------------------")
                    print(f"Value: {employee.payment.value}")
                    if employee.issyndicate:
                        print(f"General syndicate taxes: {self.syndicate.taxes}")
                    else:
                        print(f"General syndicate taxes: 0")
                    print(f"Aditional syndicate taxes: {employee.aditional_taxes}")
                    print(f"Total: {total}")
                    print(f"Pay Method: {employee.payment.paymethod}")
                    print(f"Data: {today[0]}/{today[1]}/{today[2]}")
                    print("--------------------------------------\n")
                    employee.resetPaymentS()
                    if employee.jobtype == "C":
                        employee.resetPaymentC()

                    elif employee.jobtype == "H":
                        employee.resetPaymentH()

                month = today[1]

                if payagenda.returnType() == "M":
                    month = (month + 1) % 12
                    if month == 0:
                        month += 1

                payagenda.getNextPayday(month, today)


class Payagenda(ABC):
    def __init__(self, day, period):
        d = dt.date.today()
        self.employees = []
        self.nextpayday = []
        self.day = day
        self.period = period
        self.getNextPayday(d.month, [d.day, d.month, d.year])


    @abstractmethod
    def getNextPayday(self, month, today):
        pass

    @abstractmethod
    def returnType(self):
        pass


class AgendaM(Payagenda):
    def getNextPayday(self, month, today):
        d = dt.date(today[2], today[1], today[0])

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

    def returnType(self):
        return "M"

    @staticmethod
    def getLastBusinessDay(year: int, month: int) -> int:
        return max(calendar.monthcalendar(year, month)[-1:][0][:5])


class AgendaW(Payagenda):
    def getNextPayday(self, month, today):
        d = dt.date(today[2], today[1], today[0])
        if len(self.nextpayday) == 0:
            while d.weekday() != self.day:
                d += dt.timedelta(1)
        else:
            d += dt.timedelta(7)

        list = [d.day, d.month, d.year]
        self.nextpayday = list

    def returnType(self):
        return "W"


class AgendaB(Payagenda):
    def getNextPayday(self, month, today):
        d = dt.date(today[2], today[1], today[0])

        if len(self.nextpayday) == 0:
            while d.weekday() != self.day:
                d += dt.timedelta(1)
        else:
            d += dt.timedelta(14)
        list = [d.day, d.month, d.year]
        self.nextpayday = list

    def returnType(self):
        return "B"


class Employee:
    def __init__(self, company = None, name = None, address = None, jobtype = None, salary = 0, issyndicate = False,
                 comission = None, salary_h = None, id = None, paymethod = None):

        if id:
            self.id = id
        else:
            self.id = self.defineID(company)

        self.name = name
        self.address = address
        self.jobtype = jobtype
        self.salary = salary
        self.comission = comission
        self.payment = None
        self.salary_h = salary_h
        self.card = None
        self.aditional_taxes = 0
        self.payment = Payment(paymethod)

        if issyndicate == "y":
            self.issyndicate = True
        else:
            self.issyndicate = False

        company.employees.append(self)

        if self.jobtype == "S":
            company.payagendas[2].employees.append(self)


    def resetPaymentS(self):
        self.payment.value = 0

    def getSalary(self):
        if self.jobtype == "C":
            self.payment.value += (self.salary/2)
        else:
            self.payment.value += (self.salary)
        self.payment.value -= self.aditional_taxes

    def info(self):
        print("###################################")
        print(f"ID do funcionário: {self.id}")
        print(f"Nome do funcionário: {self.name}")
        self.address.printAddress()
        print(f"Tipo de afiliação: {self.jobtype}")
        print(f"Salário fixo: {self.salary}")
        print(f"Salário Horário: {self.salary_h}")
        print(f"Taxa de Comissão: {self.comission}")
        print(f"Afiliação Sindical: {self.issyndicate}")
        print(f"Método de pagamento: {self.payment.paymethod}")
        if self.card:
            print(f"ID do cartão de ponto: {self.card.cardid}")
        print("###################################")

    def getAttribute(self, parameter):
        if parameter == "paymethod":
            return getattr(self.payment, parameter)
        return getattr(self, parameter)

    def update(self, parameter, value):
        if parameter == "paymethod":
            setattr(self.payment, parameter, value)
        else:
            setattr(self, parameter, value)

    @staticmethod
    def takeIDs(company):
        ids = []
        for i in company.employees:
            ids.append(i.id)
        return ids

    def defineID(self, company):
        id = randint(100000000, 999999999)  # return the id
        ids = self.takeIDs(company)
        while id in ids:
            id = randint(100000000, 999999999)
        return id


class Hourly(Employee):
    def __init__(self, company, name = None, address = None, jobtype = None, salary = None, issyndicate = False,
                 salary_h = None, day = 1, paymethod = None, id = None):
        super().__init__(company, name, address, jobtype, 0, issyndicate, salary_h=salary_h, paymethod=paymethod,
                         id=id)
        self.card = PointCard(self.id, self)
        self.salary_h = salary_h
        self.hours_amount = 0
        self.day = day
        self.workstarthour = 0
        self.workendhour = 0
        company.payagendas[0].employees.append(self)

    def resetPaymentH(self):
        self.hours_amount = 0
        self.workstarthour = 0
        self.workendhour = 0
        self.aditional_taxes = 0

    def punchTheClockIn(self, hour):
        self.workstarthour = hour

    def punchTheClockOut(self, fhour, shour):
        self.workendhour = fhour
        self.workstarthour = shour
        work_day = self.workendhour - self.workstarthour
        self.hours_amount = self.hours_amount + work_day
        self.payment.value += self.calculateSalary(work_day)


    def calculateSalary(self, work_day):
        total = 0
        if work_day > 8:
            extra = work_day - 8
            total = 8 * self.salary_h + (extra * 1.5 * self.salary_h)
        else:
            total = work_day * self.salary_h

        return total


class Commissioned(Employee):
    def __init__(self, company, name = None, address = None, jobtype = None, salary = None, issyndicate = False,
                 comission_percent = 0, paymethod = None, id = None):
        super().__init__(company, name, address, jobtype, salary, issyndicate, comission_percent, paymethod=paymethod,
                         id = id)
        self.comission_amount = 0
        self.sales = []
        self.comission_percent = comission_percent
        company.payagendas[1].employees.append(self)

    def addSale(self, date, value):
        self.sales.append(Sales(date, value))
        self.comission_amount = self.getComission(value)
        self.payment.value += self.comission_amount

    def getComission(self, value):
        self.comission_amount += (value * self.comission_percent)
        return self.comission_amount

    def resetPaymentC(self):
        self.payment.value = 0
        self.comission_amount = 0
        self.aditional_taxes = 0


class Address:
    def __init__(self, street, number, district, city, state):
        self.street = street
        self.number = number
        self.district = district
        self.city = city
        self.state = state

    def printAddress(self):
        print(f"Endereço: {self.street} Nº {self.number}; Bairro {self.district};{self.city} - {self.state}")


class Sales:
    def __init__(self, date = None, value = None):
        self.date = date
        self.value = value


class Syindicate:
    def __init__(self, taxes = 0, syndicate_id = 1):
        self.syndicate_id = syndicate_id
        self.taxes = taxes

    def changeGeneralTaxes(self, new_g_tax):
        self.taxes = new_g_tax


    @staticmethod
    def signSyindicate(company, employee_id, aditional_taxes = 0):
        employee = company.getEmployeeByID(employee_id)
        employee.aditional_taxes = aditional_taxes
        employee.issyndicate = True

    @staticmethod
    def plusAditionalTaxes(company, employee_id, aditional_taxes):
        employee = company.getEmployeeByID(employee_id)
        employee.aditional_taxes += aditional_taxes


class Payment:
    def __init__(self, paymethod = None, value = 0):
        self.value = value
        self.paymethod = paymethod


class PointCard:
    def __init__(self, employeeid = None, employee = None):
        if employeeid is None:
            self.cardid = None
        else:
            self.cardid = employeeid
        self.employee = employee


    def addCard(self, company, employeeid, salary_h):
        employee = company.getEmployeeByID(employeeid)
        if employee.card is None:
            self.cardid = employeeid
            self.employee = employee
            employee.card = self
            employee.job_type = "H"
            employee.salary = 0
            employee.comission = 0
            employee.salary_h = salary_h

            return self

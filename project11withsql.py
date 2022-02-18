"""НАРАХУВАННЯ ЗАРПЛАТИ (ВЕБ) Скласти програму, яка працює в оточенні веб-сервера та здійснює нарахування заробітної
платні співробітникам підприємства Нарахування здійснюється за табелем, що заповнюється за місяць. У табелі за кожен
день місяця вказується кількість відпрацьованих годин або в - відпустка, л - лікарняний. За кожен місяць відома
загальна кількість годин, яку потрібно відпрацювати. Понаднормові години не враховуються. Заробітна платня
визначається посадою, яку обіймає співробітник та кількістью відпрацьованих годин. Робітники у відпустці отримують
заробітню платню за день у розмірі середнього на день значення отриманої платні за останній рік. За лікарняний - 80%
заробітної платні, що визначається посадою. Дані робітників, табелів, відомості про нарахування зберігати в базі
даних. Програма повинна дозвляти додати/змінити/видалити дані робітника,додати/змінити/видалити дані посади,
додати/змінити/видалити табель робітника за вказаний місяць, показати дані про нарахування усім співробітникам за
місяць або вибраному співробітнику за період """
import cgi
import sqlite3
import datetime

# привязка к базе данных - с данными всех работ и всех работников
conn = sqlite3.connect("project11.db")
# conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS jobdata
                  (name text, wage text, hours text)
               """)
cursor.execute("""CREATE TABLE IF NOT EXISTS workersdata
                  (name text, job text, tabel text)
               """)
cursor.execute("""SELECT * FROM workersdata""")
a = cursor.fetchall()
print(a)


# Функция, превращающая словарь табеля в строчку, не конфликтующую с синтаксисом SQL, и обратная к ней функция
def make_s(table):
    s = str(table)
    a = s.split("\'")
    return "_".join(a)


def make_table(s):
    a = s.split("_")
    table = "\'".join(a)
    return eval(table)


encoding = "utf-16"

# формальности для страницы
HTML_PAGE = """
<html>
<title>НАРАХУВАНЯ ЗАРПЛАТИ (ВЕБ)</title>
<body>
<br>
<form method=POST action="project11withsql.py">
{}
<br>
</form>
</body>
</html>
"""

# стартовая страница выбора
HTML_FORM = """
<font size="5" color="blue" face="Arial">
Оберіть дію:
</font>
<br>
<select style="font-size: 10pt" size = 7 name = start>
<option value="worker">Додати/змінити/видалити дані робітника</option>
<option value="job">Додати/змінити/видалити дані посади</option>
<option value="table">Додати/змінити/видалити табель робітника за вказаний місяць</option>
<option value="allwages">Показати дані про нарахування усім співробітникам за місяць</option>
<option value="onewage">Показати дані про нарахування співробітника за період</option>
</select>
<br><input type="submit">
"""

# страница первого варианта
WORKER = """
<font size="5" color="blue" face="Arial">
Введіть ім'я співробітника:
</font>
<input type=text name="workername" value="">
<select style="font-size: 10pt" size = 1 name = worker>
<option value="add">Додати</option>
<option value="change">Змінити</option>
<option value="delete">Видалити</option>
{}
<br><input type="submit">
"""

# страница добавления работника
ADDWORKER = """
<font size="5" color="blue" face="Arial">
Введіть посаду співробітника:
</font>
<input type=text name="addjob" value="">
<input type="submit">
"""

# страница изменения работника
CHANGEWORKER = """
<font size="5" color="blue" face="Arial">
Заповніть поля, які хочете змінити:
</font>
<br>Посада<br><input type=text name="changejob" value="">
<br>Ім'я<br><input type=text name="changename" value=""><br>
<input type="submit">
"""

# страница второго варианта
JOB = """
<font size="5" color="blue" face="Arial">
Введіть назву посади:
</font>
<input type=text name="jobname" value="">
<select style="font-size: 10pt" size = 1 name = job>
<option value="add1">Додати</option>
<option value="change1">Змінити</option>
<option value="delete1">Видалити</option>
<input type="submit">
"""

# страница добавления работы
ADDJOB = """
<font size="5" color="blue" face="Arial">
Введіть дані посади:
</font>
<br>Зарплата за місяць<br><input type=text name="wage" value="">
<br>Потрібна кількість годин<br><input type=text name="hours" value="">
<input type="submit">
"""

# страница изменения работы
CHANGEJOB = """
<font size="5" color="blue" face="Arial">
Заповніть поля, які хочете змінити:
</font>
<br>Назва посади<br><input type=text name="changejobname" value="">
<br>Зарплата за місяць<br><input type=text name="changewage" value="">
<br>Потрібна кількість годин<br><input type=text name="changehours" value="">
<input type="submit">
"""

# страница третьего варианта
TABLE = """
<font size="5" color="blue" face="Arial">
Введіть ім'я співробітника, місяць та рік:
</font>
<input type=text name="tablename" size=2 value="">
<select style="font-size: 10pt" size = 1 name = table>
<option value="add2">Додати</option>
<option value="change2">Змінити</option>
<option value="delete2">Видалити</option>
{}
"""

# выбор даты табеля
DATE = """
<font size="5" color="blue" face="Arial">
Введіть потрібні рік та місяць:
</font>
<input type=text name="year" size=2 value="">
<select size="1" name = month>
<option disabled>Місяць</option>
<option value="1">1</option>
<option value="2">2</option>
<option value="3">3</option>
<option value="4">4</option>
<option value="5">5</option>
<option value="6">6</option>
<option value="7">7</option>
<option value="8">8</option>
<option value="9">9</option>
<option value="10">10</option>
<option value="11">11</option>
<option value="12">12</option>
</select>
<input type="submit">
"""

# сам табель
INPUT_TABLE = """
<font size="5" color="blue" face="Arial">
Введіть табель:
</font>
{}
"""

# страница пятого варианта
FROMTO = """
<font size="5" color="blue" face="Arial">
Введіть ім'я; рік та місяць початку періоду; рік і місяць кінця періоду, за який вас цікавить зарплата:
</font><br><br>
<label>Ім'я</label><input type=text name="wagename" size=2 value="">
<label>Рік та місяць початку</label><input type=text name="year1" size=2 value="">
<select size="1" name = month1>
<option disabled>Місяць</option>
<option value="1">1</option>
<option value="2">2</option>
<option value="3">3</option>
<option value="4">4</option>
<option value="5">5</option>
<option value="6">6</option>
<option value="7">7</option>
<option value="8">8</option>
<option value="9">9</option>
<option value="10">10</option>
<option value="11">11</option>
<option value="12">12</option>
</select>
<br><br>
<label>Рік та місяць кінця</label><input type=text name="year2" size=2 value="">
<select size="1" name = month2>
<option disabled>Місяць</option>
<option value="1">1</option>
<option value="2">2</option>
<option value="3">3</option>
<option value="4">4</option>
<option value="5">5</option>
<option value="6">6</option>
<option value="7">7</option>
<option value="8">8</option>
<option value="9">9</option>
<option value="10">10</option>
<option value="11">11</option>
<option value="12">12</option>
</select>
<input type="submit">
"""
# отсутсвующие страницы - это стартовая с добавлением надписи, зависящей от результата работы

# переменная, зависящая от количества дней в месяце - чтобы не вызывать дейттайм каждый раз
columns = 0


# генерирует хтмл-код страницы с добавлением табеля
def generate_table(month, workersname):
    num_days = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    global columns
    columns = num_days[int(month) - 1]
    wholetable = """"""
    htmlrow = """<label></label>"""
    x = ""
    for i in range(columns):
        x += """<th>""" + htmlrow[:(len(htmlrow) - 8)] + str(i + 1) + "." + str(month) + htmlrow[7:] \
             + """<input type="text" value="" size="1" name="{}">""".format(str(i + 1)) + """</th> """
        z = x + """</tr>"""
    wholetable += """<tr><th>""" + workersname + """</th>""" + z
    return """<table style="width:100%">""" + wholetable + """</table><input type="submit">"""


# возвращает дейттаймы от старт до энд с промежутками в дельту
def datetime_range(start, end, delta):
    current = start
    if not isinstance(delta, datetime.timedelta):
        delta = datetime.timedelta(**delta)
    while current < end:
        yield current
        current += delta


class Job:
    def __init__(self, name):
        sql = "SELECT * FROM jobdata WHERE name=?"
        cursor.execute(sql, [(name)])
        try:
            data = cursor.fetchall()[0]
        except IndexError:
            data = []
        if name not in data:
            self.name = name
            self.wage = 0
            self.hours = 0
            cursor.execute("""INSERT INTO jobdata
                                                      VALUES ('{}', '{}', '{}')""".format(name, "0.0", "0.0")
                           )
            conn.commit()
        else:
            self.name = data[0]
            self.wage = float(data[1])
            self.hours = float(data[2])

    def change(self, whattochange, newvalue):
        sql = """
                    UPDATE jobdata 
                    SET {} = '{}' 
                    WHERE {} = '{}'
                    """
        if whattochange == "name":
            sql = "DELETE FROM jobdata WHERE name = '{}'".format(self.name)
            cursor.execute(sql)
            conn.commit()
            cursor.execute("""INSERT INTO jobdata
                              VALUES ('{}', '{}', '{}')""".format(newvalue, self.wage, self.hours)
                           )
            cursor.execute(sql)
            conn.commit()
            self.__init__(newvalue)
        elif whattochange == "wage":
            sql = sql.format(whattochange, str(float(newvalue)), whattochange, str(float(self.wage)))
            cursor.execute(sql)
            conn.commit()
            self.__init__(self.name)
        elif whattochange == "hours":
            sql = sql.format(whattochange, str(float(newvalue)), whattochange, str(self.hours))
            cursor.execute(sql)
            conn.commit()
            self.__init__(self.name)
        else:
            print("no")


class Worker:
    def __init__(self, name):
        sql = "SELECT * FROM workersdata WHERE name=?"
        cursor.execute(sql, [(name)])
        try:
            data = cursor.fetchall()[0]
        except IndexError:
            data = []
        if name not in data:
            self.name = name
            self.jobname = ""
            self.table = make_s({})
            self.data = None
            self.wageforholiday = 0
            cursor.execute("""INSERT INTO workersdata
                            VALUES ('{}', '{}', '{}')""".format(name, self.jobname, str(self.table))
                           )
            conn.commit()
        else:
            self.name = name
            self.data = data
            self.table = make_table(self.data[2])
            self.jobname = self.data[1]
            self.job = Job(self.jobname)
            self.wageforholiday = float(0)
            hours = float(0)
            for i in self.table.keys():  # считает зарплату за прошлый год, для рассчета оплаты отпуска
                if i[0:4] == str(int(today.year)):
                    for i in self.table.keys():
                        if i[0:4] == str(int(today.year)):
                            for j in self.table[i]:
                                if j.isdigit():
                                    hours += float(j)
                                elif j == "л":
                                    try:
                                        self.wageforholiday += 0.8 * self.job.wage / 21
                                    except:
                                        pass
                    try:
                        self.wageforholiday += hours * float(self.job.wage) / float(self.job.hours)
                    except ZeroDivisionError:
                        self.wageforholiday = 0
            self.wageforholiday /= 365

    def change(self, whattochange, newvalue):
        sql = """
                            UPDATE workersdata 
                            SET {} = '{}' 
                            WHERE {} = '{}'
                            """
        if whattochange == "name":
            sql = "DELETE FROM workersdata WHERE name = '{}'".format(self.name)
            cursor.execute(sql)
            conn.commit()
            cursor.execute("""INSERT INTO workersdata
                                          VALUES ('{}', '{}')""".format(newvalue, self.jobname)
                           )
            cursor.execute(sql)
            conn.commit()
            self.__init__(newvalue)
        elif whattochange == "job":
            sql = sql.format(whattochange, newvalue, whattochange, self.jobname)
            cursor.execute(sql)
            conn.commit()
            self.__init__(self.name)
        else:
            print("no")

    def calcwage(self, month):
        hours = 0
        wage = 0
        if str(month) in self.table.keys():
            for i in self.table[str(month)]:
                if i.isdigit():
                    hours += float(i)
                elif i == "л":
                    wage += 0.8 * self.job.wage / 21
                elif i == "в":
                    wage += self.wageforholiday
            try:
                wage += hours * self.job.wage / self.job.hours
            except ZeroDivisionError:
                wage = 0
        return round(wage, 2)


# обьявлены для глобализации
today = datetime.datetime.now()
tablepage = False
workername = None
jobname = None
tablename = 0
year = 0
month = 0
newtable = 0
body = ""


def application(environ, start_response):
    if environ.get('PATH_INFO', '').lstrip('/'):
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        global body
        global tablepage
        global workername
        global jobname
        global tablename
        global year
        global month
        global newtable
        # проверка на наличие в форме хоть одной заполненной ячейки табеля
        for i in range(columns):
            if (str(i + 1)) in form:
                tablepage = True
        if "start" in form:  # стартовая страница
            if "worker" == form["start"].value:
                body = HTML_PAGE.format(WORKER.format(""))
            elif "job" == form["start"].value:
                body = HTML_PAGE.format(JOB)
            elif "table" == form["start"].value:
                body = HTML_PAGE.format(TABLE.format(DATE))
            elif "allwages" == form[
                "start"].value:  # сразу калькулирует все зарплаты и дополняет ними стартовую страницу
                month = int(today.month)
                year = int(today.year)
                list = """<font size="5" color="blue" face="Arial">Зарплати працівників за цей міcяць:</font> <br><br>"""
                sql = "SELECT * FROM workersdata"
                cursor.execute(sql)
                workersdata = cursor.fetchall()
                for i in workersdata:
                    NewWorker = Worker(i[0])
                    NewWorker.change("job", i[1])
                    wage = NewWorker.calcwage(int(str(year) + str(month)))
                    list += "{}:  {} гривень<br><br>".format(i[0], wage)
                list += HTML_FORM
                body = HTML_PAGE.format(list)
            elif "onewage" == form["start"].value:
                body = HTML_PAGE.format(FROMTO)
        # страница с действиями над работником
        elif "worker" in form:
            if "add" == form["worker"].value:
                workername = form["workername"].value.lower()
                body = HTML_PAGE.format(ADDWORKER)
            elif "change" == form["worker"].value:
                workername = form["workername"].value.lower()
                body = HTML_PAGE.format(CHANGEWORKER)
            elif "delete" == form["worker"].value:
                workername = form["workername"].value.lower()
                sql = "SELECT * FROM workersdata WHERE name=?"
                cursor.execute(sql, [(workername)])
                try:
                    workersdata = cursor.fetchall()[0]
                except IndexError:
                    workersdata = []
                if workername in workersdata:
                    sql = "DELETE FROM workersdata WHERE name = '{}'".format(workername)
                    cursor.execute(sql)
                    conn.commit()
                    result = """<font size="5" color="green" face="Arial">Працівника видалено</font> 
                                                                                        <br><br>""" + HTML_FORM
                    body = HTML_PAGE.format(result)
                else:
                    result = """<font size="5" color="red" face="Arial">Такого працівника і так не існує!</font> 
                                                                                        <br><br>""" + HTML_FORM
                    body = HTML_PAGE.format(result)
        elif "addjob" in form:  # добавляет работнику должность, проверяя существует ли он и существует ли должность
            workersjob = form["addjob"].value.lower()
            sql = "SELECT * FROM jobdata WHERE name=?"
            cursor.execute(sql, [(workersjob)])
            try:
                data = cursor.fetchall()[0]
            except IndexError:
                data = []
            if workersjob in data:
                sql = "SELECT * FROM workersdata WHERE name=?"
                cursor.execute(sql, [(workername)])
                try:
                    workersdata = cursor.fetchall()[0]
                except IndexError:
                    workersdata = []
                if workername in workersdata:
                    result = """<font size="5" color="red" face="Arial">Такий працівник вже існує!</font> 
                                                        <br><br>""" + HTML_FORM
                else:
                    NewJob = Job(workersjob)
                    NewWorker = Worker(workername)
                    NewWorker.change("job", workersjob)
                    result = """<font size="5" color="green" face="Arial">Співробітника додано!</font> 
                        <br><br>""" + HTML_FORM
            else:
                result = """<font size="5" color="red" face="Arial">Такої посади не існує!</font> 
                                    <br><br>""" + HTML_FORM
            body = HTML_PAGE.format(result)
        elif "changejob" in form or "changename" in form:  # меняет работнику имя или должность, проверяя их на существование
            sql = "SELECT * FROM workersdata WHERE name=?"
            cursor.execute(sql, [(workername)])
            try:
                workersdata = cursor.fetchall()[0]
            except IndexError:
                workersdata = []
            if workername in workersdata:
                try:
                    changejob = form["changejob"].value
                except:
                    changejob = ""
                try:
                    changename = form["changename"].value
                except:
                    changename = ""
                all_right = True
                if len(changejob) > 0:
                    sql = "SELECT * FROM jobdata WHERE name=?"
                    cursor.execute(sql, [(changejob)])
                    data = cursor.fetchall()
                    if changejob in data:
                        Changejob = Job(changejob)
                        NewWorker = Worker(workername)
                        NewWorker.change("job", changejob)
                        result = """<font size="5" color="green" face="Arial">Дані працівника змінено!</font> 
                                                                                            <br><br>""" + HTML_FORM
                    else:
                        result = """<font size="5" color="red" face="Arial">Такої посади не існує!</font><br><br>""" + HTML_FORM
                        all_right = False
                if len(changename) > 0:
                    sql = "SELECT * FROM workersdata WHERE name=?"
                    cursor.execute(sql, [(changename)])
                    data = cursor.fetchall()
                    if len(data) == 0 and all_right:
                        NewWorker = Worker(workername)
                        NewWorker.change("name", changename)
                        result = """<font size="5" color="green" face="Arial">Дані працівника змінено!</font> 
                                                                    <br><br>""" + HTML_FORM
                    else:
                        result = """<font size="5" color="red" face="Arial">Таке ім'я вже існує!</font><br><br>""" + HTML_FORM

                body = HTML_PAGE.format(result)
            else:
                result = """<font size="5" color="red" face="Arial">Такого працівника не існує!</font> 
                                                    <br><br>""" + HTML_FORM
                body = HTML_PAGE.format(result)
        #
        #
        #
        elif "job" in form:
            if "add1" == form["job"].value:
                jobname = form["jobname"].value.lower()
                sql = "SELECT * FROM jobdata WHERE name=?"
                cursor.execute(sql, [(jobname)])
                try:
                    jobdata = cursor.fetchall()[0]
                except IndexError:
                    jobdata = []
                if jobname not in jobdata:
                    body = HTML_PAGE.format(ADDJOB)
                else:
                    result = """<font size="5" color="red" face="Arial">Така посада вже існує!</font> 
                                                            <br><br>""" + HTML_FORM
                    body = HTML_PAGE.format(result)
            elif "change1" == form["job"].value:
                jobname = form["jobname"].value.lower()
                body = HTML_PAGE.format(CHANGEJOB)
            elif "delete1" == form["job"].value:
                jobname = form["jobname"].value.lower()
                sql = "SELECT * FROM jobdata WHERE name=?"
                cursor.execute(sql, [(jobname)])
                try:
                    jobdata = cursor.fetchall()[0]
                except IndexError:
                    jobdata = []
                if jobname in jobdata:
                    sql = "DELETE FROM jobdata WHERE name = '{}'".format(jobname)
                    cursor.execute(sql)
                    conn.commit()
                    result = """<font size="5" color="green" face="Arial">Посада видалена!</font> 
                                                                                            <br><br>""" + HTML_FORM
                    body = HTML_PAGE.format(result)
                else:
                    result = """<font size="5" color="red" face="Arial">Такої посади і так не існує!</font> 
                                                                                            <br><br>""" + HTML_FORM
                    body = HTML_PAGE.format(result)
        elif "wage" in form or "hours" in form:
            wage = form["wage"].value
            hours = form["hours"].value
            if len(wage) > 0 and len(hours) > 0:
                NewJob = Job(jobname)
                NewJob.change("wage", wage)
                NewJob.change("hours", hours)
                result = """<font size="5" color="green" face="Arial">Посаду додано!</font> 
                                                                    <br><br>""" + HTML_FORM
                body = HTML_PAGE.format(result)
            else:
                result = """<font size="5" color="red" face="Arial">Ви не вказали всі дані посади</font> 
                                                                        <br><br>""" + HTML_FORM
                body = HTML_PAGE.format(result)
        elif "changejobname" in form or "changewage" in form or "changehours" in form:
            sql = "SELECT * FROM jobdata WHERE name=?"
            cursor.execute(sql, [(jobname)])
            try:
                jobdata = cursor.fetchall()[0]
            except IndexError:
                jobdata = []
            if jobname in jobdata:
                try:
                    wage = form["changewage"].value
                except:
                    wage = ""
                try:
                    hours = form["changehours"].value
                except:
                    hours = ""
                try:
                    name = form["changejobname"].value
                except:
                    name = ""
                if len(wage) > 0:
                    NewJob = Job(jobname)
                    NewJob.change("wage", wage)
                if len(hours) > 0:
                    NewJob = Job(jobname)
                    NewJob.change("hours", hours)
                if len(name) > 0:
                    NewJob = Job(jobname)
                    NewJob.change("name", name)
                result = """<font size="5" color="green" face="Arial">Посаду змінено!</font> 
                                                                        <br><br>""" + HTML_FORM
                body = HTML_PAGE.format(result)
            else:
                result = """<font size="5" color="red" face="Arial">Такої посади не існує!</font> 
                                                        <br><br>""" + HTML_FORM
                body = HTML_PAGE.format(result)
        #
        #
        #
        elif "table" in form:
            if "add2" == form["table"].value:
                tablename = form["tablename"].value.lower()
                year = form["year"].value
                month = form["month"].value
                sql = "SELECT * FROM workersdata WHERE name=?"
                cursor.execute(sql, [(tablename)])
                try:
                    workersdata = cursor.fetchall()[0]
                    if year + month in make_table(workersdata[2]).keys():
                        result = """<font size="5" color="red" face="Arial">Такий табель вже існує!</font> 
                                                                                                                <br><br>""" + HTML_FORM
                        body = HTML_PAGE.format(result)
                    else:
                        body = HTML_PAGE.format(INPUT_TABLE.format(generate_table(month, tablename)))
                        newtable = 1
                except IndexError:
                    result = """<font size="5" color="red" face="Arial">Такого працівника не існує!</font> <br><br>""" + \
                             HTML_FORM
                    body = HTML_PAGE.format(result)
            elif "change2" == form["table"].value:
                tablename = form["tablename"].value.lower()
                year = form["year"].value
                month = form["month"].value
                sql = "SELECT * FROM workersdata WHERE name=?"
                cursor.execute(sql, [(tablename)])
                try:
                    workersdata = cursor.fetchall()[0]
                    if year + month not in make_table(workersdata[2]).keys():
                        result = """<font size="5" color="red" face="Arial">Такого табелю не існує!</font> <br><br>""" + \
                                 HTML_FORM
                        body = HTML_PAGE.format(result)
                    else:
                        body = HTML_PAGE.format(INPUT_TABLE.format(generate_table(month, tablename)))
                        newtable = 2
                except IndexError:
                    result = """<font size="5" color="red" face="Arial">Такого табелю не існує!</font> <br><br>""" + \
                             HTML_FORM
                    body = HTML_PAGE.format(result)
            elif "delete2" == form["table"].value:
                tablename = form["tablename"].value.lower()
                year = form["year"].value
                month = form["month"].value
                sql = "SELECT * FROM workersdata WHERE name=?"
                cursor.execute(sql, [(tablename)])
                try:
                    data = cursor.fetchall()[0]
                    workersdata = make_table(data[2])
                    if year + month not in workersdata.keys():
                        result = """<font size="5" color="red" face="Arial">Такого табелю і так не існує!</font> <br><br>""" + \
                                 HTML_FORM
                        body = HTML_PAGE.format(result)
                    else:
                        del workersdata[year + month]
                        sql = """
                                                                    UPDATE workersdata 
                                                                    SET {} = '{}' 
                                                                    WHERE {} = '{}'
                                                                    """
                        sql = sql.format("tabel", str(workersdata), "tabel", data[2])
                        cursor.execute(sql)
                        conn.commit()
                        result = """<font size="5" color="green" face="Arial">Табель видалено!</font> <br><br>""" + \
                                 HTML_FORM
                        body = HTML_PAGE.format(result)
                except IndexError:
                    result = """<font size="5" color="red" face="Arial">Такого працівника не існує!</font> <br><br>""" + \
                             HTML_FORM
                    body = HTML_PAGE.format(result)
        elif tablepage:
            f = []
            for j in range(columns):
                if str(j + 1) in form:
                    try:
                        a = form[str(j + 1)].value
                        f.append(a)
                    except KeyError:
                        pass
                else:
                    f.append("0")
            sql = "SELECT * FROM workersdata WHERE name=?"
            cursor.execute(sql, [(tablename)])
            data = cursor.fetchall()[0]
            workersdata = make_table(data[2])
            if newtable == 2:
                for i in range(columns):
                    if workersdata[year + month][i] != "0" and f[i] == "0":
                        pass
                    else:
                        workersdata[year + month][i] = f[i]
            elif newtable == 1:
                workersdata[year + month] = f
            sql = """
                                                            UPDATE workersdata 
                                                            SET {} = '{}' 
                                                            WHERE {} = '{}'
                                                            """
            sql = sql.format("tabel", """{}""".format(make_s(workersdata)), "tabel", data[2])
            cursor.execute(sql)
            conn.commit()
            result = """<font size="5" color="green" face="Arial">Дані змінено! Дякую за заповнення.</font> <br><br>""" \
                     + HTML_FORM
            body = HTML_PAGE.format(result)
            tablepage = False
            newtable = 0
        elif "wagename" in form:
            wagename = form["wagename"].value.lower()
            year1 = form["year1"].value
            month1 = form["month1"].value
            year2 = form["year2"].value
            month2 = form["month2"].value
            wage = 0
            print(year1, year2, month1, month2)
            sql = "SELECT * FROM workersdata WHERE name=?"
            cursor.execute(sql, [(wagename)])
            try:
                data = cursor.fetchall()[0]
                workersdata = make_table(data[2])
                dates = []
                for result in datetime_range(datetime.datetime(int(year1), int(month1), 15),
                                             datetime.datetime(int(year2), int(month2), 15),
                                             {'days': 30}):
                    print(result)
                    if str(result)[5] != "0":
                        date = str(result)[0:4] + "1" + str(result)[6]
                        dates.append(date)
                    else:
                        date = str(result)[0:4] + str(result)[6]
                        dates.append(date)
                print(dates)
                for i in dates:
                    if i in workersdata.keys():
                        NewWorker = Worker(wagename)
                        NewWorker.change("job", data[1])
                        wage += NewWorker.calcwage(int(i))
                list = """<font size="5" color="blue" face="Arial">Зарплата за вибраний період:</font> <br><br>"""
                list += "{} гривень<br><br>".format(wage)
                list += HTML_FORM
                body = HTML_PAGE.format(list)
            except IndexError:
                result = """<font size="5" color="red" face="Arial">Такого працівника не існує!</font> <br><br>""" + \
                         HTML_FORM
                body = HTML_PAGE.format(result)
        else:
            result = HTML_FORM
            body = HTML_PAGE.format(result)
        start_response('200 OK', [('Content-Type', 'text/html')])
    else:
        start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
        body = HTML_PAGE.format('Сторінку не знайдено( ')
    return [bytes(body, encoding=encoding)]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    httpd = make_server('localhost', 8010, application)
    print("localhost:8010/project11with11sql.py")
    httpd.serve_forever()

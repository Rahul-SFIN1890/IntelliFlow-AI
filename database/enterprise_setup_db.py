
import sqlite3
import random
from pathlib import Path

DB_DIR = Path("database")
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / "company.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

for t in ["employees","finance","attendance","payroll","leave_balance","projects"]:
    cur.execute(f"DROP TABLE IF EXISTS {t}")

cur.execute("""
CREATE TABLE employees(
 employee_id INTEGER PRIMARY KEY,
 name TEXT,
 department TEXT,
 designation TEXT,
 experience INTEGER,
 salary INTEGER,
 city TEXT)
""")

cur.execute("""
CREATE TABLE finance(
 employee_id INTEGER PRIMARY KEY,
 name TEXT,
 bonus INTEGER,
 tax INTEGER,
 reimbursement INTEGER,
 loan INTEGER,
 incentive INTEGER)
""")

cur.execute("""
CREATE TABLE attendance(
 employee_id INTEGER PRIMARY KEY,
 name TEXT,
 present_days INTEGER,
 absent_days INTEGER,
 work_from_home INTEGER)
""")

cur.execute("""
CREATE TABLE payroll(
 employee_id INTEGER PRIMARY KEY,
 name TEXT,
 gross_salary INTEGER,
 pf INTEGER,
 esi INTEGER,
 deductions INTEGER,
 net_salary INTEGER)
""")

cur.execute("""
CREATE TABLE leave_balance(
 employee_id INTEGER PRIMARY KEY,
 name TEXT,
 paid_leave INTEGER,
 casual_leave INTEGER,
 sick_leave INTEGER,
 remaining_leave INTEGER)
""")

cur.execute("""
CREATE TABLE projects(
 employee_id INTEGER PRIMARY KEY,
 name TEXT,
 project_name TEXT,
 project_status TEXT,
 client TEXT,
 rating REAL)
""")

names=["Rahul","Aman","Priya","Neha","Arjun","Karan","Sneha","Ritika","Ankit","Pooja","Vikas","Meena","Rohit","Simran","Aditya","Nisha","Yash","Tanya","Mohit","Divya","Harsh","Sakshi","Ayush","Komal","Nitin","Anjali","Varun","Payal","Shubham","Isha","Rajat","Kriti","Deepak","Muskan","Abhishek","Kavya","Manish","Saloni","Akash","Riya","Tarun","Mansi","Gaurav","Preeti","Lokesh","Aarti","Chirag","Tanvi","Sandeep","Bhavna"]
departments=["AI","Backend","Frontend","HR","Finance","Cloud","DevOps","Security","Data Science"]
designations=["Intern","Junior Engineer","Software Engineer","Senior Engineer","Lead Engineer","Manager"]
cities=["Delhi","Noida","Gurugram","Mumbai","Pune","Hyderabad","Bangalore","Chennai"]
projects=["Apollo","Titan","Nova","Phoenix","Mercury","Atlas","Neptune"]
clients=["Microsoft","Google","Amazon","Adobe","IBM","Oracle","Accenture"]
statuses=["Active","Completed","On Hold"]

for i,name in enumerate(names,1):
    salary=random.randint(40000,250000)
    gross=salary*12
    pf=int(gross*0.05)
    esi=int(gross*0.015)
    deductions=pf+esi+random.randint(5000,20000)
    net=gross-deductions

    cur.execute("INSERT INTO employees VALUES(?,?,?,?,?,?,?)",
        (i,name,random.choice(departments),random.choice(designations),random.randint(1,12),salary,random.choice(cities)))
    cur.execute("INSERT INTO finance VALUES(?,?,?,?,?,?,?)",
        (i,name,random.randint(20000,150000),random.randint(10000,90000),random.randint(0,30000),random.choice([0,50000,100000,150000]),random.randint(5000,50000)))
    cur.execute("INSERT INTO attendance VALUES(?,?,?,?,?)",
        (i,name,random.randint(18,22),random.randint(0,4),random.randint(0,8)))
    cur.execute("INSERT INTO payroll VALUES(?,?,?,?,?,?,?)",
        (i,name,gross,pf,esi,deductions,net))
    cur.execute("INSERT INTO leave_balance VALUES(?,?,?,?,?,?)",
        (i,name,18,12,10,random.randint(5,40)))
    cur.execute("INSERT INTO projects VALUES(?,?,?,?,?,?)",
        (i,name,random.choice(projects),random.choice(statuses),random.choice(clients),round(random.uniform(3.5,5.0),1)))

conn.commit()
conn.close()

print("Enterprise database created successfully.")

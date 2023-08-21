from persistence import *

def main():
    activities_list = repo.activities.find_all()
    activities_list.sort(key=lambda x: x.date)
    branches_list = repo.branches.find_all()
    branches_list.sort(key=lambda x: x.id)
    employees_list = repo.employees.find_all()
    employees_list.sort(key=lambda x: x.id)
    products_list = repo.products.find_all()
    products_list.sort(key=lambda x: x.id)
    suppliers_list = repo.suppliers.find_all()
    suppliers_list.sort(key=lambda x: x.id)
    print("Activities")
    for line in activities_list:
        print(line.__print__())
    print("Branches")
    for line in branches_list:
        print(line.__print__())
    print("Employees")
    for line in employees_list:
        print(line.__print__())
    print("Products")
    for line in products_list:
        print(line.__print__())
    print("Suppliers")
    for line in suppliers_list:
        print(line.__print__())
    print()
    print("Employees report")
    emp_report()
    print()
    print("Activities report")
    act_report()


def emp_report():
    emp_table = repo._conn.execute("""SELECT e.name, e.salary, b.location, 
                                        SUM(IFNULL(ABS(a.quantity * p.price), 0)) as total_income
                                    FROM employees e
                                    LEFT JOIN activities a ON e.id = a.activator_id
                                    LEFT JOIN products p ON a.product_id = p.id
                                    LEFT JOIN branches b ON e.branche = b.id
                                    GROUP BY e.name, e.salary, b.location
                                    ORDER BY e.name""")
    for employee in emp_table:
        print('{} {} {} {}'.format(str(employee[0].decode()), employee[1], str(employee[2].decode()), employee[3]))


def act_report():
    act_table = repo._conn.execute("""SELECT a.date, p.description, a.quantity,
                                        CASE 
                                            WHEN a.quantity < 0 THEN e.name
                                            ELSE 'None'
                                        END as seller,
                                        CASE 
                                            WHEN a.quantity > 0 THEN s.name
                                            ELSE 'None'
                                        END as supplier
                                    FROM activities a
                                    LEFT JOIN products p ON a.product_id = p.id
                                    LEFT JOIN employees e ON e.id = a.activator_id 
                                    LEFT JOIN suppliers s ON s.id = a.activator_id
                                    ORDER BY a.date
                                    """)
    for action in act_table:
        emp = str(action[4].decode())
        branch = str(action[3].decode())
        if(emp != "None"):
            emp = '\''+emp+'\''
        else:
            branch = '\''+str(action[3].decode())+'\''
        print("('{}', '{}', {}, {}, {}".format(str(action[0].decode()), str(action[1].decode()), str(action[2]),
                                                branch, emp)+')')






if __name__ == '__main__':
    main()
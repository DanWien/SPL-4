from persistence import *

import sys

def main(args : list):
    inputfilename : str = args[1]
    with open(inputfilename) as inputfile:
        for line in inputfile:
            splittedline: list[str] = line.strip().split(", ")
            product_list = repo.products.find(id = splittedline[0])
            product = product_list[0]
            new_quantity = int(splittedline[1])
            if (new_quantity > 0) | (new_quantity+int(product.quantity) >= 0):
                repo.activities.insert(Activitie(*splittedline))
                repo.products.update({"id": splittedline[0], "quantity": int(product.quantity)+new_quantity})



if __name__ == '__main__':
    main(sys.argv)
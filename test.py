import os
abs_path = os.path.abspath(__file__) 
app_path = os.path.dirname(__file__)
db_path = os.path.dirname(abs_path)+os.sep+'db'
print db_path
os.listdir(db_path)
for txtfile in os.walk('db'):
    print txtfile[0]

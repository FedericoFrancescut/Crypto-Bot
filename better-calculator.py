num1 = float(input("insert the first number: "))
operator = input("insert the operator: ")
num2 = float(input("insert the second number: "))

if operator == "+":
    print(str(num1) + operator + str(num2) + " = " + str(num1 + num2))
elif operator == "-":
    print(str(num1) + operator + str(num2) + " = " + str(num1 - num2))
elif operator == "*":
    print(str(num1) + operator + str(num2) + " = " + str(num1 * num2))
elif operator == "/":
    if num2 != 0:
        print(str(num1) + operator + str(num2) + " = " + str(num1 / num2))
    else:
        print("the second number must be different from 0!")
else:
    print("insert a valid operator!!")
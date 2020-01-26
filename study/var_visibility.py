# Разные области видимости
x = 3

def f1():
	 # выдаст ошибку, что переменная не определена
	# print('Переменная x в функции', x, id(x))
	x = 50
	print('Заменяем x в функции', x, id(x))

print('Переменная x до вызова', x, id(x))
f1()
print('Переменная x вне функции', x, id(x))

print('='*30)

# global
y = 3

def f3():
	global y
	print('Переменная y в функции', y, id(y))
	y = 50
	print('Заменяем y в функции', y, id(y))

print('Переменная y до функции', y, id(y))
f3()
print('Переменная y после функции', y, id(y))


print('='*30)

#nonlocal

def outer1():
	z1 = 2
	print('Переменная z1 в outer1', z1, id(z1))
	
	def inner1():
		nonlocal z1
		z1 = 50		
	
	inner1()
	print('Переменная z1 в inner1 сменилась', z1, id(z1))
	
outer1()

print('='*30)

def outer2():
	z2 = 2
	print('Переменная z2 в outer2', z2, id(z2))
	
	def inner2():
		global z2
		z2 = 50		
	
	inner2()
	print('Переменная z2 в inner2 сменилась', z2, id(z2))
	
outer2()

print('='*30)

def outer3():
	z3 = 2
	print('Переменная z3 в outer3', z3, id(z3))
	
	def inner3():		
		z3 = 50
	
	inner3()
	print('Переменная z3 в inner3 сменилась', z3, id(z3))
	
outer3()
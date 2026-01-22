# Password generation functions

import random
import string

def generate_password(length=12):
	"""
	Генерирует случайный пароль заданной длины

	Args:
		length (int): Длина пароля (по умолчанию 12)

	Returns:
		str: Сгенерированный пароль
	"""
	# Используем все доступные символы
	all_characters = (
		string.ascii_uppercase +  # A-Z
		string.ascii_lowercase +  # a-z
		string.digits +           # 0-9
		string.punctuation        # Специальные символы
	)

	# Генерируем пароль
	password = ''.join(random.sample(all_characters, min(length, len(all_characters))))

	return password

def generate_strong_password(length=16):
	"""
	Генерирует усиленный пароль с гарантированным содержанием всех типов символов

	Args:
		length (int): Длина пароля (по умолчанию 16)

	Returns:
		str: Сгенерированный усиленный пароль
	"""
	if length < 4:
		length = 4

	# Гарантируем наличие каждого типа символов
	password_chars = [
		random.choice(string.ascii_uppercase),
		random.choice(string.ascii_lowercase),
		random.choice(string.digits),
		random.choice(string.punctuation)
	]

	# Добавляем остальные символы
	all_characters = string.ascii_letters + string.digits + string.punctuation
	password_chars += [random.choice(all_characters) for _ in range(length - 4)]

	# Перемешиваем
	random.shuffle(password_chars)

	return ''.join(password_chars)
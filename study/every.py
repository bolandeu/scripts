email_pattern1 = ['Sure@mail.ru', 'R.Bolandau@gmail.com', 'mail@mail.ru']
email_pattern2 = ['Sure@mail.ru', 'R.Bolandau@gmail.com', 'mail@mail.ru']


# мой вариант
i = 0
for email in email_pattern1:
    email_pattern1[i] = email.lower()
    i += 1
print(email_pattern1)


# коротка запись
for i in range(len(email_pattern2)):
    email_pattern2[i] = email_pattern2[i].lower()
print(email_pattern2)
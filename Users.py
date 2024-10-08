class User:
    def __init__(self, username, password, role, name, phone_number, email, governorate, age, national_id):
        self.__username = username
        self.__password = password
        self.__role = role
        self.__name = name
        self.__phone_number = phone_number
        self.__email = email
        self.__governorate = governorate
        self.__age = age
        self.__national_id = national_id

    def get_role(self):
        return self.__role

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_name(self):
        return self.__name

    def get_phone_number(self):
        return self.__phone_number

    def get_email(self):
        return self.__email

    def get_gender(self):
        return self.__gender

    def get_governorate(self):
        return self.__governorate

    def get_age(self):
        return self.__age

    def get_national_id(self):
        return self.__national_id

class Admin(User):
    def __init__(self, username, password, name, phone_number, email, governorate, age, national_id):
        super().__init__(username, password, role="Admin", name=name, phone_number=phone_number, email=email,
                          governorate=governorate, age=age, national_id=national_id)

class NormalUser(User):
    def __init__(self, username, password, name, phone_number, email, governorate, age, national_id):
        super().__init__(username, password, role="NormalUser", name=name, phone_number=phone_number, email=email,
                          governorate=governorate, age=age, national_id=national_id)


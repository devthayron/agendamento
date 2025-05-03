# utils.py

def is_gerente(user):
    return user.groups.filter(name='gerente').exists()

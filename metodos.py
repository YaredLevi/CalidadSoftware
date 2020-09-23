def autentificacion(self, usu, contra):
    self.validacion = False

    if usu == 'yared' and contra != 'adminxd':
        print('contra mala')
        self.validacion = False
    elif usu != 'yared' and contra != 'adminxd':
        print('algo anda mal')
        self.validacion = False
    elif usu != 'yared' and contra == 'adminxd':
        print('user no existe')
        self.validacion = False
    else:
        self.validacion = True
        return self.validacion


def total(self, producto, cantidad):
    total = producto*cantidad
    return total
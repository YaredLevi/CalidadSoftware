import unittest
import metodos

class Pruebas_unitarias(unittest.TestCase):


    def test_Totalcompra(self):
        metodos.total
        esperado = 1000
        resultado = metodos.total(self, 500, 2)
        self.assertEqual(esperado,resultado)
    
    

#autentificacion
    def test_auntenticacion(self):
        
        metodos.autentificacion
        esperado = True
        resultado = metodos.autentificacion(self,'yared','adminxd')
        self.assertEqual(esperado,resultado)


    

    
if __name__ == '__main__':
    unittest.main()
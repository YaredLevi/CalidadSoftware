import unittest
import metodos

class Pruebas_unitarias(unittest.TestCase):

#total de compra
    ValorProducto = 5000
    Cantidad = 2

    def test_Totalcompra(self):
        self.assertEqual(self.ValorProducto * self.Cantidad, 10000)
    
    

#autentificacion
    def test_auntenticacion(self):
        
        metodos.autentificacion
        esperado = True
        resultado = metodos.autentificacion(self,'yared','adminxd')
        self.assertEqual(esperado,resultado)


    

    
if __name__ == '__main__':
    unittest.main()
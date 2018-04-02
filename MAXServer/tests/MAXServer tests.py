import unittest
from MAXServer.MAXClient import MAXClient

class TestMXSCommands(unittest.TestCase):
        
    def testServerIsRunning(self):
        result = MAXClient().send('"Message sent!"')
        self.assertEqual(result, 'Message sent!')
    
    def testGetSceneName(self):
        command = 'maxFileName'
        result = MAXClient().send(command)
        self.assertEqual(result, 'file1.max')
        
    def testCreateObjects(self):
        command = '''
        delete objects
        for i = 0 to 1000 by 100 do
        (
            b = box()
            b.name = "Python Box " + i as string
            b.pos = [i,i,0]
        )
        objects.count as string
        '''
        result = MAXClient().send(command)
        self.assertEqual(result, '11')
        
if __name__ == '__main__':
    unittest.main()
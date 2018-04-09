import unittest
from MAXServer.MAXClient import MAXClient

class TestMXSCommands(unittest.TestCase):  
    @classmethod
    def setUpClass(self):
        self.client = MAXClient()
        self.activeScenes = self.client.getActiveScenes()
        if self.activeScenes:
            print('Active 3ds Max scenes:')
            for port, scene in self.activeScenes.items():
                print('Port:',port,'|','Scene:',scene)
        else:
            print('No active 3ds Max scenes found!')
        
#     @classmethod
#     def tearDownClass(self):
#         for port, file in self.activeScenes.items():
#             self.client.attemptShutDown(port)

    def testServerIsRunning(self):
        for port, file in self.activeScenes.items():
            result = self.client.send(port,'"Message sent!"')
            self.assertEqual(result, 'Message sent!')
    
    def testGetSceneName(self): # scene "file1.max" must be open during this test
        for port, file in self.activeScenes.items():
            command = 'maxFileName'
            result = self.client.send(port,command)
            self.assertEqual(result, 'file1.max')
        
    def testCreateObjects(self):
        for port, file in self.activeScenes.items():
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
            result = self.client.send(port,command)
            self.assertEqual(result, '11')
        
if __name__ == '__main__':
    unittest.main()
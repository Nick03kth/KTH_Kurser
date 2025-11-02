import unittest
from linkedQFile import LinkedQ

class TestQueue(unittest.TestCase): #Vi tester...

    def test_isEmpty(self):
        #isEmpty  returnerar True vid tom kö, annars False 
        q = LinkedQ()
        self.assertTrue(q.is_empty(), "isEmpty på tom kö")
        q.enqueue(18)
        self.assertFalse(q.is_empty(), "isEmpty på icke-tom kö")

    def test_order(self):
        #Kontrollerar att kö-ordningen blir rätt
        q = LinkedQ()
        q.enqueue(1)
        q.enqueue(2)
        q.enqueue(3)
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.dequeue(), 2)
        self.assertEqual(q.dequeue(), 3)

if __name__ == "__main__":
    unittest.main()
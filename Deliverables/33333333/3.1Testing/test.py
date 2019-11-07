import unittest
from GameBoard import GameBoard

class BackendTest(unittest.TestCase):
    def testSimpleInsertion(self):
        board = GameBoard()
        self.assertEqual(board.locationContains([1,1]), " ")
        board.insertPiece([1,1], "B")
        self.assertEqual(board.locationContains([1,1]), "B")

        # Already contains a piece!
        self.assertEqual(board.insertPiece([1,1], "B"), "This seat is taken!")
        self.assertEqual(board.insertPiece([1,1], "W"), "This seat is taken!")

        # # Check to make sure we throw with board insertion errors
        with self.assertRaises(ValueError):
            board.insertPiece([20,20], "B")
            board.insertPiece([0,0], "W")
            board.insertPiece([0,0], "B")
            board.insertPiece([0,0], "W")
            board.insertPiece([20,20], "W")
            board.insertPiece([2,2], "R")
            board.insertPiece([2,3], "asasdas")

        # print(board.board)

    def testSimpleDeletion(self):
        board = GameBoard()
        # print(board.board)
        self.assertEqual(board.locationContains([1,1]), " ")
        board.insertPiece([1,1], "B")
        self.assertEqual(board.locationContains([1,1]), "B")

        # Test for removal
        self.assertEqual(board.removePiece("R", [1,1]), "I am just a board! I cannot remove what is not there!")
        self.assertEqual(board.removePiece("B", [2,1]), "I am just a board! I cannot remove what is not there!")
        self.assertEqual(board.removePiece("W", [1,1]), "I am just a board! I cannot remove what is not there!")
        self.assertEqual(board.removePiece("W", [1,1]), "I am just a board! I cannot remove what is not there!")

        with self.assertRaises(ValueError):
            board.removePiece("B", [20,20])
        with self.assertRaises(ValueError):
            board.removePiece("R", [0,0])

        # print(board.board)

    def testTestReachable(self):
        board = GameBoard()
        board.insertPiece([1, 1], "B")
        board.insertPiece([1, 2], "B")
        board.insertPiece([2, 1], "B")

        board.insertPiece([2, 1], "W")
        board.insertPiece([3, 1], "W")
        board.insertPiece([1, 2], "W")
        board.insertPiece([1, 3], "W")

        board.insertPiece([2, 2], "W")
        board.insertPiece([2, 3], "B")
        board.insertPiece([3, 2], "B")

        board.insertPiece([3, 3], "W")
        board.insertPiece([5, 2], "W")
        board.insertPiece([5, 3], "W")
        board.insertPiece([4, 4], "W")

        board.insertPiece([4, 2], "B")
        board.insertPiece([4, 3], "B")
        board.insertPiece([4, 5], "B")
        board.insertPiece([3, 5], "B")

        self.assertEqual(board.canBeReached([1, 1], "B"), True)
        self.assertEqual(board.canBeReached([1, 1], "W"), True)
        self.assertEqual(board.canBeReached([1, 1], " "), False)

        # print(board.board)

    def testOtherReachable(self):
        board = GameBoard()
        board.insertPiece([4, 1], "B")
        board.insertPiece([4, 4], "B")
        board.insertPiece([4, 5], "W")
        board.insertPiece([3, 3], "W")
        board.insertPiece([2, 4], "B")
        board.insertPiece([1, 2], "W")

        self.assertEqual(board.canBeReached([4, 1], "B"), True)
        self.assertEqual(board.canBeReached([4, 1], "W"), False)
        self.assertEqual(board.canBeReached([4, 1], " "), True)

        # print(board.board)

    def testGetPoints(self):
        board = GameBoard()
        board.insertPiece([4, 1], "B")
        board.insertPiece([4, 4], "B")
        board.insertPiece([4, 5], "W")
        board.insertPiece([3, 3], "W")
        board.insertPiece([2, 4], "B")
        board.insertPiece([1, 2], "W")

        self.assertEqual(board.getPoints("B"), ["2-4", "4-1", "4-4"])



if __name__ == "__main__":
    unittest.main()
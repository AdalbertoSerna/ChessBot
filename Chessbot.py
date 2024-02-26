import string
import random
import os
import sys
import time
from IPython.display import clear_output
import pdb
from posixpath import basename

def ChessBoardSetup():
  board = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
  ]
  return board




def DrawBoard(board):
  for row in board:
    print(row)



def MovePiece(board, from_square, to_square):

    if IsMoveLegal(board, from_square, to_square):
      piece = board[from_square[0]][from_square[1]]
      if (piece == 'p' and to_square[0] == 7) or (piece == 'P' and to_square[0] == 0):
            promoted_piece = 'Q' if piece == 'p' else 'q'
            board[from_square[0]][from_square[1]] = promoted_piece
      board[from_square[0]][from_square[1]] = '.'
      board[to_square[0]][to_square[1]] = piece
      return board
    else:
      return board

def IsMoveLegal(board, from_square, to_square):


    from_piece = board[from_square[0]][from_square[1]]
    to_piece = board[to_square[0]][to_square[1]]

    if from_square == to_square:
      return False

    if from_piece == '.':
      return False
    diff_row = to_square[0]-from_square[0]
    diff_col = abs(to_square[1]-from_square[1])

    if from_piece == 'p':
       if diff_row == 1 and diff_col ==0 and to_piece == '.':
        return True
       elif diff_row == 2 and from_square[0]  == 1 and IsClearPath(board, from_square, to_square) and diff_col == 0:
        return True
       elif diff_row == 1 and diff_col == 1 and from_piece.isupper() != to_piece.isupper() and to_piece != '.':
        return True
    if from_piece == 'P':
       if diff_row == -1 and diff_col ==0 and to_piece == '.':
        return True
       elif diff_row == -2 and from_square[0] == 6 and IsClearPath(board, from_square, to_square) and diff_col == 0:
        return True
       elif diff_row == -1 and diff_col == -1 and from_piece.isupper() != to_piece.isupper() and to_piece != '.':
        return True


    elif from_piece.lower() == 'r':
      if diff_row == 0 or diff_col == 0:
        if to_piece == '.' or from_piece.isupper() != to_piece.isupper():
          return IsClearPath(board,from_square,to_square)

    elif from_piece.lower() == 'b':
      if diff_row == diff_col:
        if to_piece == '.' or (from_piece.isupper() and to_piece.islower()) or (from_piece.islower() and to_piece.isupper()):
          if IsClearPath(board, from_square, to_square):
            return True

    elif from_piece.lower() == 'q':
      if from_square[0] == to_square[0] or from_square[1] == to_square[1]:
        if IsClearPath(board, from_square, to_square):
            if to_piece == '.' or (from_piece.isupper() and to_piece.islower()) or (from_piece.islower() and to_piece.isupper()):
                return True
      direc_x = to_square[0] - from_square[0]
      direc_y = to_square[1] - from_square[1]

      if abs(direc_x) == abs(direc_y):
        if IsClearPath(board, from_square, to_square):
            if to_piece == '.' or (from_piece.isupper() and to_piece.islower()) or (from_piece.islower() and to_piece.isupper()):
                return True


    elif from_piece.lower() == 'n':
      if (abs(diff_row) == 1 and diff_col == 2) or (abs(diff_row) == 2 and diff_col == 1):
        if to_piece == '.' or from_piece.isupper() != to_piece.isupper():
          return True

    elif from_piece.lower() == 'k':
      if abs(diff_row) <= 1 and abs(diff_col) <= 1:
        if to_piece == '.' or from_piece.isupper() != to_piece.isupper():
          return True

    return False



def GetListOfLegalMove(board, from_square):
    from_piece = board[from_square[0]][from_square[1]]
    legal_moves = []  # empty list of legal moves
    is_lower = from_piece.islower()
    for i in range(8):
        for j in range(8):
            to_piece = board[i][j]
            if to_piece == '.' or (is_lower and to_piece.isupper()) or (not is_lower and to_piece.islower()):
                if IsMoveLegal(board, from_square, (i, j)):
                    if not DoesMovePutPlayerInCheck(board, from_square, (i, j)):
                        legal_moves.append((i, j))
    return legal_moves


def GetPiecesWithLegalMoves(board, player_color):
    pieces_with_moves = []
    if player_color == "black":
      is_lower = True
    else:
      is_lower = False

    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if (is_lower and piece.islower()) or (not is_lower and piece.isupper()):
                legal_moves = GetListOfLegalMove(board, (i, j))
                if legal_moves:
                    pieces_with_moves.append((i, j))

    return pieces_with_moves



  lists = GetPiecesWithLegalMoves(board, player_color)
  if len(lists) == 0:
    print("Checkmate")
    return True
  else:
    return False

def IsInCheck(board, player_color):
    if player_color == 'black':
        king_piece = 'k'
    elif player_color == 'white':
        king_piece = 'K'

    king_location = None
    king_threats = [(1, -2), (2, -1), (1, 2), (2, 1), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]

    # Find the king's location
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == king_piece:
                king_location = (row, col)
                break
        if king_location is not None:
            break

    if king_location is None:
        return False

    for x, y in king_threats:
        row = king_location[0] + x
        col = king_location[1] + y

        if 0 <= row < 8 and 0 <= col < 8:
            current_piece = board[row][col]
            if current_piece != '.' and IsMoveLegal(board, (row, col), king_location):
                if (current_piece.islower() and king_piece.isupper()) or (current_piece.isupper() and king_piece.islower()):
                    return True

    king_moves = [(1, 0), (0, 1), (1, 1), (-1, 0), (0, -1), (-1, -1), (1, -1), (-1, 1)]

   
    for x, y in king_moves:
        row = king_location[0] + x
        col = king_location[1] + y

        while 0 <= row < 8 and 0 <= col < 8:
            current_piece = board[row][col]
            if IsMoveLegal(board, (row, col), king_location):
                if current_piece != '.':
                    if (current_piece.islower() and king_piece.isupper()) or (current_piece.isupper() and king_piece.islower()):
                        return True
                break  
            row = row + x
            col = col + y

    return False

def IsClearPath(board, from_square, to_square):
    if from_square == to_square:
        return True

    direc_x = to_square[0] - from_square[0]
    direc_y = to_square[1] - from_square[1]

    if direc_x == 0 and direc_y == 0:
        return False

    next_x = from_square[0] + (direc_x // abs(direc_x)) if direc_x != 0 else from_square[0]

    next_y = from_square[1] + (direc_y // abs(direc_y)) if direc_y != 0 else from_square[1]

    next_square = (next_x, next_y)

    if board[next_square[0]][next_square[1]] != '.':
        return False

    return IsClearPath(board, next_square, to_square)



def DoesMovePutPlayerInCheck(board, from_square, to_square):

  from_piece = board[from_square[0]][from_square[1]]
  to_piece = board[to_square[0]][to_square[1]]

  if from_piece.islower():
    player_color = "black"
  elif from_piece.isupper():
    player_color = "white"

  if IsMoveLegal(board,from_square,to_square):
    temp = [row[:] for row in board]
    temp[to_square[0]][to_square[1]] = board[from_square[0]][from_square[1]]
    temp[from_square[0]][from_square[1]] = '.'

    return IsInCheck(temp,player_color)

def GetRandomMove(board):
  pieces_list = GetPiecesWithLegalMoves(board,"black")
  if pieces_list:
    piece = random.choice(pieces_list)
    move_list = GetListOfLegalMove(board,piece)
    move = random.choice(move_list)
    board = MovePiece(board,piece,move)
  return board

def evl(board):
  piece_vals = {
        'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 20,
        'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': 20
    }
  eval = 0
  for row in board:
    for piece in row:
      if piece in piece_vals:
        eval+=piece_vals[piece]
  return eval

def GetMinMaxMove(board, depth, if_max, alpha=float('-inf'), beta=float('inf')):
    if if_max:
        player = "white"
    else:
        player = "black"

    if depth == 0:
        return None, None, evl(board)

    bestMove = None
    bestPiece = None

    if if_max:
        pieces = GetPiecesWithLegalMoves(board, player)
        maxEval = float("-inf")

        for piece in pieces:
            moves = GetListOfLegalMove(board, piece)

            for move in moves:
                temp = [row[:] for row in board]
                temp = MovePiece(temp, piece, move)
                _, _, eval = GetMinMaxMove(temp, depth - 1, False, alpha, beta)

                if eval > maxEval:
                    maxEval = eval
                    bestMove = move
                    bestPiece = piece

                alpha = max(alpha, eval)
                if alpha >= beta:
                    break  

        return bestMove, bestPiece, maxEval

    else:
        pieces = GetPiecesWithLegalMoves(board, player)
        minEval = float("inf")

        for piece in pieces:
            moves = GetListOfLegalMove(board, piece)

            for move in moves:
                temp = [row[:] for row in board]
                temp = MovePiece(temp, piece, move)
                _, _, eval = GetMinMaxMove(temp, depth - 1, True, alpha, beta)

                if eval < minEval:
                    minEval = eval
                    bestMove = move
                    bestPiece = piece

                beta = min(beta, eval)
                if alpha >= beta:
                    break  

        return bestMove, bestPiece, minEval

board = ChessBoardSetup()
turns = 0
N = 100
player = "white"
while not IsCheckmate(board,player) and turns < N:
    clear_output()
    DrawBoard(board)

    # write code to take turns and move the pieces
    if turns %2 ==0:
      player = "white"
      move, piece, _ = GetMinMaxMove(board,2,True)
      if move is not None and piece is not None:
        board = MovePiece(board,piece,move)
    else:
      player ="black"
      board = GetRandomMove(board)

    clear_output()
    DrawBoard(board)
    print(" ")
    time.sleep(5)
    turns+=1

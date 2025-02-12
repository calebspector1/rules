#I used https://plainenglish.io/blog/a-python-example-of-the-flood-fill-algorithm-bced7f96f569 for my flood fill algorithm 
#Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "calebspector1",  # TODO: Your Battlesnake Username
        "color": "#2b8cb6",  # TODO: Choose color
        "head": "snowman",  # TODO: Choose head
        "tail": "nr-booster",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def getSafeMoves(game_state, snake):
    safe_moves = {"up":True,"down":True,"left":True,"right":True}
    my_head = snake[0]
    for s in game_state["board"]["snakes"]:
      a = s["body"]
      for i in range(len(a)):
        my_neck = a[i]
        if my_neck["x"] == my_head["x"]-1 and my_neck["y"]==my_head["y"]:
          safe_moves["left"] = False
        elif my_neck["x"] == my_head["x"]+1 and my_neck["y"]==my_head["y"]:
          safe_moves["right"] = False
        elif my_neck["y"] == my_head["y"]-1 and my_neck["x"]==my_head["x"]:
          safe_moves["down"] = False
        elif my_neck["y"] == my_head["y"]+1 and my_neck["x"]==my_head["x"]:
          safe_moves["up"] = False
    if my_head["x"] == 0:
      safe_moves["left"] = False
    elif my_head["x"] == game_state["board"]["width"]-1:
      safe_moves["right"] = False
    if my_head["y"] == 0:
      safe_moves["down"] = False
    elif my_head["y"] == game_state["board"]["height"]-1:
      safe_moves["up"] = False
    moves=[]
    for move in list(safe_moves.keys()):
      if safe_moves[move]:
        moves.append(move)
    return moves
def evaluatePos(game_state,snakes,x,y):
  moves_score=0
  if {"x":x,"y":y} in game_state["board"]["hazards"]:
    moves_score-=20
    print("hazard")
  board=[[0]*game_state["board"]["width"] for i in range(game_state["board"]["height"])]
  for snake in game_state["board"]["snakes"]:
    for body in snake["body"]:
      board[body["x"]][body["y"]]=-1
  board[x][y]=-2
  for snake in game_state["board"]["snakes"]:
    if not snake == snakes:
      moves=getSafeMoves(game_state,snake["body"])
      opp_move=[]
      for j in moves:
        pos=[snake["body"][0]["x"],snake["body"][0]["y"]]
        if j=="up":
          pos[1]+=1
        elif j=="down":
          pos[1]-=1
        elif j=="left":
          pos[0]-=1
        elif j=="right":
          pos[0]+=1
        floodFill(board, pos[0], pos[1])
        opp_move.append(sum([i for row in board for i in row if i == 1]))
        board=[[0]*game_state["board"]["width"] for i in range(game_state["board"]["height"])]
        for snake in game_state["board"]["snakes"]:
          for body in snake["body"]:
            board[body["x"]][body["y"]]=-1
      if len(opp_move)>0:
        moves_score-=max(opp_move)/4
  floodFill(board, x, y)
  mo = sum([i for row in board for i in row if i == 1])
  if not game_state["game"]["ruleset"]["name"]=="constrictor":
    if mo>=game_state["you"]["length"]:
      for snake in game_state["board"]["snakes"]:
        if not snake["id"]==game_state["you"]["id"]:
          for body in snake["body"]:
            board[body["x"]][body["y"]]=-1
    else:
      for snake in game_state["board"]["snakes"]:
        if not snake["id"]==game_state["you"]["id"]:
          for body in snake["body"]:
            board[body["x"]][body["y"]]=-1
        else:
          for i in range(mo):
            board[snake["body"][i]["x"]][snake["body"][i]["y"]]=-1
  floodFill(board, x, y)
  mo = sum([i for row in board for i in row if i == 1])
  moves_score += mo
  if not len(game_state["board"]["food"])==0:
    moves_score-=2*min([(abs(food["x"]-x)+abs(food["y"]-y)) for food in game_state["board"]["food"]])
  for i in range(len(board)):
    for s in range(len(board[0])):
      if countNeighbors(board,i,s)<=2:
        moves_score-=3
      else:
        moves_score+=3
  #for s in board:
  #  print([i for i in s])
  #print("\n")
  return moves_score
def countNeighbors(board,x,y):
  count=0
  neighbors = ((x+1,y),(x-1,y),(x,y+1),(x,y-1))
  for i in neighbors:
    if i[0]>=0 and i[0]<len(board) and i[1]>=0 and i[1]<len(board[0]) and board[i[0]][i[1]]==1:
      count+=1
  return count
def floodFill(board, x, y):
  if x<0 or x>=len(board) or y<0 or y>=len(board[0]):
    return
  if not board[x][y]==-2:
    if not board[x][y]==0:
      return
    board[x][y]=1
  floodFill(board, x+1, y)
  floodFill(board,x-1,y)
  floodFill(board,x,y+1)
  floodFill(board,x,y-1)
def headToHead(game_state,snake,change):
  move_change={"left":0,"right":0,"up":0,"down":0}
  head=game_state["you"]["body"][0]
  h=snake["body"][0]
  if abs(h["x"]-head["x"])+abs(h["y"]-head["y"])==2:
    if h["x"]==head["x"] and h["y"]-head["y"]==2:
      move_change["up"]+=change
    elif h["x"]==head["x"] and h["y"]-head["y"]==-2:
      move_change["down"]+=change
    elif h["x"]-head["x"]==2 and h["y"]==head["y"]:
      move_change["right"]+=change
    elif h["x"]-head["x"]==-2 and h["y"]==head["y"]:
      move_change["left"]+=change
    elif h["x"]-head["x"]==1 and h["y"]-head["y"]==1:
      move_change["up"]+=change
      move_change["right"]+=change
    elif h["x"]-head["x"]==-1 and h["y"]-head["y"]==1:
      move_change["up"]+=change
      move_change["left"]+=change
    elif h["x"]-head["x"]==-1 and h["y"]-head["y"]==-1:
      move_change["down"]+=change
      move_change["left"]+=change
    elif h["x"]-head["x"]==1 and h["y"]-head["y"]==-1:
      move_change["down"]+=change
      move_change["right"]+=change
  return move_change
def move(game_state: typing.Dict) -> typing.Dict:
  for snake in game_state["board"]["snakes"]:
    if snake["health"]<100:
      snake["body"].pop()
  me = game_state["you"]["body"]
  safe_moves=getSafeMoves(game_state,me)
  if len(safe_moves) == 0:
      print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
      return {"move": "down"}
  weighted_moves={}
  for move in safe_moves:
    print(move)
    if move=="up":
      weighted_moves[move]=evaluatePos(game_state,me,me[0]["x"],me[0]["y"]+1)
    elif move=="down":
      weighted_moves[move]=evaluatePos(game_state,me,me[0]["x"],me[0]["y"]-1)
    elif move=="left":
      weighted_moves[move]=evaluatePos(game_state,me,me[0]["x"]-1,me[0]["y"])
    elif move=="right":
      weighted_moves[move]=evaluatePos(game_state,me,me[0]["x"]+1,me[0]["y"])
  temp={"up":0,"down":0,"left":0,"right":0}
  for snake in game_state["board"]["snakes"]:
    if not snake == me:
      change=0
      if game_state["you"]["length"]>snake["length"]:
        change=20
        head = game_state["you"]["body"][0]
        h = snake["body"][0]
        if h["x"]>head["x"]:
          temp["right"]+=1
        elif h["x"]<head["x"]:
          temp["left"]+=1
        if h["y"]>head["y"]:
          temp["up"]+=1
        elif h["y"]<head["y"]:
          temp["down"]+=1
      else:
        change=-20
        head = game_state["you"]["body"][0]
        h = snake["body"][0]
        if h["x"]>head["x"]:
          temp["right"]-=1
        elif h["x"]<head["x"]:
          temp["left"]-=1
        if h["y"]>head["y"]:
          temp["up"]-=1
        elif h["y"]<head["y"]:
          temp["down"]-=1
      dict=headToHead(game_state,snake,change)
      print(dict)
      for move in list(weighted_moves.keys()):
        weighted_moves[move]+=dict[move]+temp[move]
  next_move=max(weighted_moves, key=weighted_moves.get)
  #funny=[]
  #for board in getMoves(game_state):
  #  funny.append(evaluatePos(board,board["you"]["body"],board["you"]["body"][0]["x"],board["you"]["body"][0]["y"]))
  print(weighted_moves)
  #print("funny",funny)

  # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
  # food = game_state['board']['food']

  print(f"MOVE {game_state['turn']}: {next_move}")
  return {"move": next_move}

# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info, 
        "start": start, 
         "move": move, 
        "end": end
    })
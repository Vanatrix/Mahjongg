import collections
#Scoring Sets and other important lists. These are used to assign multiple variables such as player winds.
Rounds = ["East", "South", "West", "North"]
Tiles_Basic = ["B2", "B3", "B4", "B5", "B6", "B7", "B8", "Ch2", "Ch3", "Ch4", "Ch5", "Ch6", "Ch7", "Ch8", "Ci2", "Ci3", "Ci4", "Ci5", "Ci6", "Ci7", "Ci8"]
Tiles_Edges = ["B1", "B9", "Ch1", "Ch9", "Ci1", "Ci9"]#Edge tiles score higher
Tiles_Winds_Dragons = ["East", "South", "West", "North", "Green", "Red", "White"]#Winds and Dragons, as well as Flowers and Seasons are the special tiles
Tiles_Flowers_Seasons = ["F1", "F2", "F3", "F4", "S1", "S2", "S3", "S4"]
Tiles_Bamboo = ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9"]#Bamboo, Characters and Circles are the suits of the regular tiles.
Tiles_Character = ["Ch1", "Ch2", "Ch3", "Ch4", "Ch5", "Ch6", "Ch7", "Ch8", "Ch9"]
Tiles_Circles = ["Ci1", "Ci2", "Ci3", "Ci4", "Ci5", "Ci6", "Ci7", "Ci8", "Ci9"]

#Player Data. used to track player's data throughout the game. some variables are required to track doubles at end of game.
Player_1 = {"Name":"", "Wind":"East", "F/S":1, "Netsum":0, "Score":0, "Hand":[], "Chow":False, "All_Hidden":True, "Doubles":0}
Player_2 = {"Name":"", "Wind":"South", "F/S":2, "Netsum":0, "Score":0, "Hand":[], "Chow":False, "All_Hidden":True, "Doubles":0}
Player_3 = {"Name":"", "Wind":"West", "F/S":3, "Netsum":0, "Score":0, "Hand":[], "Chow":False, "All_Hidden":True, "Doubles":0}
Player_4 = {"Name":"", "Wind":"North", "F/S":4, "Netsum":0, "Score":0, "Hand":[], "Chow":False, "All_Hidden":True, "Doubles":0}
Players = [Player_1, Player_2, Player_3, Player_4]

#Wind of the round affects who is dealer. dealer scores affect the netsum by x2.
Wind_of_Round = "East"

def StartGame(Round, Wall):
    #Determine Player Names
    global round
    round = Round
    global wall
    wall = Wall
    Player_1["Name"] = input("Player 1 Name: ")
    Player_2["Name"] = input("Player 2 Name: ")
    Player_3["Name"] = input("Player 3 Name: ")
    Player_4["Name"] = input("Player 4 Name: ")

    if Round != "East" or Wall != 1:
        #if the group are resuming a game, their recorded scores are inserted here.
        Player_1["Netsum"] = input("Player 1, type your current score here: ")
        Player_2["Netsum"] = input("Player 2, type your current score here: ")
        Player_3["Netsum"] = input("Player 3, type your current score here: ")
        Player_4["Netsum"] = input("Player 4, type your current score here: ")
        #assign Player Winds
        WoR_Assigned = False
        Pos_Assigned = False
        r = 0
        w = 1
        while WoR_Assigned == False:#Determines the Wind of the Round.
            if Rounds[r] == Round:
                Wind_of_Round = Rounds[r]
                WoR_Assigned = True
            else:
                r = r+1
        while Pos_Assigned == False:#Assigns wind directions to the Players,
            if w == Wall:
                Player_1["Wind"] = Rounds[(r-1+w)%4]
                Player_1["F/S"] = r+w%4
                Player_2["Wind"] = Rounds[(r+w)%4]
                Player_2["F/S"] = r+w+1%4
                Player_3["Wind"] = Rounds[(r+w+1)%4]
                Player_3["F/S"] = r+w+2%4
                Player_4["Wind"] = Rounds[(r+w+2)%4]
                Player_4["F/S"] = r+w+3%4
                Pos_Assigned = True
            else:
                w = w+1

    #Position Players in their seats
    print(Player_1["Name"], "is the", Player_1["Wind"], "Wind")
    print(Player_2["Name"], "is the", Player_2["Wind"], "Wind")
    print(Player_3["Name"], "is the", Player_3["Wind"], "Wind")
    print(Player_4["Name"], "is the", Player_4["Wind"], "Wind")

    print("You may now begin Wall", Wall, "of the", Round, "round.")
    return

def AddScore(Wind, Type, Tiles, Hidden):
    #separate tiles into a list of strings
    Tiles = list(Tiles.split(" "))

    for Player in Players:
        #add tiles to player's hand
        if Player["Wind"] == Wind:
            Player["Hand"] = Player["Hand"] + Tiles
        #add to player's score
        if Type == "F/S":
            Player["Score"] = Player["Score"] + 4
            Number = Tiles[0]
            if Number[1] == Player["F/S"]:
                Player["Doubles"] = Player["Doubles"] +1
        elif Type == "P":
            if Tiles[0] in Tiles_Basic:
                if Hidden == True:
                    Player["Score"] = Player["Score"] + 4
                else:
                    Player["Score"] = Player_1["Score"] + 2
            elif Tiles[0] in Tiles_Edges or Tiles_Winds_Dragons:
                if Hidden == True:
                    Player["Score"] = Player["Score"] + 8
                else:
                    Player["Score"] = Player["Score"] + 4
        elif Type == "K":
            if Tiles[0] in Tiles_Basic:
                if Hidden == True:
                    Player["Score"] = Player["Score"] + 16
                else:
                    Player["Score"] = Player["Score"] + 8
            elif Tiles[0] in Tiles_Edges or Tiles_Winds_Dragons:
                if Hidden == True:
                    Player["Score"] = Player["Score"] + 32
                else:
                    P1S = Player_1["Score"] + 16
        elif Type == "C":
            Player["Chow"] = True
        #Determine if "All Hidden" Variable is maintained
        if Hidden == False:
            Player["All_Hidden"] = False
        #inspect for doubles
        if Type == "P" or Type == "K" and Tiles[0] == Player["Wind"]:
            Player["Doubles"] == Player["Doubles"] + 1
        if Type == "P" or Type == "K" and Tiles[0] == Wind_of_Round:
            Player["Doubles"] == Player["Doubles"] + 1
        if Type == "P" or Type == "K" and Tiles[0] in Tiles_Winds_Dragons[5:]:
            Player["Doubles"] == Player["Doubles"] + 1
    return

def EndGame(PlayerWind,DeadWall):
    #check for dead wall, if true, replay the wall
    if DeadWall == True:
        Player_1["Score"]=0
        Player_2["Score"]=0
        Player_3["Score"]=0
        Player_4["Score"]=0
        print ("No Scores added to Player Totals. Replay Wall", wall, "of the", round, "round.")
        return
    else:
        for Player in Players:
            #Check each player's hand was recorded correctly.
            print (Player["Name"], "'s hand is", Player["Hand"])
            if input("Correct? Y/N") == "N":
                #correct any hand errors
                Player["Hand"] = input("please input your full hand here.")
                Player["Hand"] = list(Player["Hand"].split(" "))
            #add any additional scores
            if Player["Hand"].count(PlayerWind) == 2:
                Player["Score"] = Player["Score"] + 2
            if Player["Hand"].count(Wind_of_Round) == 2:
                Player["Score"] = Player["Score"] + 2
            Dragon = -1
            while Dragon > -4:
                if Player["Hand"].count(Tiles_Winds_Dragons[Dragon]) == 2:
                    Player["Score"] = Player["Score"] + 2
                    Dragon = Dragon - 1
            #calculate number of doubles and extra score for winner
            if Player == PlayerWind:
                Player["Score"] = Player["Score"] + 20
                if input("Winning Tile From Wall? Y/N") == "Y":
                    Player["Score"] = Player["Score"] + 2
                if input("Winning From Loose Tile? Y/N") == "Y":
                    Player["Doubles"] == Player["Doubles"] + 1
                if input("Winning From Last Tile in Wall? Y/N") == "Y":
                    Player["Doubles"] == Player["Doubles"] + 1
                if input("Winning From Last Discard Before Dead Wall? Y/N") == "Y":
                    Player["Doubles"] == Player["Doubles"] + 1
                if input("Winning By Robbing a Kong? Y/N") == "Y":
                    Player["Doubles"] == Player["Doubles"] + 1
                if input("Winning From Original Call (Calling After First Discard)? Y/N") == "Y":
                    Player["Doubles"] == Player["Doubles"] + 1
                if Player["Chow"] == False:
                    Player["Doubles"] == Player["Doubles"] + 1
                if Player["All_Hidden"] == True:
                    Player["Doubles"] == Player["Doubles"] + 1
                Suits = []
                for Tile in Player["Hand"]:
                    if Tile in Tiles_Bamboo:
                        Suits.append(1)
                    if Tile in Tiles_Circles:
                        Suits.append(2)
                    if Tile in Tiles_Character:
                        Suits.append(3)
                SuitSet = set(Suits)
                if len(SuitSet) <= 1:
                    Player["Doubles"] == Player["Doubles"] + 1
            #calculate doubles for all players
            if input("Original Call (Calling from first discard)? Y/N") == "Y":
                Player["Doubles"] = Player["Doubles"] + 1
            if ["F1", "F2", "F3", "F4"] in Players["Hand"]:
                Player["Doubles"] = Player["Doubles"] + 2
            if ["S1", "S2", "S3", "S4"] in Players["Hand"]:
                Player["Doubles"] = Player["Doubles"] + 2
        #Assign doubles.
        for Player in Players:
            Player["Score"] = Player["Score"] * 2 ^ Player["Doubles"]
        #Announce scores
        print(Player_1["Name"], "scored", Player_1["Score"], "points.")
        print(Player_2["Name"], "scored", Player_2["Score"], "points.")
        print(Player_3["Name"], "scored", Player_3["Score"], "points.")
        print(Player_4["Name"], "scored", Player_4["Score"], "points.")
        #Calculate Netsums
        if Player_1["wind"] == PlayerWind:
            if Player_1["Wind"] == "East":
                Player_1["Netsum"] = Player_1["Netsum"] + Player_1["Score"] * 6
                Player_2["Netsum"] = Player_2["Netsum"] - Player_2["Score"] * 2
                Player_3["Netsum"] = Player_3["Netsum"] - Player_3["Score"] * 2
                Player_4["Netsum"] = Player_4["Netsum"] - Player_4["Score"] * 2
                Player_2["Netsum"] = Player_2["Netsum"] + (Player_2["Score"] - Player_3["Score"])
                Player_2["Netsum"] = Player_2["Netsum"] + (Player_2["Score"] - Player_4["Score"])
                Player_3["Netsum"] = Player_3["Netsum"] + (Player_3["Score"] - Player_2["Score"])
                Player_3["Netsum"] = Player_3["Netsum"] + (Player_3["Score"] - Player_4["Score"])
                Player_4["Netsum"] = Player_4["Netsum"] + (Player_4["Score"] - Player_2["Score"])
                Player_4["Netsum"] = Player_4["Netsum"] + (Player_4["Score"] - Player_3["Score"])
            elif Player_2 ["Wind"] == "East":
                Player_1["Netsum"] = Player_1["Netsum"] + Player_1["Score"] * 4
                Player_2["Netsum"] = Player_2["Netsum"] - Player_2["Score"] * 2
                Player_3["Netsum"] = Player_3["Netsum"] - Player_3["Score"]
                Player_4["Netsum"] = Player_4["Netsum"] - Player_4["Score"]
                Player_2["Netsum"] = Player_2["Netsum"] + (Player_2["Score"] - Player_3["Score"]) * 2
                Player_2["Netsum"] = Player_2["Netsum"] + (Player_2["Score"] - Player_4["Score"]) * 2
                Player_3["Netsum"] = Player_3["Netsum"] + (Player_3["Score"] - Player_2["Score"]) * 2
                Player_3["Netsum"] = Player_3["Netsum"] + (Player_3["Score"] - Player_4["Score"])
                Player_4["Netsum"] = Player_4["Netsum"] + (Player_4["Score"] - Player_2["Score"]) * 2
                Player_4["Netsum"] = Player_4["Netsum"] + (Player_4["Score"] - Player_3["Score"])
            elif Player_3 ["Wind"] == "East":
                Player_1["Netsum"] = Player_1["Netsum"] + Player_1["Score"] * 4
                Player_2["Netsum"] = Player_2["Netsum"] - Player_2["Score"]
                Player_3["Netsum"] = Player_3["Netsum"] - Player_3["Score"] * 2
                Player_4["Netsum"] = Player_4["Netsum"] - Player_4["Score"]
                Player_2["Netsum"] = Player_2["Netsum"] + (Player_2["Score"] - Player_3["Score"]) * 2
                Player_2["Netsum"] = Player_2["Netsum"] + (Player_2["Score"] - Player_4["Score"])
                Player_3["Netsum"] = Player_3["Netsum"] + (Player_3["Score"] - Player_2["Score"]) * 2
                Player_3["Netsum"] = Player_3["Netsum"] + (Player_3["Score"] - Player_4["Score"]) * 2
                Player_4["Netsum"] = Player_4["Netsum"] + (Player_4["Score"] - Player_2["Score"])
                Player_4["Netsum"] = Player_4["Netsum"] + (Player_4["Score"] - Player_3["Score"]) * 3
            else:
                Player_1["Netsum"] = Player_1["Netsum"] + Player_1["Score"] * 4
                Player_2["Netsum"] = Player_2["Netsum"] - Player_2["Score"]
                Player_3["Netsum"] = Player_3["Netsum"] - Player_3["Score"]
                Player_4["Netsum"] = Player_4["Netsum"] - Player_4["Score"] * 2
                Player_2["Netsum"] = Player_2["Netsum"] + (Player_2["Score"] - Player_3["Score"])
                Player_2["Netsum"] = Player_2["Netsum"] + (Player_2["Score"] - Player_4["Score"]) * 2
                Player_3["Netsum"] = Player_3["Netsum"] + (Player_3["Score"] - Player_2["Score"])
                Player_3["Netsum"] = Player_3["Netsum"] + (Player_3["Score"] - Player_4["Score"]) * 2
                Player_4["Netsum"] = Player_4["Netsum"] + (Player_4["Score"] - Player_2["Score"]) * 2
                Player_4["Netsum"] = Player_4["Netsum"] + (Player_4["Score"] - Player_3["Score"]) * 2

        if Player_2["wind"] == PlayerWind:
            if Player_2["Wind"] == "East":
                Player_2["Netsum"] = Player_2["Netsum"] + Player_2["Score"] * 6
                Player_1["Netsum"] = Player_1["Netsum"] - Player_1["Score"] * 2
                Player_3["Netsum"] = Player_3["Netsum"] - Player_3["Score"] * 2
                Player_4["Netsum"] = Player_4["Netsum"] - Player_4["Score"] * 2
                Player_1["Netsum"] = Player_1["Netsum"] + (Player_1["Score"] - Player_3["Score"])
                Player_1["Netsum"] = Player_1["Netsum"] + (Player_1["Score"] - Player_4["Score"])
                Player_3["Netsum"] = Player_3["Netsum"] + (Player_3["Score"] - Player_1["Score"])
                Player_3["Netsum"] = Player_3["Netsum"] + (Player_3["Score"] - Player_4["Score"])
                Player_4["Netsum"] = Player_4["Netsum"] + (Player_4["Score"] - Player_1["Score"])
                Player_4["Netsum"] = Player_4["Netsum"] + (Player_4["Score"] - Player_3["Score"])
            elif Player_3["Wind"] == "East":
                Player_2["Netsum"] = Player_2["Netsum"] + Player_2["Score"] * 4
                Player_1["Netsum"] = Player_1["Netsum"] - Player_1["Score"]
                Player_3["Netsum"] = Player_3["Netsum"] - Player_3["Score"] * 2
                Player_4["Netsum"] = Player_4["Netsum"] - Player_4["Score"]
                Player_1["Netsum"] = Player_1["Netsum"] + (Player_1["Score"] - Player_3["Score"]) * 2
                Player_1["Netsum"] = Player_1["Netsum"] + (Player_1["Score"] - Player_4["Score"])
                Player_3["Netsum"] = Player_3["Netsum"] + (Player_3["Score"] - Player_1["Score"]) * 2
                Player_3["Netsum"] = Player_3["Netsum"] + (Player_3["Score"] - Player_4["Score"]) * 2
                Player_4["Netsum"] = Player_4["Netsum"] + (Player_4["Score"] - Player_1["Score"])
                Player_4["Netsum"] = Player_4["Netsum"] + (Player_4["Score"] - Player_3["Score"]) * 2
            elif Player_4["Wind"] == "East":
                Player_2["Netsum"] = Player_2["Netsum"] + Player_2["Score"] * 4
                Player_1["Netsum"] = Player_1["Netsum"] - Player_1["Score"]
                Player_3["Netsum"] = Player_3["Netsum"] - Player_3["Score"]
                Player_4["Netsum"] = Player_4["Netsum"] - Player_4["Score"] * 2
                Player_1["Netsum"] = Player_1["Netsum"] + (Player_1["Score"] - Player_3["Score"])
                Player_1["Netsum"] = Player_1["Netsum"] + (Player_1["Score"] - Player_4["Score"]) * 2
                Player_3["Netsum"] = Player_3["Netsum"] + (Player_3["Score"] - Player_1["Score"])
                Player_3["Netsum"] = Player_3["Netsum"] + (Player_3["Score"] - Player_4["Score"]) * 2
                Player_4["Netsum"] = Player_4["Netsum"] + (Player_4["Score"] - Player_1["Score"]) * 2
                Player_4["Netsum"] = Player_4["Netsum"] + (Player_4["Score"] - Player_3["Score"]) * 2
            else:
                Player_2["Netsum"] = Player_2["Netsum"] + Player_2["Score"] * 6
                Player_1["Netsum"] = Player_1["Netsum"] - Player_1["Score"] * 2
                Player_3["Netsum"] = Player_3["Netsum"] - Player_3["Score"]
                Player_4["Netsum"] = Player_4["Netsum"] - Player_4["Score"]
                Player_1["Netsum"] = Player_1["Netsum"] + (Player_1["Score"] - Player_3["Score"]) * 2
                Player_1["Netsum"] = Player_1["Netsum"] + (Player_1["Score"] - Player_4["Score"]) * 2
                Player_3["Netsum"] = Player_3["Netsum"] + (Player_3["Score"] - Player_1["Score"]) * 2
                Player_3["Netsum"] = Player_3["Netsum"] + (Player_3["Score"] - Player_4["Score"])
                Player_4["Netsum"] = Player_4["Netsum"] + (Player_4["Score"] - Player_1["Score"]) * 2
                Player_4["Netsum"] = Player_4["Netsum"] + (Player_4["Score"] - Player_3["Score"])

        if Player_3["wind"] == PlayerWind:
            if Player_3["Wind"] == "East":
                Player_3["Netsum"] = Player_3["Netsum"] + Player_3["Score"] * 6
                Player_2["Netsum"] = Player_2["Netsum"] - Player_2["Score"] * 2
                Player_1["Netsum"] = Player_1["Netsum"] - Player_1["Score"] * 2
                Player_4["Netsum"] = Player_4["Netsum"] - Player_4["Score"] * 2
                Player_1["Netsum"] = Player_1["Netsum"] + (Player_1["Score"] - Player_2["Score"])
                Player_1["Netsum"] = Player_1["Netsum"] + (Player_1["Score"] - Player_4["Score"])
                Player_2["Netsum"] = Player_2["Netsum"] + (Player_2["Score"] - Player_1["Score"])
                Player_2["Netsum"] = Player_2["Netsum"] + (Player_2["Score"] - Player_4["Score"])
                Player_4["Netsum"] = Player_4["Netsum"] + (Player_4["Score"] - Player_1["Score"])
                Player_4["Netsum"] = Player_4["Netsum"] + (Player_4["Score"] - Player_2["Score"])
            elif Player_4["Wind"] == "East":
                Player_3["Netsum"] = Player_3["Netsum"] + Player_3["Score"] * 4
                Player_2["Netsum"] = Player_2["Netsum"] - Player_2["Score"]
                Player_1["Netsum"] = Player_1["Netsum"] - Player_1["Score"]
                Player_4["Netsum"] = Player_4["Netsum"] - Player_4["Score"] * 2
                Player_1["Netsum"] = Player_1["Netsum"] + (Player_1["Score"] - Player_2["Score"])
                Player_1["Netsum"] = Player_1["Netsum"] + (Player_1["Score"] - Player_4["Score"]) * 2
                Player_2["Netsum"] = Player_2["Netsum"] + (Player_2["Score"] - Player_1["Score"]) * 2
                Player_2["Netsum"] = Player_2["Netsum"] + (Player_2["Score"] - Player_4["Score"]) * 2
                Player_4["Netsum"] = Player_4["Netsum"] + (Player_4["Score"] - Player_1["Score"])
                Player_4["Netsum"] = Player_4["Netsum"] + (Player_4["Score"] - Player_2["Score"]) * 2
            elif Player_1["Wind"] == "East":
                Player_3["Netsum"] = Player_3["Netsum"] + Player_3["Score"] * 4
                Player_2["Netsum"] = Player_2["Netsum"] - Player_2["Score"]
                Player_1["Netsum"] = Player_1["Netsum"] - Player_1["Score"] * 2
                Player_4["Netsum"] = Player_4["Netsum"] - Player_4["Score"]
                Player_1["Netsum"] = Player_1["Netsum"] + (Player_1["Score"] - Player_2["Score"]) * 2
                Player_1["Netsum"] = Player_1["Netsum"] + (Player_1["Score"] - Player_4["Score"]) * 2
                Player_2["Netsum"] = Player_2["Netsum"] + (Player_2["Score"] - Player_1["Score"]) * 2
                Player_2["Netsum"] = Player_2["Netsum"] + (Player_2["Score"] - Player_4["Score"])
                Player_4["Netsum"] = Player_4["Netsum"] + (Player_4["Score"] - Player_1["Score"]) * 2
                Player_4["Netsum"] = Player_4["Netsum"] + (Player_4["Score"] - Player_2["Score"])
            else:
                Player_3["Netsum"] = Player_3["Netsum"] + Player_3["Score"] * 6
                Player_2["Netsum"] = Player_2["Netsum"] - Player_2["Score"] * 2
                Player_1["Netsum"] = Player_1["Netsum"] - Player_1["Score"]
                Player_4["Netsum"] = Player_4["Netsum"] - Player_4["Score"]
                Player_1["Netsum"] = Player_1["Netsum"] + (Player_1["Score"] - Player_2["Score"]) * 2
                Player_1["Netsum"] = Player_1["Netsum"] + (Player_1["Score"] - Player_4["Score"])
                Player_2["Netsum"] = Player_2["Netsum"] + (Player_2["Score"] - Player_1["Score"]) * 2
                Player_2["Netsum"] = Player_2["Netsum"] + (Player_2["Score"] - Player_4["Score"]) * 2
                Player_4["Netsum"] = Player_4["Netsum"] + (Player_4["Score"] - Player_1["Score"])
                Player_4["Netsum"] = Player_4["Netsum"] + (Player_4["Score"] - Player_2["Score"]) * 2

        if Player_4["wind"] == PlayerWind:
            if Player_4["Wind"] == "East":
                Player_4["Netsum"] = Player_4["Netsum"] + Player_4["Score"] * 6
                Player_2["Netsum"] = Player_2["Netsum"] - Player_2["Score"] * 2
                Player_3["Netsum"] = Player_3["Netsum"] - Player_3["Score"] * 2
                Player_1["Netsum"] = Player_1["Netsum"] - Player_1["Score"] * 2
                Player_1["Netsum"] = Player_1["Netsum"] + (Player_1["Score"] - Player_2["Score"])
                Player_1["Netsum"] = Player_1["Netsum"] + (Player_1["Score"] - Player_3["Score"])
                Player_2["Netsum"] = Player_2["Netsum"] + (Player_2["Score"] - Player_1["Score"])
                Player_2["Netsum"] = Player_2["Netsum"] + (Player_2["Score"] - Player_3["Score"])
                Player_3["Netsum"] = Player_3["Netsum"] + (Player_3["Score"] - Player_1["Score"])
                Player_3["Netsum"] = Player_3["Netsum"] + (Player_3["Score"] - Player_2["Score"])
            elif Player_1["Wind"] == "East":
                Player_4["Netsum"] = Player_4["Netsum"] + Player_4["Score"] * 4
                Player_2["Netsum"] = Player_2["Netsum"] - Player_2["Score"]
                Player_3["Netsum"] = Player_3["Netsum"] - Player_3["Score"]
                Player_1["Netsum"] = Player_1["Netsum"] - Player_1["Score"] * 2
                Player_1["Netsum"] = Player_1["Netsum"] + (Player_1["Score"] - Player_2["Score"]) * 2
                Player_1["Netsum"] = Player_1["Netsum"] + (Player_1["Score"] - Player_3["Score"]) * 2
                Player_2["Netsum"] = Player_2["Netsum"] + (Player_2["Score"] - Player_1["Score"]) * 2
                Player_2["Netsum"] = Player_2["Netsum"] + (Player_2["Score"] - Player_3["Score"])
                Player_3["Netsum"] = Player_3["Netsum"] + (Player_3["Score"] - Player_1["Score"]) * 2
                Player_3["Netsum"] = Player_3["Netsum"] + (Player_3["Score"] - Player_2["Score"])
            elif Player_2["Wind"] == "East":
                Player_4["Netsum"] = Player_4["Netsum"] + Player_4["Score"] * 4
                Player_2["Netsum"] = Player_2["Netsum"] - Player_2["Score"] * 2
                Player_3["Netsum"] = Player_3["Netsum"] - Player_3["Score"]
                Player_1["Netsum"] = Player_1["Netsum"] - Player_1["Score"]
                Player_1["Netsum"] = Player_1["Netsum"] + (Player_1["Score"] - Player_2["Score"]) * 2
                Player_1["Netsum"] = Player_1["Netsum"] + (Player_1["Score"] - Player_3["Score"])
                Player_2["Netsum"] = Player_2["Netsum"] + (Player_2["Score"] - Player_1["Score"]) * 2
                Player_2["Netsum"] = Player_2["Netsum"] + (Player_2["Score"] - Player_3["Score"]) * 2
                Player_3["Netsum"] = Player_3["Netsum"] + (Player_3["Score"] - Player_1["Score"])
                Player_3["Netsum"] = Player_3["Netsum"] + (Player_3["Score"] - Player_2["Score"]) * 2
            else:
                Player_4["Netsum"] = Player_4["Netsum"] + Player_4["Score"] * 4
                Player_2["Netsum"] = Player_2["Netsum"] - Player_2["Score"]
                Player_3["Netsum"] = Player_3["Netsum"] - Player_3["Score"] * 2
                Player_1["Netsum"] = Player_1["Netsum"] - Player_1["Score"]
                Player_1["Netsum"] = Player_1["Netsum"] + (Player_1["Score"] - Player_2["Score"])
                Player_1["Netsum"] = Player_1["Netsum"] + (Player_1["Score"] - Player_3["Score"]) * 2
                Player_2["Netsum"] = Player_2["Netsum"] + (Player_2["Score"] - Player_1["Score"])
                Player_2["Netsum"] = Player_2["Netsum"] + (Player_2["Score"] - Player_3["Score"]) * 2
                Player_3["Netsum"] = Player_3["Netsum"] + (Player_3["Score"] - Player_1["Score"]) * 2
                Player_3["Netsum"] = Player_3["Netsum"] + (Player_3["Score"] - Player_2["Score"]) * 2

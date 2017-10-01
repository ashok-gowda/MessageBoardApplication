import redis
dir(redis)

r = redis.Redis()
boardName=""









































def performSelect(command):
    splitCommand=command.split()
    if len(splitCommand)!=2:
        print("\nInsufficient number of parameters for the command select \n Syntax select <board name>")
    else:
        boardName=splitCommand[1]
        r.client_setname(username)


def performRead(command):
    splitCommand = command.split()
    if len(splitCommand)!=1:
        print("\nInsufficient number of parameters for the command read \n Syntax 'read'")
    elif boardName=="":
        print("\n No board was selected before run command was issued")
    else:
        messages=r.get("messages")
        for message in messages:
            print("\n"+ message)








def performListen(command):
    pass







def performStop(command):
    pass










def performWrite(command):
    pass








































print("\nEnter the Username")
username=input()
while True:
    command=input()
    if command.__contains__("select"):
        performSelect(command)
    elif command.__contains__("read"):
        performRead(command)
    elif command.__contains__("write"):
        performWrite(command)
    elif command.__contains__("listen"):
        performListen(command)
    elif command.__contains__("stop"):
        performStop(command)
    else:
        print("Command does not exist")


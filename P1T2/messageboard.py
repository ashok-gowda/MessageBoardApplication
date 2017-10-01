import redis
dir(redis)

r = redis.Redis()
boardName=""
subscribing = False;
publisherSubscribe=1

def performSelect(command):
    global boardName
    splitCommand=command.split()
    if len(splitCommand)!=2:
        print("\nInsufficient number of parameters for the command select \n Syntax select <board name>")
    else:
        boardName=splitCommand[1]


def performRead(command):
    global boardName,subscribing,publisherSubscribe
    splitCommand = command.split()
    if len(splitCommand)!=1:
        print("\nInsufficient number of parameters for the command read \n Syntax 'read'")
    elif boardName=="":
        print("\n No board was selected before read command was issued")
    else:
        messages=r.get(boardName)
        for message in messages:
            print("\n"+ message)




def performListen(command):
    global boardName, subscribing, publisherSubscribe
    splitCommand = command.split()
    if len(splitCommand) != 1:
        print("\nInsufficient number of parameters for the command listen \n Syntax 'listen'")
    elif boardName == "":
        print("\n No board was selected before listen command was issued")
    else:
        subscribing=True
        publisherSubscribe=r.pubsub()
        res = publisherSubscribe.subscribe(boardName)
        print(res)



def performStop(command):
    pass










def performWrite(command):
    global boardName, subscribing, publisherSubscribe
    splitCommand = command.split()
    if boardName == "":
        print("\n No board was selected before write command was issued")
    else:
        message=username+":"+" ".join(splitCommand[1:])
        r.publish(boardName,message)
        if r.exists(boardName):
            r.get(boardName)
            r.rpush(boardName,message)
        else:
            r.rpush(boardName,message)


print("\nEnter the Username")
username=input()
while True:
    try:
        if subscribing:
            print("Sub")
            for item in publisherSubscribe.listen():
                print(item)
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
    except KeyError as e:
        performStop("stop")
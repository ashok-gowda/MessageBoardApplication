import redis
dir(redis)

r = redis.Redis()
#Start of Global Variables
boardName=""
subscribing = False;
publisherSubscribe=1
thread=-1
username=""
#End of Global Variables

def my_handler(message):
     dataMessage=message['data'].decode("utf-8")
     print(str(dataMessage))



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
        messages=r.lrange(boardName,0,-1)
        for message in messages:
            message=message.decode("utf-8")
            print("\n"+ str(message))




def performListen(command):
    global boardName, subscribing, publisherSubscribe,thread
    splitCommand = command.split()
    if len(splitCommand) != 1:
        print("\nInsufficient number of parameters for the command listen \n Syntax 'listen'")
    elif boardName == "":
        print("\n No board was selected before listen command was issued")
    else:
        subscribing=True
        publisherSubscribe=r.pubsub()
        publisherSubscribe.subscribe(**{boardName: my_handler})
        thread=publisherSubscribe.run_in_thread(sleep_time=0.001)
        print("\n"+username + " Has been subscribed to listen to boardName " + boardName)



def performStop(command):
    global thread
    splitCommand = command.split()
    if len(splitCommand) != 1:
        print("\nInsufficient number of parameters for the command listen \n Syntax 'listen'")
    elif boardName == "":
        print("\n No board was selected before listen command was issued")
    else:
        if thread!=-1:
            thread.stop()
            print("\n"+username+" has been unsubscribed from listening to boardName"+boardName)
            thread=-1
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
            r.rpush(boardName,message)
        else:
            r.rpush(boardName,message)



def inputCommand():
    while True:
        try:
            print("\nEnter command input")
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

print("\n List of Commands")
print("\n  select <boardname>")
print("\n  write message")
print("\n listen")
print("\n read")
print("\n stop- Use this to stop listening and write new messages or read new messages")
print("\n CTRL-C End the program")
print("\n Press stop after listen if you want to start writing messages else you will be listening to the messages you have written")
print("\nEnter the Username")
username=input()
inputCommand()
import sqlite3 as sql
import Classes as cls
import DataSetFirst as first
conn=sql.connect('database.db')
c=conn.cursor()
                    
# make MakeAnswer()????
# Change the makequestion to make supquistions to??
# fix DeleteAccount+
# make OutBox()+

# check:
# 1-feed()+
# 2-Inbox()+
# 3-MakeQuestions()
# len
# c.fetchall
# None
def UI(user):
    print(f'Hi there {user.FullName} how are you')
    print('what do you want to see:')
    print('________________')
    print('1- feed')
    print('2- Inbox')
    print('3- Outbox')
    print('4- users')
    print()
    print('or you want to do:')
    print('________________')
    print('5- ask some one')
    print('6- answer a question')
    print('7- logout')
    print('8- Delete something')
    print('9- quit')
    print()
    print('Enter a number in the range [ 1 , 9 ]:',end=' ')
    while True:
        where=input()
        if where =='1':
            Feed(user)
            break
        elif where=='2':
            InBox(user)
            break
        elif where=='3':
            OutBox(user)
            break
        elif where=='4':
            EndUsers(user)
            break
        elif where=='5':
            MakeQuestion(user)
            break
        elif where=='6':
            MakeAnswer(user)
            break
        elif where=='7':
            Front()
            break
        elif where=='8':
            Delete(user)
            break
        elif where=='9':
            quit()
        else:
            print('enter a valed number [ 1 , 9 ]:')

def SupInBox(user):
    sqript=f'select rowid,* from Questions where ToWho={user.ID}'
    c.execute(sqript)
    data=c.fetchall()
    for i in data:
        ques=cls.Question()
        ques.Set(i)
        sqript=f'select rowid,* from SupQuestions where SupFrom={ques.ID}'
        c.execute(sqript)
        sups=c.fetchall()
        supques=cls.SupQuestion()
        for j in sups:
            supques.Set(j)
            PrintSupQuestion(supques)
    input('Done...')
    UI(user)

def SupOutBox(user):
    sqript=f'select rowid,* From SupQuestions where FromWho={user.ID}'
    c.execute(sqript)
    data=c.fetchall()
    ques=cls.SupQuestion()
    for i in data:
        ques.Set(i)
        PrintSupQuestion(ques)
    input('Done...')
    UI(user)

def MakeAnswer(user):
    where=input('1- answer a question\n2- answer a supquestion\nto cancel enter anything else:\n')
    if where=='1' or where=='2':
        print('Enter the question\'s id that you want to answer or \'-1\' to cancel')
        while True:
            id=input()
            try:
                id=int(id)
                id=str(id)
            except:
                print('Enter a valed id or \'-1\' to cancel:')
                continue
            if id=='-1':
                input('canceled...')
                break
            else:
                table='SupQuestions'
                if where=='1':
                    table='Questions'
                
                sqript=f'select rowid,* from {table} where rowid={id}'
                c.execute(sqript)
                data=c.fetchone()
                if data==None:
                    print('Enter a valed id or \'-1\' to cancel:')
                    continue
                ques=''
                if where=='1':
                    ques=cls.Question()
                else:
                    ques=cls.SupQuestion()
                ques.Set(data)
                to=''
                if table=='SupQuestions':
                    sqript=f"select ToWho from Questions where rowid={ques.SupFrom}"
                    c.execute(sqript)
                    data=c.fetchone()
                    to=data[0]
                    print(to)
                else:
                    to=ques.ToWho
                t=int(to)
                # print(to,user.ID)
                if to!=user.ID:
                    print('Enter a valed id:')
                    continue
                if ques.Answer!='N0tAnswered':
                    print('already answered so get out')
                    do=input('do you want to change the answer? (\'1\' for yes anythong else for no)')
                    if do!='1':
                        print('Enter a valed id or \'-1\' to cancel:')
                        continue
                answer=input('Enter The answer (press enter to end it):\n')
                sqript=f'update {table} set Answer=\"{answer}\" where rowid={id}'
                c.execute(sqript)
                conn.commit()
                input('Done...')
                break
        UI(user)    
    else:
        input('canceled...')
        UI(user)

def OutBox(user):
    print('For Questions enter 1\nfor Supquestions enret anything else')
    where=input()
    if(where!='1'):
        SupOutBox(user)
    sqript=f'select rowid,* from Questions where FromWho={user.ID}'
    c.execute(sqript)
    data=c.fetchall()
    if len(data)==0:
        input('The OutBox is empty (: ')
    else:
        for item in data:
            ques=cls.Question()
            ques.Set(item)
            PrintQuestion(ques)
        print('Enter the ID of the question to see its supquestions or any thing to cancel: ')
        while True:
            id =input()
            try:
                id=int(id)
                id=str(id)
            except:
                input('canceled...')
                break
            sqript=f'select rowid,* from SupQuestions where SupFrom={id}'
            c.execute(sqript)
            data=c.fetchall()
            if len(data)==0:
                print('There is no sup questions here (;')
            else:
                for item in data:
                    supques=cls.SupQuestion()
                    supques.Set(item)
                    PrintSupQuestion(supques)
                
                    
    UI(user)
    
def MakeQuestion(user):
    where=input('1- Question\n2- SupQuesteion\nAny thing else to cancel:\n')
    if where=='1':
        print('First who do you want to ask or \'-1\' to cancel? (Enter the username): ',end=' ')
        to=''
        while True:
            to=input()
            if to == '-1':
                break
            elif to==user.UserName:
                print('Don\'t ask your salfe domp (;')
            else: 
                sqript=f'select rowid,* from Users where UserName = \'{to}\''
                c.execute(sqript)
                to=c.fetchone()
                if to != None:
                    break
                    
                else:
                    print ('Enter a valed Username or \'-1\' to cancel:')
        if to =='-1':
            input('canceled...')
            UI(user)
        else:
            # PrintUser(user)
            Anon=-1
            touser=cls.User()
            touser.Set(to)
            # PrintUser(touser)
            # PrintUser(user)
            if touser.AcceptAnon == 1:
                print('do you want this question to be anonymos?\nEnter 1 if yes or any thing else for no') 
                Anon=input()
                if Anon=='1':
                    Anon=1
                else:
                    Anon=-1
            Question=input('What is th question:(press enter to conferm):\n')
            sqript=f'insert into Questions(FromWho,ToWho,Question,Anon) values({str(user.ID)},{str(touser.ID)},\'{str(Question)}\',{str(Anon)})'
            # print(sqript)
            c.execute(sqript)
            conn.commit()
            input('You asked saccesfully...')
    elif where=='2':
        print('Enter the question\'s id that you want to ask under it (it has to be answered) or \'-1\' to cancel:')
        while True:
            id=input()
            try:
                id=int(id)
                id=str(id)
            except:
                print('Enter a valed number')
                continue
            if id=='-1':
                input('canceled...')
                break
            else:
                sqript=f'select rowid,* from Questions where rowid={id}'
                c.execute(sqript)
                data=c.fetchone()
                if data==None:
                    print('Enter a valeed number:')
                else:
                    ques=cls.Question()
                    ques.Set(data)
                    if(ques.Answer=='N0tAnswered'):
                        print('Sorry not answered );')
                    else:
                        sqript=f'select rowid,* from Users where rowid={ques.ToWho}'
                        c.execute(sqript)
                        to=cls.User()
                        
                        to.Set(c.fetchone())
                        if (to.ID==user.ID):
                            print('you cant ask yourselfe dump (;')
                            continue
                        Text=input('Enter the question (press enter to end it):\n')
                        Anon='-1'
                        if(to.AcceptAnon):
                            Anon=input('If you want this question to be anon enter \'1\' else enter anythong else:')
                            if Anon!='1':
                                Anon='-1'
                        sqript=f'insert into SupQuestions(SupFrom,FromWho,Question,Anon) values({ques.ID},{user.ID},\'{Text}\',{Anon})'
                        c.execute(sqript)
                        conn.commit()
                        input('Done...')
                        break
        UI(user)

    else:
        input('canceled...')
    UI(user)

def InBox(user): 
    print('For Questions enter 1\nfor Supquestions enret anything else')
    where=input()
    if(where!='1'):
        SupInBox(user)
    sqript =f'select rowid,* from Questions where ToWho={user.ID}'
    c.execute(sqript)
    data=c.fetchall()
    # print(data)
    if len(data) == 0:
        input('the inbox is empty')
    else:
        for item in data:
            ques=cls.Question()
            ques.Set(item)
            PrintQuestion(ques)
        print('Enter the ID of the question to see its supquestions or any thing to cancel: ')
        while True:
            id =input()
            try:
                id=int(id)
                id=str(id)
            except:
                input('canceled...')
                break
            sqript=f'select rowid,* from SupQuestions where SupFrom={id}'
            c.execute(sqript)
            data=c.fetchall()
            if len(data)==0:
                print('There is no sup questions here (;')
            else:
                for item in data:
                    supques=cls.SupQuestion()
                    supques.Set(item)
                    PrintSupQuestion(supques)
                    
    UI(user)

def Delete(user):
    print('what do you want to delete?')
    print('1- your account\n2- Quistions of yours\n3- Answer of yours\n4- Supquestion of yours\n5- Supanswer of yours\n(Enter -1 to cancle):')
    while True:
        where= input()
        if where=='-1':#cancel
            UI(user)
        
        elif where=='1':#Account
            print ('Enter your password or \'-1\' to cancel:')
            password=input()
            while(password!=user.PassWord and password!='-1'):
                password=input('Try again or enter \'-1\' to cancel')
            if(password=='-1'):
                input('Canceled...')
                UI(user)
            else:
                DeleteAccount(user)
                Front()
 
        elif where=='2':#Question
            print ('Enter your password or \'-1\' to cancel:')
            password=input()
            while(password!=user.PassWord and password!='-1'):
                password=input('Try again or enter \'-1\' to cancel: ')
            if(password=='-1'):
                input('Canceled...')
                UI(user)
            else:
                print('Enter the question or \'-1\' to cancel:\'s ID')
                while True:
                    id=input()
                    if id=='-1':
                        input('canceld...')
                        UI(user)
                    try:
                        id=int(id)
                        id=str(id)
                    except:
                        print('Enter a valed id number or \'-1\' to cancel: ')
                        continue
                    sqript=f'select rowid,* from Questions where rowid={id}'
                    c.execute(sqript)
                    data=c.fetchone()
                    # print(data)
                    if data==None:
                        print('Enter a valed id number or \'-1\' to cancel: ')
                    else:
                        ques=cls.Question()
                        ques.Set(data)
                        # print(ques.FromWho,user.ID)
                        if ques.FromWho==user.ID:
                            DeleteQuestion(ques)
                            input()
                            UI(user)
                        else:
                            print('Enter a valed number or \'-1\' to cancel: ')

        elif where=='3':#Answer
            print('Enter the question\'s ID or \'-1\' to cancel:')
            while True:
                id=input()
                try:
                    id=int(id)
                    id=str(id)
                except:
                    print('enter a valed number:')
                    continue
                if(id=='-1'):
                    input('canceled...')
                    break
                sqript=f'select rowid,* from Questions where rowid={id}'
                c.execute(sqript)
                data=c.fetchone()
                if data==None:
                    print('Enter a valed ID: ')
                    continue
                ques=cls.Question()
                ques.Set(data)
                if ques.ToWho==user.ID:
                    sqript=f'update Questions set Answer=NULL where rowid={ques.ID}'
                    c.execute(sqript)
                    conn.commit()
                    input('Answer deleted....')
                    UI(user)
                else:
                    print('Enter a valed id number:')
        
        elif where=='4':#SupQuestion
            print ('Enter your password or \'-1\' to cancel:')
            password=input()
            while(password!=user.PassWord and password!='-1'):
                password=input('Try again or enter \'-1\' to cancel')
            if(password=='-1'):
                input('Canceled...')
                UI(user)
            else:
                print('Enter the supquestion\'s ID or \'-1\' to cancele:')
                while True:
                    id=input()
                    try:
                        id=int(id)
                        id=str(id)
                    except:
                        input('canceled...')
                        break
                    sqript=f'select rowid,* from SupQuestions where rowid={id}'
                    c.execute(sqript)
                    data=c.fetchone()
                    if data==None:
                        print('enter a valed number:')
                        continue
                    ques=cls.SupQuestion()
                    ques.Set(data)
                    # print(supques.FromWho,user.ID)
                    if ques.FromWho==user.ID:
                        sqript=f'delete from SupQuestions where rowid={ques.ID}'
                        c.execute(sqript)
                        conn.commit()
                        input('supquestion deleted....')
                        UI(user)
                    else:
                        print('Enter a valed id number:')

        elif where=='5':#SupAnswer
            print('Enter the supquestion\'s ID or \'-1\' to cancel:')
            while True:
                id=input()
                try:
                    id=int(id)
                    id=str(id)
                except:
                    print('enter a valed number:')
                    continue
                if(id=='-1'):
                    input('canceled...')
                    break
                sqript=f'select rowid,* from SupQuestions where rowid={id}'
                c.execute(sqript)
                data=c.fetchone()
                if data==None:
                    print('Enter a valed ID: ')
                    continue
                ques=cls.SupQuestion()
                ques.Set(data)
                sqript=f'select rowid,* from Questions where rowid={ques.SupFrom}'
                c.execute(sqript)
                ques=cls.Question()
                ques.Set(c.fetchone())
                if ques.ToWho==user.ID:
                    sqript=f'update SupQuestions set Answer=NULL where rowid={ques.ID}'
                    c.execute(sqript)
                    conn.commit()
                    input('Answer deleted....')
                    break
                else:
                    print('Enter a valed ID: ')
            UI(user)

        else:
            print('Enter a valed number ')
    
def DeleteAccount(user):
    sqript=f'delete from Users where rowid={user.ID}'
    c.execute(sqript)
    conn.commit()
    sqript=f'select rowid,* from Questions where ToWho ={user.ID}'
    c.execute(sqript)
    conn.commit()
    data=c.fetchall()
    for i in range(len(data)):
        ques=cls.Question()
        ques.Set(data[i])
        DeleteQuestion(ques)
    sqript=f'select rowid,* from Questions where FromWho ={user.ID}'
    c.execute(sqript)
    conn.commit()
    data=c.fetchall()
    for i in range(len(data)):
        ques=cls.Question()
        ques.Set(data[i])
        DeleteQuestion(ques)
    input('Account deleted...')

def DeleteQuestion(ques):
    sqript=f'delete from Questions where rowid={ques.ID}'
    c.execute(sqript)
    conn.commit()
    sqript=f'delete from SupQuestions where SupFrom={ques.ID}'
    c.execute(sqript)
    conn.commit()    
    print('deleted....')

def PrintQuestion(ques):
    print(f'Question id = {ques.ID} :')
    if ques.Anon == -1:
        sqript=f'select UserName from Users where rowid={ques.FromWho}'
        c.execute(sqript)
        username=c.fetchone()
        print(f'From {username[0]}',end=' ')
    sqript=f'select rowid,* from Users where rowid={ques.ToWho}'
    c.execute(sqript)
    to=cls.User()
    to.Set(c.fetchone())
    print(f'To: {to.UserName}')
    print(ques.Text)
    if ques.Answer=='N0tAnswered':
        print("!!sorry not answerd!!")
    else:
        print(f'The aswer is: \n    {ques.Answer}')
    print('\n___________________________________________________\n')

def PrintSupQuestion(supques):
    print(f'Sup question Id={supques.ID}')
    if supques.Anon == -1:
        sqript=f'select UserName from Users where rowid={supques.FromWho}'
        c.execute(sqript)
        name=c.fetchone()
        print(f'Form {name[0]}.')
    print(supques.Text)
    if supques.Answer=='N0tAnswered':
        print("!!sorry not answerd!!",end='')
    else:
        print(f'The answer is:\n    {supques.Answer}',end='')
    print('\n___________________________________________________\n')

def PrintUser(user):
    print(f'User fullname: {user.FullName}')
    print(f'User ID: {user.ID}',end="\n___________________________________________________\n")

def EndUsers(user):
    sqript='select rowid,* from Users'
    c.execute(sqript)
    for item in c.fetchall():
        users=cls.User()
        users.Set(item)
        PrintUser(users)
    input()
    UI(user)

def LogIn():
    good=True
    Data=()
    print('If you want to quit enter \'-1\': ')
    print ('Enter your username or your email: ',end='')
    while good:
        name=''
        name=input() 
        script=f"select rowid,* from Users where UserName ='{name}' or Email='{name}'"
        if name == '-1':
            break   
        c.execute(script)
        conn.commit()
        Data = c.fetchone()
        if(Data != None):
            # None
            good=False
        else:
            print("Enter a valed username or email:",end=' ')

    if good != True:
        UserData=cls.User()
        UserData.Set(Data)
        print ('Enter your password or \'-1\' to quit: ')
        while(True):
            password=input()
            if password == UserData.PassWord:
                print('you loged in will...')
                UI(UserData)
                break
            elif password =='-1':
                quit()
            else:
                print('try again or enter \'-1\' to quit')
    else:
        quit()
                
def SingUp():
    FullName=input('Enter your full name: ')
    Email=''
    
    while True:
        Email=input('Enter your email: ')
        sqript=f"select * from Users where Email='{Email}'"
        c.execute(sqript)
        conn.commit()
        if c.fetchone() ==None:
            # None
            print('It is a valed Email :D')
            break
        else:
            print('Not this one ); ')
    
    UserName=''
    
    while True:
        UserName=input('Enter a user name for your accaunt \'it have to be unique\': ')
        sqript=f"select * from Users where UserName ='{UserName}'"
        c.execute(sqript)
        conn.commit()
        if c.fetchone() ==None:
            # None
            print('It is a valed one :D')
            break
        else:
            print('Not this one );')
    
    Password=input("enter your password \"you will conferm it\": ")
    RePassWord=''
    
    while Password != RePassWord:
        RePassWord=input('to close the app enter \'-1\'\nconfirm your password: ')
        if RePassWord=='-1':
            quit()
        
    AcceptAnon=0
    while AcceptAnon != '-1' and AcceptAnon!= '1' :
        AcceptAnon=input('if you accept to recive anonymos masseges enter \'1\' \nif you dont enter \'-1\' ')

    sqript=f"insert into Users(UserName,FullName,PassWord,AcceptAnon,email) values('{UserName}','{FullName}','{Password}',{int(AcceptAnon)},'{Email}')"
    c.execute(sqript)
    conn.commit()
    print('you have made an account saccesfully...\ndo you want to login ?! \n\'1\'to yes\n\'-1\'to no')
    while True:
        where=input()
        if where=='1':
            LogIn()
            break
        elif where=='-1':
            Front()
        else:
            print('enter a valed number ( -1 , 1 ): ')

def Front():
    first.SetUsers()
    first.SetQuestions()
    first.SetSupQuestions()
    print('To login enter \'1\'\nTo singup enter\'2\'\nTo quit enter\'-1\'\nChose yours')
    while True:
        where=input()
        if where=='1':
            LogIn()
            break
        elif where=='2':
            SingUp()
            break
        elif where=='-1':
            quit()
        else:
            print('Enter a valed nouber')

def Feed(user):
    sqript="select rowid,* from Questions"
    c.execute(sqript)
    data=c.fetchall()
    if len(data)==0:
        input('No questions her to see')
        # input()
        UI(user)


    for i in range(len(data)):
        ques=cls.Question()
        # print(data[i],type(data[i][4]))
        ques.Set(data[i])
        PrintQuestion(ques)
    
    print('To see the supquestions enter the question ID if you don\'t enter any thing else: ',end='')
    while True:
        id=input()
        try:
            id=int(id)
            id=str(id)
        except:
            input('canceled...')
            break
        sqript=f'select rowid,* from SupQuestions where SupFrom = {id}'
        c.execute(sqript)
        Data=c.fetchall()
        if len(Data)==0:
            print('there is no supquestuions for this );\nWhat more?: ')
        else :
            for sup in Data:
                cur =cls.SupQuestion()
                cur.Set(sup)
                PrintSupQuestion(cur)
            input('Done...')
            break
    UI(user)
# for DEV
def AllQuestions():
    sqript="select rowid,* from Questions"
    c.execute(sqript)
    conn.commit()
    print(c.fetchall())

def AllUsers():
    sqript="select rowid,* from Users"
    c.execute(sqript)
    conn.commit()
    print(c.fetchall())

def AllSups():
    sqript='select rowid,* from SupQuestions'
    c.execute(sqript)
    print(c.fetchall())
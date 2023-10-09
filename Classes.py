class User:
    FullName=None
    UserName=None
    PassWord=None
    Email=None
    ID=None
    AcceptAnon=None
    
    def Set(user,DataHolder):
        user.ID=int(DataHolder[0])
        user.UserName=str(DataHolder[1])
        user.FullName=str(DataHolder[2])
        user.Email=str(DataHolder[3])
        user.PassWord=str(DataHolder[4])
        user.AcceptAnon=int(DataHolder[5])
        pass

class Question:
    ID=None
    FromWho=None
    ToWho=None
    Text=None
    Answer=None
    Anon=None
    
    def Set(question,DataHolder):
        # print(DataHolder)
        question.ID=int(DataHolder[0])
        question.FromWho=int(DataHolder[1])
        question.ToWho=int(DataHolder[2])
        question.Text=str(DataHolder[3])
        if DataHolder[4]==None:
            question.Answer='N0tAnswered'
        else:
            question.Answer=str(DataHolder[4])
        question.Anon=int(DataHolder[5])
        pass

class SupQuestion:
    ID=None
    SupFrom=None
    FromWho=None
    Text=None
    Answer=None
    Anon=None
    
    def Set(supquestion,DataHolder):
        supquestion.ID=int(DataHolder[0])
        supquestion.SupFrom=int(DataHolder[1])
        supquestion.FromWho=int(DataHolder[2])
        supquestion.Text=str(DataHolder[3])
        if DataHolder[4]==None:
            supquestion.Answer='N0tAnswered'
        else:
            supquestion.Answer=str(DataHolder[4])
        supquestion.Anon=int(DataHolder[5])
        pass

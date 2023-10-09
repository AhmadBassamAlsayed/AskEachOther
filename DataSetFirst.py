import sqlite3 as sql
conn=sql.connect('database.db')
c=conn.cursor()
def SetUsers():
    c.execute("PRAGMA foreign_keys = ON;")
    c.execute("""
        create table if not exists Users
        (
            UserName text
            ,
            FullName text
            ,
            Email text 
            ,
            PassWord text
            ,
            AcceptAnon int
            ,
            primary key(UserName)
            ,
            unique(Email)
        );
    """)
    conn.commit()
    # print("Users table created saccesfully...")
    # print ()
    return

def SetQuestions():
    c.execute("PRAGMA foreign_keys = ON;")
    c.execute("""
        create table if not exists Questions
        (
            FromWho int 
            ,
            ToWho int 
            ,
            Question text 
            ,
            Answer text default NULL
            ,
            Anon int 
            ,
            foreign key (FromWho)references Users(rowid) 
            on delete cascade 
            on update cascade
            ,
            foreign key(Towho) references Users(rowid) 
            on delete cascade 
            on update cascade
            );
    """)
    conn.commit()
    # print("Questions table created saccesfully...")
    # print ()
    return

def SetSupQuestions():
    c.execute("PRAGMA foreign_keys = ON;")
    c.execute("""
        create table if not exists SupQuestions
        (
            SupFrom int 
            ,
            FromWho int
            ,
            Question text 
            ,
            Answer text default NULL
            ,
            Anon int 
            ,
            foreign key (SupFrom) references Questions(rowid)
            on delete cascade
            on update cascade
            ,
            foreign key (FromWho) references Users(rowid)
            on delete cascade
            on update cascade
            );
    """)
    conn.commit()
    # print("SupQuestions table created saccesfully...")
    # print ()
    return

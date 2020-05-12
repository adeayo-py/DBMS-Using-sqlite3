import sqlite3

#creating an sqlite file named orgdb and initializing the cursor
con=sqlite3.connect('orgdb.sqlite')
cur=con.cursor()

#Delete predefined table named Counts and create new one
cur.execute('DROP TABLE IF EXISTS Counts')
cur.execute('CREATE TABLE Counts (org TEXT, count INTEGER)')

#file you to work with...mbox.txt
file=input('Enter name of file you want to work with: ')
fhandle=open(file)

for line in fhandle:
    line.strip()
    # Get lines that starts with 'From:'
    if not line.startswith('From: '):continue
    breakline=line.split()
    #email address from the set of lines are indexed 1 
    email=breakline[1]
    #split the mail where you have the @ sign and extract the domain...last index
    splitemail=email.split('@')
    domain=splitemail[-1]
    # retrieve count in row where you have the domain
    cur.execute('SELECT count FROM Counts WHERE org=?',(domain,))
    #check the retrieved row. If empty insert value for count. else, update
    row=cur.fetchone()
    if row is None:
        cur.execute('INSERT INTO Counts (org, count) VALUES (?,1) ',(domain,))
    else:
        cur.execute('UPDATE Counts SET count=count+1 WHERE org=?',(domain,))
    #commit on orgdb.sqlite file...took time on my pc :(
    con.commit()
    
#optional...display in python terminal in descending order of count

sql=cur.execute('SELECT org,count FROM Counts ORDER BY count DESC')


for row in sql:
    print(row[0],row[1])

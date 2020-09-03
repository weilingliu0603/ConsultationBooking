import sqlite3
from flask import *

app = Flask(__name__)

@app.route('/') #decorator for home page
def home():
       lst_names = []
       file = open("NAMES.TXT",'r')
       for line in file:
              line = line.strip()
              lst_names.append(line)
              
       connection = sqlite3.connect("Consultations.db")
       
       lst_available = connection.execute("SELECT * FROM Slots WHERE Taken = ?", ("No",)).fetchall()
       
       lst_booked = connection.execute("SELECT Slots.ID, Slots.Date, Slots.Time, Slots.Tutor, Booked.Student FROM Slots," +
                                       "Booked WHERE Slots.ID = Booked.ID").fetchall()

       connection.close()   

       return render_template("index.html", lst_available = lst_available, lst_booked = lst_booked, lst_names = lst_names)

 
@app.route('/processing', methods = ["POST"]) #path is set as query
def processing():
       lst_names = []
       file = open("NAMES.TXT",'r')
       for line in file:
              line = line.strip()
              lst_names.append(line)
       connection = sqlite3.connect("Consultations.db")
       
       data = request.form
       #retrieve values from webpage and store into data which is a dict 
       slotID = data["slotID"]
       if slotID.isdigit():
              slotID = int(slotID)
       else:
              return render_template("unavailable.html")              
              
       name = data["name"]     
       lst = []

       num_booked = connection.execute("SELECT COUNT (Student) FROM Booked WHERE Student = ?", (name,)).fetchall()
       
       available_slots = connection.execute("SELECT ID FROM Slots WHERE Taken = ?", ("No",)).fetchall()
       for tup in available_slots:
              lst.append(tup[0])

       if slotID not in lst:
              connection.close()
              return render_template("unavailable.html")
       elif num_booked[0][0] == 2:
              connection.close()
              return render_template("unavailable.html")
       else:
              connection.execute("UPDATE Slots SET Taken = ? WHERE ID = ?", ("Yes", slotID))
              connection.commit()

              connection.execute("INSERT INTO Booked VALUES (?,?)", (slotID, name))
              connection.commit()
              
              connection = sqlite3.connect("Consultations.db")
       
              lst_available = connection.execute("SELECT * FROM Slots WHERE Taken = ?", ("No",)).fetchall()
       
              lst_booked = connection.execute("SELECT Slots.ID, Slots.Date, Slots.Time, Slots.Tutor, Booked.Student FROM Slots," +
                                       "Booked WHERE Slots.ID = Booked.ID").fetchall()

              connection.close()   

              return render_template("index.html", lst_available = lst_available, lst_booked = lst_booked, lst_names = lst_names)
              
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)      
       
##if __name__ == '__main__':
##    app.run(port = 3363, debug=True)



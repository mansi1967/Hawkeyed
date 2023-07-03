from tkinter import *
from tkinter import messagebox
import mysql.connector
import os
import time
from PIL import Image,ImageTk
from features import *
from datetime import datetime
global now1
global user_varify
def alarm(msg,alarm_status,alarm_status2,warn_count,us):
    #global alarm_status
    #global alarm_status2
    #global saying
    print(alarm_status,alarm_status2)
    print(warn_count)
    while alarm_status:
        print('call drowsy')
        s = "wake-me-up-9886.mp3"
        os.system(s)
        
        print('message to supervisor warning:',warn_count)
        
        username_info=us
        
        print(username_info)
        


        sql = "SELECT * FROM login1 WHERE user = %s"
        adr = (username_info,)

        mycur.execute(sql, adr)

        myresult = mycur.fetchone()

        for x in myresult:
            supervisor_info=str(x)
            print(x)


        now = datetime.now()
        loginat=now
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        
        sql = "INSERT INTO spvmsg1 (supervisor,user1,msg,login_at,slept_at) VALUES (%s, %s, %s,%s,%s)"
        val = (supervisor_info,username_info,"User  {} ".format(username_info)+"is drowsy",formatted_date,formatted_date)
        mycur.execute(sql, val)
        db.commit()

        print(mycur.rowcount, "record inserted.")
        


        
        alarm_status=False
            
        
        

    while alarm_status2:
        print('call yawn')
        #saying = True
        s = "wake-me-up-9886.mp3"
        os.system(s)
        alarm_status2=False



global warn_count
global us
warn_count=0

def start():
    ap = argparse.ArgumentParser()
    ap.add_argument("-w", "--webcam", type=int, default=0,
    help="index of webcam on system")
    args = vars(ap.parse_args())

    EYE_AR_THRESH = 0.25
    EYE_AR_CONSEC_FRAMES = 30
    YAWN_THRESH = 20
    alarm_status = False
    alarm_status2 = False
    saying = False
    COUNTER = 0
    warn_count=0

    print("-> Loading the predictor and detector...")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('drw\shape_predictor_68_face_landmarks.dat')

    print("-> Starting Video Stream")
    vs = VideoStream(src=args["webcam"]).start()
    time.sleep(1.0)


    while True:
        us=username_varify.get()
        frame = vs.read()
        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        rects = detector(gray, 0)

        for rect in rects:

            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            eye = final_ear(shape)
            ear = eye[0]
            leftEye = eye[1]
            rightEye = eye[2]

            distance = lip_distance(shape)

            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

            lip = shape[48:60]
            cv2.drawContours(frame, [lip], -1, (0, 255, 0), 1)

            if ear < EYE_AR_THRESH:
                COUNTER += 1
                print(COUNTER)
                print(ear)

                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    if alarm_status == False:
                        alarm_status = True
                        warn_count=warn_count+1
                        t = Thread(target=alarm, args=('wake up',alarm_status,alarm_status2,warn_count,us,))
                        t.deamon = True
                        t.start()

                    cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            else:
                COUNTER = 0
                alarm_status = False

            if (distance > YAWN_THRESH):
                if alarm_status2 == False:
                    alarm_status2 = True
                    t = Thread(target=alarm, args=('get some fresh air',alarm_status,alarm_status2,warn_count,us,))
                    t.deamon = True
                    t.start()

                    cv2.putText(frame, "Yawn Alert", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                alarm_status2 = False

            cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, "YAWN: {:.2f}".format(distance), (300, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    cv2.destroyAllWindows()
    vs.stop()





#connecting to the database
db = mysql.connector.connect(
  host ="localhost",
  user ="root",
  passwd ="sleep",
  database="mydatabase"
)
mycur = db.cursor()

def error_destroy():
    err.destroy()

def succ_destroy():
    succ.destroy()
    root1.destroy()

def error():
    global err
    err = Toplevel(root1)
    err.title("Error")
    err.geometry("200x100")
    Label(err,text="All fields are required..",fg="red",font="bold").pack()
    Label(err,text="").pack()
    Button(err,text="Ok",bg="grey",width=8,height=1,command=error_destroy).pack()

def success():
    global succ
    succ = Toplevel(root1)
    succ.title("Success")
    succ.geometry("200x100")
    Label(succ, text="Registration successful...", fg="green", font="bold").pack()
    Label(succ, text="").pack()
    Button(succ, text="Ok", bg="grey", width=8, height=1, command=succ_destroy).pack()

def register_user():
    username_info = username.get()
    password_info = password.get()
    supervisor_info= supervisor.get()
    if username_info == "":
        error()
    elif password_info == "":
        error()
    elif supervisor_info == "":
        error()
    else:
        sql = "insert into login1 values(%s,%s,%s)"
        t = (username_info, password_info,supervisor_info)
        mycur.execute(sql,t)
        db.commit()
        Label(root1, text="").pack()
        time.sleep(0.50)
        success()



def registration():
    global root1
    root1 = Toplevel(root)
    root1.title("Registration Portal")
    root1.geometry("300x250")
    global username
    global password
    global supervisor
    Label(root1,text="Register your account",bg="grey",fg="black",font="bold",width=300).pack()
    username = StringVar()
    password = StringVar()
    supervisor = StringVar()
    Label(root1,text="").pack()
    Label(root1,text="Username :",font="bold").pack()
    Entry(root1,textvariable=username).pack()
    Label(root1, text="").pack()
    Label(root1, text="Password :").pack()
    Entry(root1, textvariable=password,show="*").pack()
    Label(root1,text="").pack()
    Label(root1,text="supervisor :",font="bold").pack()
    Entry(root1,textvariable=supervisor).pack()
    Label(root1, text="").pack()
    Button(root1,text="Register",bg="red",command=register_user).pack()

def login():
    global root2
    root2 = Toplevel(root)
    root2.title("Log-In Portal")
    root2.geometry("300x300")
    global username_varify
    global password_varify
    Label(root2, text="Log-In Portal", bg="grey", fg="black", font="bold",width=300).pack()
    username_varify = StringVar()
    password_varify = StringVar()
    Label(root2, text="").pack()
    Label(root2, text="Username :", font="bold").pack()
    Entry(root2, textvariable=username_varify).pack()
    Label(root2, text="").pack()
    Label(root2, text="Password :").pack()
    Entry(root2, textvariable=password_varify, show="*").pack()
    Label(root2, text="").pack()
    Button(root2, text="Log-In", bg="red",command=login_varify).pack()
    Label(root2, text="")

def logg_destroy():
    logg.destroy()
    root2.destroy()

def fail_destroy():
    fail.destroy()

def logged():
    global logg
    logg = Toplevel(root2)
    logg.title("Welcome")
    logg.geometry("200x100")
    Label(logg, text="Welcome {} ".format(username_varify.get()), fg="green", font="bold").pack()
    Label(logg, text="").pack()
    Button(logg, text="start detection", bg="grey", width=20, height=2, command=start).pack()
    Button(logg, text="supervisor portal ", bg="grey", width=20, height=2, command=supervise).pack()

def supervise():

    global spv
    spv = Toplevel(root2)
    spv.title("supervisor portal")
    spv.geometry("200x100")
    

    user_varify = username_varify.get()
    
    sql = "select * from login1 where supervisor =%s"
    mycur.execute(sql,[(user_varify)])
    results = mycur.fetchall()
    if results:
        for i in results:
            now1=datetime.now()
            print("notifications")
            sql = "SELECT msg FROM spvmsg1 WHERE supervisor = %s"
            adr = (user_varify,)
            
            mycur.execute(sql, adr)
            myresult = mycur.fetchone()

            for x in myresult:
                msg1=str(x)
                print(x)
                Label(spv, text=msg1, fg="red", font="bold").pack()
                Label(spv, text="").pack()
            break
    else:
        failed()




    Label(spv, text="notifications", fg="red", font="bold").pack()
    Label(spv, text="").pack()
    Button(fail, text="Ok", bg="grey", width=8, height=1, command=fail_destroy).pack()


def failed():
    global fail
    fail = Toplevel(root2)
    fail.title("Invalid")
    fail.geometry("200x100")
    Label(fail, text="Invalid attempt...", fg="red", font="bold").pack()
    Label(fail, text="").pack()
    Button(fail, text="Ok", bg="grey", width=8, height=1, command=fail_destroy).pack()


def login_varify():
    user_varify = username_varify.get()
    pas_varify = password_varify.get()
    sql = "select * from login1 where user = %s and password = %s"
    mycur.execute(sql,[(user_varify),(pas_varify)])
    results = mycur.fetchall()
    if results:
        for i in results:
            now1=datetime.now()
            logged()
            break
    else:
        failed()
    


def main_screen():
    global root
    root = Tk()
    root.title("Log in")
    root.geometry("700x600")
    Label(root,text="     Welcome to Hawk Eyed ",font=("Arial Bold",25), bg="purple",fg="white",width=80,height="3").pack()
    

    # Create a photoimage object of the image in the path
    image1 = Image.open("logo.PNG")
    image2=image1.resize((150, 100))
    test = ImageTk.PhotoImage(image2)

    label1 =Label(image=test)
    label1.image = test

    # Position image
    label1.place(x=20, y=8)
    
    image3 = Image.open("drowsygirl.PNG")
    test1 = ImageTk.PhotoImage(image3)
    label12 =Label(image=test1)
    label12.image = test1
    label12.place(x=140, y=300)


    
    Label(root,text="").pack()
    Button(root,text="Log in",width="8",height="1",bg="orange",font=("Times New Roman Bold",20),command=login).pack()
    Label(root,text="").pack()
    Button(root, text="Registration",height="1",width="15",bg="orange",font=("Times New Roman Bold",20),command=registration).pack()
    Label(root,text="").pack()
    Label(root,text="").pack()
    Label(root,text="sleep alert").pack()

main_screen()
root.mainloop()
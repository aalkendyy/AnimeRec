import tkinter as tk 
import sqlite3
import requests
import pandas as pd
from PIL import Image, ImageTk
from io import BytesIO




#design the log in UI
window = tk.Tk()
window.title("AnimeRec Login")
window.geometry("800x600")

#database gor login and first page 
con = sqlite3.connect("Animerec.db")
cur =con.cursor()
#cur.execute("CREATE TABLE ANIME (User,Pass,rating,Anime)")

#cur.execute("ALTER TABLE ANIME ADD COLUMN favoritAnime TEXT")
con.commit()
res=cur.execute("SELECT name FROM sqlite_master")
print(res.fetchone())

#msg label 
msglabel= tk.Label(window,text="Welcome to anime Rec")
msglabel.grid(column=1,row=8)
#function to take values from register to database
def obtainReg():
    username = NameEntery.get()
    password= PassEntery.get()
    username.strip()
    password.strip()
    print(username,password)
    cur.execute("INSERT INTO ANIME (User,Pass) VALUES (?,?)",(username,password))
    con.commit()
    msglabel.config(text=f"Hello {username} WELCOME TO ANIME REC")
    checkdb=cur.execute("SELECT User, Pass FROM ANIME")
    print(checkdb)

#create a new window for when they log in success
def newwindow():
    Mainwindow = tk.Toplevel(window)
     # sets the title of the
 
    Mainwindow.title(f"{NameEntery.get()}'s Profile")
 
    # sets the geometry of toplevel
    Mainwindow.geometry("900x1000")
    anime_title = tk.Entry(Mainwindow)
    animesearch=tk.Label(Mainwindow,text="anime name:")
    animesearch.grid(row=2,column=1 , padx=10, pady=10)
    anime_title.grid(row=2 ,column=2 , padx=10, pady=10)
    showinfo=tk.Label(Mainwindow,text="search info here")
    showinfo.grid(row=5,column=1, padx=10, pady=10)
    image_label = tk.Label(Mainwindow)
    image_label.grid(row=5, column=2, padx=10, pady=10)
    
    def open_anime_details(anime):
        details_window = tk.Toplevel(window)
        details_window.title(f"Details of {anime.get('title')}")
        details_window.geometry("500x500")
        
        title = anime.get("title")
        episodes = anime.get("episodes")
        rating = anime.get("rating")
        synopsis = anime.get("synopsis")
        photo = anime.get("images", {}).get("jpg", {}).get("image_url")

        tk.Label(details_window, text=f"Title: {title}").pack()
        tk.Label(details_window, text=f"Episodes: {episodes}").pack()
        tk.Label(details_window, text=f"Rating: {rating}").pack()
        tk.Label(details_window, text=f"Synopsis: {synopsis}").pack()
        
        if photo:
            response = requests.get(photo)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img = img.resize((150, 200))  
            img = ImageTk.PhotoImage(img)
            img_label = tk.Label(details_window, image=img)
            img_label.image = img 
            img_label.pack()

        
        def add_to_favorites():
            cur.execute("UPDATE ANIME SET favoritAnime = ? WHERE User = ?", (title, NameEntery.get()))
            con.commit()
            tk.Label(details_window, text="Added to favorites!").pack()

        def rate_anime():
            rating = rating_entry.get()
            cur.execute("UPDATE ANIME SET rating = ? WHERE User = ?", (rating, NameEntery.get()))
            con.commit()
            tk.Label(details_window, text="Rating saved!").pack()

        tk.Button(details_window, text="Add to Favorites", command=add_to_favorites).pack()
        tk.Label(details_window, text="Rate this anime:").pack()
        rating_entry = tk.Entry(details_window)
        rating_entry.pack()
        tk.Button(details_window, text="Submit Rating", command=rate_anime).pack()
        
    #anime api request 
    def searchanime():
    


        animeinfo=anime_title.get()
        r=requests.get(f"https://api.jikan.moe/v4/anime?q={animeinfo}")
        if r.status_code==200:
            print(r.status_code)
            allinfo=""
            #print(r.json())
            info=r.json()
            row_number = 11
            for i in info["data"]:
                title=i.get(f"title")
                episodes=i.get("episodes")
                rating=i.get("rating")
                synopsis = i.get("synopsis")
                allinfo+=f"Title: {title}, Episodes: {episodes}, Rating: {rating} \n"
                button = tk.Button(Mainwindow, text=f" {title}\n", command=lambda anime=i: open_anime_details(anime))
                button.grid(row=row_number, column=1, padx=5, pady=5)
                row_number += 1
            showinfo.config(text=allinfo)
                


        else:
            print(r.status_code,"invalid search buddy")
    searchbtn=tk.Button(Mainwindow,text="search",command=searchanime)
    searchbtn.grid(row=3, column=1, padx=10, pady=10)
   
   

    #search by gerne
    def Searchgerne():
        gernetype=gerneEntery.get()
        r=requests.get(f"https://api.jikan.moe/v4/anime?q={gernetype}")
        info=r.json()
        row_number = 11
        allgernes=""
        for i in info["data"]:
            print(i.get("type"))
            ger=i.get("type")
            anime=i.get("title")
            photo=i.get("images", {}).get("jpg", {}).get("image_url")
            score=i.get("score")
            synopsis = i.get("synopsis")
            allgernes += f"Anime: {anime}, Genre: {ger},Score: {score}\n"
            if photo:
                response = requests.get(photo)
                img_data = response.content
                img = Image.open(BytesIO(img_data))
                img = img.resize((150, 200))  
                img = ImageTk.PhotoImage(img)
                image_label.config(image=img)
                image_label.image = img  
            print(photo)
            button = tk.Button(Mainwindow, text=f"{anime}", command=lambda anime=i: open_anime_details(anime))
            button.grid(row=row_number, column=1, padx=5, pady=5)
            row_number += 1
        showinfo.config(text=allgernes)
    gernelabel=tk.Label(Mainwindow,text="gerne your interested in:").grid(row=2,column=4)
    gerneEntery=tk.Entry(Mainwindow)
    gerneEntery.grid(row=2,column=5)
    gerneseatchbtn=tk.Button(Mainwindow,text="gerne search",command=Searchgerne)
    gerneseatchbtn.grid(row=3, column=2, padx=10, pady=10)

    

    
    
    


 


def login():
    for info in cur.execute("SELECT User , Pass from ANIME"):
        print(info)
        print(info[0])
        print(info[1])

        usercheck=info[0]
        passcheck=info[1]

        if NameEntery.get()==usercheck and PassEntery.get()==passcheck:
            print(f"pass through {usercheck}")
            msglabel.config(text=f"WELCOME TO ANIME REC {usercheck}")
            newwindow()
            window.withdraw()
        else:
            msglabel.config(text="No user with this name / pass please register")




namelabel = tk.Label(window,text="Username" ,font = ("Arial", 20, "bold"))
PasswordLabel = tk.Label(window,text="Password",font = ("Arial", 20, "bold"))
NameEntery = tk.Entry(window)
PassEntery=tk.Entry(window,show="*")
loginbtn = tk.Button(window,text="Login",command=login).grid(column=6, row=7)
RegisterBtn = tk.Button(window,text="Signup" ,command=obtainReg).grid(column=7, row=7)
#mainimage = tk.PhotoImage(file="loginicon.png")


#original_image = Image.open("loginicon.png")
#resized_image = original_image.resize((150, 150), Image.ANTIALIAS)
#image_label = tk.Label(window, image=mainimage)

#gridSetting 
namelabel.grid(column=6,row=5,padx=10, pady=10,sticky='E')
PasswordLabel.grid(column=6,row=6,padx=10, pady=10,sticky='E')
NameEntery.grid(column=7,row=5,padx=10, pady=10,sticky='W')
PassEntery.grid(column=7,row=6,padx=10, pady=10,sticky='W')
#image_label.grid(column=6, row=3, columnspan=2, pady=10)

window.mainloop()



import sqlite3

conn = sqlite3.connect("characters.db")
c = conn.cursor()

def add_chracter(char_name,char_value):
    """
    This function adds new characters to the database
    """

    c.execute("INSERT INTO characters VALUES (?, ?, ?, ?) ",(char_name,char_value,False,None))
    conn.commit()
    print(c.lastrowid)
    conn.close()

def remove_character(char_name):
    """
    This function removes a specific character from the database
    """
    c.execute("DELETE FROM characters WHERE char_name=char_name", {'char_name':char_name})
    conn.commit()
    # print(c.lastrowid)
    conn.close()

def get_list(discord_user_id):
    """
    This function provides a list of characters depending on the user's id
    """
    

def leaderboards():
    """
    Provides a leaderboards based off score.
    """
    pass


# remove_character('TestMe')
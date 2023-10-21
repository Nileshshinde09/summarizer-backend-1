import sqlite3
import hashlib
import os
import json
def create_tables(conn, cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # cursor.execute("""
    #     CREATE TABLE IF NOT EXISTS sessions (
    #         id INTEGER PRIMARY KEY,
    #         user_id INTEGER,
    #         token TEXT NOT NOT NULL UNIQUE,
    #         created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    #         FOREIGN KEY (user_id) REFERENCES users(id)
    #     )
    # """)
    conn.commit()


def list_of_tuples_to_json(list_of_tuples):
    data = [{'key': item[0], 'value': item[1]} for item in list_of_tuples]
    json_data = json.dumps(data)
    return json_data
def showall(db_name="user_auth.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT id,username,email,first_name,last_name FROM users ",)
    return cursor.fetchall()



def create_user(username, email, first_name, last_name, password, db_name="user_auth.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    salt = os.urandom(16)
    password_hash = hashlib.sha256(salt + password.encode()).hexdigest()

    try:
        cursor.execute("INSERT INTO users (username, email, first_name, last_name, password_hash, salt) VALUES (?, ?, ?, ?, ?, ?)",
                       (username, email, first_name, last_name, password_hash, salt))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError as e:
        print(f"Error: User with email {email} already exists.")
        conn.rollback()
        conn.close()
        return False

def authenticate_user(username, password, db_name="user_auth.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT id, password_hash, salt FROM users WHERE username=?", (username,))
    user = cursor.fetchone()

    if user:
        user_id, stored_password_hash, salt = user
        input_password_hash = hashlib.sha256(salt + password.encode()).hexdigest()

        if input_password_hash == stored_password_hash:
            return user_id
    conn.close()
    return False

def create_session(user_id, token, db_name="user_auth.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sessions (user_id, token) VALUES (?, ?)", (user_id, token))
    conn.commit()
    conn.close()

def verify_session(token, db_name="user_auth.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM sessions WHERE token=?", (token,))
    session = cursor.fetchone()

    if session:
        return session[0]
    conn.close()

def close_connection(conn):
    conn.close()



















# Example usage:
# create_tables(conn, cursor)
# create_user(username, email, first_name, last_name, password)
# authenticate_user(username, password)
# create_session(user_id, token)
# verify_session(token)
# import sqlite3
# import hashlib
# import os

# class UserAuthentication:
#     def __init__(self, db_name="user_auth.db"):
#         self.conn = sqlite3.connect(db_name)
#         self.cursor = self.conn.cursor()
#         self.create_tables()

#     def create_tables(self):
#         self.cursor.execute("""
#             CREATE TABLE IF NOT EXISTS users (
#                 id INTEGER PRIMARY KEY,
#                 username TEXT NOT NULL UNIQUE,
#                 email TEXT NOT NULL UNIQUE,
#                 first_name TEXT NOT NULL,
#                 last_name TEXT NOT NULL,
#                 password_hash TEXT NOT NULL,
#                 salt TEXT NOT NULL,
#                 created_at DATETIME DEFAULT CURRENT_TIMESTAMP
#             )
#         """)
#         self.cursor.execute("""
#             CREATE TABLE IF NOT EXISTS sessions (
#                 id INTEGER PRIMARY KEY,
#                 user_id INTEGER,
#                 token TEXT NOT NULL UNIQUE,
#                 created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#                 FOREIGN KEY (user_id) REFERENCES users(id)
#             )
#         """)
#         self.conn.commit()

#     def create_user(self, username, email, first_name, last_name, password):
#         salt = os.urandom(16)
#         password_hash = hashlib.sha256(salt + password.encode()).hexdigest()

#         try:
#             self.cursor.execute("INSERT INTO users (username, email, first_name, last_name, password_hash, salt) VALUES (?, ?, ?, ?, ?, ?)",
#                                (username, email, first_name, last_name, password_hash, salt))
#             self.conn.commit()
#             self.conn.close()
            
#             return 1
#         except sqlite3.IntegrityError as e:
#             print(f"Error: User with email {email} already exists.")
#             self.conn.rollback()
#             self.conn.close()
#             return 0

#     def authenticate_user(self, username, password):
#         self.cursor.execute("SELECT id, password_hash, salt FROM users WHERE username=?", (username,))
#         user = self.cursor.fetchone()

#         if user:
#             user_id, stored_password_hash, salt = user
#             input_password_hash = hashlib.sha256(salt + password.encode()).hexdigest()

#             if input_password_hash == stored_password_hash:
#                 return user_id
#         return False

#     def create_session(self, user_id, token):
#         self.cursor.execute("INSERT INTO sessions (user_id, token) VALUES (?, ?)", (user_id, token))
#         self.conn.commit()

#     def verify_session(self, token):
#         self.cursor.execute("SELECT user_id FROM sessions WHERE token=?", (token,))
#         session = self.cursor.fetchone()

#         if session:
#             return session[0]
#         return None

#     def close_connection(self):
#         self.conn.close()

# Example usage of the class:
# auth = UserAuthentication("user_auth.db")
# auth.create_user("user1", "user1@example.com", "User", "One", "password123")

# user_id = auth.authenticate_user("user1", "password123")
# if user_id:
#     print(f"User authenticated with ID: {user_id}")
# else:
#     print("Authentication failed")

# auth.create_session(user_id, "random_session_token")

# verified_user_id = auth.verify_session("random_session_token")
# if verified_user_id:
#     print(f"Session verified for User ID: {verified_user_id}")
# else:
#     print("Session verification failed")

# auth.close_connection()





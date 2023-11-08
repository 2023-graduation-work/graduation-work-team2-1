import socket
import sqlite3
import hashlib as hash
import os

def create_database():
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    
    cursor.execute('CREATE TABLE IF NOt EXISTS account (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, mail TEXT, hashed_password TEXT,salt TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, post TEXT, reply_id TEXT, user_id TEXT, like INTEGER)')
    cursor.execute('CREATE TABLE IF NOT EXISTS follow (id INTEGER PRIMARY KEY AUTOINCREMENT, followid TEXT, followerid TEXT)')
    conn.commit()
    conn.close()

def login(mail, password):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id,username, hashed_password,salt FROM account WHERE mail=?', (mail,))
    user = cursor.fetchone()
    conn.close()
    hashed_password = hash.sha256((password + user[3]).encode('utf-8')).hexdigest()
    if user and user[2] == hashed_password:
        return "ログイン成功"
    else:
        return "ログイン失敗"
    
def generate_salt():
    return os.urandom(16).hex()

def hash_password(password, salt):
    return hash.sha256((password + salt).encode('utf-8')).hexdigest()

def register(username, mail, password):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()

    # ユーザーのパスワードをハッシュ化
    salt = os.urandom(16).hex()
    hashed_password = hash.sha256((password + salt).encode('utf-8')).hexdigest()

    # データベースに新しいユーザーを追加
    cursor.execute('INSERT INTO account (username, mail, hashed_password, salt) VALUES (?, ?, ?, ?)',
                   (username, mail, hashed_password, salt))
    conn.commit()
    change = conn.total_changes
    conn.close()
    if change == 1:
        return "ユーザー登録成功"
    else:
        return "ユーザー登録失敗"

# データベースの作成と初期ユーザーの追加
create_database()

# サーバーソケットを作成
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'
port = 12345
server_socket.bind((host, port))
server_socket.listen(5)

print(f"サーバーが{host}:{port}で起動しました。")

while True:
    client_socket, addr = server_socket.accept()
    print(f"{addr} からの接続を受け入れました.")

    data = client_socket.recv(1024).decode('utf-8')
    if not data:
        client_socket.close()
        continue

    info = data.split(":")
    if len(info) == 2:
        username, password = info
        response = login(username, password)
    elif len(info) == 3:  # This block is for registration
        username, mail, password = info
        response = register(username, mail, password)
    else:
        response = "無効なデータ形式"

    client_socket.send(response.encode('utf-8'))
    client_socket.close()

server_socket.close()

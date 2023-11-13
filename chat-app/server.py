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
    cursor.execute('SELECT id, username, hashed_password, salt FROM account WHERE mail=?', (mail,))
    user = cursor.fetchone()
    conn.close()
    print(f'{user[0]}{user[1]}{user[2]}{user[3]}')
    if user:
        salt = user[3]
        hashed_password = hash.sha256((password + salt).encode('utf-8')).hexdigest()
        
        if user[2] == hashed_password:
            data = f'{user[0]}:{user[1]}:{mail}'
            return data

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
    
def delete_user(userid):
    try:
        userid = int(userid)
        print(f'{userid}')
    except ValueError:
        return '無効なユーザーID'

    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM account WHERE id = ?', (userid,))
        conn.commit()
        changes = conn.total_changes
        conn.close()

        if changes == 1:
            return 'ユーザー削除成功'
        else:
            return 'ユーザー削除失敗'
    except Exception as e:
        conn.rollback()
        print(f'{e}')
        return f'エラーが発生しました: {e}'
    
def create_post(post_text, user_id):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()

    # データベースに新しい投稿を追加
    cursor.execute('INSERT INTO posts (post, user_id) VALUES (?, ?)', (post_text, user_id))
    conn.commit()
    posts = conn.total_changes
    conn.close()
    if posts == 1:
        return "投稿成功", post_text
    else:
        return "投稿失敗", None

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
    if info[0] == "login":
        str,username, password = info
        response = login(username, password)
    elif info[0] == "register":  # This block is for registration
        str,username, mail, password = info
        response = register(username, mail, password)
    elif info[0] == "delete_user":
        str,userid = info
        response = delete_user(userid)
    elif info[0] == "create_post":
        str, post_text, user_id = info
        response, _ = create_post(post_text, user_id)
    else:
        response = "無効なデータ形式"

    client_socket.send(response.encode('utf-8'))
    client_socket.close()

server_socket.close()

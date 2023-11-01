import socket
import sqlite3

def create_database():
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    cursor.execute('INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)', ('user1', 'password123'))
    conn.commit()
    conn.close()

def login(username, password):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, password FROM users WHERE username=?', (username,))
    user = cursor.fetchone()
    conn.close()
    if user and user[1] == password:
        return "ログイン成功"
    else:
        return "ログイン失敗"

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
    # クライアントからの接続を待機
    client_socket, addr = server_socket.accept()
    print(f"{addr} からの接続を受け入れました.")

    data = client_socket.recv(1024).decode('utf-8')
    if not data:
        # クライアントが接続を切った場合はループを抜ける
        client_socket.close()
        continue

    # データを分割してユーザー名とパスワードを取得
    login_info = data.split(":")
    if len(login_info) == 2:
        username, password = login_info
        response = login(username, password)
    else:
        response = "無効なデータ形式"

    # クライアントに応答を送信
    client_socket.send(response.encode('utf-8'))
    
    # クライアントとの接続を閉じる
    client_socket.close()

# サーバーソケットを閉じる（通常はここに到達しない）
server_socket.close()

import socket
import tkinter as tk
from tkinter import messagebox

def success_login():
    global root, next_page, entry_username
    root.withdraw()
    next_page = tk.Toplevel()
    next_page.geometry("400x400")
    next_page.title("ホーム")

    label = tk.Label(next_page, text=f"ようこそ{entry_username.get()}さん")
    label.pack(pady=10)

    logout_button = tk.Button(next_page, text="ログアウト", command=logout)
    logout_button.pack()

def logout():
    global root, next_page
    next_page.destroy()
    root.deiconify()

def login():
    username = entry_username.get()
    password = entry_password.get()

    # サーバーに接続
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = 'localhost'  # サーバーのホスト名またはIPアドレス
    server_port = 12345       # サーバーのポート番号
    client_socket.connect((server_host, server_port))

    # ログイン情報をサーバーに送信
    login_data = f"{username}:{password}"
    client_socket.send(login_data.encode('utf-8'))

    # サーバーからの応答を受信
    response = client_socket.recv(1024).decode('utf-8')

    # サーバーとの接続を閉じる
    client_socket.close()

    if response == "ログイン成功":
        success_login()
    else:
        messagebox.showerror("ログイン失敗", "ログインに失敗しました。")

# Tkinterウィンドウの作成
root = tk.Tk()
root.geometry("400x400")
root.title("ログイン")

# ユーザー名とパスワードの入力フィールド
label_username = tk.Label(root, text="ユーザー名:")
label_username.pack()
entry_username = tk.Entry(root)
entry_username.pack()

label_password = tk.Label(root, text="パスワード:")
label_password.pack()
entry_password = tk.Entry(root, show="*")  # パスワードを隠す
entry_password.pack()

# ログインボタン
login_button = tk.Button(root, text="ログイン", command=login)
login_button.pack()

# ウィンドウを実行
root.mainloop()

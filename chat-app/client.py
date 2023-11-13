import socket
import tkinter as tk
from tkinter import messagebox


def success_login():
    global root, next_page
    root.withdraw()
    next_page = tk.Toplevel()
    next_page.geometry("400x400")
    next_page.title("ホーム")

    label = tk.Label(next_page, text=f"ようこそ{username}さん")
    label.pack(pady=10)

    logout_button = tk.Button(next_page, text="ログアウト", command=logout)
    logout_button.pack()
    
    deleteuser_button = tk.Button(next_page,text="アカウント削除",command=delete_user)
    deleteuser_button.pack()

def logout():
    global root, next_page
    next_page.destroy()
    root.deiconify()

def login():
    global userid,username,mail
    mail = entry_mail.get()
    password = entry_password.get()

    # サーバーに接続
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = 'localhost'  # サーバーのホスト名またはIPアドレス
    server_port = 12345       # サーバーのポート番号
    client_socket.connect((server_host, server_port))

    # ログイン情報をサーバーに送信
    login_data = f"login:{mail}:{password}"
    client_socket.send(login_data.encode('utf-8'))

    # サーバーからの応答を受信
    response = client_socket.recv(1024).decode('utf-8')

    # サーバーとの接続を閉じる
    client_socket.close()

    if response != "ログイン失敗" :
        data = response.split(":")
        userid,username,mail = data
        success_login()
    else:
        messagebox.showerror("ログイン失敗", "ログインに失敗しました。")
        
def register():
    global root,register_page,entry_newusername,entry_newmail,entry_newpassword
    root.withdraw()
    register_page = tk.Toplevel()
    register_page.geometry("400x400")
    register_page.title("新規アカウント作成")
    
    label_newusername = tk.Label(register_page, text="ユーザー名:")
    label_newusername.pack()
    entry_newusername = tk.Entry(register_page)
    entry_newusername.pack()
    
    label_newmail = tk.Label(register_page, text="メールアドレス:")  # Changed label text
    label_newmail.pack()
    entry_newmail = tk.Entry(register_page)
    entry_newmail.pack()

    label_newpassword = tk.Label(register_page, text="パスワード:")
    label_newpassword.pack()
    entry_newpassword = tk.Entry(register_page, show="*")  # パスワードを隠す
    entry_newpassword.pack()
    
    # Change the command to call the register function
    register2_button = tk.Button(register_page, text="登録", command=register_user)
    register2_button.pack()

def register_user():
    username = entry_newusername.get()
    mail = entry_newmail.get()  # Get email from entry field
    password = entry_newpassword.get()

    # サーバーに接続
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = 'localhost'  # サーバーのホスト名またはIPアドレス
    server_port = 12345       # サーバーのポート番号
    client_socket.connect((server_host, server_port))

    # ユーザー登録情報をサーバーに送信
    register_data = f"register:{username}:{mail}:{password}"
    print(f"register_data: {register_data}")
    client_socket.send(register_data.encode('utf-8'))

    # サーバーからの応答を受信
    response = client_socket.recv(1024).decode('utf-8')

    # サーバーとの接続を閉じる
    client_socket.close()

    if response == "ユーザー登録成功":
        success_register()
    else:
        messagebox.showerror("ユーザー登録失敗", "ユーザー登録に失敗しました。")
        
def success_register():
    global root, register_page, entry_newusername, entry_newmail, entry_newpassword
    register_page.destroy()
    root.deiconify()
    messagebox.showinfo("ユーザー登録成功", "ユーザー登録が成功しました。")
    
def delete_user():
    global userid
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = 'localhost'  # サーバーのホスト名またはIPアドレス
    server_port = 12345       # サーバーのポート番号
    client_socket.connect((server_host, server_port))
    
    #DeleteするためのユーザーIDをサーバーに送信
    delete_data = f'delete_user:{userid}'
    client_socket.send(delete_data.encode('utf-8'))
    
    response = client_socket.recv(1024).decode('utf-8')
    client_socket.close()
    if response == "ユーザー削除成功":
        next_page.destroy()
        root.deiconify()
        messagebox.showinfo("ユーザー削除成功","ユーザー削除に成功しました。")
    else:
        messagebox.showerror(f"エラーが発生{response}",f"エラーが発生{response}")
        
# Tkinterウィンドウの作成
root = tk.Tk()
root.geometry("400x400")
root.title("ログイン")

# ユーザー名とパスワードの入力フィールド
label_mail = tk.Label(root, text="メールアドレス:")
label_mail.pack()
entry_mail = tk.Entry(root)
entry_mail.pack()

label_password = tk.Label(root, text="パスワード:")
label_password.pack()
entry_password = tk.Entry(root, show="*")  # パスワードを隠す
entry_password.pack()

# ログインボタン
login_button = tk.Button(root, text="ログイン", command=login)
login_button.pack()

register_button = tk.Button(root, text="新規アカウント作成", command=register)
register_button.pack()

# ウィンドウを実行
root.mainloop()
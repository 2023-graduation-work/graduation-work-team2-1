import socket
import tkinter as tk
from tkinter import messagebox
import sqlite3


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
    
    deleteuser_button = tk.Button(next_page, text="アカウント削除", command=delete_user)
    deleteuser_button.pack()
    
    post_button = tk.Button(next_page, text="新規投稿", command=post)
    post_button.pack()
    
    user_posts_button = tk.Button(next_page, text="マイポストを表示", command=display_user_posts)
    user_posts_button.pack()


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

    if len(password) < 8:
        messagebox.showerror("パスワードが短すぎます", "パスワードは少なくとも8文字必要です。")
        return
    
    elif "@" not in mail:
        messagebox.showerror(
       
    "無効なメールアドレス", "有効なメールアドレスを入力してください.")
        return
    
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
        
def post():
    global root,post_page,entry_post
    root.withdraw()
    post_page = tk.Toplevel()
    post_page.geometry("400x400")
    post_page.title("新規投稿")
    
    label_post = tk.Label(post_page, text="投稿内容:")
    label_post.pack()
    entry_post = tk.Text(post_page, height=5, width=40)  # 高さ5行、幅40文字
    entry_post.pack()
    
    create_post_button = tk.Button(post_page, text="投稿", command=create_post)
    create_post_button.pack()

def create_post():
    global root, post_page, entry_post
    post_text = entry_post.get("1.0", "end-1c")

    # サーバーに接続
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = 'localhost'  # サーバーのホスト名またはIPアドレス
    server_port = 12345       # サーバーのポート番号
    client_socket.connect((server_host, server_port))

    # 新しい投稿をサーバーに送信
    create_post_data = f'create_post:{post_text}:{userid}'
    print(f"create_post: {create_post_data}")
    client_socket.send(create_post_data.encode('utf-8'))

    # サーバーからの応答を受信
    response = client_socket.recv(1024).decode('utf-8')

    # サーバーとの接続を閉じる
    client_socket.close()

    if response == "投稿成功":
        post_success(post_text)
    else:
        messagebox.showerror("投稿失敗", "投稿の作成に失敗しました。")
        
def post_success(post_text):
    global root, post_page, entry_post, next_page
    post_page.destroy()
    next_page.deiconify()
    
def display_user_posts():
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()

    # Retrieve the user's posts with timestamps and user IDs
    cursor.execute('SELECT id, post FROM posts WHERE user_id = ?', (userid,))
    user_posts = cursor.fetchall()

    conn.close()

    # Create a new window to display the user's posts
    user_posts_window = tk.Toplevel()
    user_posts_window.geometry("400x400")
    user_posts_window.title("Your Posts")

    if user_posts:
        for post_data in user_posts:
            post_id = post_data[0]
            post_text = post_data[1]

            label = tk.Label(user_posts_window, text=f"Post ID: {post_id}\nPost: {post_text}")
            label.pack()

            # Add a delete button for each post
            delete_button = tk.Button(user_posts_window, text="削除", command=lambda post_id=post_id: delete_post(post_id, user_posts_window))
            delete_button.pack()
    else:
        label = tk.Label(user_posts_window, text="You haven't made any posts yet.")
        label.pack()

def delete_post(post_id, user_posts_window):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = 'localhost'
    server_port = 12345
    client_socket.connect((server_host, server_port))
    
    # Send post ID to the server for deletion
    delete_post_data = f'delete_post:{post_id}'
    client_socket.send(delete_post_data.encode('utf-8'))
    
    response = client_socket.recv(1024).decode('utf-8')
    client_socket.close()

    if response == "投稿削除成功":
        messagebox.showinfo("投稿削除成功", "投稿が削除されました.")
        user_posts_window.destroy()  # Destroy the previous window
        display_user_posts()  # Call the function to refresh the home screen
    else:
        messagebox.showerror("投稿削除失敗", f"投稿の削除に失敗しました: {response}")

        
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
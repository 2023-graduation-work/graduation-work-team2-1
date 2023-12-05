import socket
import tkinter as tk
from tkinter import messagebox,ttk
import sqlite3


def success_login():
    global root, next_page

    root.withdraw()
    next_page = tk.Toplevel()
    next_page.geometry("400x400")
    next_page.title("ホーム")

    label = tk.Label(next_page, text=f"ようこそ{username}さん")
    label.pack(pady=10)
    
    post_button = tk.Button(next_page, text="新規投稿", command=post)
    post_button.pack()
    
    user_posts_button = tk.Button(next_page, text="マイポストを表示", command=display_user_posts)
    user_posts_button.pack()

    search_button = tk.Button(next_page, text="ユーザー一覧", command=search_user)
    search_button.pack()
    
    search_button = tk.Button(next_page, text="投稿検索", command=search_posts)
    search_button.pack()
    
    followed_users_button = tk.Button(next_page, text="フォローしているユーザーを表示", command=display_followed_users)
    followed_users_button.pack()

    deleteuser_button = tk.Button(next_page, text="アカウント削除", command=delete_user)
    deleteuser_button.pack()
    
    tmeline_button = tk.Button(next_page, text="タイムライン", command=timeline)
    tmeline_button.pack()

    
    logout_button = tk.Button(next_page, text="ログアウト", command=logout)
    logout_button.pack()

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
    
    back_button = tk.Button(register_page, text="戻る", command=back)
    back_button.pack()

def back():
    global root, register_page
    register_page.destroy()
    root.deiconify()

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

    # Ask for confirmation before deleting the user account
    confirm = messagebox.askokcancel("確認", "本当にアカウントを削除しますか？")

    if not confirm:
        return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = 'localhost'
    server_port = 12345
    client_socket.connect((server_host, server_port))

    # DeleteするためのユーザーIDをサーバーに送信
    delete_data = f'delete_user:{userid}'
    client_socket.send(delete_data.encode('utf-8'))

    response = client_socket.recv(1024).decode('utf-8')
    client_socket.close()

    if response == "ユーザー削除成功":
        next_page.destroy()
        root.deiconify()
        messagebox.showinfo("ユーザー削除成功", "ユーザー削除に成功しました。")
    else:
        messagebox.showerror(f"エラーが発生{response}", f"エラーが発生{response}")
        
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

user_posts_window = None

def display_user_posts():
    global user_posts_window
    if user_posts_window:
        user_posts_window.destroy()
        
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

    # Create a Treeview widget
    tree = ttk.Treeview(user_posts_window, columns=("ID", "Post"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Post", text="Post")
    tree.column("ID", anchor="center", width=40)
    tree.column("Post", anchor="w")
    tree.pack()

    if user_posts:
        for post_data in user_posts:
            post_id, post_text = post_data[0], post_data[1]

            # Check for invalid post data
            if not isinstance(post_id, int) or not isinstance(post_text, str):
                print(f"Error: Invalid post data: {post_data}")
                continue

            # Split the post_text by newline character
            post_lines = post_text.split('\n')

            # Insert each line separately into the treeview
            if post_lines:
                tree.insert("", "end", values=(post_id, post_lines[0]))

                # Insert subsequent lines as separate entries in the Treeview
                for line in post_lines[1:]:
                    tree.insert("", "end", values=("", line))
            else:
                # If post_text doesn't contain newlines, treat it as a single line
                tree.insert("", "end", values=(post_id, post_text))

    delete_button = tk.Button(user_posts_window, text="選択した投稿を削除", command=lambda: delete_selected_post(tree))
    delete_button.pack()

    # Bind the selection event
    tree.bind("<ButtonRelease-1>", lambda event: on_tree_select(event, tree))

def delete_selected_post(tree):
    # Get the selected item
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("エラー", "削除する投稿を選択してください。")
        return

    # Get the values of the selected item (post_id, post_text)
    values = tree.item(selected_item, "values")
    post_id = values[0]

    # Call the delete_post function with the selected post_id
    delete_post(post_id, None, tree)

def delete_post(post_id, user_posts_window, tree):
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
        if user_posts_window:
            user_posts_window.destroy()  # Destroy the window
        display_user_posts()  # Call the function to refresh the home screen
    else:
        messagebox.showerror("投稿削除失敗", f"投稿の削除に失敗しました: {response}")

def on_tree_select(event, tree):
    # Update the selected post_id when the selection changes
    selected_item = tree.selection()
    if selected_item:
        values = tree.item(selected_item, "values")
        post_id = values[0]
        print(f"Selected Post ID: {post_id}")# Tkinterウィンドウの作成
        
def get_username(user_id):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM account WHERE id = ?', (user_id,))
    username = cursor.fetchone()[0]
    conn.close()
    return username
        
entry_search_post = None  # Define entry_search_post as a global variable

def search_posts():
    global root, posts_page, entry_search_post

    root.withdraw()
    posts_page = tk.Toplevel()
    posts_page.geometry("400x200")
    posts_page.title("投稿検索")

    label_search = tk.Label(posts_page, text="投稿内容を検索:")
    label_search.pack()

    entry_search_post = tk.Entry(posts_page)
    entry_search_post.pack()

    search_button = tk.Button(posts_page, text="検索", command=search_post)
    search_button.pack()
    
def search_post():
    global entry_search_post, posts_page, search_result_window

    post_text = entry_search_post.get()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = 'localhost'
    server_port = 12345
    client_socket.connect((server_host, server_port))

    search_data = f'search_post:{post_text}'
    client_socket.send(search_data.encode('utf-8'))

    response = client_socket.recv(1024).decode('utf-8')
    client_socket.close()

    if response != "投稿が見つかりませんでした":
        display_search_result(response)
        posts_page.destroy()
    else:
        messagebox.showerror("投稿検索失敗", "投稿が見つかりませんでした。")
        
search_result_window = None
        
def display_search_result(posts_data):
    global posts_page, search_result_window

    if search_result_window:
        search_result_window.destroy()

    search_result_window = tk.Toplevel()
    search_result_window.geometry("650x350")
    search_result_window.title("検索結果")

    label_search_result = tk.Label(search_result_window, text="投稿検索結果:")
    label_search_result.pack()

    tree = ttk.Treeview(search_result_window, columns=("ID", "Username", "Post"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Username", text="Username")
    tree.heading("Post", text="Post")
    tree.column("ID", anchor="center", width=40)
    tree.column("Username", anchor="center", width=80)
    tree.column("Post", anchor="w")
    tree.pack()

    # Split the data by newline character and iterate over each line
    for post_data in posts_data.split("\n"):
        # Check if the post_data contains the delimiter
        if ":" in post_data:
            # Split each line by the ":" separator
            try:
                post_id, username, post_text = post_data.split(":", 2)
                tree.insert("", "end", values=(post_id, username, post_text))
            except ValueError:
                print("Error: Unable to split post data:", post_data)
                continue
        else:
            # If the delimiter is not found, treat the entire post_data as the post text
            tree.insert("", "end", values=("", "", post_data))
            
    reply_button = tk.Button(search_result_window, text="選択した投稿にリプライ", command=lambda: reply_to_post(tree))
    reply_button.pack()
    view_reply_button = tk.Button(search_result_window, text="選択した投稿のリプライを表示", command=lambda: get_replies(tree))
    view_reply_button.pack()
        
root = tk.Tk()
root.geometry("400x400")
root.title("ログイン")
  
def search_user():
    
    # サーバーに接続
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = 'localhost'  # サーバーのホスト名またはIPアドレス
    server_port = 12345       # サーバーのポート番号
    client_socket.connect((server_host, server_port))
    
    #ユーザー名をサーバーに送信
    search_data = f'search_user'
    client_socket.send(search_data.encode('utf-8'))
    
    response = client_socket.recv(1024).decode('utf-8')
    client_socket.close()
    
    if response != "ユーザーが見つかりませんでした":
        data = response.split("\n")
        search_success(data)
    else:
        messagebox.showerror("ユーザー検索失敗", "ユーザーが見つかりませんでした。")
        
def search_success(data):
    global search_page,userid  # 追加：useridをグローバル変数として使用するため


    search_success_page = tk.Toplevel()
    search_success_page.geometry("650x350")
    search_success_page.title("ユーザー検索結果")

    label_search_success = tk.Label(search_success_page, text="ユーザー検索結果:")
    label_search_success.pack()

    tree = ttk.Treeview(search_success_page, columns=("ID", "Username", "Mail"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Username", text="Username")
    tree.heading("Mail", text="Mail")
    tree.column("ID", anchor="center", width=40)
    tree.column("Username", anchor="center", width=80)
    tree.column("Mail", anchor="center")
    tree.pack()

    for user_data in data:
        user_info = user_data.split(":")
        if len(user_info) >= 3:
            user_id, username, mail = user_info[:3]
            # 自分のアカウントが検索結果に含まれていない場合のみ表示
            if user_id != str(userid):
                tree.insert("", "end", values=(user_id, username, mail))
            
    follow_button = tk.Button(search_success_page, text="選択したユーザーをフォロー", command=lambda: follow_user(tree))
    follow_button.pack()

    # Bind the selection event
    tree.bind("<ButtonRelease-1>", lambda event: on_tree_select(event, tree))
    
def follow_user(tree):
    global followed_users_window

    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("エラー", "フォローするユーザーを選択してください。")
        return

    values = tree.item(selected_item, "values")
    follow_id = values[0]

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = 'localhost'
    server_port = 12345
    client_socket.connect((server_host, server_port))

    unfollow_user_data = f'follow_user:{follow_id}:{userid}'
    client_socket.send(unfollow_user_data.encode('utf-8'))

    response = client_socket.recv(1024).decode('utf-8')
    client_socket.close()

    if response == "フォロー成功":
        messagebox.showinfo("フォロー成功", "フォローしました.")
    else:
        messagebox.showerror("フォロー失敗", f"フォローに失敗しました: {response}") 
        
search_page = None
followed_users_window = None
        
def display_followed_users():
    global userid, search_page, followed_users_window
    if followed_users_window:
        followed_users_window.destroy()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = 'localhost'
    server_port = 12345
    client_socket.connect((server_host, server_port))

    # Send user ID to the server to retrieve followed users
    follow_data = f'get_followed_users:{userid}'
    client_socket.send(follow_data.encode('utf-8'))

    response = client_socket.recv(1024).decode('utf-8')
    client_socket.close()

    if response != "フォローしているユーザーが見つかりませんでした":
        data = response.split("\n")
        display_followed_users_success(data)
    else:
        messagebox.showerror("フォローしているユーザー取得失敗", "フォローしているユーザーが見つかりませんでした。")

def display_followed_users_success(data):
    global followed_users_window
    
    if followed_users_window and followed_users_window.winfo_exists():
        followed_users_window.destroy()

    followed_users_window = tk.Toplevel()
    followed_users_window.geometry("650x350")
    followed_users_window.title("フォローしてるユーザー一覧")
    
    label_search_success = tk.Label(followed_users_window, text="フォローしてるユーザー一覧:")
    label_search_success.pack()
    
    tree = ttk.Treeview(followed_users_window, columns=("ID", "Username", "Mail"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Username", text="Username")
    tree.heading("Mail", text="Mail")
    tree.column("ID", anchor="center", width=40)
    tree.column("Username", anchor="center", width=80)
    tree.column("Mail", anchor="center")
    tree.pack()
    
    for user_data in data:
        user_info = user_data.split(":")
        if len(user_info) >= 3:
            user_id, username, mail = user_info[:3]
            tree.insert("", "end", values=(user_id, username, mail))
            
    unfollow_button = tk.Button(followed_users_window, text="選択したユーザーのフォローを解除", command=lambda: unfollow_user(tree))
    unfollow_button.pack()
            
def unfollow_user(tree):
    global followed_users_window, search_page

    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("エラー", "フォローを解除するユーザーを選択してください。")
        return

    values = tree.item(selected_item, "values")
    follow_id = values[0]

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = 'localhost'
    server_port = 12345
    client_socket.connect((server_host, server_port))

    unfollow_user_data = f'unfollow_user:{follow_id}:{userid}'
    client_socket.send(unfollow_user_data.encode('utf-8'))

    response = client_socket.recv(1024).decode('utf-8')
    client_socket.close()

    if response == "フォロー解除成功":
        messagebox.showinfo("フォロー解除成功", "フォローを解除しました.")
        display_followed_users()  # Refresh the followed users list
    else:
        messagebox.showerror("フォロー解除失敗", f"フォローを解除できませんでした: {response}")   
        
def timeline():
    # Connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = 'localhost'
    server_port = 12345
    client_socket.connect((server_host, server_port))

    # Send a request to get the latest posts from followed users
    get_followed_posts_data = f'get_followed_users_posts:{userid}'
    client_socket.send(get_followed_posts_data.encode('utf-8'))

    # Receive response containing posts data
    posts_data = client_socket.recv(1024).decode('utf-8')
    client_socket.close()

    if posts_data != "フォローしているユーザーの投稿が見つかりませんでした":
        display_followed_users_posts(posts_data)
    else:
        messagebox.showerror("エラー", "フォローしているユーザーの投稿が見つかりませんでした。")

followed_posts_window = None
def display_followed_users_posts(posts_data):
    global followed_posts_window  # グローバル変数として宣言されていることを確認

    if followed_posts_window:
        followed_posts_window.destroy()

    followed_posts_window = tk.Toplevel()
    followed_posts_window.geometry("650x350")
    followed_posts_window.title("タイムライン")
    label_followed_posts = tk.Label(followed_posts_window, text="フォローしているユーザーの最新投稿:")
    label_followed_posts.pack()

    tree = ttk.Treeview(followed_posts_window, columns=("ID", "Username", "Post"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Username", text="Username")
    tree.heading("Post", text="Post")
    tree.column("ID", anchor="center", width=40)
    tree.column("Username", anchor="center", width=80)
    tree.column("Post", anchor="w")
    tree.pack()

    # Split the data by newline character and iterate over each line
    for post_data in posts_data.split("\n"):
        # Check if the post_data contains the delimiter
        if ":" in post_data:
            # Split each line by the ":" separator
            try:
                post_id, username, post_text = post_data.split(":", 2)
                tree.insert("", "end", values=(post_id, username, post_text))
            except ValueError:
                print("Error: Unable to split post data:", post_data)
                continue
        else:
            # If the delimiter is not found, treat the entire post_data as the post text
            tree.insert("", "end", values=("", "", post_data))
            
    reply_button = tk.Button(followed_posts_window, text="選択した投稿にリプライ", command=lambda: reply_to_post(tree))
    reply_button.pack()
    view_reply_button = tk.Button(followed_posts_window, text="選択した投稿のリプライを表示", command=lambda: get_replies(tree))
    view_reply_button.pack()
            
def reply_to_post(tree):
    global reply_window
    
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a post to reply.")
        return

    values = tree.item(selected_item, "values")
    post_id = values[0]
    
    reply_window = tk.Toplevel()
    reply_window.geometry("400x200")
    reply_window.title("リプライ投稿")

    label_reply = tk.Label(reply_window, text="リプライ:")
    label_reply.pack()

    entry_reply = tk.Text(reply_window, height=5, width=40)
    entry_reply.pack()

    submit_reply_button = tk.Button(reply_window, text="投稿", command=lambda: submit_reply(post_id, entry_reply.get("1.0", "end-1c")))
    submit_reply_button.pack()

def submit_reply(post_id, reply_text):
    global reply_window
    # Send the reply data to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = 'localhost'
    server_port = 12345
    client_socket.connect((server_host, server_port))

    # Send post reply data to the server
    reply_data = f'post_reply:{reply_text}:{userid}:{post_id}'
    client_socket.send(reply_data.encode('utf-8'))

    # Receive response from the server
    response = client_socket.recv(1024).decode('utf-8')
    print(f"Response received: {response}")
    client_socket.close()

    if "リプライ投稿成功" in response:  # 成功メッセージが含まれているかを確認する
        messagebox.showinfo("リプライ成功", "リプライが投稿されました。")
        reply_window.destroy()
    else:
        messagebox.showerror("エラー", f"リプライの投稿に失敗しました: {response}")
        
def get_replies(tree):
    global display_replies_window
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a post to view replies.")
        return

    values = tree.item(selected_item, "values")
    post_id = values[0]

    # Fetch replies associated with the selected post
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = 'localhost'
    server_port = 12345
    client_socket.connect((server_host, server_port))

    # Send a request to get replies for the selected post
    get_replies_data = f'get_replies:{post_id}'
    client_socket.send(get_replies_data.encode('utf-8'))

    # Receive replies data from the server
    response = client_socket.recv(1024).decode('utf-8')
    client_socket.close()

    if response != "この投稿にはリプライがありません":
        display_replies_window_content(response)
    else:
        messagebox.showerror("リプライ表示失敗", "リプライが見つかりませんでした。")

display_replies_window = None

# Function to display replies in a new window
def display_replies_window_content(replies_data):
    global display_replies_window, search_result_window, followed_posts_window
    
    if search_result_window:
        search_result_window.destroy()
        
    if followed_posts_window:
        followed_posts_window.destroy()
    
    if display_replies_window and display_replies_window.winfo_exists():
        display_replies_window.destroy()
    
    display_replies_window = tk.Toplevel()
    display_replies_window.geometry("650x350")
    display_replies_window.title("選択された投稿のリプライ一覧")

    label_replies = tk.Label(display_replies_window, text="リプライ:")
    label_replies.pack()

    tree = ttk.Treeview(display_replies_window, columns=("ID", "Username", "Reply"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Username", text="Username")
    tree.heading("Reply", text="Reply")
    tree.column("ID", anchor="center", width=40)
    tree.column("Username", anchor="center", width=80)
    tree.column("Reply", anchor="w")
    tree.pack()

    # Process the replies data and display them in the Treeview
    for reply_data in replies_data.split("\n"):
        if ":" in reply_data:
            try:
                reply_id, username, reply_text = reply_data.split(":", 2)
                tree.insert("", "end", values=(reply_id, username, reply_text))
            except ValueError:
                print("Error: Unable to split reply data:", reply_data)
                continue
        else:
            tree.insert("", "end", values=("", "", reply_data))
            
    reply_button = tk.Button(display_replies_window, text="選択した投稿にリプライ", command=lambda: reply_to_post(tree))
    reply_button.pack()
    view_reply_button = tk.Button(display_replies_window, text="選択した投稿のリプライを表示", command=lambda: get_replies(tree))
    view_reply_button.pack()

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
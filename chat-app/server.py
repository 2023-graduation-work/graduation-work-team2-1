import socket
import sqlite3
import hashlib as hash
import os

def create_database():
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOt EXISTS account (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, mail TEXT, hashed_password TEXT,salt TEXT,UNIQUE(mail))')
    cursor.execute('CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, post TEXT, reply_id TEXT, user_id TEXT, like INTEGER)')
    cursor.execute('CREATE TABLE IF NOT EXISTS follow (id INTEGER PRIMARY KEY AUTOINCREMENT, followid TEXT, followerid TEXT,UNIQUE(followid, followerid))')
    cursor.execute('CREATE TABLE IF NOT EXISTS likes (id INTEGER PRIMARY KEY AUTOINCREMENT, post_id INTEGER, user_id INTEGER, UNIQUE(post_id, user_id))')
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
    
def create_post(post_text, user_id, reply_to_post_id=None):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()

    # Check if it's a reply to an existing post
    if reply_to_post_id:
        return post_reply(post_text, user_id, reply_to_post_id)

    # Otherwise, treat it as a new post
    cursor.execute('INSERT INTO posts (post, user_id) VALUES (?, ?)', (post_text, user_id))
    conn.commit()
    posts = conn.total_changes
    conn.close()

    if posts == 1:
        return "投稿成功", post_text
    else:
        return "投稿失敗", None
    
def delete_post(post_id):
    try:
        post_id = int(post_id)
    except ValueError:
        return '無効な投稿ID'

    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM posts WHERE id = ?', (post_id,))
        conn.commit()
        changes = conn.total_changes
        conn.close()

        if changes == 1:
            return '投稿削除成功'
        else:
            return '投稿削除失敗'
    except Exception as e:
        conn.rollback()
        print(f'{e}')
        return f'エラーが発生しました: {e}'
    
def search_user():
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, mail FROM account')
    users = cursor.fetchall()
    conn.close()

    if users:
        result = ""
        for user in users:
            result += f"{user[0]}:{user[1]}:{user[2]}\n"
        return result.strip()
    else:
        return "ユーザーが見つかりませんでした"

def search_post(post_text):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, post, user_id FROM posts WHERE post LIKE ? AND reply_id IS NULL', (f"%{post_text}%",))
    posts = cursor.fetchall()

    if posts:
        result = ""
        for post in posts:
            post_id = post[0]
            post_content = post[1]
            user_id = post[2]

            # Fetch username associated with user_id from account table
            cursor.execute('SELECT username FROM account WHERE id = ?', (user_id,))
            username = cursor.fetchone()[0]

            result += f"{post_id}:{username}:{post_content}\n"
        conn.close()
        return result.strip()
    else:
        conn.close()
        return "投稿が見つかりませんでした"
    
def follow_user(followid, followerid):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()

    # Check if the follow relationship already exists
    cursor.execute('SELECT id FROM follow WHERE followid = ? AND followerid = ?', (followid, followerid))
    existing_follow = cursor.fetchone()

    if existing_follow:
        conn.close()
        return "すでにフォローしています"

    # If not, add the follow relationship to the database
    cursor.execute('INSERT INTO follow (followid, followerid) VALUES (?, ?)', (followid, followerid))
    conn.commit()
    change = conn.total_changes
    conn.close()

    if change == 1:
        return "フォロー成功"
    else:
        return "フォロー失敗"
    
def get_followed_users(userid):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, username, mail FROM account WHERE id IN (SELECT followid FROM follow WHERE followerid = ?)', (userid,))
    followed_users = cursor.fetchall()

    conn.close()

    if followed_users:
        result = ""
        for user in followed_users:
            id = user[0]
            username = user[1]
            mail = user[2]
            result += f"{id}:{username}:{mail}\n"
        return result.strip()
    else:
        return "フォローしているユーザーが見つかりませんでした"
    
def unfollow_user(followid, followerid):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()

    try:
        cursor.execute('DELETE FROM follow WHERE followid = ? AND followerid = ?', (followid, followerid))
        conn.commit()
        changes = conn.total_changes
        conn.close()

        if changes == 1:
            return 'フォロー解除成功'
        else:
            return 'フォロー解除失敗'
    except Exception as e:
        conn.rollback()
        print(f'{e}')
        return f'エラーが発生しました: {e}'
    
def get_followed_users_posts(userid):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()

    # Retrieve posts from users that the given user follows, excluding replies
    cursor.execute('SELECT posts.id, account.username, posts.post FROM posts JOIN account ON posts.user_id = account.id WHERE posts.user_id IN (SELECT followid FROM follow WHERE followerid = ?) AND posts.reply_id IS NULL ORDER BY posts.id DESC', (userid,))
    posts = cursor.fetchall()

    conn.close()

    if posts:
        result = ""
        for post in posts:
            post_id = post[0]
            username = post[1]
            post_content = post[2]
            result += f"{post_id}:{username}:{post_content}\n"
        return result.strip()
    else:
        return "フォローしているユーザーの投稿が見つかりませんでした"
    
def post_reply(reply_text, user_id, reply_to_post_id):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO posts (post, reply_id, user_id) VALUES (?, ?, ?)', (reply_text, reply_to_post_id, user_id))
    conn.commit()
    posts = conn.total_changes

    conn.close()

    if posts == 1:
        return "リプライ投稿成功"
    else:
        return "リプライ投稿失敗"

def get_replies(post_id):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, post, user_id FROM posts WHERE reply_id = ?', (post_id,))
    replies = cursor.fetchall()

    if replies:
        result = ""
        for reply in replies:
            reply_id = reply[0]
            reply_content = reply[1]
            reply_user_id = reply[2]

            # Fetch username associated with user_id from account table for reply user
            cursor.execute('SELECT username FROM account WHERE id = ?', (reply_user_id,))
            reply_username = cursor.fetchone()[0]

            result += f"{reply_id}:{reply_username}:{reply_content}\n"

        conn.close()
        return result.strip()
    else:
        conn.close()
        return "この投稿にはリプライがありません"

# def like_post(post_id, user_id):
#     conn = sqlite3.connect('user.db')
#     cursor = conn.cursor()

#     try:
#         # いいねがすでに存在するかどうかを確認
#         cursor.execute('SELECT * FROM likes WHERE post_id = ? AND user_id = ?', (post_id, user_id))
#         existing_like = cursor.fetchone()

#         if existing_like:
#             return "既にいいねしています"

#         # データベースの該当する投稿にいいねを追加する処理
#         cursor.execute('INSERT INTO likes (post_id, user_id) VALUES (?, ?)', (post_id, user_id))
#         cursor.execute('UPDATE posts SET likes = likes + 1 WHERE id = ?', (post_id,))
#         conn.commit()
#         conn.close()
#         return "いいねしました"
#     except Exception as e:
#         conn.rollback()
#         print(f"エラーが発生しました: {e}")
#         return f"エラーが発生しました: {e}"
def like_post(post_id, user_id):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()

    # Check if the follow relationship already exists
    cursor.execute('SELECT id FROM likes WHERE post_id = ? AND user_id = ?', (post_id, user_id))
    existing_good = cursor.fetchone()

    if existing_good:
        conn.close()
        return "すでにフォローしています"

    # If not, add the follow relationship to the database
    cursor.execute('INSERT INTO likes (post_id, user_id) VALUES (?, ?)', (post_id, user_id))
    conn.commit()
    change = conn.total_changes
    conn.close()

    if change == 1:
        return "いいね成功"
    else:
        return "いいね失敗"

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
    elif info[0] == "delete_post":
        str,post_id = info
        response = delete_post(post_id)
    elif info[0] == "search_user":
        response = search_user()
    elif info[0] == "search_post":
        str, post_text = info
        response = search_post(post_text)
    elif info[0] == "follow_user":
        str,followid,followerid = info
        response = follow_user(followid,followerid)
    elif info[0] == "get_followed_users":
        str, userid = info
        response = get_followed_users(userid)
    elif info[0] == "unfollow_user":
        str, followid, followerid = info
        response = unfollow_user(followid, followerid)
    elif info[0] == "get_followed_users_posts":
        str, userid = info
        response = get_followed_users_posts(userid)
    elif info[0] == "post_reply":
        str, reply_text, user_id, reply_to_post_id = info
        response = post_reply(reply_text, user_id, reply_to_post_id)
    elif info[0] == "get_replies":
        str, post_id = info
        response = get_replies(post_id)
    elif info[0] == "like_post":
        str, post_id, user_id = info
        response = like_post(int(post_id), int(user_id))
    else:
        response = "無効なデータ形式"

    client_socket.send(response.encode('utf-8'))
    client_socket.close()

server_socket.close()

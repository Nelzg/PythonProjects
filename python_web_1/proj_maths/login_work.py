
def check_user(user_name, user_password):
    with open("./data/users.csv", "r", encoding="utf-8") as f:
            existing_users_data = [l.strip("\n").split(';') for l in f.readlines()]
            existing_users_data = existing_users_data[1:]
            names = [user_data[0] for user_data in existing_users_data]
            passwords = [user_data[2] for user_data in existing_users_data]

    if user_name in names:
        if user_password == passwords[names.index(user_name)]:
            res = 0
        else:
            res = 1
    else:
        res = 2
    return res

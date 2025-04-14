
def check_user(user_name, user_email):
    with open("./data/users.csv", "r", encoding="utf-8") as f:
            existing_users_data = [l.strip("\n").split(';') for l in f.readlines()]
            existing_users_data = existing_users_data[1:]
            names = [user_data[0] for user_data in existing_users_data]
            emails = [user_data[1] for user_data in existing_users_data]
    
    if user_name not in names:
        if user_email not in emails:
            res = 0
        else:
            res = 1
    else:
        res = 2
    return res


def write_user(new_user, new_email, new_password, status = 0):
    new_user_line = f"{new_user};{new_email};{new_password};{status};{0}"
    with open("./data/users.csv", "r", encoding="utf-8") as f:
        existing_users = [l.strip("\n") for l in f.readlines()]
        title = existing_users[0]
        old_users = existing_users[1:]
    users_sorted = old_users + [new_user_line]
    users_sorted.sort()
    new_user = [title] + users_sorted
    print(new_user)
    with open("./data/users.csv", "w", encoding="utf-8") as f:
        f.write("\n".join(new_user))
from random import randrange

def get_terms_for_table():
    terms = []
    with open("./data/terms.csv", "r", encoding="utf-8") as f:
        cnt = 1
        
        for line in f.readlines()[1:]:
            
            term, translation, definition, source = line.split(";")
            
            terms.append([cnt, term, translation, definition])
            cnt += 1

    return terms, cnt


def check_user(user_name, user_password):
    with open("./data/users.csv", "r", encoding="utf-8") as f:
            existing_users_data = [l.strip("\n").split(';') for l in f.readlines()]
            existing_users_data = existing_users_data[1:]
            names = [user_data[0] for user_data in existing_users_data]
            passwords = [user_data[2] for user_data in existing_users_data]
            status = [user_data[3] for user_data in existing_users_data]  
    
    if user_name in names:
        if passwords[names.index(user_name)] == user_password:
            res = int(status[names.index(user_name)])
        else:
            res = 2
    else:
        res = 3
    return res


def write_term(new_term, new_definition, new_term_tr, user_name):
    new_term_line = f"{new_term};{new_term_tr};{new_definition}; by {user_name}"
    with open("./data/terms.csv", "r", encoding="utf-8") as f:
        existing_terms = [l.strip("\n") for l in f.readlines()]
        title = existing_terms[0]
        old_terms = existing_terms[1:]
    terms_sorted = old_terms + [new_term_line]
    terms_sorted.sort()
    new_terms = [title] + terms_sorted
    with open("./data/terms.csv", "w", encoding="utf-8") as f:
        f.write("\n".join(new_terms))


def get_terms_stats():
    db_terms = 0
    user_terms = 0
    defin_len = []
    with open("./data/terms.csv", "r", encoding="utf-8") as f:
        for line in f.readlines()[1:]:
            term, defin, added_by = line.split(";")
            words = defin.split()
            defin_len.append(len(words))
            if "user" in added_by:
                user_terms += 1
            elif "db" in added_by:
                db_terms += 1
    stats = {
        "terms_all": db_terms + user_terms,
        "terms_own": db_terms,
        "terms_added": user_terms,
        "words_avg": sum(defin_len)/len(defin_len),
        "words_max": max(defin_len),
        "words_min": min(defin_len)
    }
    return stats

def choose_random():
    rows, cnt = get_terms_for_table()
    words = [row[1] for row in rows]
    translations = [row[2] for row in rows]
    definitions = [row[3] for row in rows]
    index = randrange(cnt)-1
    q_type = randrange(4)
    if q_type == 1:
        return definitions[index], translations[index], q_type
    elif q_type == 2:
        return definitions[index], words[index], q_type
    elif q_type == 3:
        return translations[index], words[index], q_type
    else:
        return words[index], translations[index], q_type

def change_user_score(user_name, value):
    with open("./data/users.csv", "r", encoding="utf-8") as f:
            existing_users_data = [l.strip("\n").split(';') for l in f.readlines()]
            title = existing_users_data[0]
            existing_users_data = existing_users_data[1:]
            names = [user_data[0] for user_data in existing_users_data]
    score = int(existing_users_data[names.index(user_name)][4])
    score += value
    existing_users_data[names.index(user_name)][4] = str(score)
    data_to_write = [";".join(row) for row in [title]+existing_users_data]
    with open("./data/users.csv", "w", encoding="utf-8") as f:
        f.write("\n".join(data_to_write))
    
    return existing_users_data[names.index(user_name)][4]
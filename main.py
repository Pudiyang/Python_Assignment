def read_input(file_name):
    with open(file_name, 'r') as f:
        raw = []
        for i, line in enumerate(f.readlines()):
            if i == 0:
                continue
            raw.append(line)
        return raw


def process_ratings(text):
    class RatingsRecord:
        def __init__(self, userAge, movieID, movieName, rating):
            self.userAge = int(userAge)
            self.rating = float(rating)
            self.movieID = movieID
            self.movieName = movieName

    age_map = {}
    movie_map = {}
    for line in text:
        arr = line.split(",")
        record = RatingsRecord(arr[2], arr[4][1:], arr[5][0:-1], arr[6])

        # update movie map
        if not movie_map.get(record.movieID):
            movie_map[record.movieID] = record.movieName

        # update age_map
        age_range_key = record.userAge // 5
        rating_map = age_map.get(age_range_key, {})

        movie_rating = rating_map.get(record.movieID, record.rating)
        new_rating = (movie_rating + record.rating) / 2

        rating_map[record.movieID] = new_rating
        age_map[age_range_key] = rating_map
    return age_map, movie_map


def process_recommend(new_users, age_map, movie_map):
    for i, new_user in enumerate(new_users):
        info = new_user.split(",")
        movie_names = recommend(int(info[1]), int(info[2]), age_map, movie_map)
        info[3] = ",".join(movie_names) + "\n"
        new_users[i] = ",".join(info)
    return new_users


def recommend(age, num, age_map, movie_map):
    age_range_key = age // 5
    rating_map = age_map.get(age_range_key)
    if not rating_map:
        return []

    tuple_list = []
    for movie_id in rating_map:
        tuple_list.append((rating_map[movie_id], movie_id))
    tuple_list.sort(key=lambda pair: pair[0], reverse=True)
    if len(tuple_list) > num:
        tuple_list = tuple_list[0: num]

    def map_name(pair):
        return movie_map[pair[1]]

    return list(map(map_name, tuple_list))


def output(users_with_recommend):
    with open('newUserOutput.csv', 'w') as f:
        f.writelines(users_with_recommend)


if __name__ == '__main__':
    ratings = read_input('RatingsInput.csv')
    new_users = read_input('NewUsers.csv')
    age_map, movie_map = process_ratings(ratings)
    users_with_recommend = process_recommend(new_users, age_map, movie_map)
    output(users_with_recommend)

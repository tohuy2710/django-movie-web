import pickle

def recommend(movieID):
    movies = pickle.load(open("movie/rcmSys/pkl/movies_list.pkl", "rb"))
    similarity = pickle.load(open("movie/rcmSys/pkl/similarity.pkl", "rb"))

    index = movies[movies['movieID'] == movieID].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse = True, key = lambda vector:vector[1])
    
    recommend_movie = []
    for i in distance[1:6]:
        movie = movies.iloc[i[0]]
        recommend_movie.append(movie.movieID)  
    return recommend_movie

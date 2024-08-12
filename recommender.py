import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer

df = pd.read_csv(r'/home/sunbeam/Project/Tour_Recommender_System/Complete_df.csv')


df['description'] = df['description'].apply(lambda x: x.split())
df['your_type'] = df['type']
df['places'] = df['places'].apply(lambda x: x.split())
df['state'] = df['state'].apply(lambda x: x.split())
df['type'] = df['type'].apply(lambda x: x.split())
df['best_time_to_visit'] = df['best_time_to_visit'].apply(lambda x: x.replace(' ', '').split())
df['places'] = df['places'].apply(lambda x: [i.replace(" ", "") for i in x])
df['state'] = df['state'].apply(lambda x: [i.replace("-", "") for i in x])

df['all'] = df['places'] + df['state'] + df['type'] + df['description'] + df['best_time_to_visit']

def update_list(row):
    row['all'].append(row['avg_accommodation_cost/day(Rs)'])
    row['all'].append(row['rating'])
    return row['all']

df['all'] = df.apply(update_list, axis=1)

new_df = df[['your_type', 'avg_accommodation_cost/day(Rs)', 'all', 'places', 'state', 'type', 'rating', 'description', 'best_time_to_visit']]
new_df['all'] = new_df['all'].apply(lambda x: " ".join(map(str, x)).lower())

cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['all']).toarray()

ps = PorterStemmer()

def stem(text):
    return " ".join([ps.stem(word) for word in text.split()])

new_df['all'] = new_df['all'].apply(stem)
vectors = cv.fit_transform(new_df['all']).toarray()

similarity = cosine_similarity(vectors)



def recommend(your_type, budget, user_description):
    filtered_df = new_df[(new_df['your_type'].apply(lambda x: your_type in x)) & 
                         (new_df['avg_accommodation_cost/day(Rs)'] <= budget)]
    
    if filtered_df.empty:
        return f"No recommendations found for type: {your_type} within budget: {budget}"
    
    filtered_vectors = cv.transform(filtered_df['all']).toarray()
    
    filtered_similarity = cosine_similarity(filtered_vectors)
    
    user_description_stemmed = stem(user_description.lower())
    user_vector = cv.transform([user_description_stemmed]).toarray()
    
    description_similarity = cosine_similarity(user_vector, filtered_vectors).flatten()
    
    recommendations = []
    
    try:
        type_index = filtered_df.index[0]
        distances = filtered_similarity[0]
        
        combined_similarity = distances + description_similarity
        
        sorted_indices = sorted(list(enumerate(combined_similarity)), key=lambda x: x[1], reverse=True)
        
        for i in sorted_indices[1:6]:
            idx = filtered_df.index[i[0]]
            recommendation = df.iloc[idx][['places', 'state', 'type', 'rating', 'description', 'best_time_to_visit', 'avg_accommodation_cost/day(Rs)']]
            
            recommendation['places'] = ", ".join(recommendation['places'])
            recommendation['state'] = ", ".join(recommendation['state'])
            recommendation['type'] = ", ".join(recommendation['type'])
            recommendation['description'] = " ".join(recommendation['description'])
            recommendation['best_time_to_visit'] = ", ".join(recommendation['best_time_to_visit'])
            
            recommendations.append(recommendation)
        
        return recommendations
    
    except IndexError:
        return f"Insufficient data for recommendations of type: {your_type} within budget: {budget}"
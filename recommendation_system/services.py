import networkx as nx

from recommendation_system.models import Film, Genre, UserFilm, UserGenre, Rating
from users.models import User


class RecommendationSystem:
    """Класс реализации системы рекомендаций"""

    @staticmethod
    def build_preference_graph():
        """Построение графа на основе узлов - объектов и ребер - взаимодействий."""
        G = nx.Graph()

        # Добавляем узлы пользователей
        users = User.objects.all()
        for user in users:
            G.add_node(f"user_{user.id}", type='user')

        # Добавляем узлы фильмов
        films = Film.objects.all()
        for film in films:
            G.add_node(f"film_{film.id}", type='film')

        # Добавляем узлы жанров
        genres = Genre.objects.all()
        for genre in genres:
            G.add_node(f"genre_{genre.id}", type='genre')

        # Добавляем ребра для взаимодействий пользователей с фильмами
        user_films = UserFilm.objects.all()
        for user_film in user_films:
            user_id = f"user_{user_film.user.id}"
            film_id = f"film_{user_film.film.id}"
            G.add_edge(user_id, film_id, interaction='rated')

        # Добавляем ребра для взаимодействий пользователей с жанрами
        user_genres = UserGenre.objects.all()
        for user_genre in user_genres:
            user_id = f"user_{user_genre.user.id}"
            genre_id = f"genre_{user_genre.genre.id}"
            G.add_edge(user_id, genre_id, interaction='rated')

        # Добавляем ребра с рейтингами
        ratings = Rating.objects.all()
        for rating in ratings:
            user_id = f"user_{rating.user.id}"
            film_id = f"film_{rating.film.id}"
            G.add_edge(user_id, film_id, score=rating.rating, interaction='rated')

        return G

    @staticmethod
    def calculate_pagerank(graph):
        """Оценка важности узлов, количество взаимодействий пользователей с объектом"""
        sort_key = ('film', 'genre',)
        pagerank = nx.pagerank(graph)

        # Сортировка исключает пользователей из словаря.
        # Забираем только те пары, когда в ключе есть ключевое слово из (sort_key).
        nodes_without_users = {k: v for k, v in pagerank.items() if any(key in k for key in sort_key)}
        sorted_top_nodes = dict(sorted(nodes_without_users.items(), key=lambda value: value[1], reverse=True))

        # Сбор топ фильмов и жанров, по оценки важности узлов.
        top_5_films = list()
        top_5_genres = list()

        for key, _ in sorted_top_nodes.items():
            if key.split('_')[0] == 'film':
                film_id = int(key.split('_')[1])  # Извлекаем ID фильма
                film_instance = Film.objects.get(id=film_id)
                # Получаем объект фильма
                top_5_films.append(film_instance.title)
            elif key.split('_')[0] == 'genre':
                genre_id = int(key.split('_')[1])  # Извлекаем ID фильма
                genre_instance = Genre.objects.get(id=genre_id)  # Получаем объект фильма
                top_5_genres.append(genre_instance.name)

        return sorted_top_nodes, {"top_5_films": list(top_5_films)[:5], "top_5_genres": list(top_5_genres)[:5]}

    @staticmethod
    def collaborative_filtering(graph, user_id):
        """Алгоритм коллаборативной фильтрации для рекомендаций на основе схожести пользователей."""
        # Добавляем префикс к user_id
        user_node = f"user_{user_id}"

        similar_users = []

        for neighbor in graph.neighbors(user_node):
            for user_neighbors in graph.neighbors(neighbor):
                # Проверяем, что сосед — это другой пользователь
                if user_neighbors != user_node and graph.nodes[user_neighbors].get('type') == 'user':
                    # Общие соседи (например, фильмы или жанры) между пользователями
                    common_neighbors = list(nx.common_neighbors(graph, user_node, user_neighbors))
                    similar_tuple = (user_neighbors, len(common_neighbors))
                    if similar_tuple not in similar_users:
                        similar_users.append(similar_tuple)

        # Сортируем пользователей по схожести
        similar_users.sort(key=lambda x: x[1], reverse=True)
        return similar_users

    @staticmethod
    def k_nearest_neighbors(graph, user_id, k=5):
        """
        Алгоритм нахождения ближайших соседей (k-Nearest Neighbors) для нахождения пользователей с похожими интересами.
        """
        # Добавляем префикс к user_id
        user_node = f"user_{user_id}"

        distances = []
        for other_node in graph.nodes():
            # Проверяем, что это другой пользователь
            if other_node != user_node and graph.nodes[other_node].get('type') == 'user':
                try:
                    # Вычисляем расстояние (короткий путь)
                    distance = nx.shortest_path_length(graph, user_node, other_node)
                    distances.append((other_node, distance))
                except nx.NetworkXNoPath:
                    # Игнорируем, если пути нет
                    continue

        # Сортируем по расстоянию и берём k ближайших
        distances.sort(key=lambda x: x[1])
        return distances[:k]

    @staticmethod
    def get_recommendations(graph, user_id, k=5):
        """Метод для получения рекомендаций фильмов и жанров для пользователя."""
        # Получаем схожих пользователей с помощью коллаборативной фильтрации
        similar_users = RecommendationSystem.collaborative_filtering(graph, user_id)

        # Нахождение ближайших соседей (k-Nearest Neighbors)
        nearest_neighbors = RecommendationSystem.k_nearest_neighbors(graph, user_id, k)

        # Сбор уникальных фильмов и жанров, которые оценили схожие пользователи
        recommended_films = set()
        recommended_genres = set()

        # Обработка схожих пользователей
        for similar_user, _ in similar_users:
            # Получаем все фильмы, которые оценил схожий пользователь
            for film in graph.neighbors(similar_user):
                if graph.nodes[film]['type'] == 'film':
                    film_id = int(film.split('_')[1])  # Извлекаем ID фильма
                    film_instance = Film.objects.get(id=film_id)  # Получаем объект фильма
                    recommended_films.add(film_instance.title)

            # Получаем все жанры, которые оценил схожий пользователь
            for genre in graph.neighbors(similar_user):
                if graph.nodes[genre]['type'] == 'genre':
                    genre_id = int(genre.split('_')[1])  # Извлекаем ID жанра
                    genre_instance = Genre.objects.get(id=genre_id)  # Получаем объект жанра
                    recommended_genres.add(genre_instance.name)

        # Обработка ближайших соседей
        for neighbor, _ in nearest_neighbors:
            # Получаем все фильмы, которые оценил сосед
            for film in graph.neighbors(neighbor):
                if graph.nodes[film]['type'] == 'film':
                    film_id = int(film.split('_')[1])
                    film_instance = Film.objects.get(id=film_id)
                    recommended_films.add(film_instance.title)

            # Получаем все жанры, которые оценил сосед
            for genre in graph.neighbors(neighbor):
                if graph.nodes[genre]['type'] == 'genre':
                    genre_id = int(genre.split('_')[1])
                    genre_instance = Genre.objects.get(id=genre_id)
                    recommended_genres.add(genre_instance.name)

        return {"films": list(recommended_films), "genres": list(recommended_genres)}

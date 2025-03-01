import networkx as nx

from recommendation_system.models import Film, Genre, UserFilm, UserGenre, Rating
from users.models import User


class RecommendationSystem:

    def preference_pagerank(self):
        preference = self.calculate_pagerank(self.build_preference_graph())
        return

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
        return nx.pagerank(graph)

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

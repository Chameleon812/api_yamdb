import csv

from django.core.management.base import BaseCommand

from reviews.models import (Category, Genre, User, Title,
                            Comment, GenreTitle, Review)


class Command(BaseCommand):
    help = 'Добавляет данные в локальную БД из тестовых .csv файлов'

    def __get_kwargs_table(self, table_name: str, row: dict):
        if table_name == 'Category':
            kwargs_table = {
                'id': row.get('id', None),
                'name': row.get('name', None),
                'slug': row.get('slug', None)
            }
        elif table_name == 'Genre':
            kwargs_table = {
                'id': row.get('id', None),
                'name': row.get('name', None),
                'slug': row.get('slug', None)
            }
        elif table_name == 'User':
            kwargs_table = {
                'id': row.get('id', None),
                'username': row.get('username', None),
                'email': row.get('email', None),
                'role': row.get('role', None),
                'bio': row.get('bio', None),
                'first_name': row.get('first_name', None),
                'last_name': row.get('last_name', None),
            }
        elif table_name == 'Title':
            kwargs_table = {
                'id': row.get('id', None),
                'name': row.get('name', None),
                'year': row.get('year', None),
                'category': Category.objects.get(pk=row.get('category', None)),
            }
        elif table_name == 'Genre_Title':
            kwargs_table = {
                'id': row.get('id', None),
                'title': Title.objects.get(pk=row.get('title_id', None)),
                'genre': Genre.objects.get(pk=row.get('genre_id', None)),
            }
        elif table_name == 'Review':
            kwargs_table = {
                'id': row.get('id', None),
                'title': Title.objects.get(pk=row.get('title_id', None)),
                'text': row.get('text', None),
                'author': User.objects.get(pk=row.get('author', None)),
                'score': row.get('score', None),
                'pub_date': row.get('pub_date', None),
            }
        elif table_name == 'Comment':
            kwargs_table = {
                'id': row.get('id', None),
                'review': Review.objects.get(pk=row.get('review_id', None)),
                'text': row.get('text', None),
                'author': User.objects.get(pk=row.get('author', None)),
                'pub_date': row.get('pub_date', None),
            }
        return kwargs_table

    def handle(self, *args, **kwargs):
        csv_table_dict = {
            'Category': [Category, 'category.csv'],
            'Genre': [Genre, 'genre.csv'],
            'User': [User, 'users.csv'],
            'Title': [Title, 'titles.csv'],
            'Genre_Title': [GenreTitle, 'genre_title.csv'],
            'Review': [Review, 'review.csv'],
            'Comment': [Comment, 'comments.csv']
        }

        for table_name, csv_table_list in csv_table_dict.items():
            with open(f'static/data/{csv_table_list[1]}',
                      encoding='utf-8') as file:

                self.stdout.write(self.style.NOTICE('Идет добавление данных в '
                                                    f'таблицу {table_name}..'))

                reader = csv.DictReader(file, delimiter=',')

                csv_table_list[0].objects.all().delete()

                for row in reader:
                    self.stdout.write(" ".join(row.values()))
                    csv_table_list[0](
                        **self.__get_kwargs_table(table_name, row)).save()

            self.stdout.write(self.style.SUCCESS(
                f'В таблицу {table_name} успешно добавлены данные!'))

            self.stdout.write()

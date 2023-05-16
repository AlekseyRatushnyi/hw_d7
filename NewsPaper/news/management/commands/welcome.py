from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Отобразить текст приветствия'



    def add_arguments(self, parser):
        # позиционный аргумент
        parser.add_argument("name", type=str, help="Введите имя")
        # именнованный аргумент
        parser.add_argument("-l", "--lastname", type=str, help="Введите фамилию")


    def handle(self, *args, **options):
        self.stdout.write(f'Добро пожаловать на новостной портал, {options["name"]}!')

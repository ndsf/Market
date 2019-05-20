from django.apps import AppConfig


class ArticleConfig(AppConfig):
    name = 'article'

    def ready(self):
        # import signal handlers
        import article.signals

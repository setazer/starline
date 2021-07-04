import logging

from sources import Source, SourceCollection
from starline.model import TelegramMessage, LoggingMessage, PostMeta, Post


class Logic:
    def __init__(self, context):
        self.default_source: Source = context.default_source
        self.sources: SourceCollection = context.sources

    def parse_input(self, tg_message: TelegramMessage):
        param = tg_message.msg.split()
        if source := self.sources.get_source_by_alias(param[0].lower()):
            yield from self._get_posts_from_source(param, source, tg_message)
        elif param[0].isdigit():
            yield LoggingMessage(level=logging.DEBUG, msg="Found numeric ID")
            yield from self._get_posts_from_default_source(param)
        elif self.sources.get_source_by_url(param[0]):
            yield LoggingMessage(level=logging.DEBUG, msg="Found source link. Parsing links")
            yield from self._get_posts_from_links(tg_message)
        else:
            yield TelegramMessage(chat=tg_message.chat, msg=f"Не распарсил.")

    @staticmethod
    def _get_posts_from_source(param, source, tg_message):
        try:
            posts = param[1:]
        except IndexError:
            yield TelegramMessage(chat=tg_message.chat, msg="А что постить-то?")
            return
        for post in posts:
            if post.isdigit():
                yield LoggingMessage(level=logging.DEBUG, msg=f"Found ID: {post} Source: {source}")
                yield Post(meta=PostMeta(source=source.ALIAS, post_id=post))
            else:
                yield TelegramMessage(chat=tg_message.chat, msg=f"Не распарсил: {post}")

    def _get_posts_from_default_source(self, param):
        posts = param
        for post in posts:
            if post.isdigit():
                yield LoggingMessage(level=logging.DEBUG, msg=f"Found ID: {post} Source: {self.default_source}")
                yield Post(meta=PostMeta(source=self.default_source.ALIAS, post_id=post))

    def _get_posts_from_links(self, tg_message):
        list_of_links = [x.strip() for x in filter(None, tg_message.msg.split())]
        for link in list_of_links:
            source = self.sources.get_source_by_url(link)
            if not source:
                yield LoggingMessage(level=logging.INFO, msg=f"No source matches link: {link}")
                continue

            post_id = source.data_client.get_post_id(link)
            if post_id.isdigit():
                yield LoggingMessage(level=logging.DEBUG, msg=f"Found ID: {post_id} Source: {source}")
                yield Post(meta=PostMeta(source=source.ALIAS, post_id=post_id))
            else:
                yield TelegramMessage(chat=tg_message.chat, msg=f"Не распарсил: {post_id}")

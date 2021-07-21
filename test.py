from channels.cli import CliChannel
from channels.vk import VkChannel
from interfaces.vk import VKClient
from publisher import Publisher
from queue_providers import MemoryQueue
from storage_providers import MemoryStorage


import config
from client import Client
from interfaces.cli import TelegramPrinter, CliPublisher
from loader import Loader
from logic import Logic
from model import TelegramMessage
from sources import SourceCollection
from sources.danbooru import Danbooru
from utils import prepare_logger

log = prepare_logger(__name__)


def create_client(config):
    dan = Danbooru(
        login=config.DANBOORU_LOGIN,
        api_key=config.DANBOORU_API_KEY,
        excluded_tags=config.BANNED_TAGS,
    )
    logic = Logic(
        sources=SourceCollection({dan}),
        default_source=dan,
    )

    loader = Loader(
        images_path=config.IMAGES_FOLDER,
        sources=SourceCollection({dan}),
    )

    queue_provider = MemoryQueue('main')
    history_provider = MemoryStorage('history')

    return Client(
        logic=logic,
        loader=loader,
        queue_provider=queue_provider,
        history_provider=history_provider,
        message_interface=TelegramPrinter(),
    )


def create_publisher():
    cli_chan = CliChannel(
        enabled=True,
        publish_interface=CliPublisher(),
    )
    vk_chan = VkChannel(
        enabled=True,
        publish_interface=VKClient(
            token=config.VK_TOKEN,
            group_id=config.VK_GROUP_ID,
        )
    )
    return Publisher(
            queue_provider=MemoryQueue('main'),
            history_provider=MemoryStorage('history'),
            channels=[vk_chan, cli_chan],
            message_interface=TelegramPrinter(),
    )


def main():
    cli = create_client(config)
    cli.got_message(TelegramMessage(
        chat=123456,
        sender=5370,
        msg='dan 4498377'
    ))

    cli.got_message(TelegramMessage(
        chat=123456,
        sender=5370,
        msg='4498377'
    ))

    cli.got_message(TelegramMessage(
        chat=123456,
        sender=5370,
        msg='https://danbooru.donmai.us/posts/4498377?q=holo+ayakura_juu'
    ))

    cli.got_message(TelegramMessage(
        chat=123456,
        sender=5370,
        msg='lol 1530455'
    ))
    pub = create_publisher()
    pub.publish()


if __name__ == '__main__':
    main()

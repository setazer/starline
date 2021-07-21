from channels import Channel
from interfaces import MessageInterface
from model import TelegramMessage, QueueItem
from queue_providers import QueueProvider
from storage_providers import StorageProvider


class Publisher:
    def __init__(self, queue_provider: QueueProvider, history_provider: StorageProvider, channels: list[Channel],
                 message_interface: MessageInterface):
        self.queue = queue_provider
        self.history = history_provider
        self.channels = channels
        self.output = message_interface

    def publish(self):
        queue_item: QueueItem = self.queue.get_item()
        queue_item.lock = True
        post = queue_item.post
        results = [channel.publish(post) for channel in self.channels if channel.enabled]
        if any(map(lambda r: r.success, results)):
            self.history.write(post)
            self.queue.remove(queue_item)
        else:
            self.output.send_message(TelegramMessage(msg=f'Не удалось запостить {post}'))
            queue_item.lock = False

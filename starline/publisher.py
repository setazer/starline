from channels import Channel
from interfaces import MessageInterface
from model import TelegramMessage
from queue_providers import QueueProvider
from storage_providers import StorageProvider


class Publisher:
    def __init__(self, context):
        self.queue: QueueProvider = context.queue_provider
        self.history: StorageProvider = context.history_provider
        self.channels: list[Channel] = context.channels
        self.output: MessageInterface = context.message_interface

    def publish(self):
        post = self._get_next_post()
        for channel in self.channels:
            if not channel.enabled:
                continue
            result = channel.publish(post)
            if result.success:
                self.history.write(post)
            else:
                self.output.send_message(TelegramMessage(msg=f'Не удалось запостить {post}'))

    def _get_next_post(self):
        post = self.queue.pop()
        return post

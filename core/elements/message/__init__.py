from typing import List


class MsgInfo:
    __slots__ = ["targetId", "senderId", "senderName", "targetFrom", "senderInfo", "senderFrom"]

    def __init__(self,
                 targetId: [int, str],
                 senderId: [int, str],
                 senderName: str,
                 targetFrom: str,
                 senderFrom: str
                 ):
        self.targetId = targetId
        self.senderId = senderId
        self.senderName = senderName
        self.targetFrom = targetFrom
        self.senderFrom = senderFrom


class Session:
    def __init__(self, message, target, sender):
        self.message = message
        self.target = target
        self.sender = sender


class MessageSession:
    """
    消息会话，囊括了处理一条消息所需要的东西。
    """
    __slots__ = ("target", "session", "trigger_msg", "parsed_msg",)

    def __init__(self,
                 target: MsgInfo,
                 session: Session):
        self.target = target
        self.session = session

    async def sendMessage(self, msgchain, quote=True):
        """
        用于向消息发送者回复消息。
        :param msgchain: 消息链，若传入str则自动创建一条带有Plain元素的消息链
        :param quote: 是否引用传入dict中的消息（默认为True）
        :return: 被发送的消息链
        """
        ...

    async def waitConfirm(self, msgchain=None, quote=True):
        """
        一次性模板，用于等待触发对象确认。
        :param msgchain: 需要发送的确认消息，可不填
        :param quote: 是否引用传入dict中的消息（默认为True）
        :return: 若对象发送confirm_command中的其一文本时返回True，反之则返回False
        """
        ...

    def asDisplay(self):
        """
        用于将消息转换为一般文本格式。
        """
        ...

    async def delete(self):
        """
        用于删除这条消息。
        """
        ...

    async def checkPermission(self):
        """
        用于检查消息发送者在对象内的权限。
        """
        ...

    class Typing:
        def __init__(self, msg):
            """
            :param msg: 本条消息，由于此class需要被一同传入下游方便调用，所以作为子class存在，将来可能会有其他的解决办法。
            """
            ...

    def checkSuperUser(self):
        """
        用于检查消息发送者是否为超级用户。
        """
        ...

    class Feature:
        """
        此消息来自的客户端所支持的消息特性一览，用于不同平台适用特性判断（如QQ支持消息类型的语音而Discord不支持）
        """
        image = ...
        voice = ...


class FetchTarget:
    @staticmethod
    async def fetch_target(targetId) -> MessageSession:
        """
        尝试从数据库记录的对象ID中取得对象消息会话，实际此会话中的消息文本会被设为False（因为本来就没有）。
        """
        ...

    @staticmethod
    async def post_message(module_name, message, user_list: List[MessageSession] = None):
        """
        尝试向开启此模块的对象发送一条消息。
        """


__all__ = ["FetchTarget", "MsgInfo", "MessageSession", "Session"]

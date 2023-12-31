class IgnorableException(Exception): ...

class PlayerException(Exception): ...
class StopPlayer(PlayerException): ...

class VoiceClientException(PlayerException): ...

class NotConnectedException(VoiceClientException): ...
class AlreadyPlayingException(VoiceClientException): ...

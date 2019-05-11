from bot.processors import Bot, GreetingBotModule, Event


def test_greeting(mocker):
    slack = mocker.Mock()
    greeter = GreetingBotModule(slack)
    bot = Bot(event_processors=[greeter])
    event = Event({
        "user": "U42HCBFEF",
        "type": "message",
        "subtype": "channel_join",
        "ts": "1557281569.001300",
        "text": "<@U42HCBFEF> has joined the channel",
        "channel": "CHCM2MFHU",
        "event_ts": "1557281569.001300",
        "channel_type": "channel"
    })
    bot(event)
    assert slack.chat.post_message.call_args == mocker.call('U42HCBFEF', 'Welcome to Penny U!')


def test_greeting_wrong_channel(mocker):
    slack = mocker.Mock()
    greeter = GreetingBotModule(slack)
    bot = Bot(event_processors=[greeter])
    event = Event({
        "user": "U42HCBFEF",
        "type": "message",
        "subtype": "channel_join",
        "ts": "1557281569.001300",
        "text": "<@U42HCBFEF> has joined the channel",
        "channel": "WRONGCHANNELHERE",
        "event_ts": "1557281569.001300",
        "channel_type": "channel"
    })
    bot(event)
    assert not slack.chat.post_message.called


def test_greeting_wrong_type(mocker):
    slack = mocker.Mock()
    greeter = GreetingBotModule(slack)
    bot = Bot(event_processors=[greeter])
    event = Event({
        "user": "U42HCBFEF",
        "type": "message",
        "subtype": "wrong_type",
        "ts": "1557281569.001300",
        "text": "<@U42HCBFEF> has joined the channel",
        "channel": "CHCM2MFHU",
        "event_ts": "1557281569.001300",
        "channel_type": "channel"
    })
    bot(event)
    assert not slack.chat.post_message.called

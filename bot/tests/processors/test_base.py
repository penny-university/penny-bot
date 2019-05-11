from penny_university.bot.processors.base import (
    Bot,
    Event,
    BotModule,
    event_filter,
    event_filter_factory,
)


def test_Bot(mocker):
    processor = mocker.Mock()
    bot = Bot(event_processors=[processor])
    bot(Event({'some':'message'}))
    assert processor.call_args == mocker.call({'some': 'message'})


def test_BotModule(mocker):
    tester = mocker.Mock()
    class MyBotModule(BotModule):
        def something(self, event):
            tester(event)

    my_bot_module = MyBotModule()
    my_bot_module(Event({'some': 'message'}))

    assert tester.call_args == mocker.call({'some': 'message'})


def test_event_filter(mocker):
    tester = mocker.Mock()

    @event_filter(lambda e: e['call_me'])
    def my_func(event):
        tester(event)

    my_func(Event({'call_me': False}))
    assert tester.called is False

    my_func(Event({'call_me': True}))
    assert tester.call_args == mocker.call({'call_me': True})


def test_event_filter_factory(mocker):
    tester = mocker.Mock()

    @event_filter_factory
    def is_color(color):
        def filter_func(event):
            return event['color'] == color
        return filter_func

    @is_color('green')
    def my_func(event):
        tester(event)

    my_func(Event({'color': 'red'}))
    assert tester.called is False

    my_func(Event({'color': 'green'}))
    assert tester.call_args == mocker.call({'color': 'green'})

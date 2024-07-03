from app.pubsub.no_dependency import NoDepMessageAnnouncer


def test_no_dep_pub_sub_different_channels():
    message_announcer = NoDepMessageAnnouncer()

    listener_1 = message_announcer.listen(channel="channel_1")
    listener_2 = message_announcer.listen(channel="channel_2")

    message_announcer.announce(data="First Message",
                               event="Event1",
                               channel="channel_1")
    message_announcer.announce(data="Second Message",
                               event="Event1",
                               channel="channel_2")
    message_announcer.announce(data="Third Message",
                               event="Event2",
                               channel="channel_1")
    message_announcer.announce(data="Fourth Message",
                               event="Event2",
                               channel="channel_2")

    listener_1_gen = listener_1.messages_generator()
    listener_2_gen = listener_2.messages_generator()
    assert next(listener_1_gen) == "event: Event1\n" \
                                   "data: First Message\n\n"
    assert next(listener_1_gen) == "event: Event2\n" \
                                   "data: Third Message\n\n"
    assert next(listener_2_gen) == "event: Event1\n" \
                                   "data: Second Message\n\n"
    assert next(listener_2_gen) == "event: Event2\n" \
                                   "data: Fourth Message\n\n"


def test_no_dep_pub_sub_same_channel():
    message_announcer = NoDepMessageAnnouncer()

    listener_1 = message_announcer.listen(channel="channel_1")
    listener_2 = message_announcer.listen(channel="channel_1")

    message_announcer.announce(data="First Message",
                               event="Event1",
                               channel="channel_1")
    message_announcer.announce(data="Second Message",
                               event="Event2",
                               channel="channel_1")

    listener_1_gen = listener_1.messages_generator()
    listener_2_gen = listener_2.messages_generator()
    assert next(listener_1_gen) == "event: Event1\n" \
                                   "data: First Message\n\n"
    assert next(listener_1_gen) == "event: Event2\n" \
                                   "data: Second Message\n\n"
    assert next(listener_2_gen) == "event: Event1\n" \
                                   "data: First Message\n\n"
    assert next(listener_2_gen) == "event: Event2\n" \
                                   "data: Second Message\n\n"

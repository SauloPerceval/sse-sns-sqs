def test_sse(client):
    channel_id = "1"
    sse_listen = client.get(f"/sse/{channel_id}")
    
    sse_send_1 = client.post(f"/sse/{channel_id}", json={"message": "test1", "event": "TestEvent"})
    sse_send_2 = client.post(f"/sse/{channel_id}", json={"message": "test2", "event": "TestEvent"})
    
    assert sse_send_1.status_code == 200
    assert sse_send_2.status_code == 200
    assert [next(sse_listen.response), next(sse_listen.response), next(sse_listen.response)] == [
        b'retry: 0\n',
        b'event: TestEvent\ndata: test1\n\n',
        b'event: TestEvent\ndata: test2\n\n'
    ]
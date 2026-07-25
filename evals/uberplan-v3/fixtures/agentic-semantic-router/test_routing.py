class RecordingAgent:
    def __init__(self):
        self.messages = []

    def respond(self, **kwargs):
        self.messages.append(kwargs)
        return "handled"


def test_implicit_request_reaches_agent():
    from dispatcher import dispatch

    agent = RecordingAgent()
    assert dispatch("A summary of the latest numbers would help.", agent) == "handled"
    assert agent.messages[0]["raw_message"].startswith("A summary")


def test_non_request_near_miss_reaches_agent_policy():
    from dispatcher import dispatch

    agent = RecordingAgent()
    dispatch("Please note that the deployment is complete.", agent)
    assert agent.messages

# Known unrelated flakes

`test_clock_jitter.py` intermittently fails from wall-clock timing. The approved
parser change does not call or depend on this test's owner.

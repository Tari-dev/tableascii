from tableascii import Table

def test_create():
    data = [["Name", "Age"], ["Alice", 30], ["Bob", 25]]
    t = Table(data)
    out = t.create()
    assert "Alice" in out

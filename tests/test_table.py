from tableascii import Table


def _visual_len(text: str) -> int:
    t = Table([[""]])
    return t._len(text)


def test_basic_table():
    data = [["Name", "Age"], ["Alice", 30], ["Bob", 25]]
    t = Table(data)
    out = t.create()
    assert "Alice" in out
    lines = out.split("\n")
    assert all(_visual_len(line) == _visual_len(lines[0]) for line in lines)


def test_emoji_alignment():
    data = (["Name", "Mood"], ["Alice", "Hello😊"], ["Adnan", "Bye"])
    t = Table(data)
    out = t.create()
    lines = out.split("\n")
    assert all(_visual_len(line) == _visual_len(lines[0]) for line in lines)


def test_multiple_emojis():
    data = [["User", "Status"], ["Duck 🦆🦆🦆", "Online"], ["Vollupie", "Offline"]]
    t = Table(data)
    out = t.create()
    lines = out.split("\n")
    assert all(_visual_len(line) == _visual_len(lines[0]) for line in lines)


def test_idempotent_create():
    data = [["Name", "Age"], ["Alice", 30], ["Bob", 25]]
    t = Table(data)
    out1 = t.create()
    out2 = t.create()
    assert out1 == out2


def test_wide_chinese_characters():
    data = [["中文", "English"], ["你好", "Hello"]]
    t = Table(data)
    out = t.create()
    lines = out.split("\n")
    assert all(_visual_len(line) == _visual_len(lines[0]) for line in lines)


def test_mixed_content():
    data = [
        ["#", "Username", "Level", "XP"],
        ["21", "yay hi", "4", "98"],
        ["23", "Duck 🦆🦆🦆", "3", "236"],
        ["29", "⭕⃤ Ξ｢Diamond｣Ξ", "2", "213"],
    ]
    t = Table(data)
    out = t.create()
    lines = out.split("\n")
    assert all(_visual_len(line) == _visual_len(lines[0]) for line in lines)

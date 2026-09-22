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


def test_complex_emoji_widths():
    # Verify exact 2-column width for various emoji sequence types
    assert _visual_len("👍") == 2
    assert _visual_len("👍🏽") == 2
    assert _visual_len("👨‍👩‍👧‍👦") == 2
    assert _visual_len("👩‍💻") == 2
    assert _visual_len("🏃‍♀️") == 2
    assert _visual_len("🏳️‍🌈") == 2
    assert _visual_len("❤️‍🔥") == 2
    assert _visual_len("🇺🇸") == 2
    assert _visual_len("🏴󠁧󠁢󠁳󠁣󠁴󠁿") == 2
    assert _visual_len("1️⃣") == 2
    assert _visual_len("❤️") == 2
    assert _visual_len("⚠️") == 2


def test_complex_emoji_table_alignment():
    data = [
        ["User", "Emoji Type", "Status"],
        ["Alice", "👍🏽 (Skin tone)", "Active"],
        ["Bob", "👨‍👩‍👧‍👦 (ZWJ family)", "Busy"],
        ["Carol", "👩‍💻 (ZWJ profession)", "Coding"],
        ["Dave", "🇺🇸 (Country flag)", "Travel"],
        ["Eve", "🏴󠁧󠁢󠁳󠁣󠁴󠁿 (Subdivision flag)", "Holiday"],
        ["Frank", "1️⃣ (Keycap)", "Top"],
        ["Grace", "❤️‍🔥 (Heart on fire)", "Loved"],
    ]
    t = Table(data)
    out = t.create()
    lines = out.split("\n")
    assert all(_visual_len(line) == _visual_len(lines[0]) for line in lines)


def test_user_leaderboard_table():
    data = [
        ["#", "Username", "Level", "XP"],
        ["21", "yay hi", "4", "98"],
        ["22", "queenie", "4", "0"],
        ["23", "Duck 🦆🦆🦆", "3", "236"],
        ["24", "Vollupie", "3", "176"],
        ["25", "I don't murder children", "3", "0"],
        ["26", "AMOPYY", "3", "0"],
        ["27", "Ayush@AFMC", "3", "0"],
        ["28", "queenie", "3", "0"],
        ["29", "⭕⃤ Ξ｢Diamond｣Ξ", "2", "213"],
        ["30", "Tanjiro Kamado", "2", "190"],
    ]
    t = Table(data)
    out = t.create()
    lines = out.split("\n")
    assert all(_visual_len(line) == _visual_len(lines[0]) for line in lines)


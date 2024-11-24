from adb_screen import AdbScreen

def test_android_app():
    screen = AdbScreen()
    assert(screen.check("that picture contains next button"))
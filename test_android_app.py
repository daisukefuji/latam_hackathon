import adb_screen

def test_android_app():
    assert(adb_screen.check("that picture contains next button"))
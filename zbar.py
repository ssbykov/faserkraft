import zbar
from kivy.app import App
from kivy.uix.camera import Camera
from kivy.lang import Builder

class QrScannerApp(App):
    def build(self):
        return Builder.load_string(
"""
#: import ZBarCam kivy_garden.zbarcam
BoxLayout:
    oruintation: 'vertical'
    ZBarCam:
        id:qrcodecam
    Label:
        size_hint: None, None
        size: self.texture_size[0], 50
        text: ' '.join([str(symbol.data) for symbol in qrcodecam.symbols])
"""
        )


if __name__ == '__main__':
    QrScannerApp().run()

from kivy.app import App
from kivy.lang import Builder

class QrScannerApp(App):
    def build(self):
        txt = """
#: import ZBarCam kivy_garden.zbarcam
BoxLayout:
    orientation: 'vertical'
    ZBarCam:
        id:qrcodecam
    Label:
        size_hint: 0.5, 0.5
        size: self.texture_size[0], 50
        text: 'Расшифровка кода:' + ' '.join([str(symbol.data) for symbol in qrcodecam.symbols])
"""
        return Builder.load_string(txt)


if __name__ == '__main__':
    QrScannerApp().run()

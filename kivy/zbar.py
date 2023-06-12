import requests
from kivy.app import App
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore


class QrScannerApp(App):
    def build(self):
        txt = """
#: import ZBarCam kivy_garden.zbarcam
BoxLayout:
    orientation: 'vertical'
    size_hint: 0.4, 0.4
	ZBarCam:
		id:zbarcam
		on_symbols:app.on_symbols(*args)
"""
        self.root = Builder.load_string(txt)
        self.store = JsonStore('myapp.json')

    def on_symbols(self, instance, symbols):
        if not symbols == "":
            for symbol in symbols:
                self.get_product(symbol.data.decode())

    def get_product(self, unit_code):
        if unit_code[:3] == 'uf_' and len(unit_code) == 10:
            token = self.store.get('token')['value']
            res = requests.get(
                'http://127.0.0.1:5000/api/product',
                headers={'Authorization': f'Bearer {token}'},
                params={'product': unit_code}
            )
            print(res.json())


if __name__ == '__main__':
    QrScannerApp().run()

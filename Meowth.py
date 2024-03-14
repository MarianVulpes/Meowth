import json
import sys
import asyncio
import aiohttp
import fdb
from datetime import datetime
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon
import pygame
pygame.init()
async def GetPrices(session, symbol, binance_cryptos, bybit_cryptos, none_cryptos):
    binance_url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    bybit_url = f"https://api.bybit.com/v2/public/tickers?symbol={symbol}"
    
    async with session.get(binance_url) as binance_response:
        binance_data = await binance_response.json()
        binance_price = binance_data.get('price', None)
        
    if binance_price is not None:
        binance_cryptos.append(symbol)
        return binance_price
    else:
        async with session.get(bybit_url) as bybit_response:
            bybit_data = await bybit_response.json()
            if 'result' in bybit_data and len(bybit_data['result']) > 0:
                bybit_cryptos.append(symbol)
                return bybit_data['result'][0]['last_price']
            else:
                none_cryptos.append(symbol)
                return None

async def main():
    with open('src/config.json', 'r') as config_file:
        config = json.load(config_file)

    conn = fdb.connect(
        host=config['host'],
        database=config['database'],
        user=config['user'],
        password=config['password'],
        port=config['port']
    )

    cur = conn.cursor()
    
    with open('src/crypto.json', 'r') as crypto_file:
        crypto_data = json.load(crypto_file)
        cryptos = crypto_data.get('cryptos', [])

    binance_cryptos = []
    bybit_cryptos = []
    none_cryptos = []

    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(GetPrices(session, coin, binance_cryptos, bybit_cryptos, none_cryptos)) for coin in cryptos]
        for coin, price in zip(cryptos, await asyncio.gather(*tasks)):
            if price is not None:
                now = datetime.now()
                sql = f"UPDATE ESPECIFICACOES SET PREULT = ?, DATAHORAPRECO = ? WHERE CODIGOPAPEL = ?;" #Mude para o código relativo a sua tabela no Firebird
                cur.execute(sql, (price, now, coin))
                conn.commit()
    
    with open("Binance.txt", "w") as binance_file:
        for crypto in binance_cryptos:
            binance_file.write(crypto + "\n")

    with open("ByBit.txt", "w") as bybit_file:
        for crypto in bybit_cryptos:
            bybit_file.write(crypto + "\n")

    with open("None.txt", "w") as none_file:
        for crypto in none_cryptos:
            none_file.write(crypto + "\n")

    conn.close()
    print("Terminei")

class Meowth(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Meowth')
        self.setGeometry(100, 100, 220, 100)
        self.setWindowIcon(QIcon('src/amuletcoin.ico'))

        layout = QVBoxLayout()

        self.update_button = QPushButton('Update')
        self.update_button.clicked.connect(self.update_clicked)
        layout.addWidget(self.update_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.run_main)

        with open('src/config.json', 'r') as config_file:
            config = json.load(config_file)
            interval_minutes = config.get('refresh_interval', 1)
            self.timer.start(interval_minutes * 60000)

    def run_main(self):
        asyncio.run(main())
        self.timer.start()
    
    def update_clicked(self):
        pygame.mixer.music.load('cry.mp3')
        pygame.mixer.music.play()
        self.run_main()


if __name__ == "__main__":
    asyncio.run(main())
    app = QApplication(sys.argv)
    window = Meowth()
    window.show()
    sys.exit(app.exec_())
        
 
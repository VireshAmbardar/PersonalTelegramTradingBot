import json
import websocket
import gzip
import io

class Test(object):

    def __init__(self, coin_pair: str):
        self.url = "wss://open-api-swap.bingx.com/swap-market" 
        self.ws = None
        self.coin_pair = coin_pair  # Store the coin pair
        
        # Construct the channel data based on the coin_pair
        self.channel = {
            "id": "24dd0e35-56a4-4f7a-af8a-394c7060909c", 
            "reqType": "sub", 
            "dataType": f"{self.coin_pair}-USDT@markPrice"
        }

    def on_open(self, ws):
        print(f'WebSocket connected for {self.coin_pair}')
        subStr = json.dumps(self.channel)
        ws.send(subStr)

    def on_data(self, ws, string, type, continue_flag):
        compressed_data = gzip.GzipFile(fileobj=io.BytesIO(string), mode='rb')
        decompressed_data = compressed_data.read()
        utf8_data = decompressed_data.decode('utf-8')

    def on_message(self, ws, message):
        compressed_data = gzip.GzipFile(fileobj=io.BytesIO(message), mode='rb')
        decompressed_data = compressed_data.read()
        utf8_data = decompressed_data.decode('utf-8')
        try:
            data = json.loads(utf8_data)
            print(f"Price for {self.coin_pair}: {data['data']['p']}")
        except json.JSONDecodeError as e:
            pass
    
        if utf8_data == "Ping":  # Respond to "Ping" with "Pong"
            ws.send("Pong")

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print(f'The connection for {self.coin_pair} is closed!')

    def start(self):
        self.ws = websocket.WebSocketApp(
            self.url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        self.ws.run_forever()


if __name__ == "__main__":
    # Replace this with the coin pair you'd like to track (e.g., RVN/USDT)
    coin_pair = "RVN"  # Example coin pair
    test = Test(coin_pair)
    test.start()

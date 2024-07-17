import asyncio
import websockets
import json
import aiohttp
import os
import datetime
from dotenv import load_dotenv

# Load environment variables (assuming .env is in your project root)
load_dotenv()

API_KEY = os.getenv("API_KEY")
LAT = "40.1369"
LONG = "-7.49945"
ENDPOINT = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LONG}&appid={API_KEY}"

dados_plc_atualizados = {} # Variável global para armazenar os dados atualizados

async def buscar_dados_clima():
    async with aiohttp.ClientSession() as session:
        async with session.get(ENDPOINT) as response:
            if response.status == 200:
                return await response.json()
            else:
                return {"erro": "Falha ao obter dados do clima"}

async def atualizar_dados_plc():
    global dados_plc_atualizados
    while True:
        dados_plc_atualizados = await buscar_dados_clima()
        await asyncio.sleep(90)  # Atualiza a cada 90 segundos


async def plc_handler(websocket, path):
    global dados_plc_atualizados
    client_ip = websocket.remote_address[0]
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Novo cliente conectado: {client_ip} em {timestamp}")

    # Inicia a tarefa de atualização dos dados do PLC em segundo plano
    asyncio.create_task(atualizar_dados_plc())

    try:
        while True:
            mensagem = await websocket.recv()
            if mensagem == "solicitar_dados":
                await websocket.send(json.dumps(dados_plc_atualizados))
    except websockets.ConnectionClosed:
        print(f"Cliente desconectado: {client_ip} em {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

async def main():
    # Inicia o servidor WebSocket
    start_server = websockets.serve(plc_handler, "localhost", 8765)
    print('Servidor rodando em: localhost:8765')

    await start_server
    await asyncio.Future()  # Mantém o servidor rodando indefinidamente

if __name__ == "__main__":
    asyncio.run(main())

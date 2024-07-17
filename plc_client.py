import asyncio
import websockets
import json
import sys
import datetime

async def cliente(intervalo=2):
    while True:
        try:
            async with websockets.connect("ws://localhost:8765") as websocket:
                print("Conectado ao servidor.")
                while True:
                    try:
                        # Solicita os dados do PLC
                        await websocket.send("solicitar_dados")

                        dados_plc = json.loads(await websocket.recv())

                        if "erro" in dados_plc:
                            print(f"Erro: {dados_plc['erro']}")
                        else:
                            # Verifica se as chaves existem
                            if 'main' in dados_plc and 'temp' in dados_plc['main'] and 'humidity' in dados_plc['main']:
                                # Extrai e converte a temperatura
                                temperatura_kelvin = dados_plc['main']['temp']
                                temperatura_celsius = temperatura_kelvin - 273.15
                            
                                # Extrai a umidade
                                umidade = dados_plc['main']['humidity']
                                nome_cidade = dados_plc['name']
                            
                                # Extrai e formata a data e hora (timezone UTC)
                                timestamp_utc = dados_plc['dt']
                                data_hora = datetime.datetime.utcfromtimestamp(timestamp_utc).strftime('%Y-%m-%d %H:%M:%S')

                                print(f"Cidade: {nome_cidade}")
                                print(f"Temperatura: {temperatura_celsius:.2f} °C")
                                print(f"Umidade: {umidade}%")
                                print(f"Data e Hora (UTC): {data_hora}")
                            else:
                                print("Dados inválidos recebidos do servidor.")

                    except websockets.WebSocketException as e:
                        print(f"Erro WebSocket: {e}")
                        break

                    await asyncio.sleep(intervalo)
        except ConnectionRefusedError:
            print("Erro: Conexão recusada. Verifique se o servidor está rodando.")
            await asyncio.sleep(5)  # Aguarda 5 segundos antes de tentar reconectar

if __name__ == "__main__":
    intervalo = 2  # Valor padrão
    if len(sys.argv) > 1:
        try:
            intervalo = float(sys.argv[1])
        except ValueError:
            print("Intervalo inválido. Usando o valor padrão de 2 segundos.")

    asyncio.run(cliente(intervalo))

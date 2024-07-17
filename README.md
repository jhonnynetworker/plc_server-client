# Simulação de PLC com WebSocket e Dados Climáticos em Tempo Real

Este projeto oferece uma simulação de um Controlador Lógico Programável (PLC) que se conecta à API OpenWeatherMap para obter dados climáticos em tempo real. A comunicação entre o PLC simulado e os clientes é feita através de um servidor WebSocket, permitindo a atualização dinâmica dos dados nos clientes.

## Funcionalidades

### Servidor PLC (plc_server.py)
- **Busca de dados**: Obtém dados climáticos da API OpenWeatherMap a cada 90 segundos.
- **Servidor WebSocket**: Estabelece um servidor WebSocket para transmitir os dados aos clientes.
- **Registro de atividade**: Registra as conexões e desconexões dos clientes, incluindo seus endereços IP e horários.
- **Atualização automática**: Inicia a busca de dados climáticos imediatamente ao ser iniciado.

### Cliente (plc_client.py)
- **Conexão WebSocket**: Conecta-se ao servidor WebSocket e solicita os dados do PLC.
- **Solicitação inicial**: Realiza uma solicitação de dados imediatamente após a conexão.
- **Solicitações periódicas**: Continua solicitando dados a cada 2 segundos (ou no intervalo especificado).
- **Exibição de dados**: Exibe os seguintes dados climáticos no console:
  - Temperatura (em graus Celsius)
  - Umidade
  - Data e hora (UTC)
  - Nome da cidade
- **Tratamento de erros**: Lida com erros de conexão, erros na resposta da API e dados inválidos.
- **Reconexão automática**: Tenta reconectar automaticamente ao servidor em caso de falha na conexão.

## Pré-requisitos

- **Python 3.7+**: Certifique-se de ter o Python 3.7 ou superior instalado.
- **Bibliotecas**:
  - `websockets`
  - `aiohttp`
  - `json`
  - `datetime`
- **Chave de API do OpenWeatherMap**: Obtenha uma chave de API gratuita no site do OpenWeatherMap e insira-a no arquivo `plc_server.py` (substitua o valor de `API_KEY`).

## Como executar

### Servidor:
1. Abra um terminal e execute `python plc_server.py`. O servidor iniciará e começará a buscar dados climáticos.

### Cliente:
1. Abra outro terminal e execute `python plc_client.py`. O cliente se conectará ao servidor e exibirá os dados climáticos.

## Personalização

- **Cidade**: Modifique a variável `ENDPOINT` no arquivo `plc_server.py` para especificar a cidade desejada.
- **Intervalo de atualização**: Altere o valor da variável `intervalo` no arquivo `plc_client.py` para ajustar a frequência de solicitação dos dados.

## Observações

- Certifique-se de ter as bibliotecas necessárias instaladas (`pip install websockets aiohttp`).
- Este projeto é uma simulação e não se destina a ser usado em ambientes de produção críticos.
- Em um ambiente de produção, considere adicionar medidas de segurança, como autenticação e criptografia.

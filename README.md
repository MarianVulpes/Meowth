# Meowth
Meowth é um script para extrair a cotação atual de cryptomoedas principalmente da Binance (e em segundos casos da ByBit) e atualizar a base de dados de um banco no Firebird. O programa tem um intervalo de tempo antes de fazer um Update automático (estipulado no arquivo config.json que é possivel modificar) e um botão Update na interface gráfica para atualizar imediatamente e reiniciar a contagem. 

## Modo de Uso
- Use o arquivo config.json para modificar as credenciais do banco de dados e o intervalo de tempo entre Update automáticos:
```
{
    "database": "", --> Caminho para o .fdb
    "user": "", --> Usuário (padrão é sysdba)
    "password": "", --> Senha (padrão é masterkey)
    "host": "", --> localhost (na maioria das vezes)
    "port": 3050,
    "refresh_interval": 1 --> Intervalo de tempo (em minutos, 1 = 1 minuto)
}
```
- Coloque os códigos completos das cryptos (não o Ticker) no arquivo cryptos.json. Ex: "BTCUSDT" (Bitcoin em Dollar)



Direitos de Som e Imagem Pokémon. © 1995–2024 Nintendo/Creatures Inc./GAME FREAK inc.

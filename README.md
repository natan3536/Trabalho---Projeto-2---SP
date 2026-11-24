# Projeto 2 - Segurança e Privacidade (PSI)

Repositório criado para partilhar os datasets e os scripts da Fase 2 do projeto de SP (Private Set Intersection).

## 1. Geração dos Dados

O ficheiro `generate_datasets.py` serve para criar as bases de dados das duas entidades que escolhemos: **Hospital** e **Seguradora de Saúde**.

- O identificador usado é o número de utente (uma linha por registo).
- O script usa uma `seed` fixa para garantir a reprodutividade.
- Cria logo as 5 versões (5k, 10k, 20k, 30k e 40k), já com 10% de dados em comum entre as entidades.
- Os ficheiros finais ficam guardados dentro da pasta `dataset/`.

# 1.1 Cenário e Problema

O caso de uso escolhido é o cruzamento de dados entre um **Hospital** e uma **Seguradora de Saúde**.

- **Problema:** A seguradora precisa de saber quais dos seus clientes também são pacientes do hospital para análise de histórico e avaliação de risco. Por outro lado, por questões de privacidade e RGPD, o hospital não pode partilhar a lista de todos os seus doentes, nem a seguradora pode expor a sua carteira de clientes.
- **Solução com PSI:** O protocolo permite que ambas as entidades descubram apenas os utentes em comum (a interseção), sem revelarem nada sobre os restantes clientes ou pacientes que não coincidem.

Para gerar ou atualizar as bases basta correr:
```bash
python generate_datasets.py
```

Relatório em world na pasta compartilhada pelo onedrive

## 2. Como Rodar no demo.exe
Para testar os protocolos abrem-se dois terminais (um para cada entidade).

Exemplo:
Terminal 1:
./demo.exe -r 0 -p 0 -f dataset/hospital_5k.txt

Terminal 2 :
./demo.exe -r 1 -p 0 -f dataset/seguradora_5k.txt

Notas rápidas:

Protocolos (-p):
    0: Naive Hashing
    1: Server-aided
    2: Diffie-Hellman
    3: Oblivious Transfer (OT)
### Medição do tempo e do tráfego

Em cada execução usam-se 3 terminais (4 no server-aided), todos com:
```bash
cd ~/PSI-master
D=~/Trabalho---Projeto-2---SP/dataset
```

Substituir `<P>` pelo protocolo (0, 1, 2 ou 3) e `<N>` pelo tamanho (5k, 10k, 20k, 30k ou 40k).

Naive, DH e OT (-p 0, 2, 3):
```bash
# Terminal 1 - captura
sudo tcpdump -i lo -B 131072 -w p<P>_<N>.pcap tcp port 7766
# Terminal 2 - hospital
./demo.exe -r 0 -p <P> -f $D/hospital_<N>.txt > /dev/null
# Terminal 3 - seguradora
time ./demo.exe -r 1 -p <P> -f $D/seguradora_<N>.txt | grep Found
```

Server-aided (-p 1):
```bash
# Terminal 1 - captura
sudo tcpdump -i lo -B 131072 -w p1_<N>.pcap tcp port 7766
# Terminal 2 - servidor
./demo.exe -r 0 -p 1 -f README.md > /dev/null
# Terminal 3 - hospital
time ./demo.exe -r 1 -p 1 -f $D/hospital_<N>.txt | grep Found
# Terminal 4 - seguradora
time ./demo.exe -r 1 -p 1 -f $D/seguradora_<N>.txt | grep Found
```

No fim, Ctrl+C no Terminal 1.

Notas:
- O tempo é o valor `real` do `time` (o `demo.exe` não mostra o tempo).
- No server-aided usa-se o tempo do último cliente a arrancar.
- No DH e no OT só o `-r 1` mostra a interseção.
- O `-B 131072` evita que se percam pacotes nos tamanhos maiores.

## 3. Resultados

Na pasta `resultados_demo/`:

- `dados_demo.csv`: tempo, pacotes, bytes e interseção de cada execução
- `grafico_tempo.png`, `grafico_tempo_log.png`, `grafico_trafego.png`: gráficos
- `capturas/`: as 20 capturas `.pcap`

Pacotes e bytes de todas as capturas:
```bash
capinfos -T -c -d p?_*k.pcap
```

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
# Demonstração NoSQL com MongoDB Atlas (Python)

Este repositório contém um script simples para uma apresentação sobre Modelagem de Dados NoSQL usando MongoDB Atlas.

O objetivo é demonstrar, de forma prática e didática, operações básicas e recursos comuns do MongoDB com Python:

- Conexão ao Atlas via `pymongo`
- Inserção (`insert_one`, `insert_many`)
- Consulta (`find`, `find_one`), projeção e contagem
- Atualização (`update_one`, `update_many`)
- Exclusão (`delete_one`)
- Indexação (`create_index`)
- Agregação (`aggregate`)

Arquivos:
- `mongodb_demo.py`: script de demonstração (exemplo comentado).
- `requirements.txt`: dependências.

Como usar

1. Instale dependências:

```bash
python -m pip install -r requirements.txt
```

2. Configure a URI de conexão do MongoDB Atlas. É recomendado usar a variável de ambiente `MONGODB_URI`:

```bash
export MONGODB_URI="mongodb+srv://arthursouza:<PASSWORD>@arthur.ui40ak0.mongodb.net/?appName=Arthur"
```

Substitua `<PASSWORD>` pela sua senha. Se preferir, você pode editar diretamente a variável `DEFAULT_URI` no `mongodb_demo.py`, mas prefira variáveis de ambiente para não expor credenciais.

3. Execute o script:

```bash
python mongodb_demo.py
```

Notas importantes sobre o exemplo
- **Campos extras nos exemplos:** os documentos de demonstração (`Alice`, `Bob`, `Charlie`) incluem agora dois campos não-relacionais para fins didáticos:
    - `url`: um link representativo (ex.: `https://www.mongodb.com/pt-br`)
    - `file`: nome/identificador de um PNG (ex.: `foto_perfil.png`)
    Esses campos demonstram como o MongoDB aceita formatos flexíveis dentro de documentos.

4. Execução automatizada (útil para demonstração/seed):

Se quiser inserir os dados de demonstração automaticamente e pular os prompts interativos, use um comando `printf` para alimentar respostas não interativas. Exemplos:

```bash
# usando Python do sistema
export MONGODB_URI="mongodb+srv://usuario:SUASENHA@cluster.mongodb.net/?appName=Demo"
printf 'n\n\n' | python mongodb_demo.py --seed-only

# se estiver usando o virtualenv do workspace (recomendado dentro deste devcontainer)
export MONGODB_URI="mongodb+srv://usuario:SUASENHA@cluster.mongodb.net/?appName=Demo"
printf 'n\n\n' | /workspaces/ModelagemPr-tica/.venv/bin/python mongodb_demo.py --seed-only
```

O `printf 'n\n\n'` responde `n` à pergunta de inserir link/PNG e envia Enter na prática interativa, pulando ambas.

5. Dependências e ambiente
- O driver Python usado é `pymongo` (lista em `requirements.txt`). Instale as dependências com:

```bash
python -m pip install -r requirements.txt
# ou, se usar o venv criado no devcontainer:
/workspaces/ModelagemPr-tica/.venv/bin/python -m pip install -r requirements.txt
```

6. Limpeza de dados de teste
Para remover os documentos de demonstração inseridos (ex.: apagar todos com `name` em [Alice,Bob,Charlie]), você pode executar um pequeno script Python ou usar o Atlas UI. Exemplo rápido (Python):

```python
from pymongo import MongoClient
import os
client = MongoClient(os.environ['MONGODB_URI'])
db = client.get_database('presentation_db')
coll = db.get_collection('students')
coll.delete_many({'name': {'$in': ['Alice','Bob','Charlie']}})
client.close()
```


Observações
- Por padrão, o script **não remove mais automaticamente** a coleção usada na demonstração. Os dados inseridos permanecem disponíveis para consulta no Atlas Data Explorer após a execução.
- Se desejar remover manualmente a coleção, descomente a linha `collection.drop()` no final do arquivo `mongodb_demo.py`.
- Para demonstrar os registros no Atlas Data Explorer (aba "Data"/"Collections") você pode preservar os dados em vez de removê-los. Há duas opções:
    - Rodar o script em modo "seed only" (insere os documentos e sai):

        ```bash
        export MONGODB_URI="mongodb+srv://arthursouza:SUASENHA@arthur.ui40ak0.mongodb.net/?appName=Arthur"
        python mongodb_demo.py --seed-only
        ```

    - Rodar o script normalmente, mas preservando a coleção (não dropar) usando `--preserve`:

        ```bash
        export MONGODB_URI="mongodb+srv://arthursouza:SUASENHA@arthur.ui40ak0.mongodb.net/?appName=Arthur"
        python mongodb_demo.py --preserve
        ```

    Depois de inserir os dados (por qualquer uma das opções acima), abra o MongoDB Atlas web UI:

    1. Acesse https://cloud.mongodb.com e entre com sua conta.
    2. Selecione o projeto e o cluster usado na conexão.
    3. Clique em `Collections` (ou `Data` > `Collections`).
    4. No painel da esquerda procure o database `presentation_db` e a coleção `students`.
    5. Clique na coleção para ver os documentos insertados. Use o botão `Refresh` se necessário.

    Observações sobre acesso:
    - Certifique-se de que o IP do ambiente onde você está rodando (se não for a própria interface do Atlas) esteja liberado nas `Network Access` (IP Whitelist) do projeto Atlas, ou habilite 0.0.0.0/0 temporariamente para demonstração (não recomendado em produção).
    - Verifique se o usuário na URI tem permissões adequadas para inserir e listar dados.
- Se a rede do container/ambiente não permitir acesso ao Atlas, execute localmente em sua máquina.

Licença e segurança
- Não inclua credenciais em repositórios públicos. Use variáveis de ambiente ou ferramentas de segredo.
# ModelagemPr-tica
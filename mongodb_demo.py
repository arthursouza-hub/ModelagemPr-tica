#!/usr/bin/env python3
"""
mongodb_demo.py

Script didático para apresentação de Modelagem NoSQL com MongoDB Atlas.

Funcionalidades mostradas:

Configure a variável de ambiente `MONGODB_URI` com sua string de conexão.
"""
"""
mongodb_demo.py

Script didático para apresentação de Modelagem NoSQL com MongoDB Atlas.

Este arquivo contém exemplos práticos (e comentados) para estudantes que
vêm de bancos relacionais (SQL) e querem entender os conceitos básicos
do MongoDB (NoSQL orientado a documentos).

Principais diferenças e anotações pedagógicas:
- Em bancos relacionais usamos tabelas, linhas e colunas. No MongoDB
    usamos *databases* -> *collections* -> *documents* (documentos JSON-like).
- Consultas simples (SELECT) correspondem a `find()`/`find_one()`.
- Inserts (INSERT INTO) correspondem a `insert_one()`/`insert_many()`.
- Atualizações (UPDATE) usam operadores como `$set`, `$inc` (semelhante a SQL
    `UPDATE ... SET col = col + 1`).
- Agregação em SQL (GROUP BY, JOIN) é feita com pipelines de agregação (`aggregate`).
- Índices funcionam de forma similar (melhoram buscas) — `create_index`.

Coloque sua string de conexão no env `MONGODB_URI` antes de rodar.
"""
from pprint import pprint
import os
import sys
import argparse
import base64
import gridfs
from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError


DEFAULT_URI = "mongodb+srv://arthursouza:Lu-300898@arthur.ui40ak0.mongodb.net/?appName=Arthur"

 
def get_client():
    # Esta função retorna um cliente conectado ao MongoDB Atlas.
    # Ela usa a URI definida na variável de ambiente MONGODB_URI ou um valor padrão.
    uri = os.environ.get("MONGODB_URI", DEFAULT_URI)
    # Validação simples da URI: verifica se não há placeholder e se tem formato correto.
    if "<" in uri or "PASSWORD" in uri or ("://" not in uri) or ("@" not in uri):
        print("\nATENÇÃO: A URI padrão contém um placeholder. Defina a variável de ambiente `MONGODB_URI` com sua conexão Atlas antes de rodar.")
        print("Exemplo (bash): export MONGODB_URI='mongodb+srv://user:senha@cluster0.mongodb.net/?appName=Demo'\n")
        sys.exit(1)

    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    try:
        # Testa a conexão com o banco (ping).
        client.admin.command("ping")
    except ServerSelectionTimeoutError as e:
        print("Erro ao conectar ao MongoDB Atlas:", e)
        sys.exit(1)
    return client


def demo_crud(collection):
    # ===============================
    # PRÁTICA EXTRA: INSERINDO LINK E PNG
    # ===============================
    # Você pode preencher os dados manualmente (editando o exemplo abaixo) OU via terminal (input).
    # Escolha uma das opções:
    #
    # Opção 1: Preencher manualmente (edite os valores abaixo e descomente)
    # manual_link_doc = {
    #     "name": "Site de Estudos",
    #     "url": "https://www.mongodb.com/pt-br"
    # }
    # manual_png_doc = {
    #     "name": "Imagem do Aluno",
    #     "file": "foto_perfil.png"  # pode ser o nome, caminho ou até um link para o arquivo
    # }
    # res_link = collection.insert_one(manual_link_doc)
    # print(f"Documento com link inserido: {res_link.inserted_id}")
    # print(collection.find_one({"_id": res_link.inserted_id}))
    # res_png = collection.insert_one(manual_png_doc)
    # print(f"Documento com PNG inserido: {res_png.inserted_id}")
    # print(collection.find_one({"_id": res_png.inserted_id}))
    #
    # Opção 2: Preencher via terminal (input)
    escolha = input("Deseja inserir dados de link/PNG via terminal? (s/n): ").strip().lower()
    if escolha == "s":
        link_nome = input("Digite o nome do site/link: ").strip()
        link_url = input("Digite a URL: ").strip()
        png_nome = input("Digite o nome da imagem: ").strip()
        png_file = input("Digite o nome/caminho do arquivo PNG: ").strip()
        if link_nome and link_url:
            link_doc = {"name": link_nome, "url": link_url}
            res_link = collection.insert_one(link_doc)
            print(f"Documento com link inserido: {res_link.inserted_id}")
            print(collection.find_one({"_id": res_link.inserted_id}))
        if png_nome and png_file:
            png_doc = {"name": png_nome, "file": png_file}
            res_png = collection.insert_one(png_doc)
            print(f"Documento com PNG inserido: {res_png.inserted_id}")
            print(collection.find_one({"_id": res_png.inserted_id}))
    # ===============================
    # EXEMPLOS AUTOMÁTICOS DE FORMATOS DE LINK/IMAGEM
    # ===============================
    print("\n--- Exemplos automáticos: URL pública, arquivo local, Data URI e GridFS (mock) ---")
    try:
        # 1) URL pública
        doc_url = {
            "name": "Example_URL",
            "url_name": "MongoDB - Página Principal",
            "url": "https://www.mongodb.com/pt-br"
        }
        r1 = collection.insert_one(doc_url)
        print("Inserted Example_URL id:", r1.inserted_id)

        # 2) Nome de arquivo local (referência)
        doc_local = {
            "name": "Example_LocalFile",
            "file_name": "Foto Perfil Local",
            "file": "foto_perfil_local.png"
        }
        r2 = collection.insert_one(doc_local)
        print("Inserted Example_LocalFile id:", r2.inserted_id)

        # 3) Data URI (base64) - pequeno PNG 1x1 transparente
        tiny_png_b64 = (
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAASsJTYQAAA" 
            "AASUVORK5CYII="
        )
        data_uri = "data:image/png;base64," + tiny_png_b64
        doc_datauri = {
            "name": "Example_DataURI",
            "file_name": "Tiny PNG embedded",
            "file": data_uri
        }
        r3 = collection.insert_one(doc_datauri)
        print("Inserted Example_DataURI id:", r3.inserted_id)

        # 4) GridFS mock: armazena bytes pequenos em GridFS e referencia o id retornado
        fs = gridfs.GridFS(collection.database)
        png_bytes = base64.b64decode(tiny_png_b64)
        gridfs_id = fs.put(png_bytes, filename="tiny.png", contentType="image/png")
        doc_gridfs = {
            "name": "Example_GridFS",
            "file_name": "Tiny PNG in GridFS",
            "file": {"gridfs_id": gridfs_id}
        }
        r4 = collection.insert_one(doc_gridfs)
        print("Inserted Example_GridFS id:", r4.inserted_id)

        # Mostrar documentos inseridos de exemplo
        for _id in (r1.inserted_id, r2.inserted_id, r3.inserted_id, r4.inserted_id):
            print("Documento exemplo:")
            pprint(collection.find_one({"_id": _id}))
    except Exception as e:
        print("Erro ao inserir exemplos automáticos:", e)
    # ===============================
    # PRÁTICA INTERATIVA
    # ===============================
    # Esta parte permite que qualquer pessoa, mesmo iniciante, insira um documento personalizado.
    # Basta seguir as instruções do terminal e preencher os campos solicitados.
    print("\n--- Prática: insira um novo estudante manualmente ---")
    # O objetivo é mostrar que o MongoDB aceita documentos com diferentes campos e formatos.
    try:
        # O usuário pode digitar o nome do estudante. Se pressionar Enter sem digitar nada, a prática é pulada.
        nome = input("Digite o nome do estudante (ou pressione Enter para pular): ").strip()
        if nome:
            # Solicita a idade (opcional, só será incluída se for um número).
            idade = input("Digite a idade: ").strip()
            # Solicita os cursos, separados por vírgula (ex: Matematica, Física).
            cursos = input("Digite os cursos separados por vírgula: ").strip()
            # Transforma a string dos cursos em uma lista, ignorando espaços extras.
            cursos_lista = [c.strip() for c in cursos.split(",") if c.strip()]
            # Monta o novo documento para inserir no MongoDB.
            novo_doc = {"name": nome}
            if idade.isdigit():
                novo_doc["age"] = int(idade)
            if cursos_lista:
                novo_doc["courses"] = cursos_lista
            # Insere o documento na coleção.
            res = collection.insert_one(novo_doc)
            print(f"Novo estudante inserido com _id: {res.inserted_id}")
            print("Documento inserido:")
            pprint(collection.find_one({"_id": res.inserted_id}))
            # Dica: experimente inserir diferentes campos ou valores para ver como o MongoDB aceita formatos variados.
            # Exemplo: tente inserir um campo extra, como "email" ou "notas".
        else:
            print("Prática pulada. Nenhum estudante inserido.")
            # Se não digitar nada, o código segue normalmente sem erro.
    except Exception as e:
        print("Erro na prática interativa:", e)
        # Se ocorrer algum erro, uma mensagem amigável será exibida.
    # ===============================
    # INSERÇÃO DE DOCUMENTOS
    # ===============================
    # Em bancos relacionais, seria equivalente a INSERT INTO students (...)
    print("\n--- Inserções (insert_one / insert_many) ---")
    # Documentos no MongoDB são dicionários Python (JSON-like). Cada documento pode ter formato diferente — isso é flexível (schema-less).
    # Campos de link e imagem embutidos explicitamente em cada aluno
    alice = {
        "name": "Alice",
        "age": 24,
        "courses": ["Math", "Physics"],
        "url": "https://www.mongodb.com/pt-br",
        "file": "foto_perfil.png"
    }
    bob = {
        "name": "Bob",
        "age": 29,
        "address": {"city": "São Paulo", "zip": "01000-000"},
        "url": "https://www.mongodb.com/pt-br",
        "file": "foto_perfil.png"
    }
    charlie = {
        "name": "Charlie",
        "age": 24,
        "visits": 1,
        "url": "https://www.mongodb.com/pt-br",
        "file": "foto_perfil.png"
    }

    # Insere um documento individualmente.
    res = collection.insert_one(alice)
    print("Inserted Alice id:", res.inserted_id)
    # Insere múltiplos documentos de uma vez.
    res_many = collection.insert_many([bob, charlie])
    print("Inserted many ids:", res_many.inserted_ids)

    # ===============================
    # CONSULTA DE DOCUMENTOS
    # ===============================
    # Equivalente ao SELECT em SQL.
    print("\n--- Consulta (find_one / find) ---")
    # find_one({}) retorna o primeiro documento que bater com o filtro (aqui vazio, retorna qualquer um).
    one = collection.find_one({})
    print("find_one (primeiro documento encontrado):")
    pprint(one)

    # find({}) retorna todos os documentos que batem com o filtro (aqui, todos).
    print("\nfind all documents:")
    for doc in collection.find({}):
        pprint(doc)

    # count_documents é equivalente a SELECT COUNT(*) WHERE ...
    print("\ncount documents where age == 24:", collection.count_documents({"age": 24}))

    # ===============================
    # ATUALIZAÇÃO DE DOCUMENTOS
    # ===============================
    print("\n--- Atualizações (update_one / update_many) ---")
    # update_one: altera apenas o primeiro documento que bate com o filtro.
    # Operadores como $inc (incrementa valor) e $set (define valor) permitem alterar campos específicos sem afetar o resto do documento.
    update_res = collection.update_one({"name": "Charlie"}, {"$inc": {"visits": 5}, "$set": {"active": True}})
    print("matched:", update_res.matched_count, "modified:", update_res.modified_count)

    # update_many: altera todos os documentos que batem com o filtro.
    update_many_res = collection.update_many({"age": 24}, {"$set": {"cohort": "2025"}})
    print("update_many matched:", update_many_res.matched_count)

    # ===============================
    # ÍNDICES
    # ===============================
    print("\n--- Index (create_index) ---")
    # Índices aceleram buscas, assim como em bancos relacionais.
    # Aqui criamos um índice crescente no campo 'name'.
    idx = collection.create_index([("name", 1)])
    print("Created index:", idx)
    print("Indexes now:")
    pprint(list(collection.list_indexes()))

    # ===============================
    # AGREGAÇÃO (ANÁLISE DE DADOS)
    # ===============================
    print("\n--- Agregação (aggregate) ---")
    # O pipeline abaixo faz uma análise dos cursos dos estudantes.
    pipeline = [
        # $unwind: transforma arrays em múltiplos documentos (similar a normalização em SQL).
        {"$unwind": {"path": "$courses", "preserveNullAndEmptyArrays": True}},
        # $group: agrupa por curso e conta quantos estudantes aparecem em cada.
        {"$group": {"_id": "$courses", "count": {"$sum": 1}}},
        # $sort: ordena do maior para o menor.
        {"$sort": {"count": -1}}
    ]
    print("Pipeline:")
    pprint(pipeline)
    print("Results:")
    for doc in collection.aggregate(pipeline):
        pprint(doc)

    # ===============================
    # EXCLUSÃO DE DOCUMENTOS
    # ===============================
    print("\n--- Exclusão (delete_one) ---")
    # delete_one: remove o primeiro documento que bate com o filtro.
    del_res = collection.delete_one({"name": "Bob"})
    print("deleted_count:", del_res.deleted_count)


def print_db_info(client, db_name, collection_name, sample_n=3):
    """Mostra informações simples do banco e coleção para que o apresentador possa checar no Atlas Data Explorer."""
    db = client.get_database(db_name)
    coll = db.get_collection(collection_name)
    print("\n--- Informações do Banco/coleção ---")
    try:
        # lista coleções
        cols = db.list_collection_names()
        print(f"Database: {db_name}")
        print("Collections:", cols)
        count = coll.count_documents({})
        print(f"Document count na coleção '{collection_name}': {count}")
        print(f"Mostrando até {sample_n} documentos de exemplo:")
        for i, doc in enumerate(coll.find({}).limit(sample_n), start=1):
            print(f"\n--- Documento {i} ---")
            pprint(doc)
    except Exception as e:
        print("Erro ao obter informações do banco/coleção:", e)


def main():
    parser = argparse.ArgumentParser(description="Script demo MongoDB para apresentação (CRUD, index, agregação)")
    parser.add_argument("--preserve", action="store_true", help="Preserva a coleção após execução (não faz collection.drop())")
    parser.add_argument("--seed-only", action="store_true", help="Insere os documentos de demonstração e sai (útil para ver no Atlas Data Explorer)")
    parser.add_argument("--show", action="store_true", help="Mostra informações do banco/coleção antes de dropar/preservar")
    args = parser.parse_args()

    client = get_client()
    db_name = "presentation_db"
    coll_name = "students"
    db = client.get_database(db_name)
    collection = db.get_collection(coll_name)

    try:
        if args.seed_only:
            # Apenas insere dados de demonstração e sai
            print("Executando em modo --seed-only: inserindo documentos de demonstração e encerrando...")
            demo_crud(collection)
            print("Seed concluído. Saindo (coleção preservada).\n")
            return

        # Executa demonstração completa
        demo_crud(collection)

        if args.show:
            print_db_info(client, db_name, coll_name)

        print("\nDemonstração concluída.")
        if args.preserve:
            print("--preserve ativado: a coleção será mantida para visualização no Atlas Data Explorer.")
        else:
            # Remoção automática desativada por padrão para preservar dados de demonstração.
            print("Remoção automática desativada: coleção preservada por padrão.")
            # collection.drop()  # comentado para preservar dados por padrão

    finally:
        client.close()


if __name__ == "__main__":
    main()

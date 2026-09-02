import pandas as pd
import json
from core.utils import clean_float, clean_dict
from config.settings import EXCEL_DTYPES

def process_excel(file) -> list:
    """
    Lê um arquivo Excel e o converte para uma lista de strings NDJSON.
    """
    df = pd.read_excel(file, dtype=EXCEL_DTYPES)
    ndjson_lines = []
    
    for index, row in df.iterrows():
        item = process_row(row)
        ndjson_lines.append(json.dumps(item, ensure_ascii=False))
        
    return ndjson_lines

def process_row(row) -> dict:
    """
    Processa uma linha do DataFrame e retorna o dicionário estruturado.
    """
    dados_gerais = {
        "inscricaoImobiliaria": row.get("inscricaoImobiliaria"),
        "tipoImovel": int(row.get("tipoImovel")) if pd.notna(row.get("tipoImovel")) else None,
        "tpArquitetonico": int(row.get("tpArquitetonico")) if pd.notna(row.get("tpArquitetonico")) else None,
        "destinacaoImovel": int(row.get("destinacaoImovel")) if pd.notna(row.get("destinacaoImovel")) else None,
        "areaTerreno": clean_float(row.get("areaTerreno")),
        "areaConstruida": clean_float(row.get("areaConstruida")),
        "anoConstrutivo": int(row.get("anoConstrutivo")) if pd.notna(row.get("anoConstrutivo")) else None,
        "temBairro": bool(row.get("temBairro")) if pd.notna(row.get("temBairro")) else None
    }
    
    endereco_imovel = {
        "tipoLogradouro": int(row.get("tipoLogradouro")) if pd.notna(row.get("tipoLogradouro")) else None,
        "nomeLogradouro": row.get("nomeLogradouro") if pd.notna(row.get("nomeLogradouro")) else None,
        "numeroImovel": row.get("numeroImovel") if pd.notna(row.get("numeroImovel")) else None,
        "bairro": row.get("bairro") if pd.notna(row.get("bairro")) else None,
        "cep": row.get("cep") if pd.notna(row.get("cep")) else None
    }
    
    titular = [
        {
            "niTitular": row.get("niTitular") if pd.notna(row.get("niTitular")) else None,
            "nomeTitular": row.get("nomeTitular") if pd.notna(row.get("nomeTitular")) else None
        }
    ]
    
    dados_gerais = clean_dict(dados_gerais)
    endereco_imovel = clean_dict(endereco_imovel)
    
    item = {
        "ui": {
            "DadosGeraisImovel": dados_gerais,
            "EnderecoImovel": endereco_imovel,
            "Titular": titular
        },
        "operacao": "I"
    }
    
    return item

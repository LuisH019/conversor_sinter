import io
import zipfile

def create_zip_buffer(file_name: str, content: str) -> io.BytesIO:
    """
    Cria um buffer de memória contendo um arquivo zip com o conteúdo fornecido.
    """
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr(file_name, content.encode('utf-8'))
    return zip_buffer

def create_zip_buffer_multiple(files: dict) -> io.BytesIO:
    """
    Cria um buffer de memória contendo um arquivo zip com múltiplos arquivos.
    :param files: dicionário com o nome do arquivo como chave e o conteúdo (string) como valor.
    """
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file_name, content in files.items():
            zip_file.writestr(file_name, content.encode('utf-8'))
    return zip_buffer

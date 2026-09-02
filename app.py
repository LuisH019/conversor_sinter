import streamlit as st
from config.settings import PAGE_TITLE, LAYOUT, HEADER_TITLE, HEADER_DESC, MAX_UPLOAD_FILES
from core.processor import process_excel
from core.exporter import create_zip_buffer, create_zip_buffer_multiple

def main():
    st.set_page_config(page_title=PAGE_TITLE, layout=LAYOUT)
    st.title(HEADER_TITLE)
    st.write(HEADER_DESC)

    uploaded_files = st.file_uploader(
        f"Escolha os arquivos Excel (máx {MAX_UPLOAD_FILES})", 
        type=["xlsx"], 
        accept_multiple_files=True
    )
    zip_download = st.checkbox("Compactar arquivos gerados em .zip individualmente")

    if uploaded_files:
        if len(uploaded_files) > MAX_UPLOAD_FILES:
            st.warning(f"⚠️ Você selecionou mais de {MAX_UPLOAD_FILES} arquivos. Apenas os {MAX_UPLOAD_FILES} primeiros serão processados.")
            uploaded_files = uploaded_files[:MAX_UPLOAD_FILES]
            
        processed_files_dict = {}

        for uploaded_file in uploaded_files:
            with st.spinner(f"Processando {uploaded_file.name}..."):
                try:
                    ndjson_lines = process_excel(uploaded_file)
                    ndjson_content = "\n".join(ndjson_lines)
                    
                    st.success(f"✅ Arquivo {uploaded_file.name} processado com sucesso! ({len(ndjson_lines)} registros gerados)")
                    
                    base_name = uploaded_file.name.rsplit('.', 1)[0]
                    ndjson_file_name = f"{base_name}.ndjson"
                    
                    # Guarda o conteúdo para o zip final
                    processed_files_dict[ndjson_file_name] = ndjson_content
                    
                    if zip_download:
                        zip_buffer = create_zip_buffer(ndjson_file_name, ndjson_content)
                        zip_file_name = f"{base_name}.zip"
                        
                        st.download_button(
                            label=f"⬇️ Baixar {zip_file_name}",
                            data=zip_buffer.getvalue(),
                            file_name=zip_file_name,
                            mime="application/zip",
                            key=f"download_zip_{uploaded_file.name}"
                        )
                    else:
                        st.download_button(
                            label=f"⬇️ Baixar {ndjson_file_name}",
                            data=ndjson_content,
                            file_name=ndjson_file_name,
                            mime="application/x-ndjson",
                            key=f"download_{uploaded_file.name}"
                        )
                    
                except Exception as e:
                    st.error(f"❌ Ocorreu um erro ao processar a planilha {uploaded_file.name}: {e}")

        # Se houver mais de 1 arquivo processado com sucesso, mostra o botão para baixar todos
        if len(processed_files_dict) > 1:
            st.markdown("---")
            st.subheader("📦 Baixar todos os arquivos")
            all_zip_buffer = create_zip_buffer_multiple(processed_files_dict)
            st.download_button(
                label="⬇️ Baixar todos em um único .zip",
                data=all_zip_buffer.getvalue(),
                file_name="todos_arquivos_ndjson.zip",
                mime="application/zip",
                key="download_all_zip"
            )

if __name__ == "__main__":
    main()
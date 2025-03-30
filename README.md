Web Scraping e Transformação de Dados - Teste de Entrada
Este projeto foi desenvolvido como parte de um teste. 
O objetivo do script é realizar o download de arquivos PDF de uma página web, extrair tabelas desses PDFs, substituir abreviações nos dados extraídos, salvar as informações em um arquivo CSV, e compactar esse arquivo em um arquivo ZIP.

Funcionalidades
Download de PDFs: O script acessa uma página web e faz o download de links de arquivos PDF.

Extração de Dados: A partir dos PDFs baixados, o script utiliza a biblioteca pdfplumber para extrair as tabelas contidas neles.

Substituição de Abreviações: Algumas abreviações nos dados extraídos são substituídas por seus significados completos usando um dicionário predefinido.

Salvamento em CSV: Os dados extraídos e transformados são salvos em um arquivo CSV.

Compactação em ZIP: O arquivo CSV gerado é compactado em um arquivo ZIP.

Registro de Logs: O script gera logs informando o status de cada etapa do processo, incluindo erros e sucesso.

Tecnologias Utilizadas
Python 3: Linguagem utilizada para o desenvolvimento do script.

requests: Para realizar requisições HTTP e fazer o download dos arquivos PDF.

BeautifulSoup: Para parsear o conteúdo HTML da página web e encontrar links de arquivos PDF.

pdfplumber: Para extrair tabelas dos arquivos PDF.

csv: Para salvar os dados extraídos em formato CSV.

zipfile: Para compactar o arquivo CSV em formato ZIP.

logging: Para gerar logs durante o processo.

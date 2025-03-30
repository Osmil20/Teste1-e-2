import os
import csv
import zipfile
import pdfplumber
import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def download_pdf(pdf_url, save_path):
    try:
        logging.info(f"Baixando o PDF: {pdf_url}")
        response = requests.get(pdf_url)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            f.write(response.content)
        logging.info(f"PDF salvo em: {save_path}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao baixar o PDF de {pdf_url}: {e}")
        raise


def find_pdf_links(url):
    try:
        logging.info(f"Acessando o site: {url}")
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        pdf_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if 'pdf' in href.lower():
                pdf_links.append(href)

        if not pdf_links:
            logging.warning("Nenhum link de PDF encontrado.")
        return pdf_links
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao acessar o site {url}: {e}")
        raise


def extract_table_from_pdf(pdf_path):
    try:
        logging.info(f"Iniciando extração dos dados do PDF: {pdf_path}")
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"Arquivo {pdf_path} não encontrado.")

        with pdfplumber.open(pdf_path) as pdf:
            all_rows = []
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    all_rows.extend(table[1:])

        logging.info(
            f"Extração concluída com sucesso. Total de {len(all_rows)} linhas extraídas.")
        return all_rows
    except Exception as e:
        logging.error(f"Erro ao extrair dados do PDF: {e}")
        raise


def replace_abbreviations_in_data(data):
    abbreviation_dict = {
        "OD": "Oftalmologia Diagnóstica",
        "AMB": "Ambulatório"
    }
    for i, row in enumerate(data):
        data[i] = [abbreviation_dict.get(cell, cell) for cell in row]
    return data


def save_to_csv(data, csv_filename):
    try:
        logging.info(f"Salvando dados em CSV: {csv_filename}")
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        logging.info(f"Arquivo CSV salvo como: {csv_filename}")
    except Exception as e:
        logging.error(f"Erro ao salvar CSV: {e}")
        raise


def zip_csv(csv_filename, zip_filename):
    try:
        logging.info(f"Compactando o CSV em {zip_filename}")
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            zipf.write(csv_filename, os.path.basename(csv_filename))
        logging.info(f"Arquivo ZIP criado: {zip_filename}")
    except Exception as e:
        logging.error(f"Erro ao compactar CSV: {e}")
        raise


def main():
    try:
        url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
        pdf_links = find_pdf_links(url)

        if len(pdf_links) < 2:
            logging.warning("Não foram encontrados PDFs suficientes.")
            return

        pdf_files = []
        for i, pdf_link in enumerate(pdf_links[:2][::-1]):
            if not pdf_link.startswith("http"):
                pdf_link = "https://www.gov.br" + pdf_link
            pdf_file_name = f"Anexo_{i+1}.pdf"
            download_pdf(pdf_link, pdf_file_name)
            pdf_files.append(pdf_file_name)

        table_data = extract_table_from_pdf(pdf_files[0])
        table_data = replace_abbreviations_in_data(table_data)

        csv_filename = "dados_rol.csv"
        save_to_csv(table_data, csv_filename)

        zip_filename = f"Teste_{os.getlogin()}.zip"
        zip_csv(csv_filename, zip_filename)

        os.remove(csv_filename)
        logging.info("Processo concluído com sucesso!")

    except Exception as e:
        logging.error(f"Erro durante o processo: {e}")


if __name__ == "__main__":
    main()

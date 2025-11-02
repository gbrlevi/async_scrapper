import asyncio
import aiohttp
import time
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text
import os

# --- Configuração do Banco de Dados ---
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./quotes.db") 

engine = create_engine(DATABASE_URL)
metadata = MetaData()

quotes_table = Table(
    'quotes',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('author', String(255)),
    Column('text', Text),
)

metadata.create_all(engine)
# --------------------------------------

async def fetch_page(session, url):
    """
    Função assíncrona que baixa e extrai dados de uma única URL.
    """
    try:
        async with session.get(url) as response:
            if response.status == 200:
                html = await response.text()
                
                soup = BeautifulSoup(html, 'html.parser')
                
                quotes = soup.find_all('div', class_='quote')
                
                extracted_data = []
                for quote in quotes:
                    text = quote.find('span', class_='text').text
                    author = quote.find('small', class_='author').text
                    
                    extracted_data.append({'author': author, 'text': text})
                
                print(f"Extraídas {len(extracted_data)} citações de {url}")
                return extracted_data
            else:
                return [] 
    except Exception as e:
        print(f"Exceção em {url}: {e}")
        return [] 


async def main():
    """
    Função principal que orquestra as tarefas assíncronas.
    """
    start_time_total = time.time()
    
    base_url = "http://quotes.toscrape.com/page/"
    urls = [f"{base_url}{i}/" for i in range(1, 11)]
    
    tasks = []
    
    async with aiohttp.ClientSession() as session:
        for url in urls:
            tasks.append(fetch_page(session, url))
        
        results = await asyncio.gather(*tasks)

    
    all_quotes_data = [data for sublist in results if sublist for data in sublist]
    
    
    print(f"\nSalvando {len(all_quotes_data)} citações no banco de dados...")
    
    with engine.begin() as connection: 
        connection.execute(quotes_table.insert(), all_quotes_data)
        
    print("Dados salvos com sucesso!")
    print(f"--- Tempo total: {time.time() - start_time_total:.2f}s ---")
    
    for quote in all_quotes_data[:3]:
        print(quote)

    

if __name__ == "__main__":
    asyncio.run(main())
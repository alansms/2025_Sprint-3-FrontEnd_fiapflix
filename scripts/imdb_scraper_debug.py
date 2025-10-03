#!/usr/bin/env python3
"""
Script de Debug para Web Scraping do IMDb
"""

import requests
from bs4 import BeautifulSoup
import json

def debug_imdb_structure():
    """Debug da estrutura atual do IMDb"""
    url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }
    
    try:
        print("🌐 Acessando IMDb Top 250...")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Tamanho da página: {len(response.content)} bytes")
        
        # Procurar por diferentes estruturas
        print("\n🔍 Procurando estruturas...")
        
        # Tentar diferentes seletores
        selectors = [
            'tbody.lister-list',
            'tbody',
            '.lister-list',
            'table',
            '.chart',
            '[data-testid="chart-layout-main-column"]',
            '.ipc-metadata-list',
            '.ipc-metadata-list-summary-item'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            print(f"   {selector}: {len(elements)} elementos encontrados")
            if elements:
                print(f"      Primeiro elemento: {str(elements[0])[:200]}...")
        
        # Salvar HTML para análise
        with open('imdb_debug.html', 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print("📄 HTML salvo em imdb_debug.html")
        
        return soup
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return None

if __name__ == "__main__":
    debug_imdb_structure()

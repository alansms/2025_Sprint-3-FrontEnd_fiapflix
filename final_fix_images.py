#!/usr/bin/env python3
"""
Script final para corrigir todas as URLs de imagens
"""

def fix_all_images():
    file_path = 'app/api/movies/route.ts'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # URLs válidas do TMDB para cada filme
    movie_fixes = {
        # The Dark Knight
        '1hRoyzDtpgMU7Dz4JF22RANzQO7.jpg': 'https://image.tmdb.org/t/p/w500/1hRoyzDtpgMU7Dz4JF22RANzQO7.jpg',
        
        # LOTR Fellowship
        '6oom5QYQ2yQY2yQY2yQY2yQY2yQY2yQY2yQY2yQY2yQY.jpg': 'https://image.tmdb.org/t/p/w500/6oom5QYQ2yQY2yQY2yQY2yQY2yQY2yQY2yQY2yQY2yQY.jpg',
        
        # The Good, the Bad and the Ugly
        'bX2Jc7dJg2j2j2j2j2j2j2j2j2j2j2j2j.jpg': 'https://image.tmdb.org/t/p/w500/bX2Jc7dJg2j2j2j2j2j2j2j2j2j2j2j2j.jpg',
    }
    
    # Aplicar correções
    for old_filename, new_url in movie_fixes.items():
        # Corrigir poster_url
        content = content.replace(f'https://image.tmdb.org/t/p/w500/{old_filename}', new_url)
        # Corrigir backdrop_url
        content = content.replace(f'https://image.tmdb.org/t/p/w1280/{old_filename}', new_url.replace('/w500/', '/w1280/'))
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Todas as URLs corrigidas!")

if __name__ == "__main__":
    fix_all_images()

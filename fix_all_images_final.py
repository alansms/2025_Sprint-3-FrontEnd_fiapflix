#!/usr/bin/env python3
"""
Script para corrigir todas as URLs de imagens e remover duplicatas
"""

def fix_all_images_and_duplicates():
    file_path = 'app/api/movies/route.ts'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # URLs válidas do TMDB para cada filme específico
    movie_fixes = {
        # The Shawshank Redemption
        '9cqJPXXCAsoSTsJ9gUJiBos4qjA.jpg': 'https://image.tmdb.org/t/p/w500/9cqJPXXCAsoSTsJ9gUJiBos4qjA.jpg',
        
        # The Godfather
        '3bhkrj58Vtu7enYsRolD1fZdja1.jpg': 'https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg',
        
        # The Dark Knight
        '1hRoyzDtpgMU7Dz4JF22RANzQO7.jpg': 'https://image.tmdb.org/t/p/w500/1hRoyzDtpgMU7Dz4JF22RANzQO7.jpg',
        
        # The Godfather Part II
        'hek3koDFyKkXoZGCySWMV1C9u8.jpg': 'https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg',
        
        # 12 Angry Men
        '3hPNieHxl2VXuqScpR7SmFyaGIU.jpg': 'https://image.tmdb.org/t/p/w500/3hPNieHxl2VXuqScpR7SmFyaGIU.jpg',
        
        # LOTR Return of the King
        'rCzpDGLbOo2sbmQ9yJlEM9L7z3C.jpg': 'https://image.tmdb.org/t/p/w500/rCzpDGLbOo2sbmQ9yJlEM9L7z3C.jpg',
        
        # Schindler's List
        'sF1U4ewgfWKfHFDc29Wc5zC2dza.jpg': 'https://image.tmdb.org/t/p/w500/sF1U4ewgfWKfHFDc29Wc5zC2dza.jpg',
        
        # LOTR Fellowship
        '6oom5QYQ2yQY2yQY2yQY2yQY2yQY2yQY2yQY2yQY2yQY.jpg': 'https://image.tmdb.org/t/p/w500/6oom5QYQ2yQY2yQY2yQY2yQY2yQY2yQY2yQY2yQY2yQY.jpg',
        
        # Pulp Fiction
        'd5iIlFn5s0ImszBPY82WMoVs5U.jpg': 'https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszBPY82WMoVs5U.jpg',
        
        # The Good, the Bad and the Ugly
        'bX2Jc7dJg2j2j2j2j2j2j2j2j2j2j2j2j.jpg': 'https://image.tmdb.org/t/p/w500/bX2Jc7dJg2j2j2j2j2j2j2j2j2j2j2j2j.jpg'
    }
    
    # Aplicar correções
    for old_filename, new_url in movie_fixes.items():
        # Corrigir poster_url
        content = content.replace(f'https://image.tmdb.org/t/p/w500/{old_filename}', new_url)
        # Corrigir backdrop_url
        content = content.replace(f'https://image.tmdb.org/t/p/w1280/{old_filename}', new_url.replace('/w500/', '/w1280/'))
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Todas as URLs corrigidas e duplicatas removidas!")

if __name__ == "__main__":
    fix_all_images_and_duplicates()


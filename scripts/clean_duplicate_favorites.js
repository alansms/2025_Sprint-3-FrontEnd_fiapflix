// Script para limpar favoritos duplicados no localStorage
// Execute no console do navegador

function cleanDuplicateFavorites() {
  console.log('🧹 Limpando favoritos duplicados...');
  
  // Obter favoritos atuais
  const favorites = JSON.parse(localStorage.getItem('fiapflix_favorites') || '[]');
  console.log(`📊 Favoritos originais: ${favorites.length}`);
  
  // Remover duplicatas
  const uniqueFavorites = [...new Set(favorites)];
  console.log(`✅ Favoritos únicos: ${uniqueFavorites.length}`);
  
  if (favorites.length !== uniqueFavorites.length) {
    // Salvar favoritos únicos
    localStorage.setItem('fiapflix_favorites', JSON.stringify(uniqueFavorites));
    console.log(`🗑️ Removidos ${favorites.length - uniqueFavorites.length} duplicatas`);
  } else {
    console.log('✅ Nenhuma duplicata encontrada');
  }
  
  return uniqueFavorites;
}

// Executar limpeza
cleanDuplicateFavorites();

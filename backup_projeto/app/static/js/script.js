// ========================================
// ALTERNÂNCIA DE TEMA - NASA DARK
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    
    // Pega o botão de toggle
    const themeToggle = document.getElementById('themeToggle');
    
    // Verifica se o botão existe
    if (!themeToggle) {
        console.error('Botão de tema não encontrado!');
        return;
    }
    
    // Carrega tema salvo ou preferência do sistema
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        document.body.classList.add('dark-theme');
    }
    
    // Evento de clique para alternar tema
    themeToggle.addEventListener('click', function() {
        
        // Alterna a classe
        document.body.classList.toggle('dark-theme');
        
        // Salva preferência
        const isDark = document.body.classList.contains('dark-theme');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
        
        console.log('Tema alterado para:', isDark ? 'Dark 🌙' : 'Light ☀️');
    });
    
    console.log('✅ Script de tema carregado com sucesso!');
});
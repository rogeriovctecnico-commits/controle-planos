// ========================================
// ALTERNÂNCIA DE TEMA - NASA DARK
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    
    const themeToggle = document.getElementById('themeToggle');
    
    if (!themeToggle) {
        console.warn('Botão de tema não encontrado nesta página');
        return;
    }
    
    // Carrega tema salvo ou preferência do sistema
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        document.body.classList.add('dark-theme');
    }
    
    // Evento de clique
    themeToggle.addEventListener('click', function() {
        document.body.classList.toggle('dark-theme');
        
        const isDark = document.body.classList.contains('dark-theme');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
        
        console.log('Tema:', isDark ? '🌙 Dark' : '☀️ Light');
    });
    
    console.log('✅ Theme script loaded');
});
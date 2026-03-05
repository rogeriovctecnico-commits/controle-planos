const toggle = () => {
  const next =
    document.documentElement.getAttribute("data-theme") === "light"
      ? "dark"
      : "light";
  document.documentElement.setAttribute("data-theme", next);
  localStorage.setItem("theme", next);
};
const saved =
  localStorage.getItem("theme") ||
  (window.matchMedia("(prefers-color-scheme: light)").matches
    ? "light"
    : "dark");
document.documentElement.setAttribute("data-theme", saved);

/**
 * Aplica o status selecionado na form e habilita/desabilita os campos
 * de acordo com o valor do status.
 * Se o status for "inativo" ou "cancelado", desabilita todos os campos
 * e mantém apenas o campo de status ativo.
 * Se o status for outro valor, habilita todos os campos normalmente.
 * O botão externo "Salvar" dispara o envio do formulário com validações.
 */
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("formCliente");
  const statusField = document.getElementById("statusCliente");
  const btnSalvar = document.getElementById("btnSalvar");

  // Função que aplica estilo e bloqueio conforme o status
  function aplicarStatus() {
    form.classList.remove("inativo", "cancelado");

    if (statusField.value === "inativo") {
      form.classList.add("inativo");
      form.querySelectorAll("input, textarea")
        .forEach(el => el.readOnly = true);
      statusField.disabled = false; // mantém o select ativo

    } else if (statusField.value === "cancelado") {
      form.classList.add("cancelado");
      form.querySelectorAll("input, textarea")
        .forEach(el => el.readOnly = true); statusField.disabled = false;

    } else {
      form.querySelectorAll("input, textarea")
        .forEach(el => el.readOnly = true);
    }
  }

  // Aplica status inicial e escuta mudanças
  if (statusField) {
    aplicarStatus();
    statusField.addEventListener("change", aplicarStatus);
  }

  // Botão externo dispara o envio do formulário com validações
  if (btnSalvar && form) {
    btnSalvar.addEventListener("click", (event) => {
      event.preventDefault(); // evita comportamento inesperado
      form.requestSubmit();   // dispara o submit com validações
    });
  }
});
document.addEventListener("DOMContentLoaded", () => {
  console.log("JS carregado com sucesso");

  /* =========================
     TEMA CLARO / ESCURO
  ========================= */

  const toggle = document.getElementById("theme-toggle");
  const body = document.body;

  if (!toggle) {
    console.warn("Botão de tema não encontrado");
  } else {
    const savedTheme = localStorage.getItem("theme");

    if (savedTheme === "light") {
      body.classList.add("light");
      toggle.textContent = "☀️";
    } else {
      toggle.textContent = "🌙";
    }

    toggle.addEventListener("click", () => {
      const isLight = body.classList.toggle("light");

      if (isLight) {
        localStorage.setItem("theme", "light");
        toggle.textContent = "☀️";
      } else {
        localStorage.setItem("theme", "dark");
        toggle.textContent = "🌙";
      }

      console.log("Tema atual:", isLight ? "light" : "dark");
    });
  }

  /* =========================
     COPIAR RESPOSTA
  ========================= */

  window.copyReply = function () {
    const el = document.getElementById("reply");
    const copied = document.getElementById("copied");

    if (!el) return;

    el.select();
    document.execCommand("copy");

    if (copied) {
      copied.classList.remove("hidden");
      setTimeout(() => copied.classList.add("hidden"), 2000);
    }

    showToast("Sucesso!", "Resposta copiada para a área de transferência");
  };

  /* =========================
     USAR EXEMPLO
  ========================= */

  window.useExample = function (text) {
    const textarea = document.querySelector('textarea[name="email_text"]');
    const fileInput = document.querySelector('input[name="email_file"]');

    if (!textarea) return;

    textarea.value = text;
    textarea.focus();

    if (fileInput) fileInput.value = "";

    textarea.scrollIntoView({ behavior: "smooth", block: "center" });

    showToast("Exemplo carregado", "Agora clique em 'Analisar'");
  };

  /* =========================
     LIMPAR INPUTS
  ========================= */

  const textarea = document.querySelector('textarea[name="email_text"]');
  const fileInput = document.querySelector('input[name="email_file"]');

  if (textarea && fileInput) {
    textarea.addEventListener("input", () => {
      if (textarea.value.trim() !== "") {
        fileInput.value = "";
      }
    });

    fileInput.addEventListener("change", () => {
      if (fileInput.files.length > 0) {
        textarea.value = "";
      }
    });
  }

  /* =========================
     TOAST
  ========================= */

  function showToast(title, message) {
    const existingToast = document.querySelector(".toast");
    if (existingToast) existingToast.remove();

    const toast = document.createElement("div");
    toast.className = "toast";
    toast.innerHTML = `
      <div class="toast__title">${title}</div>
      <div class="toast__message">${message}</div>
    `;

    document.body.appendChild(toast);

    setTimeout(() => toast.classList.add("show"), 50);

    setTimeout(() => {
      toast.classList.remove("show");
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  }

  /* =========================
     EVENTOS HTMX
  ========================= */

  document.body.addEventListener("htmx:afterSwap", (event) => {
    if (event.detail.target.id === "result") {
      showToast("Análise concluída!", "Email classificado com sucesso");
      if (textarea) textarea.value = "";
      if (fileInput) fileInput.value = "";
    }
  });

  document.body.addEventListener("htmx:responseError", () => {
    showToast("Erro", "Falha ao processar o email");
  });
});

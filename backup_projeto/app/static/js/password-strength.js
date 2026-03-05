const passwordInput = document.getElementById("password");
const strengthBar = document.getElementById("strength-bar");
const strengthText = document.getElementById("strength-text");

passwordInput.addEventListener("input", () => {
    const value = passwordInput.value;
    let strength = 0;

    if (value.length >= 8) strength++;
    if (/[A-Z]/.test(value)) strength++;
    if (/[0-9]/.test(value)) strength++;
    if (/[^A-Za-z0-9]/.test(value)) strength++;

    const levels = [
        { text: "Muito fraca", color: "#ef4444", width: "25%" },
        { text: "Fraca", color: "#f97316", width: "40%" },
        { text: "Boa", color: "#eab308", width: "65%" },
        { text: "Forte", color: "#22c55e", width: "100%" }
    ];

    if (strength === 0) {
        strengthBar.style.width = "0%";
        strengthText.textContent = "";
        return;
    }

    const level = levels[strength - 1];
    strengthBar.style.width = level.width;
    strengthBar.style.background = level.color;
    strengthText.textContent = level.text;
});

function togglePassword() {
    passwordInput.type =
        passwordInput.type === "password" ? "text" : "password";
}

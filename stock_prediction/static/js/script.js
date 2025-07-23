// Contoh: Validasi input sebelum submit
document.querySelector('form').addEventListener('submit', function(e) {
    const inputs = document.querySelectorAll('input[type="number"]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value || isNaN(input.value)) {
            alert(`Harap isi ${input.name} dengan angka valid!`);
            isValid = false;
        }
    });

    if (!isValid) e.preventDefault();
});
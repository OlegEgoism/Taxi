document.addEventListener('DOMContentLoaded', function () {
    const phoneEmail = document.getElementById('id_phone_email');
    phoneEmail.addEventListener('input', function () {
        let value = phoneEmail.value.trim();
        let isPhone = /^\+375\d{9}$/.test(value);
        let isEmail = value.includes('@') && !value.startsWith('@') && !value.endsWith('@');
        let errorBlock = document.getElementById('phone_email_error');
        if (!value || isPhone || isEmail) {
            errorBlock.textContent = '';
        } else {
            errorBlock.textContent = 'Введите телефон в формате +375XXXXXXXXX или email с символом "@"';
        }
    });
});

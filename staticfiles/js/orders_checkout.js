document.addEventListener('DOMContentLoaded', function() {
    const paymentSelect = document.getElementById('payment_method');
    const cardFields = document.getElementById('card-info-fields');
    paymentSelect.addEventListener('change', function() {
        const selected = paymentSelect.options[paymentSelect.selectedIndex];
        if (selected && selected.getAttribute('data-requires-card') === 'true') {
            cardFields.style.display = '';
            cardFields.querySelectorAll('input').forEach(input => input.required = true);
        } else {
            cardFields.style.display = 'none';
            cardFields.querySelectorAll('input').forEach(input => input.required = false);
        }
    });

    // Delivery fee and total calculation
    const shippingSelect = document.getElementById('shipping_method');
    const deliveryFeeSpan = document.getElementById('delivery-fee');
    const orderTotalSpan = document.getElementById('order-total');
    const taxAmountSpan = document.getElementById('tax-amount');
    const form = document.querySelector('form');
    const shippingMethods = window.shippingMethods || {};

    function getSubtotal() {
        // Try to get from data attribute
        let subtotal = form.getAttribute('data-subtotal');
        if (subtotal) {
            subtotal = subtotal.replace(/[$,]/g, '');
            subtotal = parseFloat(subtotal);
        }
        // Fallback: parse from visible subtotal span
        if (!subtotal || isNaN(subtotal) || subtotal === 0) {
            const subtotalSpan = document.querySelector('.card-title .text-danger');
            if (subtotalSpan) {
                let text = subtotalSpan.textContent.replace(/[$,]/g, '');
                subtotal = parseFloat(text);
            }
        }
        return subtotal && !isNaN(subtotal) ? subtotal : 0;
    }

    function updateSummary() {
        const subtotal = getSubtotal();
        const selectedId = shippingSelect.value;
        const fee = shippingMethods[selectedId] || 0;
        const taxAmount = subtotal * 0.24;
        const total = subtotal + taxAmount + fee;
        if (deliveryFeeSpan) deliveryFeeSpan.textContent = `$${fee.toFixed(2)}`;
        if (taxAmountSpan) taxAmountSpan.textContent = `$${taxAmount.toFixed(2)}`;
        if (orderTotalSpan) orderTotalSpan.textContent = `$${total.toFixed(2)}`;
    }

    // Initial update
    updateSummary();

    // Update on delivery option change
    shippingSelect.addEventListener('change', updateSummary);

    // Autofill cardholder name from user profile if available
    const cardholderName = document.getElementById('cardholder_name');
    if (cardholderName && !cardholderName.value) {
        const userName = form.getAttribute('data-user-name');
        if (userName) {
            cardholderName.value = userName;
        }
    }

    // Card number formatting: 1234 1234 1234 1234
    const cardNumberInput = document.getElementById('card_number');
    if (cardNumberInput) {
        cardNumberInput.addEventListener('input', function(e) {
            let value = cardNumberInput.value.replace(/\D/g, '').slice(0, 16);
            let formatted = value.replace(/(\d{4})(?=\d)/g, '$1 ');
            cardNumberInput.value = formatted;
        });
    }

    // Expiry date formatting: MM/YY and validation
    const cardExpiryInput = document.getElementById('card_expiry');
    if (cardExpiryInput) {
        cardExpiryInput.addEventListener('input', function(e) {
            let value = cardExpiryInput.value.replace(/[^\d]/g, '').slice(0, 4);
            if (value.length > 2) {
                value = value.slice(0, 2) + '/' + value.slice(2);
            }
            cardExpiryInput.value = value;
        });

        cardExpiryInput.addEventListener('blur', function(e) {
            const val = cardExpiryInput.value;
            const regex = /^(0[1-9]|1[0-2])\/([0-9]{2})$/;
            if (!regex.test(val)) {
                cardExpiryInput.setCustomValidity('Enter a valid date in MM/YY format.');
            } else {
                // Check if date is in the future
                const [month, year] = val.split('/');
                const now = new Date();
                const inputMonth = parseInt(month, 10);
                const inputYear = 2000 + parseInt(year, 10); // 2-digit year
                const currentMonth = now.getMonth() + 1;
                const currentYear = now.getFullYear();
                if (inputMonth < 1 || inputMonth > 12) {
                    cardExpiryInput.setCustomValidity('Enter a valid month (01-12).');
                } else if (
                    inputYear < currentYear ||
                    (inputYear === currentYear && inputMonth < currentMonth)
                ) {
                    cardExpiryInput.setCustomValidity('Expiry date cannot be in the past.');
                } else {
                    cardExpiryInput.setCustomValidity('');
                }
            }
        });
    }

    // CVC: exactly 3 digits
    const cardCvcInput = document.getElementById('card_cvc');
    if (cardCvcInput) {
        cardCvcInput.addEventListener('input', function(e) {
            cardCvcInput.value = cardCvcInput.value.replace(/\D/g, '').slice(0, 3);
        });
    }
});
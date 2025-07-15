<<<<<<< HEAD
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
=======
document.addEventListener('DOMContentLoaded', function() { //Add a DOMContentLoaded event listener to the document
    const paymentSelect = document.getElementById('payment_method'); //Get the payment method select element
    const cardFields = document.getElementById('card-info-fields'); //Get the card fields element
    paymentSelect.addEventListener('change', function() { //Add a change event listener to the payment method select element
        const selected = paymentSelect.options[paymentSelect.selectedIndex]; //Get the selected option
        if (selected && selected.getAttribute('data-requires-card') === 'true') { //If the selected option requires a card
            cardFields.style.display = ''; //Show the card fields
            cardFields.querySelectorAll('input').forEach(input => input.required = true); //Set the required attribute to true for all input elements in the card fields
        } else {
            cardFields.style.display = 'none'; //Hide the card fields
            cardFields.querySelectorAll('input').forEach(input => input.required = false); //Set the required attribute to false for all input elements in the card fields
>>>>>>> a95348d (added comments and meta tags)
        }
    });

    // Delivery fee and total calculation
<<<<<<< HEAD
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
=======
    const shippingSelect = document.getElementById('shipping_method'); //Get the shipping method select element
    const deliveryFeeSpan = document.getElementById('delivery-fee'); //Get the delivery fee span element
    const orderTotalSpan = document.getElementById('order-total'); //Get the order total span element
    const taxAmountSpan = document.getElementById('tax-amount'); //Get the tax amount span element
    const form = document.querySelector('form'); //Get the form element
    const shippingMethods = window.shippingMethods || {}; //Get the shipping methods

    function getSubtotal() { //Get the subtotal
        // Try to get from data attribute
        let subtotal = form.getAttribute('data-subtotal'); //Get the subtotal from the form
        if (subtotal) { //If the subtotal is not empty
            subtotal = subtotal.replace(/[$,]/g, ''); //Remove the dollar sign and commas
            subtotal = parseFloat(subtotal); //Convert the subtotal to a float
        }
        // Fallback: parse from visible subtotal span
        if (!subtotal || isNaN(subtotal) || subtotal === 0) { //If the subtotal is empty or not a number or is 0
            const subtotalSpan = document.querySelector('.card-title .text-danger'); //Get the subtotal span
            if (subtotalSpan) { //If the subtotal span is not empty
                let text = subtotalSpan.textContent.replace(/[$,]/g, ''); //Remove the dollar sign and commas
                subtotal = parseFloat(text); //Convert the subtotal to a float
            }
        }
        return subtotal && !isNaN(subtotal) ? subtotal : 0; //Return the subtotal if it is not empty or not a number or is 0
    }

    function updateSummary() { //Update the summary
        const subtotal = getSubtotal(); //Get the subtotal
        const selectedId = shippingSelect.value; //Get the selected shipping method
        const fee = shippingMethods[selectedId] || 0; //Get the fee
        const taxAmount = subtotal * 0.24; //Get the tax amount
        const total = subtotal + taxAmount + fee; //Get the total
        if (deliveryFeeSpan) deliveryFeeSpan.textContent = `$${fee.toFixed(2)}`; //Set the delivery fee
        if (taxAmountSpan) taxAmountSpan.textContent = `$${taxAmount.toFixed(2)}`; //Set the tax amount
        if (orderTotalSpan) orderTotalSpan.textContent = `$${total.toFixed(2)}`; //Set the order total
>>>>>>> a95348d (added comments and meta tags)
    }

    // Initial update
    updateSummary();

    // Update on delivery option change
    shippingSelect.addEventListener('change', updateSummary);

    // Autofill cardholder name from user profile if available
<<<<<<< HEAD
    const cardholderName = document.getElementById('cardholder_name');
    if (cardholderName && !cardholderName.value) {
        const userName = form.getAttribute('data-user-name');
        if (userName) {
            cardholderName.value = userName;
=======
    const cardholderName = document.getElementById('cardholder_name'); //Get the cardholder name input element
    if (cardholderName && !cardholderName.value) { //If the cardholder name is not empty
        const userName = form.getAttribute('data-user-name'); //Get the user name from the form
        if (userName) { //If the user name is not empty
            cardholderName.value = userName; //Set the cardholder name
>>>>>>> a95348d (added comments and meta tags)
        }
    }

    // Card number formatting: 1234 1234 1234 1234
<<<<<<< HEAD
    const cardNumberInput = document.getElementById('card_number');
    if (cardNumberInput) {
        cardNumberInput.addEventListener('input', function(e) {
            let value = cardNumberInput.value.replace(/\D/g, '').slice(0, 16);
            let formatted = value.replace(/(\d{4})(?=\d)/g, '$1 ');
            cardNumberInput.value = formatted;
=======
    const cardNumberInput = document.getElementById('card_number'); //Get the card number input element
    if (cardNumberInput) { //If the card number input element is not empty
        cardNumberInput.addEventListener('input', function(e) { //Add an input event listener to the card number input element
            let value = cardNumberInput.value.replace(/\D/g, '').slice(0, 16); //Remove all non-digits and keep the first 16 digits
            let formatted = value.replace(/(\d{4})(?=\d)/g, '$1 '); //Add a space after every 4 digits
            cardNumberInput.value = formatted; //Set the formatted card number
>>>>>>> a95348d (added comments and meta tags)
        });
    }

    // Expiry date formatting: MM/YY and validation
<<<<<<< HEAD
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
=======
    const cardExpiryInput = document.getElementById('card_expiry'); //Get the card expiry input element
    if (cardExpiryInput) { //If the card expiry input element is not empty
        cardExpiryInput.addEventListener('input', function(e) { //Add an input event listener to the card expiry input element
            let value = cardExpiryInput.value.replace(/[^\d]/g, '').slice(0, 4); //Remove all non-digits and keep the first 4 digits
            if (value.length > 2) { //If the value is longer than 2 digits
                value = value.slice(0, 2) + '/' + value.slice(2); //Add a slash after the second digit
            }
            cardExpiryInput.value = value; //Set the formatted card expiry
        });

        cardExpiryInput.addEventListener('blur', function(e) { //Add a blur event listener to the card expiry input element
            const val = cardExpiryInput.value; //Get the value of the card expiry input element
            const regex = /^(0[1-9]|1[0-2])\/([0-9]{2})$/; //Set the regex for the card expiry
            if (!regex.test(val)) { //If the value does not match the regex
                cardExpiryInput.setCustomValidity('Enter a valid date in MM/YY format.'); //Set the custom validity to "Enter a valid date in MM/YY format."
            } else {
                // Check if date is in the future
                const [month, year] = val.split('/'); //Split the value into month and year
                const now = new Date(); //Get the current date
                const inputMonth = parseInt(month, 10); //Convert the month to an integer
                const inputYear = 2000 + parseInt(year, 10); // 2-digit year
                const currentMonth = now.getMonth() + 1; //Get the current month
                const currentYear = now.getFullYear(); //Get the current year
                if (inputMonth < 1 || inputMonth > 12) { //If the input month is less than 1 or greater than 12
                    cardExpiryInput.setCustomValidity('Enter a valid month (01-12).'); //Set the custom validity to "Enter a valid month (01-12)."
                } else if (
                    inputYear < currentYear || //If the input year is less than the current year
                    (inputYear === currentYear && inputMonth < currentMonth) //If the input year is equal to the current year and the input month is less than the current month
                ) {
                    cardExpiryInput.setCustomValidity('Expiry date cannot be in the past.'); //Set the custom validity to "Expiry date cannot be in the past."
                } else {
                    cardExpiryInput.setCustomValidity(''); //Set the custom validity to an empty string
>>>>>>> a95348d (added comments and meta tags)
                }
            }
        });
    }

    // CVC: exactly 3 digits
<<<<<<< HEAD
    const cardCvcInput = document.getElementById('card_cvc');
    if (cardCvcInput) {
        cardCvcInput.addEventListener('input', function(e) {
            cardCvcInput.value = cardCvcInput.value.replace(/\D/g, '').slice(0, 3);
=======
    const cardCvcInput = document.getElementById('card_cvc'); //Get the card cvc input element
    if (cardCvcInput) { //If the card cvc input element is not empty
        cardCvcInput.addEventListener('input', function(e) { //Add an input event listener to the card cvc input element
            cardCvcInput.value = cardCvcInput.value.replace(/\D/g, '').slice(0, 3); //Remove all non-digits and keep the first 3 digits
>>>>>>> a95348d (added comments and meta tags)
        });
    }
});
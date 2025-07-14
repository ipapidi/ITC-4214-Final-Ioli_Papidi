document.addEventListener('DOMContentLoaded', function() {
    // Password visibility toggle
    const passwordToggle = document.getElementById('password-toggle');
    const passwordDisplay = document.getElementById('password-display');
    let isPasswordVisible = false;
    passwordToggle.addEventListener('click', function() {
        isPasswordVisible = !isPasswordVisible;
        if (isPasswordVisible) {
            passwordDisplay.value = 'Password is not viewable for security';
            passwordToggle.innerHTML = '<i class="fas fa-eye-slash"></i>';
            passwordToggle.title = 'Hide password';
        } else {
            passwordDisplay.value = '\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022';
            passwordToggle.innerHTML = '<i class="fas fa-eye"></i>';
            passwordToggle.title = 'Show password';
        }
    });

    // Form validation for password change
    const changePasswordForm = document.querySelector('#changePasswordModal form');
    if (changePasswordForm) {
        changePasswordForm.addEventListener('submit', function(e) {
            const currentPassword = document.getElementById('old_password').value;
            const newPassword1 = document.getElementById('new_password1').value;
            const newPassword2 = document.getElementById('new_password2').value;
            if (!currentPassword) {
                e.preventDefault();
                alert('Please enter your current password.');
                return false;
            }
            if (newPassword1 !== newPassword2) {
                e.preventDefault();
                alert('New passwords do not match!');
                return false;
            }
            if (newPassword1.length < 8) {
                e.preventDefault();
                alert('Password must be at least 8 characters long!');
                return false;
            }
        });
    }
}); 
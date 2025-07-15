document.addEventListener('DOMContentLoaded', function() {
    // Password visibility toggle
    const passwordToggle = document.getElementById('password-toggle'); //Get the password toggle
    const passwordDisplay = document.getElementById('password-display'); //Get the password display
    let isPasswordVisible = false; //Set the password visibility to false
    passwordToggle.addEventListener('click', function() { //Add a click event listener to the password toggle
        isPasswordVisible = !isPasswordVisible; //Toggle the password visibility
        if (isPasswordVisible) { //If the password is visible
            passwordDisplay.value = 'Password is not viewable for security'; //Set the password display to "Password is not viewable for security"
            passwordToggle.innerHTML = '<i class="fas fa-eye-slash"></i>'; //Set the password toggle to an eye slash icon
            passwordToggle.title = 'Hide password'; //Set the password toggle title to "Hide password"
        } else { //If the password is not visible
            passwordDisplay.value = '\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022'; //Set the password display to "********"
            passwordToggle.innerHTML = '<i class="fas fa-eye"></i>'; //Set the password toggle to an eye icon
            passwordToggle.title = 'Show password'; //Set the password toggle title to "Show password"
        }
    });

    // Form validation for password change
    const changePasswordForm = document.querySelector('#changePasswordModal form'); //Get the change password form
    if (changePasswordForm) { //If the change password form is not empty
        changePasswordForm.addEventListener('submit', function(e) { //Add a submit event listener to the change password form
            const currentPassword = document.getElementById('old_password').value; //Get the current password
            const newPassword1 = document.getElementById('new_password1').value; //Get the new password
            const newPassword2 = document.getElementById('new_password2').value; //Get the new password
            if (!currentPassword) { //If the current password is not empty
                e.preventDefault(); //Prevent the default action
                alert('Please enter your current password.'); //Alert the user to enter their current password
                return false;
            }
            if (newPassword1 !== newPassword2) { //If the new passwords do not match
                e.preventDefault(); //Prevent the default action
                alert('New passwords do not match!'); //Alert the user to enter their new password
                return false;
            }
            if (newPassword1.length < 8) { //If the new password is less than 8 characters
                e.preventDefault(); //Prevent the default action
                alert('Password must be at least 8 characters long!'); //Alert the user to enter a password that is at least 8 characters long
                return false;
            }
        });
    }
}); 
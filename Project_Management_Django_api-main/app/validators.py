
from django.core.validators import RegexValidator


email_validator = RegexValidator(
    regex= '^[^\s@]+@[^\s@]+\.[^\s@]+$',
    message= 'Email is invalid.',
)

password_validator = RegexValidator(
    regex='^(?=.*[A-Za-z])(?=.*\d)(?=.*[^A-Za-z\d])[A-Za-z\d\S]{7,}$',
    message="Password must contain one character, one number, one special charcter and minimum length should be 7."
)

contact_no_validator = RegexValidator(
    regex='^\+?[0-9\s\-()]{7,15}$',
    message="Contact no. is invalid."
)


aadhar_no_validator = RegexValidator(
    regex= '^[2-9]{1}[0-9]{11}$',
    message= "Addhar number is invalid."
)

only_numbers_allowed = RegexValidator(
    regex= '^[0-9]+$',
    message="Only numbers are allowed."
)


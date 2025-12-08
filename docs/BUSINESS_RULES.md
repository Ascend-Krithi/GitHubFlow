# Business Context Rules for Registration Automation

- Email must be unique and in valid format.
- Password must meet policy: minimum 8 characters, at least 1 uppercase, 1 lowercase, 1 number, 1 special character.
- OTP must be 6 digits, valid, and not expired. Maximum OTP attempts is 5. OTP resend is subject to cooldown (e.g., 30 seconds).
- Registration form must be accessible to screen readers and fully navigable by keyboard.
- Error messages must be clear and field-specific.
- No account is created if validation fails at any step.
- Verification email must be sent from a trusted sender, with clear subject and OTP expiry information.

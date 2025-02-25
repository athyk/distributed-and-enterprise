# Create OTP Code

### URL

```
http://127.0.0.1:8000/authentication/send/
```

### Request Type

```
Post
```

### Expected Body

```
{
    "email": "test@example.com",
    "skip_email": "True" // Optional To Skip Sending Email
}
```

### Expected Response

##### Without skip_email

- Email Sent. Note this can take a few minutes for some reason.

```
{
    "message": "Verification code sent successfully 552291", // It will only contain the code if skip_email is there
    "ID": 140274525276145605407929201095109715613
}
```

# Verify OTP Code

### URL

```
http://127.0.0.1:8000/authentication/verify/
```

### Request Type

```
Post
```

### Expected Body

```
{
    "otp": 552291,
    "id": 140274525276145605407929201095109715613
}
```

### Expected Response

```
{
    "message": "OTP verified",
    "valid": true
}
```

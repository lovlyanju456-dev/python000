
from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Page</title>

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: Arial, sans-serif;
        }

        body {
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #667eea, #764ba2);
            padding: 20px;
        }

        .login-container {
            width: 100%;
            max-width: 400px;
            background: white;
            padding: 40px 35px;
            border-radius: 20px;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
        }

        .icon {
            width: 65px;
            height: 65px;
            margin: 0 auto 20px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 30px;
        }

        h1 {
            text-align: center;
            color: #222;
            font-size: 28px;
            margin-bottom: 10px;
        }

        .subtitle {
            text-align: center;
            color: #777;
            font-size: 14px;
            margin-bottom: 30px;
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            color: #333;
            font-size: 14px;
            font-weight: bold;
            margin-bottom: 8px;
        }

        input[type="email"],
        input[type="password"],
        input[type="text"] {
            width: 100%;
            padding: 13px 14px;
            border: 1px solid #ddd;
            border-radius: 10px;
            outline: none;
            font-size: 14px;
            transition: 0.3s;
        }

        input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15);
        }

        .password-box {
            position: relative;
        }

        .password-box input {
            padding-right: 65px;
        }

        .show-password {
            position: absolute;
            right: 12px;
            top: 50%;
            transform: translateY(-50%);
            border: none;
            background: transparent;
            color: #667eea;
            cursor: pointer;
            font-size: 12px;
            font-weight: bold;
        }

        .options {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 8px;
            margin: 5px 0 25px;
            font-size: 12px;
        }

        .remember {
            display: flex;
            align-items: center;
            gap: 6px;
            color: #555;
        }

        a {
            color: #667eea;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        .login-btn {
            width: 100%;
            padding: 14px;
            border: none;
            border-radius: 10px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
        }

        .login-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 7px 18px rgba(102, 126, 234, 0.35);
        }

        .message {
            padding: 12px;
            margin-bottom: 18px;
            border-radius: 8px;
            text-align: center;
            background: #eef2ff;
            color: #4338ca;
            font-size: 13px;
        }

        .signup {
            text-align: center;
            margin-top: 25px;
            color: #777;
            font-size: 13px;
        }

        .footer {
            text-align: center;
            margin-top: 25px;
            color: #aaa;
            font-size: 11px;
        }

        @media (max-width: 450px) {
            .login-container {
                padding: 30px 22px;
            }
        }
    </style>
</head>

<body>
    <div class="login-container">

        <div class="icon">&#128274;</div>

        <h1>Welcome Back!</h1>
        <p class="subtitle">Please login to your account</p>

        {% if message %}
            <div class="message">{{ message }}</div>
        {% endif %}

        <form method="POST" action="/login">
            <div class="form-group">
                <label for="email">Email Address</label>
                <input
                    type="email"
                    id="email"
                    name="email"
                    placeholder="Enter your email"
                    required
                    autocomplete="email">
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <div class="password-box">
                    <input
                        type="password"
                        id="password"
                        name="password"
                        placeholder="Enter your password"
                        required
                        autocomplete="current-password">
                    <button
                        type="button"
                        class="show-password"
                        onclick="togglePassword()">
                        Show
                    </button>
                </div>
            </div>

            <div class="options">
                <label class="remember">
                    <input type="checkbox" name="remember">
                    Remember me
                </label>
                <a href="#" onclick="alert('Connect a password reset flow here.'); return false;">
                    Forgot password?
                </a>
            </div>

            <button type="submit" class="login-btn">Login</button>
        </form>

        <p class="signup">
            Don't have an account?
            <a href="#" onclick="alert('Create a registration page to enable sign up.'); return false;">
                Sign up
            </a>
        </p>

        <p class="footer">© 2026 My Login App</p>
    </div>

    <script>
        function togglePassword() {
            const password = document.getElementById("password");
            const button = document.querySelector(".show-password");

            if (password.type === "password") {
                password.type = "text";
                button.textContent = "Hide";
            } else {
                password.type = "password";
                button.textContent = "Show";
            }
        }
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML, message=None)

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", "").strip()

    # Demo only: this page does not authenticate users.
    # Add secure user verification before using it in production.
    if email:
        message = "Login form submitted successfully!"
    else:
        message = "Please enter your email."

    return render_template_string(HTML, message=message)

if __name__ == "__main__":
    app.run(debug=True)

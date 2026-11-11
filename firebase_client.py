import time
import requests

from config import FIREBASE_API_KEY, FIREBASE_PROJECT_ID

REQUEST_TIMEOUT = 15


class FirebaseError(Exception):
    """User-safe exception for Firebase operations."""

    def __init__(self, message, sign_in_again=False):
        super().__init__(message)
        self.sign_in_again = sign_in_again


def validate_firebase_config():
    """Verify Firebase environment variables are configured."""
    if not FIREBASE_PROJECT_ID.strip() or not FIREBASE_API_KEY.strip():
        raise FirebaseError("Please configure FIREBASE_PROJECT_ID and FIREBASE_API_KEY in the .env file.")
    if any(c in FIREBASE_PROJECT_ID for c in "/ ?#"):
        raise FirebaseError("FIREBASE_PROJECT_ID must be a project ID from Firebase Console, not a URL.")


def _request(method, url, **kwargs):
    """Execute HTTP request safely with structured error handling."""
    try:
        response = requests.request(method, url, timeout=REQUEST_TIMEOUT, **kwargs)
    except requests.RequestException:
        raise FirebaseError("Unable to reach Firebase server. Please check your network connection.") from None

    try:
        data = response.json()
    except ValueError:
        raise FirebaseError("Invalid response from Firebase server.") from None

    if not isinstance(data, dict):
        raise FirebaseError("Malformed response from Firebase server.")

    if response.ok:
        return data

    error = data.get("error", {})
    code = str(error.get("message", "")) if isinstance(error, dict) else ""

    if any(item in code for item in ("TOKEN_EXPIRED", "INVALID_ID_TOKEN", "USER_DISABLED")) or response.status_code == 401:
        raise FirebaseError("Session has expired. Please sign in again.", sign_in_again=True)
    if "EMAIL_EXISTS" in code:
        raise FirebaseError("This email is already registered. Please sign in.")
    if "OPERATION_NOT_ALLOWED" in code:
        raise FirebaseError("Please enable Email/Password provider in Firebase Console Authentication.")
    if "WEAK_PASSWORD" in code or "PASSWORD_DOES_NOT_MEET_REQUIREMENTS" in code:
        raise FirebaseError("Password is too weak (minimum 6 characters).")
    if "INVALID_EMAIL" in code:
        raise FirebaseError("Invalid email address format.")
    if any(item in code for item in ("INVALID_LOGIN_CREDENTIALS", "INVALID_PASSWORD", "EMAIL_NOT_FOUND")):
        raise FirebaseError("Authentication failed. Please check your email or password.")
    if "TOO_MANY_ATTEMPTS" in code or response.status_code == 429:
        raise FirebaseError("Too many attempts. Please try again later.")
    if response.status_code == 403:
        raise FirebaseError("Access denied. Please verify your Firebase API key.")
    if "API_KEY" in code or "PROJECT_NOT_FOUND" in code or response.status_code == 404:
        raise FirebaseError("Invalid FIREBASE_API_KEY or FIREBASE_PROJECT_ID in .env.")

    raise FirebaseError(f"Firebase error: {code if code else 'Unknown error'}")


def _authenticate(action, email, password):
    validate_firebase_config()
    email = email.strip()
    if not email or not password:
        raise FirebaseError("Please enter both email and password.")
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:{action}"
    return _request(
        "POST",
        url,
        params={"key": FIREBASE_API_KEY.strip()},
        json={"email": email, "password": password, "returnSecureToken": True},
    )


def create_account(email, password):
    """Create a new user account."""
    _authenticate("signUp", email, password)


def sign_in(email, password):
    """Authenticate user with email and password and return session data."""
    data = _authenticate("signInWithPassword", email, password)
    try:
        user = {
            "uid": data["localId"],
            "email": data["email"],
            "id_token": data["idToken"],
            "expires_at": time.time() + int(data["expiresIn"]),
        }
        if not all(isinstance(user[k], str) and user[k] for k in ("uid", "email", "id_token")):
            raise ValueError
    except (KeyError, TypeError, ValueError):
        raise FirebaseError("Incomplete response received during sign in.") from None
    return user

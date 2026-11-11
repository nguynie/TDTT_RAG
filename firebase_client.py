"""Firebase Authentication client using REST API.
Reused and adapted from Lab 3.
"""

import time
import requests

from config import FIREBASE_API_KEY, FIREBASE_PROJECT_ID

REQUEST_TIMEOUT = 15


class FirebaseError(Exception):
    """Safe exception message to display in UI without exposing credentials."""

    def __init__(self, message, sign_in_again=False):
        super().__init__(message)
        self.sign_in_again = sign_in_again


def validate_firebase_config():
    """Verify Firebase environment variables are populated."""
    if not FIREBASE_PROJECT_ID.strip() or not FIREBASE_API_KEY.strip():
        raise FirebaseError("Vui lòng cấu hình FIREBASE_PROJECT_ID và FIREBASE_API_KEY trong file .env.")
    if any(c in FIREBASE_PROJECT_ID for c in "/ ?#"):
        raise FirebaseError("FIREBASE_PROJECT_ID phải là ID từ Firebase Console, không phải URL hay project name.")


def _request(method, url, **kwargs):
    """Send one request safely."""
    try:
        response = requests.request(method, url, timeout=REQUEST_TIMEOUT, **kwargs)
    except requests.RequestException:
        raise FirebaseError("Không thể kết nối đến máy chủ Firebase. Vui lòng kiểm tra mạng.") from None

    try:
        data = response.json()
    except ValueError:
        raise FirebaseError("Máy chủ Firebase phản hồi không hợp lệ.") from None

    if not isinstance(data, dict):
        raise FirebaseError("Phản hồi Firebase không đúng định dạng.")

    if response.ok:
        return data

    error = data.get("error", {})
    code = str(error.get("message", "")) if isinstance(error, dict) else ""

    if any(item in code for item in ("TOKEN_EXPIRED", "INVALID_ID_TOKEN", "USER_DISABLED")) or response.status_code == 401:
        raise FirebaseError("Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.", sign_in_again=True)
    if "EMAIL_EXISTS" in code:
        raise FirebaseError("Email này đã được đăng ký. Vui lòng chọn Đăng nhập.")
    if "OPERATION_NOT_ALLOWED" in code:
        raise FirebaseError("Vui lòng bật Email/Password Provider trong Firebase Console > Authentication.")
    if "WEAK_PASSWORD" in code or "PASSWORD_DOES_NOT_MEET_REQUIREMENTS" in code:
        raise FirebaseError("Mật khẩu quá yếu (tối thiểu 6 ký tự).")
    if "INVALID_EMAIL" in code:
        raise FirebaseError("Địa chỉ email không hợp lệ.")
    if any(item in code for item in ("INVALID_LOGIN_CREDENTIALS", "INVALID_PASSWORD", "EMAIL_NOT_FOUND")):
        raise FirebaseError("Đăng nhập thất bại. Kiểm tra lại email hoặc mật khẩu.")
    if "TOO_MANY_ATTEMPTS" in code or response.status_code == 429:
        raise FirebaseError("Quá nhiều yêu cầu. Vui lòng đợi trong giây lát.")
    if response.status_code == 403:
        raise FirebaseError("Truy cập bị từ chối. Kiểm tra lại thiết lập Firebase API Key.")
    if "API_KEY" in code or "PROJECT_NOT_FOUND" in code or response.status_code == 404:
        raise FirebaseError("Kiểm tra lại FIREBASE_API_KEY và FIREBASE_PROJECT_ID trong .env.")

    raise FirebaseError(f"Lỗi Firebase: {code if code else 'Không xác định'}")


def _authenticate(action, email, password):
    validate_firebase_config()
    email = email.strip()
    if not email or not password:
        raise FirebaseError("Vui lòng nhập cả email và mật khẩu.")
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:{action}"
    return _request(
        "POST",
        url,
        params={"key": FIREBASE_API_KEY.strip()},
        json={"email": email, "password": password, "returnSecureToken": True},
    )


def create_account(email, password):
    """Create an account with email and password."""
    _authenticate("signUp", email, password)


def sign_in(email, password):
    """Sign in with email and password, returning session user info."""
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
        raise FirebaseError("Đăng nhập nhận phản hồi không đầy đủ.") from None
    return user

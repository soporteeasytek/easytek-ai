"""
SSL certificate fix for macOS Python environments.

Uses truststore to hook into the OS native trust store (macOS Keychain),
which resolves the common CERTIFICATE_VERIFY_FAILED error.

Import this module and call apply() early (before making HTTP requests).
"""


def apply():
    """Inject OS-native trust store into Python's ssl module."""
    try:
        import truststore
        truststore.inject_into_ssl()
    except ImportError:
        pass

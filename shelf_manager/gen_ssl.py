"""สร้าง self-signed certificate สำหรับ HTTPS — รันครั้งเดียว"""
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime, ipaddress, socket
from pathlib import Path

key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

# หา local IP อัตโนมัติ
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
except Exception:
    local_ip = "127.0.0.1"

subject = x509.Name([
    x509.NameAttribute(NameOID.COMMON_NAME, "VitroShelf"),
])
cert = (
    x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(subject)
    .public_key(key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.datetime.utcnow())
    .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=3650))
    .add_extension(x509.SubjectAlternativeName([
        x509.DNSName("localhost"),
        x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
        x509.IPAddress(ipaddress.IPv4Address(local_ip)),
    ]), critical=False)
    .sign(key, hashes.SHA256())
)

out = Path(__file__).parent
(out / "cert.pem").write_bytes(cert.public_bytes(serialization.Encoding.PEM))
(out / "key.pem").write_bytes(key.private_bytes(
    serialization.Encoding.PEM,
    serialization.PrivateFormat.TraditionalOpenSSL,
    serialization.NoEncryption(),
))
print(f"Done — cert valid 10 years")
print(f"Local IP included: {local_ip}")
print(f"Saved: cert.pem, key.pem")

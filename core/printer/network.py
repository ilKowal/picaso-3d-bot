import socket
from core.config import update_ip

def send_request(ip : str, port : int, request_data : bytes, timeout: float = 5.0):

    response = _try_send(ip, port, request_data, timeout)
    if response:
        return response

    # Если по IP не сработало, пробуем через broadcast
    ip, response = _broadcast_request(port, request_data, timeout)
    if ip and response:
        update_ip(ip)
        return response

    return False


def _try_send(ip: str, port: int, request_data: bytes, timeout: float):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(timeout)
        try:
            sock.sendto(request_data, (ip, port))
            data, _ = sock.recvfrom(1024)
            return data
        except Exception:
            return None


def _broadcast_request(port: int, request_data: bytes, timeout: float):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(timeout)
        try:
            sock.sendto(request_data, ('255.255.255.255', port))
            data, addr = sock.recvfrom(1024)
            return addr[0], data
        except Exception:
            return None, None
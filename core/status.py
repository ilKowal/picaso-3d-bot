from core.storage import save_status
from core.printer.network import send_request
from core.printer.parser import PrinterStatus, parse_printer_data


def get_status(ip : str, port : int, request_data : bytes) -> PrinterStatus:
    raw_data = send_request(ip, port, request_data)
    if not raw_data:
        print('Ошибка получения данных от принтера')
        return None
    try:
        # return None
        status: PrinterStatus = parse_printer_data(raw_data)
        save_status(status)
        return status
    except Exception as e:
        print(f'Ошибка парсинга: {e}')
       
        return None

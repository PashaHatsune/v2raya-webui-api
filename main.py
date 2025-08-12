import argparse

from loguru import logger

from .src.connection import connect_server, off_v2raya, on_v2raya
from .src.get_subscriptions import get_subscriptions
from .src.ping import ping_all_servers


def main():
    parser = argparse.ArgumentParser(description="V2ray automation CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("on", help="Включить V2ray")
    subparsers.add_parser("off", help="Выключить V2ray")
    subparsers.add_parser("ping", help="Пинговать все сервера")
    subparsers.add_parser("list", help="Показать список серверов")

    connect_parser = subparsers.add_parser("connect", help="Подключиться к серверу")
    connect_parser.add_argument("server_id", type=int, help="ID сервера")
    connect_parser.add_argument("--sub", type=int, default=0, help="Индекс подписки (sub_index)")
    connect_parser.add_argument("--outbound", default="proxy", help="Тип исходящего подключения")

    args = parser.parse_args()

    if args.command == "on":
        if on_v2raya():
            logger.info("V2ray включен")
        else:
            logger.error("Не удалось включить V2ray")
    elif args.command == "off":
        if off_v2raya():
            logger.info("V2ray выключен")
        else:
            logger.error("Не удалось выключить V2ray")
    elif args.command == "ping":
        ping_all_servers()
    elif args.command == "list":
        servers = get_subscriptions()
        if servers:
            logger.info(f"Найдено серверов: {len(servers)}")
            for srv in servers:
                logger.info(f"{srv['name']} | {srv['id']} | sub_index={srv.get('sub_index', 0)}")
            
    elif args.command == "connect":
        result = connect_server(args.server_id, sub_index=args.sub, outbound=args.outbound)
        logger.info(f"Результат подключения: {result}")
    else:
        parser.print_help()


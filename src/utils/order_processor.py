def load_orders_from_file(filename):
    try:
        with open(filename, encoding='utf-8') as file:
            orders = []
            for line in file:
                orders.append(line.strip())
            return orders
    except FileNotFoundError:
        print(f'Файл {filename} не найден')
        return []


def calculate_order_total(price, discount_rate):
    return round(price * (1 - discount_rate), 2)


def get_discount_by_total(total):
    discount = 0
    if total <=0:
        discount = 0
    else:
        if total > 10000:
            discount = 0.15
        elif total > 5000:
            discount = 0.10
        else:
            discount = 0.05
    return discount


def process_orders(orders_data):
    result = []

    for order in orders_data:
        try:
            parts = order.split(':')
            if len(parts) == 4:
                total = int(parts[1].strip())
                discount_amount = get_discount_by_total(total)
                new_total = calculate_order_total(total, discount_amount)
                d = {
                    'order_id': parts[0].strip(),
                    'total': new_total,
                    'status': parts[2].strip(),
                    'user': parts[3].strip()
                }
                result.append(d)
            else:
                print('Неверный формат строки', order)
        except ValueError:
            print('Неверный формат строки', total)

    return result


def analyze_orders(processed_orders):
    stats = {
        'total_orders': 0,
        'total_sum': 0,
        'by_status': {},
        'unique_users': set()
    }
    order_status = {}

    for order in processed_orders:
        stats['total_orders'] = len(processed_orders)
        stats['total_sum'] += order['total']
        order_status[order['status']] = order_status.get(order['status'], 0) + 1
        stats['by_status'] = order_status
        stats['unique_users'].add(order['user'])
    stats['unique_users'] = list(stats['unique_users'])
    
    return stats


def process_order_file(input_file, output_file):
    orders = load_orders_from_file(input_file)
    processed_orders = process_orders(orders)
    stats = analyze_orders(processed_orders)
    by_status = stats['by_status']
    result = [
        f'Обработано заказов: {stats['total_orders']}',
        f'Общая сумма: {stats['total_sum']} руб.',
        f'По статусам: {', '.join(f'{k}: {v}' for k, v in by_status.items())}',
        f'Уникальных пользователей: {len(stats['unique_users'])}'
    ]
    
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(result))



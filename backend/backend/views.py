from django.shortcuts import render
from django.db import connection

def get_all(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM backend_customer")
        customers = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM backend_order WHERE YEAR(order_date) = 2023 AND MONTH(order_date) = 1")
        january_orders = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT backend_order.*, backend_customer.first_name, backend_customer.last_name, backend_customer.email
            FROM backend_order
            JOIN backend_customer ON backend_order.customer_id = backend_customer.customer_id
        """)
        orders_with_customer_details = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT backend_product.product_name, backend_orderitem.quantity
            FROM backend_orderitem
            JOIN backend_product ON backend_orderitem.product_id = backend_product.product_id
            WHERE backend_orderitem.order_id = 1
        """)
        products_in_order = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT backend_customer.customer_id, backend_customer.first_name, backend_customer.last_name, 
                   SUM(backend_product.price * backend_orderitem.quantity) AS TotalSpent
            FROM backend_customer
            JOIN backend_order ON backend_customer.customer_id = backend_order.customer_id
            JOIN backend_orderitem ON backend_order.order_id = backend_orderitem.order_id
            JOIN backend_product ON backend_orderitem.product_id = backend_product.product_id
            GROUP BY backend_customer.customer_id, backend_customer.first_name, backend_customer.last_name
        """)
        total_spent_by_customer = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT backend_product.product_id, backend_product.product_name, 
                   SUM(backend_orderitem.quantity) AS TotalOrdered
            FROM backend_orderitem
            JOIN backend_product ON backend_orderitem.product_id = backend_product.product_id
            GROUP BY backend_product.product_id, backend_product.product_name
            ORDER BY TotalOrdered DESC
            LIMIT 1
        """)
        most_popular_product = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DATE_FORMAT(order_date, '%Y-%m') AS Month, 
                   COUNT(*) AS TotalOrders, 
                   SUM(backend_product.price * backend_orderitem.quantity) AS TotalSales
            FROM backend_order
            JOIN backend_orderitem ON backend_order.order_id = backend_orderitem.order_id
            JOIN backend_product ON backend_orderitem.product_id = backend_product.product_id
            WHERE YEAR(order_date) = 2023
            GROUP BY Month
        """)
        monthly_sales = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT backend_customer.customer_id, backend_customer.first_name, backend_customer.last_name, 
                   SUM(backend_product.price * backend_orderitem.quantity) AS TotalSpent
            FROM backend_customer
            JOIN backend_order ON backend_customer.customer_id = backend_order.customer_id
            JOIN backend_orderitem ON backend_order.order_id = backend_orderitem.order_id
            JOIN backend_product ON backend_orderitem.product_id = backend_product.product_id
            GROUP BY backend_customer.customer_id, backend_customer.first_name, backend_customer.last_name
            HAVING TotalSpent > 1000
        """)
        big_spender_customers = cursor.fetchall()

    context = {
        'customers': customers,
        'january_orders': january_orders,
        'orders_with_customer_details': orders_with_customer_details,
        'products_in_order': products_in_order,
        'total_spent_by_customer': total_spent_by_customer,
        'most_popular_product': most_popular_product,
        'monthly_sales': monthly_sales,
        'big_spender_customers': big_spender_customers
    }
    print(big_spender_customers)
    return render(request, 'all.html', context)

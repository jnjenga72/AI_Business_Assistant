sales = [
    {"product": "Laptop", "quantity": 2, "price": 60000},
    {"product": "Phone", "quantity": 5, "price": 25000},
    {"product": "Laptop", "quantity": 1, "price": 60000},
    {"product": "Tablet", "quantity": 3, "price": 30000},
]


def calculate_total_sales():
    return sum(
        item["quantity"] * item["price"]
        for item in sales
    )


def get_top_product():
    revenue = {}

    for item in sales:
        product = item["product"]
        amount = item["quantity"] * item["price"]

        revenue[product] = revenue.get(product, 0) + amount

    top = max(revenue, key=revenue.get)

    return {
        "product": top,
        "revenue": revenue[top]
    }


def get_product_revenue(product_name):
    total = 0

    for item in sales:
        if item["product"].lower() == product_name.lower():
            total += item["quantity"] * item["price"]

    return {
        "product": product_name,
        "revenue": total
    }

def stats_cart(cart):
    total_amount = 0
    total_quantity = 0 
    print(cart)
    for p_value in cart.values():
        
        total_quantity += int(p_value['quantity'])
        total_amount += p_value['price'] * total_quantity

    return {
        'total_amount': total_amount,
        'total_quantity': total_quantity
    }

    #get total_amount & total_quantity
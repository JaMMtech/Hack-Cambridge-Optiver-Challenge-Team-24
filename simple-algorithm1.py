from optibook.synchronous_client import Exchange
import time
import logging
logging.getLogger('client').setLevel('ERROR')

print("Setup was successful.")

# connect to the exchange
e = Exchange()
a = e.connect()

# define instruments
STOCK_A_ID = 'PHILIPS_A'
STOCK_B_ID = 'PHILIPS_B'

idarray = [STOCK_A_ID, STOCK_B_ID]

instrument_id = STOCK_A_ID

order_bookA = e.get_last_price_book(STOCK_A_ID)
order_bookB = e.get_last_price_book(STOCK_B_ID)
best_bid_priceA = order_bookA.bids[0].price
best_bid_priceB = order_bookB.bids[0].price

if best_bid_priceA >= best_bid_priceB:
    buy_id = STOCK_A_ID
else:
    buy_id = STOCK_B_ID
    

    

#print(f"CHOSEN INSTRUMENT ID: {instrument_id}")


# Insert bid limit order - This trades against any current orders, and any remainders become new resting orders in the book
# Use this to buy.
#result = e.insert_order(buy_id, price=3000, volume=21, side='bid', order_type='limit')
#print(f"Order Id: {result}")

# Insert ask limit order - This trades against any current orders, and any remainders become new resting orders in the book
# Use this to sell.
#result = e.insert_order(instrument_id, price=3000, volume=1, side='ask', order_type='limit')
#print(f"Order Id: {result}")


#result = e.insert_order(instrument_id, price=, volume=1, side='ask', order_type='ioc')
#print(f"Order Id: {result}")

print()

while True:
    positions = e.get_positions()   
    for p in positions:
        print(f'POSITIONS : {positions[p]}')
        try:
            if positions[p] > 0:
                sell_id = p
                order_bookP = e.get_last_price_book(sell_id)
                best_bid_priceP = order_bookP.bids[0].price
                result = e.insert_order(sell_id, price=best_bid_priceP, volume=1, side='ask', order_type='ioc')
                print(f"Order Id: {result}")
            elif positions[p] <= 10:
                order_bookP = e.get_last_price_book(buy_id)
                best_bid_priceP = order_bookP.bids[0].price
                result = e.insert_order(buy_id, price=best_bid_priceP, volume=1, side='bid', order_type='ioc')
                print(f"Order Id: {result}")
        except:
            continue
    
        
    print()
    for stock_id in idarray:
        print(f'ID: {stock_id}')
        
        print("orders:")
        orders = e.get_outstanding_orders(stock_id)
        for o in orders.values():
            print(o)
            
        #print("tradeticks:")
        #tradeticks = e.get_trade_tick_history(stock_id)
        #for t in tradeticks:
        #    print(t)
                
        print("order book:")
        book = e.get_last_price_book(stock_id)
        print(book)
        
        print()
    
    
    # Returns all current positions
    print("all current positions:")
    positions = e.get_positions()
    for p in positions:
        print(p, positions[p])    
    
    print("all current positions with cash invested:")
    # Returns all current positions with cash invested
    positions = e.get_positions_and_cash()
    for p in positions:
        print(p, positions[p])
        
    print(f'PnL: {e.get_pnl()}') #print PnL

    time.sleep(0.1)

print("end")
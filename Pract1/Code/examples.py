# Extract Variable

# До рефакторингу
async def cart_edit(bot: Bot, callback_query: CallbackQuery):
    is_actual = await checking_actual_quantity(
        bot, callback_query.from_user.id, callback_query.message.chat.id
    )
    if not is_actual:
        await cart_page_creation(
            bot,
            callback_query.message.chat.id,
            callback_query.from_user.id,
            callback_query.message.message_id,
            is_actual,
        )
        return

    button_prefix = "edit_product_"
    back_button_name = "‹ Cart"
    back_button_callback = "cart"

    text = await cart_edit_text(
        bot,
        callback_query.message.chat.id,
        callback_query.from_user.id,
        callback_query.message.message_id,
    )
    products_in_cart = await products_in_cart_info(callback_query.from_user.id)

    if not products_in_cart:
        await cart_page(
            bot,
            callback_query.message.chat.id,
            callback_query.from_user.id,
            callback_query.message.message_id,
        )
        return
        
# Після рефакторингу
async def cart_edit(bot: Bot, callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id

    is_actual = await checking_actual_quantity(bot, user_id, chat_id)
    if not is_actual:
        await cart_page_creation(bot, chat_id, user_id, message_id, is_actual)
        return

    button_prefix = "edit_product_"
    back_button_name = "‹ Cart"
    back_button_callback = "cart"

    text = await cart_edit_text(bot, chat_id, user_id, message_id)
    products_in_cart = await products_in_cart_info(user_id)

    if not products_in_cart:
        await cart_page(bot, chat_id, user_id, message_id)
        return


# Replace Error Code with Exception

# До рефакторингу
class BankAccount:
    def __init__(self, balance):
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            return -1
        self.balance -= amount
        return 0

def perform_withdrawal(account, amount):
    result = account.withdraw(amount)
    if result == -1:
        print(f"Помилка: недостатньо коштів для зняття {amount}")
    else:
        print(f"Знято {amount}, залишок {account.balance}")


# Після рефакторингу
class InsufficientFunds(Exception):
    pass

class BankAccount:
    def __init__(self, balance):
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFunds(f"Недостатньо коштів для зняття {amount}")
        self.balance -= amount

def perform_withdrawal(account, amount):
    try:
        account.withdraw(amount)
        print(f"Знято {amount}, залишок {account.balance}")
    except InsufficientFunds as e:
        print(f"Помилка: {e}")


# Introduce Null Object

# До рефакторингу
async def order_creation(callback_query: CallbackQuery, bot: Bot, user_id: int, chat_id: int):
    order_id = await create_order(user_id)
    order_id = order_id[0]['create_order']

    if order_id is None:
        is_actual = await checking_actual_quantity(bot, user_id, chat_id)
        if is_actual:
            await order_creation_error(bot, chat_id)
        else:
            await order_confirmation_content(callback_query, bot, is_actual)

    return order_id

# Після рефакторингу
class Order:
    def __init__(self, order_id):
        self.order_id = order_id

    async def handle_creation_result(self, bot, user_id, chat_id):
        return self.order_id

class NullOrder(Order):
    async def handle_creation_result(self, bot, user_id, chat_id):
        is_actual = await checking_actual_quantity(bot, user_id, chat_id)
        if is_actual:
            await order_creation_error(bot, chat_id)
        else:
            await order_confirmation_content(None, bot, is_actual)
        return None  

async def create_order(user_id) -> Order:
    order_data = await some_database_call(user_id)
    if order_data and order_data[0]['create_order']:
        return Order(order_data[0]['create_order'])
    return NullOrder()

async def order_creation(callback_query: CallbackQuery, bot: Bot, user_id: int, chat_id: int):
    order = await create_order(user_id)
    result = await order.handle_creation_result(bot, user_id, chat_id)
    return result

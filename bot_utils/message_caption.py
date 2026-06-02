def text_for_caption(name, description, base_price):
    """текст под изображением товара"""
    text=(
        f"<b>{name}</b>\n"
        f"<b>описание :{description}</b>\n"
        f"<b>цена :{float(base_price):.2f} ₽</b>\n"
    )
    return text

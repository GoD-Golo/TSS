from dataclasses import dataclass


@dataclass(frozen=True)
class CartItem:
    name: str
    unit_price: float
    quantity: int


class ShoppingCart:
    """Calculates the final total for an online shopping cart."""

    VAT_RATE = 0.19
    DISCOUNT_THRESHOLD = 500.0
    DISCOUNT_RATE = 0.10
    FREE_SHIPPING_THRESHOLD = 300.0
    STANDARD_SHIPPING = 20.0

    def __init__(self):
        self._items = []

    def add_item(self, name: str, unit_price: float, quantity: int = 1) -> None:
        if not name or not name.strip():
            raise ValueError("name must not be empty")
        if unit_price <= 0:
            raise ValueError("unit_price must be positive")
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        if not isinstance(quantity, int):
            raise TypeError("quantity must be an integer")

        self._items.append(CartItem(name.strip(), unit_price, quantity))

    def subtotal(self) -> float:
        total = sum(item.unit_price * item.quantity for item in self._items)
        return round(total, 2)

    def discount(self) -> float:
        subtotal = self.subtotal()
        if subtotal >= self.DISCOUNT_THRESHOLD:
            return round(subtotal * self.DISCOUNT_RATE, 2)
        return 0.0

    def shipping_cost(self) -> float:
        subtotal_after_discount = self.subtotal() - self.discount()
        if subtotal_after_discount == 0:
            return 0.0
        if subtotal_after_discount >= self.FREE_SHIPPING_THRESHOLD:
            return 0.0
        return self.STANDARD_SHIPPING

    def vat(self) -> float:
        taxable_amount = self.subtotal() - self.discount()
        return round(taxable_amount * self.VAT_RATE, 2)

    def total(self) -> float:
        final_total = self.subtotal() - self.discount() + self.vat() + self.shipping_cost()
        return round(final_total, 2)

    def classify_cart(self) -> str:
        subtotal = self.subtotal()
        if subtotal == 0:
            return "gol"
        if subtotal < self.FREE_SHIPPING_THRESHOLD:
            return "standard"
        if subtotal < self.DISCOUNT_THRESHOLD:
            return "transport gratuit"
        return "discount aplicat"

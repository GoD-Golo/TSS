import unittest

from tss_project import ShoppingCart


class TestShoppingCartBaseSuite(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()

    def test_empty_cart_has_zero_total(self):
        self.assertEqual(self.cart.subtotal(), 0.0)
        self.assertEqual(self.cart.total(), 0.0)

    def test_add_single_item_and_compute_subtotal(self):
        self.cart.add_item("Mouse", 100.0, 2)
        self.assertEqual(self.cart.subtotal(), 200.0)

    def test_invalid_price_is_rejected(self):
        with self.assertRaises(ValueError):
            self.cart.add_item("Keyboard", 0, 1)

    def test_standard_shipping_is_added_for_small_order(self):
        self.cart.add_item("Book", 100.0, 1)
        self.assertEqual(self.cart.shipping_cost(), 20.0)
        self.assertEqual(self.cart.total(), 139.0)

    def test_large_order_gets_discount(self):
        self.cart.add_item("Monitor", 500.0, 1)
        self.assertEqual(self.cart.discount(), 50.0)
        self.assertEqual(self.cart.total(), 535.5)


if __name__ == "__main__":
    unittest.main()

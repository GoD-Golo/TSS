import unittest

from tss_project import ShoppingCart


class TestShoppingCartExtraSuite(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()

    def test_empty_name_is_rejected(self):
        with self.assertRaises(ValueError):
            self.cart.add_item("", 10.0, 1)
        with self.assertRaises(ValueError):
            self.cart.add_item("   ", 10.0, 1)

    def test_negative_price_is_rejected(self):
        with self.assertRaises(ValueError):
            self.cart.add_item("Cable", -1.0, 1)

    def test_quantity_must_be_positive_integer(self):
        with self.assertRaises(ValueError):
            self.cart.add_item("Cable", 10.0, 0)
        with self.assertRaises(ValueError):
            self.cart.add_item("Cable", 10.0, -1)
        with self.assertRaises(TypeError):
            self.cart.add_item("Cable", 10.0, 1.5)

    def test_item_name_is_trimmed(self):
        self.cart.add_item("  Mouse  ", 50.0, 1)
        self.assertEqual(self.cart._items[0].name, "Mouse")

    def test_free_shipping_boundary(self):
        self.cart.add_item("Chair", 300.0, 1)
        self.assertEqual(self.cart.discount(), 0.0)
        self.assertEqual(self.cart.shipping_cost(), 0.0)
        self.assertEqual(self.cart.total(), 357.0)

    def test_order_below_free_shipping_boundary_pays_shipping(self):
        self.cart.add_item("Chair", 299.99, 1)
        self.assertEqual(self.cart.shipping_cost(), 20.0)

    def test_discount_boundary(self):
        self.cart.add_item("Laptop", 500.0, 1)
        self.assertEqual(self.cart.discount(), 50.0)
        self.assertEqual(self.cart.shipping_cost(), 0.0)

    def test_order_below_discount_boundary_has_no_discount(self):
        self.cart.add_item("Laptop", 499.99, 1)
        self.assertEqual(self.cart.discount(), 0.0)

    def test_vat_is_computed_after_discount(self):
        self.cart.add_item("Laptop", 1000.0, 1)
        self.assertEqual(self.cart.discount(), 100.0)
        self.assertEqual(self.cart.vat(), 171.0)
        self.assertEqual(self.cart.total(), 1071.0)

    def test_multiple_items_are_accumulated(self):
        self.cart.add_item("Mouse", 100.0, 2)
        self.cart.add_item("Cable", 25.5, 2)
        self.assertEqual(self.cart.subtotal(), 251.0)
        self.assertEqual(self.cart.total(), 318.69)

    def test_cart_classification_boundaries(self):
        self.assertEqual(self.cart.classify_cart(), "gol")

        self.cart.add_item("Book", 299.99, 1)
        self.assertEqual(self.cart.classify_cart(), "standard")

        self.cart = ShoppingCart()
        self.cart.add_item("Chair", 300.0, 1)
        self.assertEqual(self.cart.classify_cart(), "transport gratuit")

        self.cart = ShoppingCart()
        self.cart.add_item("Laptop", 500.0, 1)
        self.assertEqual(self.cart.classify_cart(), "discount aplicat")


if __name__ == "__main__":
    unittest.main()

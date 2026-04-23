from pages.products_page import ProductsPage



    def test_product_page_logo(login):
        driver = login("standard_user", "secret_sauce")
        products = ProductsPage(driver)  # ✅ create object
        assert products.verifylogo() == "Swag Labs"


    def test_products(login):
        driver = login("standard_user", "secret_sauce")
        products = ProductsPage(driver)
        assert products.verifyproducts() == "Sauce Labs Backpack"

    def test_product_page(login):
        driver = login("standard_user", "secret_sauce")
        products = ProductsPage(driver)
        assert products.verifyimg() == "Swag Labs"

    def test_products(login):
        driver = login("standard_user", "secret_sauce")
        products = ProductsPage(driver)
        assert products.verifyaddtocart() == "Add to cart"






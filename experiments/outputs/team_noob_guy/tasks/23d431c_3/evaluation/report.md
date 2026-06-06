──────────────────────────────────────────────────────────── Overall Stats ─────────────────────────────────────────────────────────────
Num Passed Tests : 5
Num Failed Tests : 3
Num Total  Tests : 8
──────────────────────────────────────────────────────────────── Passes ────────────────────────────────────────────────────────────────
>> Passed Requirement
assert answers match.
>> Passed Requirement
assert model changes match
amazon.Order, amazon.OrderItem, amazon.Product,
file_system.File, file_system.Directory, gmail.GlobalEmailThread, gmail.Attachment,
gmail.Email, gmail.UserEmailThread, ignoring amazon.CartEntry, amazon.Address.
>> Passed Requirement
assert there is 1 new amazon.Order using models.changed_records.
>> Passed Requirement
assert the ordered product has price <= data.public.max_price.
>> Passed Requirement
assert 0 records have been updated or deleted from amazon.Address using models.changed_records.
──────────────────────────────────────────────────────────────── Fails ─────────────────────────────────────────────────────────────────
>> Failed Requirement
assert this new order has 1 quantity of a single product.
```python
with test(
    """
    assert this new order has 1 quantity of a single product.
    """
):
    order_items = order.order_items
    test.case(len(order_items), "==", 1)
    order_item = order_items[0]
```
----------
AssertionError:  5 == 1
>> Failed Requirement
assert the ordered product is of type data.public.product_type.
```python
with test(
    """
    assert the ordered product is of type data.public.product_type.
    """
):
    ordered_product = order.products[0]
    test.case(ordered_product.product_type, "==", public_data.product_type)
```
----------
AssertionError:  'tape measure' == 'watch'
>> Failed Requirement
assert the ordered product's seller is in data.private.trusted_seller_ids.
```python
with test(
    """
    assert the ordered product's seller is in data.private.trusted_seller_ids.
    """
):
    test.case(ordered_product.seller.id, "in", private_data.trusted_seller_ids)
```
----------
AssertionError:
19
in
[256, 131, 3, 4, 6, 7, 11, 139, 268, 14, 15, 145, 21, 285, 33, 162, 163, 36, 168, 170, 298, 42, 44, 302, 179, 310, 184, 57, 187, 62,
190, 64, 319, 70, 71, 198, 201, 74, 202, 78, 79, 81, 211, 87, 216, 102, 104, 109, 240, 120, 126]
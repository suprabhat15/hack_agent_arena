──────────────────────────────────────────────────────────── Overall Stats ─────────────────────────────────────────────────────────────
Num Passed Tests : 5
Num Failed Tests : 5
Num Total  Tests : 10
──────────────────────────────────────────────────────────────── Passes ────────────────────────────────────────────────────────────────
>> Passed Requirement
assert model changes match splitwise.Expense, splitwise.ExpenseShare, splitwise.Notification,
ignoring file_system.Directory, file_system.File.
>> Passed Requirement
obtain added, updated, removed splitwise.Expense records using models.changed_records,
and assert 0 were updated or removed.
>> Passed Requirement
assert all added expenses have payer_id of private_data.splitwise_user_id.
>> Passed Requirement
obtain added, updated, removed splitwise.ExpenseShare records using models.changed_records,
and assert 0 were updated or removed.
>> Passed Requirement
assert all added expense shares have expense_id matching the added expenses.
──────────────────────────────────────────────────────────────── Fails ─────────────────────────────────────────────────────────────────
>> Failed Requirement
assert answers match.
```python
with test(
    """
    assert answers match.
    """
):
    test.answer(predicted_answer, ground_truth_answer)
```
----------
AssertionError:  'cable bill 06-23 recorded' == 'null'
>> Failed Requirement
assert all added expenses have group_id matching private_data.group_id.
```python
with test(
    """
    assert all added expenses have group_id matching private_data.group_id.
    """
):
    test.case(set_of(added_expenses, "group_id"), "==", {private_data.group_id})
```
----------
AssertionError:  {None} == {5}

In left but not right:
[None]

In right but not left:
[5]
>> Failed Requirement
assert expense_description_to_amount obtained from added expenses
match the private_data.expense_description_to_amount.
```python
with test(
    """
    assert expense_description_to_amount obtained from added expenses
    match the private_data.expense_description_to_amount.
    """
):
    expense_description_to_amount = dict_of(added_expenses, "description", "amount")
    test.case(
```
----------
AssertionError:
{'cable bill 06-23': 89.0 ± 0.51}
==
Munch({'cable bill [06-23]': 186 ± 0.51, 'cable bill [05-23]': 117 ± 0.51, 'cable bill [04-23]': 153 ± 0.51, 'cable bill [03-23]': 146 ±
0.51, 'cable bill [02-23]': 200 ± 0.51, 'cable bill [01-23]': 164 ± 0.51})

Original values:
{'cable bill 06-23': 89.0}
==
Munch({'cable bill [06-23]': 186, 'cable bill [05-23]': 117, 'cable bill [04-23]': 153, 'cable bill [03-23]': 146, 'cable bill [02-23]':
200, 'cable bill [01-23]': 164})
>> Failed Requirement
assert member_ids from added expense shares from all unique expenses match
private_data.member_ids.
```python
with test(
    """
    assert member_ids from added expense shares from all unique expenses match
    private_data.member_ids.
    """
):
    expense_to_member_ids = dict_list_of(added_expense_shares, "expense_id", "debtor_id")
    list_of_member_ids = list(expense_to_member_ids.values())
```
----------
AssertionError:  [1, 2, 3] == [40, 46, 90]

In left but not right:
[1, 2, 3]

In right but not left:
[40, 46, 90]

Original values:
[2, 1, 3] == [90, 40, 46]
>> Failed Requirement
assert user_id_to_debt_amounts from added expense shares match
private_data.user_id_to_debt_amounts.
```python
with test(
    """
    assert user_id_to_debt_amounts from added expense shares match
    private_data.user_id_to_debt_amounts.
    """
):
    user_id_to_debt_amounts = defaultdict(list)
    for share in added_expense_shares:
```
----------
AssertionError:
{2: [29.67 ± 0.51], 1: [29.67 ± 0.51], 3: [29.67 ± 0.51]}
==
{90: [39.0 ± 0.51, 48.67 ± 0.51, 51.0 ± 0.51, 54.67 ± 0.51, 62.0 ± 0.51, 66.67 ± 0.51], 40: [39.0 ± 0.51, 48.67 ± 0.51, 51.0 ± 0.51,
54.67 ± 0.51, 62.0 ± 0.51, 66.67 ± 0.51], 46: [39.0 ± 0.51, 48.67 ± 0.51, 51.0 ± 0.51, 54.67 ± 0.51, 62.0 ± 0.51, 66.67 ± 0.51]}

Original values:
{2: [29.67], 1: [29.67], 3: [29.67]}
==
{90: [39.0, 48.67, 51.0, 54.67, 62.0, 66.67], 40: [39.0, 48.67, 51.0, 54.67, 62.0, 66.67], 46: [39.0, 48.67, 51.0, 54.67, 62.0, 66.67]}
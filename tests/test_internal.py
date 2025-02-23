from receipt_processor.internal import point_processor
from receipt_processor.models.receipt import Receipt, Item
from datetime import date

# unit tests for the internal functions that do the actual computation
mock_receipt = Receipt(
    retailer="M&M Corner Market",
    purchase_date=date(2022,3,20),
    purchase_time="14:33",
    items = [
        Item(short_description="Gatorade",price="2.25"),
        Item(short_description="Gatorade",price="2.25"),
        Item(short_description="Gatorade",price="2.25"),
        Item(short_description="Gatorade",price="2.25"),
    ],
    total="9.00"
)

mock_items =[
        Item(short_description="Gatorade",price="2.25"),
        Item(short_description="Gatorade",price="2.25"),
        Item(short_description="Gatorade",price="2.25"),
        Item(short_description=" ",price="2.25"),
        Item(short_description="Emils Cheese Pizza", price="12.25")
    ]

def test_calculate_name_points():
    points = point_processor.calculate_name_points('M&M Corner Market')
    assert points == 14

def test_calculate_whole_dollar_points():
    points = point_processor.calculate_whole_dollar_points('9.00')
    assert points == 50

def test_calculate_total_multiple_points():
    points = point_processor.calculate_total_multiple_points('9.00')
    assert points == 25

def test_calculate_day_points():
    points = point_processor.calculate_day_points('2022-03-21')
    assert points == 6

def test_calculate_time_points():
    points = point_processor.calculate_time_points('14:33')
    assert points == 10

def test_calculate_item_count_points():
    points = point_processor.calculate_item_count_points(mock_items)
    assert points == 10

def test_calculate_item_description_points():
    points = point_processor.calculate_item_description_points(mock_items[4])
    assert points == 3

def test_get_receipt_points():
    points = point_processor.get_receipt_points(mock_receipt)
    assert points == 109

# test alternate cases
def test_calculate_name_points_empty():
    points = point_processor.calculate_name_points(' ')
    assert points == 0

def test_calculate_name_points_symbols():
    points = point_processor.calculate_name_points('& %^*()#@')
    assert points == 0

def test_calculate_whole_dollar_points_valued():
    points = point_processor.calculate_whole_dollar_points('9.39')
    assert points == 0

def test_calculate_total_multiple_points_not_multiple():
    points = point_processor.calculate_total_multiple_points('9.13')
    assert points == 0

def test_calculate_day_points_even():
    points = point_processor.calculate_day_points('2022-03-20')
    assert points == 0

def test_calculate_time_points_out_of_range():
    points = point_processor.calculate_time_points('9:33')
    assert points == 0

def test_calculate_item_count_points_single():
    points = point_processor.calculate_item_count_points(mock_items[:1])
    assert points == 0

def test_calculate_item_description_points_empty():
    points = point_processor.calculate_item_description_points(mock_items[3])
    assert points == 0

def test_calculate_item_description_points_non_multiple():
    points = point_processor.calculate_item_description_points(mock_items[2])
    assert points == 0
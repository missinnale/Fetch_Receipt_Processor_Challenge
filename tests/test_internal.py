from receipt_processor.internal import point_processor
# unit tests for the internal functions that do the actual computation

mock_receipt = {
    "retailer": "M&M Corner Market",
    "purchaseDate": "2022-03-20",
    "purchaseTime": "14:33",
    "items": [
        {
        "shortDescription": "Gatorade",
        "price": "2.25"
        },{
        "shortDescription": "Gatorade",
        "price": "2.25"
        },{
        "shortDescription": "Gatorade",
        "price": "2.25"
        },{
        "shortDescription": "Gatorade",
        "price": "2.25"
        }
    ],
    "total": "9.00"
    }

mock_items =[
        {
        "shortDescription": "Gatorade",
        "price": "2.25"
        },{
        "shortDescription": "Gatorade",
        "price": "2.25"
        },{
        "shortDescription": "Gatorade",
        "price": "2.25"
        },{
        "shortDescription": "Gatorade",
        "price": "2.25"
        },{
        "shortDescription": "Emils Cheese Pizza",
        "price": "12.25"
        }
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
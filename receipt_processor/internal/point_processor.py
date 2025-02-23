import math
import datetime
import re
from receipt_processor.models.receipt import Receipt, Item


def get_receipt_points(receipt: Receipt) -> int:
    points = 0
    points += calculate_name_points(receipt.retailer)
    points += calculate_whole_dollar_points(receipt.total)
    points += calculate_total_multiple_points(receipt.total)
    points += calculate_day_points(str(receipt.purchase_date))
    points += calculate_time_points(receipt.purchase_time)
    points += calculate_item_count_points(receipt.items)
    for item in receipt.items:
        points += calculate_item_description_points(item)
    return points

# Rules

# One point for every alphanumeric character in the retailer name.
def calculate_name_points(name: str) -> int:
    return len(re.findall(r'\w', name))

# 50 points if the total is a round dollar amount with no cents.
def calculate_whole_dollar_points(receipt_total: str) -> int:
    if receipt_total[2:4] == "00":
        return 50
    return 0

# 25 points if the total is a multiple of 0.25.
# I assume that means a multiple of 25 cents, i.e. 25 cent, 50 cent, 75 cent, 1 dollar, divides by 0.25 with no remainder
def calculate_total_multiple_points(receipt_total: str) -> int:
    num_total = float(receipt_total)
    if num_total % 0.25 == 0:
        return 25
    return 0

# 5 points for every two items on the receipt.
def calculate_item_count_points(items: list[Item]) -> int:
    total_count = len(items)
    points_floored = (total_count // 2) * 5
    return points_floored

# If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
def calculate_item_description_points(item: Item) -> int:
    len_count = len(item.short_description.strip())
    if len_count and len_count % 3 == 0:
        points = float(item.price) * 0.2
        return math.ceil(points)
    return 0

# 6 points if the day in the purchase date is odd.
def calculate_day_points(purchase_date: str) -> int:
    if int(purchase_date[-2:]) % 2 == 1:
        return 6
    return 0

# 10 points if the time of purchase is after 2:00pm and before 4:00pm.
def calculate_time_points(purchase_time: str) -> int:
    if len(purchase_time) == 4:
        purchase_time = '0' + purchase_time
    time_purchased = datetime.time(int(purchase_time[0:2]), int(purchase_time[3:]))
    two_afternoon = datetime.time(14, 0)
    four_afternoon = datetime.time(16, 0)
    if time_purchased > two_afternoon and time_purchased < four_afternoon:
        return 10
    return 0
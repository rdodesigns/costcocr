""" Fuzzy Dictionary of Costco Receipt Codes.

Only contains the data structure codes, which is a fuzzy dictionary of
receipt code names to the actual names of the items.
"""
from fuzzy import FuzzyDict

codes = FuzzyDict({
    "MAR BSBSMOKE"  : "Barbecue Smoked Chicken Breast",
    "KS SEAWEED"    : "Kirkland Seaweed",
    "NAAN BREAD"    : "Naan Bread",
    "HABANERO SSG"  : "Habanero Sausage",
    "AID CHKN SSG"  : "Chicken Sausage",
    "PEPHOTPOCKET"  : "Hot Pockets",
    "FOOD WRAP"     : "Cling Wrap",
    "MORNING BUN"   : "Morning bun",
    "SABRA GR/CLA"  : "Sabra Classic/Garlic Hummus",
    "ORG. CARROTS"  : "Organic Carrots",
    "STIR FRY VEG"  : "Stir Fry Vegetables",
    "YAKISOBA"      : "Yakisoba",
    "HERB TURKEY"   : "Herb Turkey Breast Slices",
    "KS SALMON"     : "Kirkland Salmon Slices",
    "FUJI APPLES"   : "Fuji Apples",
    "SALMON BURGER" : "Salmon Burger Patties",
    "KS TUNA"       : "Kirkland Canned Tuna",
    "FIBER ONE"     : "Fiber One Granola Bar",
    "RAISIN BRAN"   : "Raisin Bran Cereal",
    "CHKN POTSTIK"  : "Chicken Potstickers",
    "PENNE PASTA"   : "Penne Pasta",
    "BLUE BISCUIT"  : "Belvita Blueberry Biscuits",
    "ZIPLOC SANDW"  : "Ziplock Sandwich Bags",
    "QUAKER OATS"   : "Quaker Oatmeal",
    "ORGCHIX/PROV"  : "Organic Chicken Provalone Sausages",
    "POWERC 2x150"  : "Power Vitamin C",
    "CASHEWS 2.5#"  : "Cashews",
    "CHOC CHUNK"    : "Chocolate Chunk Cookies",
    "FRZ GAL ZIPR"  : "Ziplock Gallon Freezer Bags",
})

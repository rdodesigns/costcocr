Internal Receipt Format
-----------------------

The internal receipt format is an attempt to make it simple to create both
readers for receipt data (manual entry, different OCR platforms) and writers
(JSON, CSV, XML, etc).


```
Receipt
    ( Meta {store = [], date = [], location = []} )
    ItemList
      [ Item
          ( Name "",
            Cost 0,
            Discount 0,
            Tax 0.0
          ),
        Item ...
      ]
```


Custom Writers
--------------

Custom writers can be created by defining the following functions, all of
which must return a string.

```python
def Receipt(body, meta): pass

def ItemList(s):
def ItemListSep(): pass

def Item(name, cost, discount, tax): pass
def Name(s): pass
def Cost(n): pass
def Discount(n): pass
def Tax(n): pass
```

Some functions have default implementations should they not be implemented.

```python
## For Name, one might want to use a conversion dictionary to turn the
## name into a human readable format.
def Name(s): return s

## For these functions, it might be desirable to constrain the number of
## decimal places.
def Cost(n): return str(n)
def Discount(n): return str(n)
def Tax(n): return str(n)
```

So, for example a simple csv writer could be defined as follows, where it
combines the item fields to make a simpler output.

```python
def Receipt(body, meta, variables):
    output = []

    def add(s) : output.append(s)

    if "store" in meta: add("# Store: {}".format(meta["store"]))
    if "date" in meta: add("# Date: {}".format(meta["date"]))
    if "location" in meta: add("# Location: {}".format(meta["location"]))

    add(body)

    return "\n".join(output)

def ItemList(s): return s
def ItemListSep(): return "\n"

## Could also be used to collapse the fields, or exclude some.
def Item(name, cost, discount, tax):
    return "{}, {}.format(name, cost)
```

Alternatively one can define overriding functions for the default functions.

```python
def Receipt(body, meta, variables):
    output = []

    def add(s) : output.append(s)

    if "store" in meta: add("# Store: {}".format(meta["store"]))
    if "date" in meta: add("# Date: {}".format(meta["date"]))
    if "location" in meta: add("# Location: {}".format(meta["location"]))

    add(body)

    return "\n".join(output)

def ItemList(s): return s
def ItemListSep(): return "\n"

## Could also be used to collapse the fields, or exclude some.
def Item(name, cost, discount, tax):
    return "{}, {}, {}, {}".format(name, cost, discount, tax)

## For Name, one might want to use a conversion dictionary to turn the
## name into a human readable format.
def Name(s): return s

## For these functions, it might be desirable to constrain the number of
## decimal places.
def Cost(n): return "${}".format(n)
def Discount(n): return "-${}".format(n)
def Tax(n): return "{}%".format(100*n)
```

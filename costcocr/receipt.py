"""Receipt internal representation.

Receipts are an intermediate representation (IR) that can be used to convert
receipts into other formats (such as CSV, JSON, etc). In addition, they
support iteration (for example, one could total a receipt).

A receipt looks like so when printed.

```
Receipt( {"store": "The Awesome Store",
          "location" : "Mars",
          "date" : "Feb 29th, 2049"},
        ItemList([
            Item("Food Name",
                 10.00, # Cost
                 2.00,  # Discount
                 9.00   #Tax
                 ),
            Item(...),
            ...
                ])
       )
```

Note that the string method for a Receipt (and its associated types) is
the same as its calling notation, meaning that receipts stored as a string
version of the IR format can be just eval'd in.

The `write` function defined in this module allows for the IR format to be
converted to a variety of output formats by just defining functions for
converting certain sections of the IR into strings. More information can be
found in the documentation for the `write` function.

The following types are defined in this module

- Receipt(dict, ItemList)
- ItemList([Items])
- Item(name, cost, discount, tax)

All of these support repr implementations that can be eval'd, as well as
equality.

In addition, the Receipt and ItemList types are interators.

The Item type has four fields (see above). The cost, discount, and tax
fields must all be numbers. The discount is a positive cash value (such as
$2.00), and the tax is the percentage (such as 9.00%).
"""
from numbers import Number
from toolz import curry

class Receipt(object):
    """Root class for receipt intermediate format.

    Receipt also supports the equality methods, iteration, and repr.

    Parameters
    ----------
    meta : dict
        A dictionary of metadata information.
    itemlist : ItemList
        A list of Items.

    Attributes
    ----------
    meta : dict
        The metadata passed into Receipt.
    itemlist : ItemList
        The list of items passed into Receipt.
    """
    def __init__(self, meta, itemlist):
        if type(meta) is not dict:
            raise TypeError("meta must be a dictionary")

        if type(itemlist) is not ItemList:
            raise TypeError("itemlist must be an ItemList")

        self._meta = meta
        self._itemlist = itemlist

    @property
    def meta(self):
        """The metadata for a receipt."""
        return self._meta

    @property
    def itemlist(self):
        """The list of Items for a receipt."""
        return self._itemlist

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "Receipt({}, {})".format(self._meta, self._itemlist)

    def __iter__(self):
        return iter(self._itemlist)

    def __eq__(self, other):
        if ((set(self.meta.items()) == set(other.meta.items())) and
           self.itemlist == other.itemlist):
            return True

        return False

    def __ne__(self, other):
        return not self == other


class ItemList(list):
    """A container for a list of items.

    This is basically just a list, but supports equality (the order is
    important for equality).

    Parameters
    ----------
    items : list or tuple of Items
        The Items in a receipt.
    """

    def __init__(self, items):

        if type(items) not in {list, tuple}:
            raise TypeError("items must be either a list or a tuple")

        if not all(type(item) is Item for item in items):
            raise TypeError("items must be a list of Items")

        list.__init__(self, items)

    def __repr__(self):
        return "ItemList({})".format(list.__repr__(self))

    def __eq__(self, other):
        if len(self) != len(other):
            return False

        if not all(a == b for a, b in zip(self, other)):
            return False

        return True

    def __ne__(self, other):
        return not self == other


class Item(object):
    """An item line on a receipt.

    Parameters
    ----------
    name : str
        The name of the item.
    cost : Number
        The cost of the item.
    discount : Number
        The amount of currency the item is reduced by. Positive quantity.
    tax : Number
        The tax rate for the item, in percent (for example, 9.00%)

    Attributes
    ----------
    name : str
        The name of the item.
    cost : Number
        The cost of the item.
    discount : Number
        The amount of currency the item is reduced by. Positive quantity.
    tax : Number
        The tax rate for the item, in percent (for example, 9.00%)
    total : Number
        The total for the item, as cost*(1 + tax) - discount
    """
    def __init__(self, name, cost, discount, tax):
        if type(name) is not str:
            raise TypeError("name must be a str")

        ## cost, discount, and tax all have the same properties.
        for v, s in ((cost, "cost"), (discount, "discount"), (tax, "tax")):

            if not isinstance(v, Number):
                raise TypeError("{} must be a Number.".format(s))

            if v < 0:
                raise ValueError("{} must be positive".format(s))

        self._name = name
        self._cost = cost
        self._discount = discount
        self._tax = tax

        self._total = (cost * (1 + tax)) - discount

    @property
    def name(self):
        """Name of the item"""
        return self._name

    @property
    def cost(self):
        """Cost of the item"""
        return self._cost

    @property
    def discount(self):
        """Discount of the item"""
        return self._discount

    @property
    def tax(self):
        """Tax of the item"""
        return self._tax

    @property
    def total(self):
        """Total for the item"""
        return self._total

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'Item("{}", {}, {}, {})'.format(self._name,
                self._cost, self._discount, self._tax)

    def __eq__(self, other):
        return (self.name == other.name and self.cost == other.cost and
            self.discount == other.discount and self.tax == other.tax)

    def __ne__(self, other):
        return not self == other


@curry
def write(convert_fs, variables, receipt):
    """Convert Receipt IR into a output format.

    Note that this function is curried.

    Takes in a dictionary defining how to convert each type inside a receipt
    into a output string. The conversion functions have the following
    declarations. Note that Item takes as input types whatever the output
    types of Cost, Discount, and Tax are.

    - def Receipt(meta : dict, body : str, variables : dict) -> str
    - def ItemList(s : str) -> str
    - def ItemListSep() -> str
    - def Item(name : str, cost : Cost, discount : Discount, tax : Tax) -> str

    The following are optional functions. Their default implementation (turn
    numbers into strings) is included in the declaration. They can return
    other types besides string as long as the Item function knows that how
    to deal with the associated type.

    - def Name(s : str) -> str: return s
    - def Cost(n : float) -> str : return str(s)
    - def Discount(n : float) -> str : return str(s)
    - def Tax(n : float) -> str : return str(s)


    Parameters
    ----------
    convert_fs : dict of (str, function)
        Conversion functions. This dictionary must at least contain the
        keys "Receipt", "Item", "ItemList", and "ItemListSep". Optional
        conversion functions are "Name", "Cost", "Discount", "Tax"
    variables : dict
        Variables to pass to the Receipt function. These will be passed in by
        someone, likely by the command line.
    receipt : Receipt
        The receipt to convert to an output format.

    Returns
    -------
    str
        A string of the output format.

    Example
    -------
    >>> def csvwriter():
    ...
    ...     def Receipt(meta, body, variables):
    ...         output = []
    ...
    ...         def add(s) : output.append(s)
    ...
    ...         if "store" in meta:
    ...             add("# Store: {}".format(meta["store"]))
    ...         if "date" in meta:
    ...             add("# Date: {}".format(meta["date"]))
    ...         if "location" in meta:
    ...             add("# Location: {}".format(meta["location"]))
    ...
    ...         add(body)
    ...
    ...         return "\n".join(output)
    ...
    ...     def ItemList(s): return s
    ...     def ItemListSep(): return "\n"
    ...
    ...     ## Could also be used to collapse the fields, or exclude some.
    ...     def Item(name, cost, discount, tax):
    ...         return "{}, {}, {}, {}".format(name, cost, discount, tax)
    ...
    ...     return {
    ...             "Receipt" : Receipt,
    ...             "ItemList" : ItemList,
    ...             "ItemListSep" : ItemListSep,
    ...             "Item" : Item,
    ...         }
    >>> r = Receipt({"store": "Costco",
    ...              "date": "Jan 27th",
    ...              "location": "Berkeley"},
    ...              ItemList([
    ...                  Item("Food 1", 10.00, 2.35, 9.00),
    ...                  Item("Food 2", 20.00, 4.00, 9.00)]))
    >>> print(write(csvwriter(), {}, r))
    # Store: Costco
    # Date: Jan 27th
    # Location: Berkeley
    Food 1, 10.0, 2.35, 9.0
    Food 2, 20.0, 4.0, 9.0
    """

    missing_fs = ({"Receipt", "Item", "ItemList", "ItemListSep"} -
            set(convert_fs.keys()))

    if len(missing_fs) > 0:
        raise ValueError(
                "Missing conversion functions: {}".format(missing_fs))

    ## Defaults are just to turn numbers into strings.
    defaults = {
        "Name"      : lambda s: s,
        "Cost"      : str,
        "Discount"  : str,
        "Tax"       : str,
    }

    ## Add the defaults into the conversion dictionary if they are not
    ## passed in.
    fs = dict(list(defaults.items()) + list(convert_fs.items()))

    ## How to call the functions when a certain type is reached.
    def receiptf(node):
        return fs["Receipt"](node.meta, __write(node.itemlist), variables)

    def itemListf(node):
        return fs["ItemList"](
                fs["ItemListSep"]().join([__write(item) for item in node]))

    def itemf(node):
        return fs["Item"](
                fs["Name"](node.name),
                fs["Cost"](node.cost),
                fs["Discount"](node.discount),
                fs["Tax"](node.tax))

    types = {
        Receipt  : receiptf,
        ItemList : itemListf,
        Item     : itemf,
    }

    ## Recur on __write, using the functions defined in types. This was done
    ## as a separate method so that the conversion functions and the types
    ## dict did not need to be passed around to each recursive call.
    def __write(node):
        try:
            return types[type(node)](node)
        except KeyError as e:
            raise e

    return __write(receipt)

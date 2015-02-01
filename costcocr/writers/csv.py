def Receipt(meta, body, variables):
    output = []

    def add(s) : output.append(s)

    if "store" in meta:
        add("# Store: {}".format(meta["store"]))
    if "date" in meta:
        add("# Date: {}".format(meta["date"]))
    if "location" in meta:
        add("# Location: {}".format(meta["location"]))

    add(body)

    return "\n".join(output)

def ItemList(s): return s
def ItemListSep(): return "\n"

## Could also be used to collapse the fields, or exclude some.
def Item(name, cost, discount, tax):
    return "{}, {}, {}, {}".format(name, cost, discount, tax)

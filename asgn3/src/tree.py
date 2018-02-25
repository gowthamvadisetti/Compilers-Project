from anytree import Node, RenderTree

udo = Node("Udo")
marc = Node("Marc", parent=udo)
lian = Node("Lian", parent=marc)
marc = Node("Dan", parent=udo)
jet = Node("Jet", parent=marc)
jan = Node("Jan", parent=marc)
joe = Node("Joe", parent=marc)


for pre, fill, node in RenderTree(udo):
    print("%s%s" % (pre, node.name))
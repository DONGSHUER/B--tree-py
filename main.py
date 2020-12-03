# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


class Node:
    def __init__(self, order):
        self.order = order
        self.keys = []
        self.values = []  # values are pointers for non-leaf nodes, and entries for the leaf nodes
        self.leaf = True  # by default te node is leaf as the newly inserted node is always the leaf
        self.temp_node = False

        # Only leaf nodes have the following two pointers
        self.next_leaf = None
        self.previous_leaf = None

    def add_key_value_pair(self, key, value):
        """Add the key value pair:
        ONLY APPLICABLE TO THE LEAF NODE!

        1. the key already in the node
        2. the key is not in the list"""
        i = -1
        for i, item in enumerate(self.keys):
            if key == item:
                self.values[i].append(value)
                break
            elif key < item:
                self.keys = self.keys[:i] + [key] + self.keys[i:]
                self.values = self.values[:i] + [[value]] + self.values[i:]
                break

        if i + 1 == len(self.keys):
            self.keys.append(key)
            self.values.append([value])

    def insert(self, key, value):
        # first insert to the next node, and then balance:
        if not self.leaf:
            for i, item in enumerate(self.keys):
                if key < item:
                    self.values[i].insert(key, value)  # insert_and_balance(key, self.values[i])
                    # balance the tree:
                    self.balance(i, 'insert')
                    break
            if (i + 1) == len(self.keys):
                self.values[i + 1].insert(key, value)
                # balance the tree:
                self.balance(i + 1, 'insert')
        else:
            self.add_key_value_pair(key, value)
            self.balance(None, 'insert')

    def delete(self, key, value):
        # here the value represents the rid:
        if self.leaf:
            for i, item in enumerate(self.keys):
                if item == key:
                    for j, v in enumerate(self.values[i]):
                        if v == value:
                            self.values[i].pop(j)
                    if len(self.values[i]) == 0:
                        self.values.pop(i)
                        self.keys.pop(i)
                    break
            self.balance(None, 'delete')

        else:
            for i, item in enumerate(self.keys):
                if key < item:
                    self.values[i].delete(key, value)
                    self.balance(i, 'delete')
                    break
            if (i + 1) == len(self.keys):
                self.values[i + 1].delete(key, value)
                self.balance(i + 1, 'delete')

    def borrow_and_merge(self, operated_child_idx):
        if operated_child_idx == 0:
            if self.values[operated_child_idx + 1].morethan_half_full():
                # borrow from the right sib:
                self.values[operated_child_idx].keys.append(self.keys[operated_child_idx])
                self.keys[operated_child_idx] = self.values[operated_child_idx + 1].keys[0]
                self.values[operated_child_idx].values.append(self.values[operated_child_idx + 1].values[0])

                self.values[operated_child_idx + 1].keys.pop(0)
                self.values[operated_child_idx + 1].values.pop(0)
            else:
                if not self.values[operated_child_idx].leaf:
                    # merge with the right child:
                    self.values[operated_child_idx].keys = self.values[operated_child_idx].keys + [
                        self.keys[operated_child_idx]] + self.values[operated_child_idx + 1].keys
                    self.values[operated_child_idx].values = self.values[operated_child_idx].values + self.values[
                        operated_child_idx + 1].values
                    self.keys.pop(operated_child_idx)
                    self.values.pop(operated_child_idx + 1)
                else:
                    # merge with the right child:
                    self.values[operated_child_idx].keys = self.values[operated_child_idx].keys + self.values[
                        operated_child_idx + 1].keys
                    self.values[operated_child_idx].values = self.values[operated_child_idx].values + self.values[
                        operated_child_idx + 1].values
                    # adjust the pointer of the leaf nodes:
                    self.values[operated_child_idx].next_leaf = self.values[operated_child_idx + 1].next_leaf
                    if not self.values[operated_child_idx + 1].next_leaf == None:
                        self.values[operated_child_idx + 2].previous_leaf = self.values[operated_child_idx]
                    self.values[operated_child_idx + 1]
                    self.keys.pop(operated_child_idx)
                    self.values.pop(operated_child_idx + 1)

        else:
            if self.values[operated_child_idx - 1].morethan_half_full():
                # borrow from the left sib:
                self.values[operated_child_idx].keys = [self.keys[operated_child_idx]] + self.values[
                    operated_child_idx].keys
                self.keys[operated_child_idx] = self.values[operated_child_idx - 1].keys[-1]
                self.values[operated_child_idx].values = [self.values[operated_child_idx - 1].values[-1]] + \
                                                         self.values[operated_child_idx].values
                self.values[operated_child_idx - 1].keys.pop(-1)
                self.values[operated_child_idx - 1].values.pop(-1)

            else:
                if not self.values[operated_child_idx].leaf:
                    # merge with the left child:
                    self.values[operated_child_idx].keys = self.values[operated_child_idx - 1].keys + [
                        self.keys[operated_child_idx]] + self.values[operated_child_idx].keys
                    self.values[operated_child_idx].values = self.values[operated_child_idx - 1].values + self.values[
                        operated_child_idx].values
                    self.keys.pop(operated_child_idx - 1)
                    self.values.pop(operated_child_idx - 1)
                else:
                    # merge with the left child:
                    self.values[operated_child_idx].keys = self.values[operated_child_idx - 1].keys + self.values[
                        operated_child_idx].keys
                    self.values[operated_child_idx].values = self.values[operated_child_idx - 1].values + self.values[
                        operated_child_idx].values
                    # adjust the pointer of the leaf nodes:
                    self.values[operated_child_idx].previous_leaf = self.values[operated_child_idx - 1].previous_leaf
                    if not self.values[operated_child_idx - 1].previous_leaf == None:
                        self.values[operated_child_idx - 2].previous_leaf = self.values[operated_child_idx]
                    self.keys.pop(operated_child_idx - 1)
                    self.values.pop(operated_child_idx - 1)

        if len(self.keys) == 0:
            # copy the state:
            self.leaf = self.values[0].leaf
            self.temp_node = self.values[0].temp_node
            self.next_leaf = self.values[0].next_leaf
            self.previous_leaf = self.values[0].previous_leaf
            self.keys = self.values[0].keys
            self.values = self.values[0].values

    def balance(self, operation_index, operation_type):
        # operation_index: the index of the child that just finish the operation (insert, delete)
        # operation_type: type of operation, "delete" or "insert"
        if self.leaf:
            if operation_type is "insert":
                if self.full():
                    left = Node(self.order)
                    right = Node(self.order)
                    mid = self.order // 2

                    left.keys = self.keys[:mid]
                    left.values = self.values[:mid]

                    right.keys = self.keys[mid:]
                    right.values = self.values[mid:]

                    left.next_leaf = right
                    right.previous_leaf = left
                    right.next_leaf = self.next_leaf
                    if not self.next_leaf == None:
                        self.next_leaf.previous_leaf = right
                    left.previous_leaf = self.previous_leaf
                    if not self.previous_leaf == None:
                        self.previous_leaf.next_leaf = left

                    self.keys = [right.keys[0]]
                    self.values = [left, right]
                    self.leaf = False
                    self.temp_node = True

                    return self

        else:
            if operation_type is "insert":
                # check if the child operated just now is the temp_node type:
                if self.values[operation_index].temp_node == True:
                    pivot = self.values[operation_index].keys[0]
                    for i, item in enumerate(self.keys):
                        if pivot < item:
                            self.keys = self.keys[:i] + [pivot] + self.keys[i:]
                            self.values = self.values[:i] + self.values[operation_index].values + self.values[i:]
                            break

                    if (i + 1) == len(self.keys):
                        self.keys += [pivot]
                        self.values += self.values[operation_index].values

                    self.values.pop(operation_index)

                # adjust the node itself for the potential overflow:
                if self.full():
                    left = Node(self.order)
                    right = Node(self.order)
                    mid = self.order // 2

                    left.keys = self.keys[:mid]
                    left.values = self.values[:mid + 1]

                    right.keys = self.keys[mid + 1:]
                    right.values = self.values[mid + 1:]

                    left.next_leaf = right
                    right.previous_leaf = left
                    left.leaf = False
                    right.leaf = False

                    self.keys = [self.keys[mid]]
                    self.values = [left, right]
                    # self.leaf = False
                    self.temp_node = True

                    return self

            else:
                # check if the child operated just now is more than half empty:
                ################################################################
                if self.values[operation_index].less_half_full():
                    self.borrow_and_merge(operation_index)

    def full(self):
        return len(self.keys) > self.order

    def less_half_full(self):
        return len(self.keys) < self.order // 2

    def morethan_half_full(self):
        return len(self.keys) > self.order // 2


class BPTree:
    def __init__(self, order=8):
        self.root = Node(order)

    def insert(self, key, value):
        self.root.insert(key, value)
        if self.root.temp_node:
            self.temp_node = False

    def delete(self, key, value):
        self.root.delete(key, value)

    def printLeaves(self):
        if self.root.keys == None:
            print('empty tree')
        nodeP = self.root
        while not nodeP.leaf:
            nodeP = nodeP.values[0]
        while not nodeP.next_leaf == None:
            print(nodeP.keys)
            nodeP = nodeP.next_leaf

tree = BPTree(4)
for i in range(1, 20):
    tree.insert(i, 0)

tree.printLeaves()

for i in range(1, 100):
    tree.delete(i, 0)

for i in range(1, 20):
    tree.insert(i, 0)

tree.printLeaves()

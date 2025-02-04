from swap_meet.item import Item


class Vendor:
    def __init__(self, inventory=None):
        if inventory is None:
            inventory = []
        self.inventory = inventory

    def add(self, item):
        self.inventory.append(item)
        return item

    def remove(self, item):
        '''
        Input: item
        Ouput: item that was removed, or False if no matching item in list
        Method removes the matching item from the inventory
        '''
        if item in self.inventory:
            self.inventory.remove(item)
            return item
        else:
            return False

    def get_by_category(self, input_category):
        ''' 
        Input: a string, representing a category
        Output: returns a list of Items in the inventory with that category
        '''
        category_items = []

        for item in self.inventory:
            if item.category == input_category:
                category_items.append(item)
        return category_items

    def swap_items(self, friend_vendor, my_item, their_item):
        '''
        Input: instance of Vendor (friend_vendor), instance of Item (my_item), instance of Item (their_item)
        Output: 
        - True, if my_item in inventory and their_item in their inventory
        -- inventories updated (their_item in my inventory, my_item in their inventory)
        - False, if my_item not in inventory or their_item not in their inventory
        '''

        if my_item not in self.inventory or their_item not in friend_vendor.inventory:
            return False
        else:
            self.add(their_item)
            self.remove(my_item)

            friend_vendor.add(my_item)
            friend_vendor.remove(their_item)
            return True

    def swap_first_item(self, friend_vendor):
        ''''
        Input: instance of another Vendor (friend_vendor)
        Output: 
        True (and swaps first item in both inventories)
        False if self.inventory or friend_vendor.inventory are empty
        '''
        if len(self.inventory) == 0 or len(friend_vendor.inventory) == 0:
            return False

        self.swap_items(
            friend_vendor, self.inventory[0], friend_vendor.inventory[0])
        return True

    def get_best_by_category(self, given_category):
        '''
        Method looks through the instance inventory for the item with the highest condition and matching category

        Input: category string
        Output:
        Return item, if item category in inventory (return 1 item if 2+ items with same best condition)
        Return None, if no items in the inventory that match the category
        '''
        category_list = self.get_by_category(given_category)

        if len(category_list) == 0:
            return None

        best_item = category_list[0]
        highest_condition = best_item.condition
        for item in category_list:
            if item.condition > highest_condition:
                highest_condition = item.condition
                best_item = item

        return best_item

    def swap_best_by_category(self, other, my_priority, their_priority):
        '''
        Input: instance of Vendor(other), my_priority(category str), their_priority(category str)
        Output:
        `True` → swap priority items
        `False` → if their_priority not in Vendor inventory OR my_priority not in `other`
        '''

        my_category_list = self.get_by_category(their_priority)
        their_category_list = other.get_by_category(my_priority)

        if len(my_category_list) > 1 and len(their_category_list) > 1:
            my_best = self.get_best_by_category(their_priority)
            their_best = other.get_best_by_category(my_priority)

            self.swap_items(other, my_best, their_best)
            return True
        else:
            return False

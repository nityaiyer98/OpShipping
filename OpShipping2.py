'''

                            Online Python Interpreter.
                Code, Compile, Run and Debug python program online.
Write your code in this editor and press "Run" button to execute it.

'''
'''

                            Online Python Interpreter.
                Code, Compile, Run and Debug python program online.
Write your code in this editor and press "Run" button to execute it.

'''
from collections import namedtuple
import functools
import pandas as pd

Packaging = namedtuple('Package', 'box, items_per_box, last_parcel')
ItemTuple = namedtuple('ItemTuple', 'item_number, dimensions, weight')

def reduce(function, iterable, initializer=None):
    it = iter(iterable)
    if initializer is None:
        value = next(it)
    else:
        value = initializer
    for element in it:
        value = function(value, element)
    return value

def does_it_fit(item_dims, box_dims):
    '''
    returns a boolean regarding whether or not
    a item will fit into box_dimensions

    item and box dimensions in ascending length order

    Args:
        item_dims (List[int, int,  int])
        box_dims (List[int, int,  int])

    Returns:
        bool: whether or not the item will fit in the box

    '''
    return all(box_dim >= item_dim
               for box_dim, item_dim in zip(box_dims, item_dims))


def _something_fits(items, box_dims):
    '''
    iterates through all items to see if one of them will fit in the dimensions
    given

    Args:
        items (List[ItemTuple])
        box_dims (List[int, int, int])

    Returns
        bool: whether or not any of the items fit into the box
    '''
    return any(does_it_fit(item[1], box_dims) for item in items)


def _get_side_2_side_3(item_dims, box_dims, side_1):
    '''
    This is a rotation method to rotate the item first checking if the item
    MUST be rotated in a specific direction based on size constraints, then
    rotates it so it leaves the largest bulk volume left in the box

    Args:
        item_dims (List[int, int int])
        box_dims (List[int, int int])
        side_1 (int): index of the side of the box the item is placed along

    Returns:
        int, int: indexes of the box sides the items will be placed along

    Exampls:
        >>> _get_side_2_side_3([5,5,5], [5,10,10], 0)
        1, 2

        >>> _get_side_2_side_3([5,6,8], [5,6,10], 2)
        1, 0
    '''
    if item_dims[1] > box_dims[side_1 - 1]:
        side_2 = side_1 - 2
        side_3 = side_1 - 1
    elif item_dims[1] > box_dims[side_1 - 2]:
        side_2 = side_1 - 1
        side_3 = side_1 - 2
    else:
        side_2 = (side_1 + 1) % 3
        side_3 = (side_1 + 2) % 3
    return side_2, side_3


def volume(dimensions):
    '''
    returns the volume of item or box dimensions
    assumes its a rectangular prism

    Args:
        dimensions (List[int, int, int])

    Returns:
        int: volume
    '''
    return reduce(lambda x, y: x * y, dimensions)


def best_fit(item_dims, box_dims):
    '''
    assumes item_dims and box_dims in order shortest to longest

    finds the shortest length of the box that is as long as the
        longest length of the item

    uses first fit, then rotates for remaining largest volume block
    returns a list of the remaining dimensions in the box

    Args:
        item_dims (List[int, int, int]): sorted item dimensions
        box_dims (List[int, int, int]): sorted box dimensions
    Returns
        List[List[int, int, int],
             List[int, int, int],
             List[int, int, int]]: a list of the dimensions left in the box
                after a item has been placed inside of it

    example:
        >>> best_fit([5,5,5], [10,10,10])
        [[5,5,5], [5,5,10], [5,10,10]]
    '''

    side_1 = None  # side of the box that we lay longest dimension of item on
    blocks = []  # potential remaining dimensions
    # rotate box until we can set the items longest side
    box_dims = list(box_dims)
    for i, b_dim in enumerate(box_dims):
        # choose the shortest side of the box we can stack the item twice
        # on its longest side
        # based on theory of if b_dim / 2 >= s_dim, don't open a new bin
        #   (or don't rotate the box)
        if b_dim >= item_dims[2] * 2:
            side_1 = i
            # block_1 is the upper layer of the box
            block_1 = sorted([box_dims[side_1] - item_dims[2],
                              box_dims[i - 1], box_dims[i - 2]])
            blocks.append(block_1)
            # reset the box dimensions to being the height of the item
            box_dims[i] = item_dims[2]
            break

        elif b_dim == item_dims[2]:
            # exact fit, move to next block
            side_1 = i
            break

    if side_1 is None:
        for i, b_dim in enumerate(box_dims):
            # if we can't do that, chose the shortest side of the box we can
            # stack the item once on it's longest side
            if b_dim >= item_dims[2]:
                side_1 = i
                block_1 = sorted([box_dims[side_1] - item_dims[2],
                                  item_dims[1], item_dims[0]])
                blocks.append(block_1)
                break

    side_2, side_3 = _get_side_2_side_3(item_dims, box_dims, side_1)

    # option one for remaining dimensions
    block_2a = sorted([box_dims[side_1],
                       box_dims[side_2],
                       box_dims[side_3] - item_dims[0]])
    block_3a = sorted([box_dims[side_1],
                       box_dims[side_2] - item_dims[1],
                       item_dims[0]])

    # option two for remaining dimensions
    block_2b = sorted([box_dims[side_1],
                       box_dims[side_2] - item_dims[1],
                       box_dims[side_3]])
    block_3b = sorted([box_dims[side_1],
                       box_dims[side_3] - item_dims[0],
                       item_dims[1]])

    # select the option where block_2 and block_3 are closest in size
    # this operator has been tested and is 5-15% more accurate than
    # if volume(block_2a) > volume(block_2b)
    # DO NOT REVERT
    if volume(block_2a) < volume(block_2b):
        blocks.append(block_2a)
        blocks.append(block_3a)
    else:
        blocks.append(block_2b)
        blocks.append(block_3b)

    remaining_dimensions = []
    for block in blocks:
        # if the blocks smallest dimension is not 0, it has volume
        # and the block should be appended
        if block[0] != 0:
            remaining_dimensions.append(block)
    # sort unsorted_remaining_dimensions by volume
    remaining_dimensions = sorted(remaining_dimensions,
                                  key=lambda block: volume(block))
    return remaining_dimensions


def insert_items_into_dimensions(remaining_dimensions, items_to_pack,
                                items_packed):
    block = remaining_dimensions[0]
    for item in items_to_pack:
        if does_it_fit(item.dimensions, block):
            # if the item fits, pack it, remove it from the items to pack
            items_packed[-1].append(item)
            items_to_pack.remove(item)
            # find the remaining dimensions in the box after packing
            left_over_dimensions = best_fit(item.dimensions, block)
            for left_over_block in left_over_dimensions:
                # only append left over block if at least one item fits
                if _something_fits(items_to_pack, left_over_block):
                    remaining_dimensions.append(left_over_block)
            # if a item fits, remaining dimensions will have changed
            # break out of loop
            break
    # remove the block from that remaining dimensions
    remaining_dimensions.pop(0)
    return remaining_dimensions, items_packed


def pack_boxes(box_dimensions, items_to_pack):
    '''
    while loop to pack boxes
    The first available dimension to pack is the box itself.
    When you pack a item into a box, find the best fit, which will change the
        dimensions available to pack items into
    While there are still items to pack and dimensions large enough to hold at
        least one of the items, it will continue to pack the same box
    If there is no remaining space in the box large enough for a item, a new
        dimension will be added to available
    After there are no more items needing to be packed, returns a list lists of
        the items in there 'boxes' (first box is first nested list, second is
        the second, etc.)
    Args:
        box_dimensions (List[int, int, int]): sorted list of box dimensions
        items_to_pack (List[ItemTuple]): list of items to pack as ItemTuples
            sorted by longest dimension
    returns:
        List[List[SimpleItem]]: list of lists including the items in the
            number of boxes the are arranged into
    example:
    >>> pack_boxes([5,5,10], [[item1, [5,5,10]], item2, [5,5,6],
                   [item3, [5,5,4]])
    [[item1], [item2, item3]]
    '''
    # remaining_dimensions represents the available space into which items can go
    # in List[List[int, int, int],] form where each nested List is a dimensional
    # block where space remains to be filled.
    remaining_dimensions = []
    items_packed = []  # the items that have been packed
    items_to_pack_copy = list(items_to_pack)
    while len(items_to_pack_copy) > 0:
        # keep going until there are no more items to pack
        if len(remaining_dimensions) == 0:
            # if there is no room for more items in the last parcel,
            # append an empty parcel with the full box dimensions
            # and append an empty parcel to the list of items packed
            remaining_dimensions = [box_dimensions]
            items_packed.append([])
        # iterate through remaining dimensions to pack boxes
        for block in remaining_dimensions:
            remaining_dimensions, items_packed = insert_items_into_dimensions(
                remaining_dimensions, items_to_pack_copy, items_packed)
    return items_packed


def setup_packages(packed_boxes, zone=None):
    if len(packed_boxes) == 0:
        raise BoxError('There are no packed boxes available to return.')
    best_boxes = {}
    # determine best flat rate and best package
    for box, packed_items in packed_boxes.iteritems():
        # is_flat_rate = box.description in usps_shipping.USPS_BOXES
        # key = 'flat_rate' if is_flat_rate else 'package'
        min_boxes = best_boxes.get('num_parcels')

        # if there are no boxes set, min boxes will be None,
        # and box_packs_better will be True
        box_packs_better = (len(packed_items) < min_boxes
                            if min_boxes is not None else True)

        box_packs_same = (len(packed_items) == min_boxes
                          if min_boxes is not None else True)

        if box_packs_better:
            # set the new best box
            best_boxes = {
                'box': box,
                'num_parcels': len(packed_items)
            }
        elif box_packs_same:
            # check a few comparisons
            if box.total_cubic_cm < best_boxes['box'].total_cubic_cm:
                best_boxes['box'] = box
            # else the box is not smaller
        # else the box does not pack better

    if best_boxes:
        return Packaging(best_boxes['box'],
            packed_boxes[best_boxes['box']], None)

    return None

def test_pack_boxes_one_item():
        '''
        test exact fit one item
        '''
        item1 = ItemTuple('Item1', [13, 13, 31], 0)
        item2 = ItemTuple('Item2', [13, 13, 31], 0)
        item_info = [item1,item2]
        box_dims = [13, 13, 31]

        packed_items = pack_boxes(box_dims, item_info)
        print(packed_items)
        print(len(packed_items))

def runerr():
    item1 = ItemTuple('Item1', [13, 13, 31], 0)
    item2 = ItemTuple('Item2', [8, 13, 29], 0)
    item3 = ItemTuple('Item3', [5, 13, 27], 0)
    item_info = [item1,item2,item3]
    items_to_pack = sorted(item_info, key=lambda item: item.dimensions[2],
                          reverse=True)
    box_dims = [[13, 24, 31],[34,34,34]]
    for i in range(0,len(box_dims)):
        print(box_dims[i])
        packed_items = pack_boxes(box_dims[i],items_to_pack)
        print(packed_items)
        print(len(packed_items))

def handle_order(sku_list):
    items = []

print("Hello World")
runerr()
print("Hello World")

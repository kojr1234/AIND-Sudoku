from utils import *

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

# TODO: Update the unit list to add the new diagonal units
unitlist = unitlist + [[rows[i]+cols[i] for i in range(9)]] + [[rows[8 - i]+cols[i] for i in reversed(range(9))]]

# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    # TODO: Implement this function!
    # get all the boxes which cantains only two possible numbers
    value2_box = [box for box in boxes if (len(values[box]) == 2)]
    pairs = []
    for box in value2_box:
        for p in peers[box]:
            if values[box] == values[p]:
                for common_box in peers[box] & peers[p]:
                    if len(values[common_box]) > 1:
                        for digit in values[box]:
                            if digit in values[common_box]:
                                values[common_box] = values[common_box].replace(digit, '')

            #[values[common_box].replace(digit, '') for digit in values[box] if len(values[common_box]) > 1
            #for common_box in peers[box] & peers[p] if values[box] == values[p]]

    return values



def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    # TODO: Copy your code from the classroom to complete this function
    new_values = dict.copy(values)
    for box in boxes:
        valid_num = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        if len(values[box]) > 1:
            for p in peers[box]:
                if values[p] in valid_num:
                    valid_num.remove(values[p])
            new_values[box] = ''.join(valid_num)

    return new_values



def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    # TODO: Copy your code from the classroom to complete this function

    for unit in unitlist:
        for box in unit:
            if len(values[box]) == 1:
                continue
            else:
                flag = False
                digits = values[box]
                for digit in digits:
                    unique_digit = ''
                    for other_box in unit:
                        if box != other_box:
                            if digit in values[other_box]:
                                flag = False
                                break
                        flag = True
                        unique_digit = digit
                    if flag is True:
                        values[box] = unique_digit

    return values








def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    # TODO: Copy your code from the classroom and modify it to complete this function
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)

        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])

        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after

        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values





def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    # TODO: Copy your code from the classroom to complete this function
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)

    if values is False:
        return False

    if max([len(values[box]) for box in boxes]) == 1:
        return values

    # Choose one of the unfilled squares with the fewest possibilities
    comp = 10
    min_box = ''
    for box in boxes:
        if len(values[box]) > 1 and len(values[box]) < comp:
            comp = len(values[box])
            min_box = box

    # Now use recurrence to solve each one of the resulting sudokus, and
    for digit in values[min_box]:
        values_copy = values.copy()
        values_copy[min_box] = digit

        #apply the naked twins function
        values = naked_twins(values)

        values_copy = search(values_copy)
        if values_copy is not False:
            return values_copy



def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    #diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    diag_sudoku_grid = '...58.4...3.2.7.5.8.........1.....692.......146.....2.........5.2.6.5.1...4.73...'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    if result:
        display(result)
    else:
        print("Falhou!")
    try:
        import PySudoku
        # PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')

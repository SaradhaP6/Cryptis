import pygame

class Block:
    def __init__(self, x, y, block_color=1, block_size=(30, 10)):
        """
        Description : Initializes a block
        Arguments :
            - x: Position x of the block
            - y: Position y of the block
            - color: Color of the block -> 1 for light purple (positive value) & -1 for dark purple (negative value)
                    & by default it is equal to 1
            - block_size: Size of the block
                        & by default 30x10 pixels
        """
        self.x = x
        self.y = y
        self.block_size = block_size

        if block_color == 1:
            # LIGHT_PURPLE_COLOR
            self.block_color = (224, 170, 255)
        else:
            # DARK_PURPLE_COLOR
            self.block_color = (123, 44, 191)

    def draw(self, surface):
        """
        Description : Draws the block
        Arguments :
            - surface: Where the block will be drawn
        """
        pygame.draw.rect(surface, self.block_color, (self.x, self.y, self.block_size[0], self.block_size[1]), 1)


class BlockColumn:
    def __init__(self, x, y_first_block, number_blocks, column_color=1, column_direction=1, block_size=(30,10)):
        """
        Description : Initializes a column of block
        Arguments :
            - x: Position x of the column
            - y: Position y of the first block
            - number_blocks: Number of blocks in the column
            - column_color: Color of the column -> 1 for light purple (positive value) & -1 for dark purple (negative value)
                    & by default it is equal to 1
            - column_direction: Direction of the colum -> 1 for down to up & -1 for up to down
                                & by default it is equal to 1
            - block_size: Size of the blocks
                        & by default 30x10 pixels
        """
        self.blocks=[]
        self.size = block_size

        for i in range (0, number_blocks):

            # Calculating the value of the position y for each blocks to have them stacked on each other
            if i==0:
                y = y_first_block
            else:
                if column_direction==1:
                    y = y_first_block - i*(block_size[1] + 2)
                else:
                    y = y_first_block + i*(block_size[1] + 2)
            
            self.blocks.append(Block(x, y, column_color, block_size))
    
    def draw(self, surface):
        """
        Description : Draws the column
        Arguments :
            - surface: Where the column will be drawn
        """
        for block in self.blocks:
            block.draw(surface)


class BlockTab:
    def __init__(self, x_first_column, y_first_line, number_blocks_per_column, number_column=8, column_direction=1, block_size=(30, 10)):
        """
        Description : Initializes a "table" of block
        Arguments :
            - x_first_column: Position x of the first column
            - y_first_block: Position y of the first line
            - number_blocks_per_column: List of the number of blocks in each column
            - number_column: Number of column
                            & by default it is equal to 8
            - column_direction: Direction of the colum -> 1 for down to up & -1 for up to down
                                & by default it is equal to 1
            - block_size: Size of the blocks
                        & by default 30x10 pixels
        """
        self.columns=[]

        for i in range (0, number_column):

            # Calculating the value of the position x for each columns to have them next to each other
            if i==0:
                x = x_first_column
            else:
                x = x_first_column + i*(block_size[0] + 2)
            
            if number_blocks_per_column[i] > 0:
                tab_color = 1
            else:
                tab_color = -1

            self.columns.append(BlockColumn(x, y_first_line, abs(number_blocks_per_column[i]), tab_color, column_direction, block_size))
    
    def draw(self, surface):
        """
        Description : Draws the table of blocks
        Arguments :
            - surface: Where the column will be drawn
        """
        for column in self.columns:
            column.draw(surface)
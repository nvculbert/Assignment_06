#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# nickculbert, 2021-Feb-21, added functions
#------------------------------------------#

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dictRow = {}  # list of data row
strFileName = 'CDInventory.txt'  # data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    
    @staticmethod
    def add_tbl_item(strID, strTitle, strArtist, table): 
        """Adds items to the table lstTbl

        Args:
            strID (string): user input for the ID of the CD being added
            strTitle (string): user input for the title of the CD being added
            strArtist (string): user input for the Artist's name on the CD being added
            table (list of dicts): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        intID = int(strID)
        dictRow = {'ID': intID, 'Title': strTitle, 'Artist': strArtist}
        table.append(dictRow)
        IO.show_inventory(table)
        
    @staticmethod
    def CD_delete(intIDDel, table):   
        """Deletes a CD based on previous user input

        Args:
            intIDDel (integer): user input, converted into an integer, which designates which CD to delete
            table (list of dicts): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == intIDDel:
                del table[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
        IO.show_inventory(table)
        

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dicts): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file
        objFile = open(file_name, 'a+')
        objFile.seek(0)
        for line in objFile:
            data = line.strip().split(',')
            dictRow = {'ID': int(data[0]), 'Title': data[1], 'Artist': data[2]}
            table.append(dictRow)
        objFile.close()

    @staticmethod
    def write_file(file_name, table):
        """Writes current inventory data to text file

        Args:
            file_name (string): name of file used to read the data from
            table (list of dicts): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        objFile = open(strFileName, 'w')
        for row in table:
            lstValues = list(row.values())
            lstValues[0] = str(lstValues[0])
            objFile.write(','.join(lstValues) + '\n')
        objFile.close()


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """
        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print()
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')
        print()
    
    @staticmethod
    def get_new_CD():
        """Gets user input for adding a new CD

        Args:
            None.

        Returns:
            strID (string): user input for the ID of the CD being added
            strTitle (string): user input for the title of the CD being added
            strArtist (string): user input for the Artist's name on the CD being added
        """
        strID = input('Enter ID: ').strip()
        strTitle = input('What is the CD\'s title? ').strip()
        strArtist = input('What is the Artist\'s name? ').strip()
        return strID, strTitle, strArtist
        
# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    
    # 3.1 process exit first
    if strChoice == 'x':
        break
    
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('Type \'yes\' to continue and reload from file. Type anything else to cancel the reload. ')
        if strYesNo.lower() == 'yes':
            print('\nreloading...\n')
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    
    # 3.3 process add a CD
    elif strChoice == 'a':
        strID, strTitle, strArtist = IO.get_new_CD()
        DataProcessor.add_tbl_item(strID, strTitle, strArtist, lstTbl)
        continue #start loop back at top
    
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get user input for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        intIDDel = int(input('Which ID would you like to delete? ').strip())
        DataProcessor.CD_delete(intIDDel, lstTbl)
        continue  # start loop back at top.
    
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be safe:
    else:
        print('General Error')





from operatorinstructions import SofficeHandler, FileHandler, DatabaseHandler

soffice_handler = SofficeHandler()
file_handler = FileHandler()
database_handler = DatabaseHandler(database='plantfloor')



if __name__ == "main":
    main()
    def createdb(self):
        sqliteConnection = sqlite3.connect("Fuel_Prices.db")
        cursor = sqliteConnection.cursor()
        log.debug("Connected to SQLite database")

        create_tables = """
            CREATE TABLE IF NOT EXISTS Brands (
            id TEXT PRIMARY KEY,
            name TEXT
            );

            CREATE TABLE IF NOT EXISTS Stations (
            id TEXT PRIMARY KEY,
            name TEXT,
            code INTEGER,
            brand_id TEXT,
            street TEXT,
            suburb_city TEXT,
            postcode INTEGER,
            FOREIGN KEY (brand_id) REFERENCES Brands (id)
            );
        """
        cursor.executescript(create_tables)

    def addtodb(self):
        sqliteConnection = sqlite3.connect("Fuel_Prices.db")
        cursor = sqliteConnection.cursor()
        log.debug("Connected to SQLite database")
import psycopg2
import uuid


class Database:
    connection = None
    dbname, user, password, host, port = '', '', '', '', ''

    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def StartConnection(self):
        try:
            self.connection = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password,
                                               host=self.host, port=self.port)
            #print("Database connection was successful!")

        except:
            print("Database connection error!")

    def StopConnection(self):
        self.connection.close()

    def Select(self, tableName, columnName, values):
        cursor = self.connection.cursor()
        result = {''}

        try:
            query = 'SELECT '
            i = 0
            for elem in columnName:
                query += elem
                if i + 1 != len(columnName):
                    query += ", "
                i+=1

            query += ' FROM ' + tableName

            if values:
                query += ' WHERE '
                i = 0
                for elem in values:
                    key = list(elem.keys())[0]
                    val = list(elem.values())[0]
                    query += '"' + key + '" = \'' + val + '\''
                    if i + 1 != len(values):
                        query += " AND "
                    i+=1

            cursor.execute(query)
            for row in cursor:
                result.add(row)
            #print("Select was successful!")

        except:
            print("Select error!")

        cursor.close()
        return result

    def Insert(self, tableName, values):
        cursor = self.connection.cursor()
        id = str(uuid.uuid4())

        try:
            query = 'INSERT INTO ' + tableName + ' (id, '

            i = 0
            for elem in values:
                key = list(elem.keys())[0]
                query += key
                if i + 1 != len(values):
                    query += ", "
                i += 1

            query += ') VALUES (\'' + id + '\', \''

            i = 0
            for elem in values:
                val = list(elem.values())[0]
                query += val
                if i + 1 != len(values):
                    query += "\', \'"
                i += 1

            query += '\')'

            cursor.execute(query)
            self.connection.commit()
            #print("Insert was successful!")
        except:
            print("Insert error!")

        cursor.close()

    def Update(self, tableName, values, conditions):
        cursor = self.connection.cursor()

        try:
            query = 'UPDATE ' + tableName + ' SET '

            i = 0
            for elem in values:
                key = list(elem.keys())[0]
                val = list(elem.values())[0]
                query += '"' + key + '" = \'' + val + '\''
                if i + 1 != len(values):
                    query += ", "
                i += 1

            query += ', "updated_at" = \'now()\' WHERE '

            i = 0
            for elem in conditions:
                key = list(elem.keys())[0]
                val = list(elem.values())[0]
                query += '"' + key + '" = \'' + val + '\''
                if i + 1 != len(conditions):
                    query += " AND "
                i += 1

            cursor.execute(query)
            self.connection.commit()
            #print("Update was successful!")

        except:
            print("Update error!")

    def Delete(self, tableName, conditions):
        self.Update(tableName, [{'is_deleted': 'true'}], conditions)

    def ImageSelect(self, tableName, columnName, keyword):
        cursor = self.connection.cursor()
        result = {''}

        try:
            query = 'SELECT '
            i = 0
            for elem in columnName:
                query += elem
                if i + 1 != len(columnName):
                    query += ", "
                i+=1

            query += ' FROM ' + tableName

            query += " WHERE (images.tags like '% ' || '"
            query += keyword
            query += "' || ' %') LIMIT 50"

            cursor.execute(query)
            for row in cursor:
                result.add(row)
            #print("Select was successful!")

        except:
            print("Image Select error!")

        cursor.close()
        return result

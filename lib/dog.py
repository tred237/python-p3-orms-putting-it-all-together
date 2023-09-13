import sqlite3
import ipdb

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def save(self):
        sql = """
            insert into dogs (name, breed)
            values (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.breed))
        CONN.commit()
        self.id = CURSOR.execute('select id from dogs order by id desc limit 1').fetchone()[0]

    def update(self):
        sql = """
            update dogs
            set name = ?, breed = ?
            where id = ?
        """
        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()

    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog
    
    @classmethod
    def create_table(cls):
        sql = """
            create table if not exists dogs (
                id integer primary key,
                name text,
                breed text
            )
        """
        CURSOR.execute(sql)
        
    @classmethod
    def drop_table(cls):
        CURSOR.execute('drop table if exists dogs')

    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog
    
    @classmethod
    def get_all(cls):
        sql = """
            select * from dogs
        """
        dogs = CURSOR.execute(sql)
        cls.all = [cls.new_from_db(row) for row in dogs]
        return cls.all
    
    @classmethod
    def find_by_name(cls, name):
        sql = """
            select * from dogs where name = ?
        """
        dog = CURSOR.execute(sql, (name,)).fetchone()
        if dog:
            return cls.new_from_db(dog)
        else:
            return None

    @classmethod
    def find_by_id(cls, id):
        sql = """
            select * from dogs where id = ?
        """
        dog = CURSOR.execute(sql, (id,)).fetchone()
        return cls.new_from_db(dog)
    
    @classmethod
    def find_or_create_by(cls, name, breed):
        sql = """
            select * from dogs where name = ? and breed = ?
        """
        dog = CURSOR.execute(sql, (name, breed)).fetchone()
        if dog:
            return cls.new_from_db(dog)
        else:
            new_dog = cls.create(name, breed)
            return cls.new_from_db((new_dog.id, new_dog.name, new_dog. breed))


# Dog.drop_table()
# Dog.create_table()
# joey = Dog.find_or_create_by("joey", "cocker spaniel")
# joey.name = "joseph"
# joey.update()

# sql = """
#         INSERT INTO dogs (name, breed)
#         VALUES ('joey', 'cocker spaniel')
#     """
# sql1 = """
#         INSERT INTO dogs (name, breed)
#         VALUES ('joey', 'cocker spaniel')
#     """
# sql2 = """
#         INSERT INTO dogs (name, breed)
#         VALUES ('joey', 'cocker spaniel')
    # """
# CURSOR.execute(sql)
# CURSOR.execute(sql1)
# CURSOR.execute(sql2)


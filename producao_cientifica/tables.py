from .models import Person
from table import Table
from table.columns import Column

class PersonTable(Table):
    id = Column(field='id')
    name = Column(field='name')
    class Meta:
        model = Person

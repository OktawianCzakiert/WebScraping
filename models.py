from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import StringField, ReferenceField, ListField, EmbeddedDocumentField, BooleanField


class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

    def __str__(self):
        return f"Author(fullname={self.fullname}, born date={self.born_date}, born location={self.born_location}, description={self.description})"


class Tag(EmbeddedDocument):
    name = StringField()

    def __str__(self):
        return f"Tag #{self.name}"


class Quote(Document):
    tags = ListField(EmbeddedDocumentField(Tag))
    author = ReferenceField(Author)
    quote = StringField(required=True)

    def __str__(self):
        return f"{self.quote} by {self.author}"

class Contact(Document):
    fullname = StringField()
    email = StringField()
    message_sent = BooleanField(default=False)
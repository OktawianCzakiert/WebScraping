from models import Author, Quote, Tag
import connect
import json


def upload_authors_to_db(homework_to_load):

    json_name = f"authors_hw{homework_to_load}.json"

    with open(json_name, 'r') as file:
        data_list = json.load(file)

        for data in data_list:
            sample_author = Author(fullname=data['fullname'], born_date=data['born_date'],born_location=data['born_location'], description=data['description'])
            sample_author.save()

def upload_quotes_to_db(homework_to_load):

    json_name = f"quotes_hw{homework_to_load}.json"

    with open(json_name, "r") as file:
        data_list = json.load(file)

        tags = []

        for data in data_list:
            author_name = data['author']
            quote = data['quote']
            list_of_tags = data['tags']
            tags = [Tag(name=tag) for tag in list_of_tags]
            author = Author.objects(fullname=author_name).first()
            if not author:
                author = Author(fullname=author_name)
                author.save()

            sample_quote = Quote(tags=tags, author=author, quote=quote)
            sample_quote.save()
            tags = []


if __name__ == "__main__":
    # As the parameter for below functions enter: "8" or "9" according to data you want to upload to database
    upload_authors_to_db(9)
    upload_quotes_to_db(9)

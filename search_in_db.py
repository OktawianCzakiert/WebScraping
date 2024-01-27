
from models import Quote, Author
import connect

# Przykład:
#
# name: Steve Martin — znajdź i zwróć listę wszystkich cytatów autora Steve Martin;
# tag:life — znajdź i zwróć listę cytatów dla tagu life;
# tags:life,live — znajdź i zwróć listę cytatów, które zawierają tagi life lub live (bez spacji między tagami life, live);
# exit — zamknij skrypt;


in_progress = True

while in_progress:
    command = input(f"\n Enter 'exit' to terminate or command and phrase to search in db: ")
    if command.lower() == 'exit':
        in_progress = False
    else:
        func = command.split(sep=":")[0].strip()
        phrase = command.split(sep=":")[1].strip()
        # print(f"func: {func}, phrase: {phrase}")

        if func == "name":
            authors = Author.objects(fullname=phrase)
            if authors:
                for author in authors:
                    print(author.fullname)
                    quotes = Quote.objects(author=author)
                    print(f"\n Quotes said by {phrase}: ")
                    for q in quotes:
                        print(f"- {q.quote}")
        elif func == "tag":
            quotes = Quote.objects(tags__name=phrase)
            print(f"\n Quotes tagged by #{phrase}: ")
            for q in quotes:
                print(f"- {q.quote}")
        elif func == "tags":
            phrase = [p.strip() for p in phrase.split(',')]
            quotes = Quote.objects(tags__name__in=phrase)
            print(f"\n Quotes tagged by #{phrase}: ")
            for q in quotes:
                print(f"- {q.quote}")


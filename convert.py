from bs4 import BeautifulSoup
import re

with open("lorem.html", 'r') as lorem:
    with open("output.html", 'w') as out:
        soup = BeautifulSoup(lorem, 'html.parser')
        for link in soup.find_all(string=re.compile("@\"")):
            ref = link[link.index('@\"')+2: link.index('\"', link.index('@\"')+2)]
            aref = re.sub(r'\W+', '', ref.replace('\n', ''))
            new_tag = soup.new_tag("a", href=f'#{aref}')
            new_tag.string = ref
            new_string = link.replace(f'@\"{ref}\"', str(new_tag))
            print(new_string)
            link.replace_with(BeautifulSoup(new_string, 'html.parser'))
        for loc in soup.find_all(string=re.compile("#\"")):
            ref = loc[loc.index('#\"')+2: loc.index('\"', loc.index('#\"')+2)]
            aref = re.sub(r'\W+', '', ref.replace('\n', ''))
            new_tag = soup.new_tag("a", id=f'{aref}')
            new_tag.string = ref
            new_string = loc.replace(f'#\"{ref}\"', str(new_tag))
            print(new_string)
            loc.replace_with(BeautifulSoup(new_string, 'html.parser'))
        out.write(str(soup).replace("\xa0", "&nbsp;"))

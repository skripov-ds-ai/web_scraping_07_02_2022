import requests

# pip install bs4
from bs4 import BeautifulSoup

response = requests.get("http://127.0.0.1:5000/")
soup = BeautifulSoup(response.text, "html.parser")

a = soup.find("a")
# a.attrs['href']
b = a.find("b")

# all sections?
sections = soup.find_all(attrs={"class": "section"})

# "red" OR "section"
red_sections = soup.find_all(attrs={"class": ["red", "section"]})
# ? "red" AND "section"; exact string matching
red_sections_2 = soup.find_all(attrs={"class": "red section"})
# ? exact string matching
red_sections_3 = soup.find_all(attrs={"class": "red  section"})

# "red" AND "section"
reds = soup.find_all(attrs={"class": "red"})
red_sections_4 = []
for element in reds:
    if "section" in element.attrs["class"]:
        red_sections_4.append(element)

N = 2
top_N_sections = soup.find_all(attrs={"class": "section"}, limit=N)

main_content = soup.find(attrs={"id": "main_content"})
parent_of_main_content = main_content.parent
# main_content.parent.parent.parent ?

# there are generator inside
parents = list(main_content.parents)
# parents[idx] - less fragile but?

main_content_children = list(main_content.children)
main_content_children_1 = main_content.findChildren()
main_content_children_2 = main_content.findChildren(recursive=False)

fifth_paragraph = main_content.find(text="5 параграф").parent
fifth_paragraph_1 = main_content.find("p", text="5 параграф")
fifth_paragraph_2 = main_content.find("p", text="5 парагра")
# fifth_paragraph.text

# previous sibling <p>
fifth_paragraph_prev_sibling = fifth_paragraph.find_previous_sibling("p")

print()


# soup = BeautifulSoup(response.text, "html.parser")
# a = soup.find("a")
# a_all = soup.find_all("a")
# span = soup.find("span")
# span_all = soup.find_all("span")
#
# red_elements = soup.find_all(attrs={"class": "red"})
# red_section_elements = soup.find_all(attrs={"class": "red section"})
# red_section_elements1 = soup.find_all(attrs={"class": ["red", "section"]})
# red_section_elements_true = [
#     tag for tag in red_elements if "section" in tag.attrs["class"]
# ]
#
# multiple_attrs_example = soup.find(attrs={"id": "some", "class": "section"})
#
# section_top_3_elements = soup.find_all(
#     attrs={"class": "section"},
#     limit=3,
# )
#
# fifth_section = soup.find(text="5 параграф")
# fifth_section_p = soup.find("p", text="5 параграф")
# fifth_section1 = soup.find(text="5 парагра")
#
# main_content = soup.find(attrs={"id": "main_content"})
# main_content_chidlren = main_content.findChildren()
# main_content_chidlren1 = main_content.findChildren(recursive=False)
# main_content_children2 = list(main_content.children)
#
# main_content_parent = main_content.parent
# main_content_parents = list(main_content.parents)
#
# print()

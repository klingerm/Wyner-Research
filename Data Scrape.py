import requests
from lxml import html
from lxml.etree import tostring
import time
import pandas as pd

top_recruit_lists = {i:'http://247sports.com/Season/%i-Football/CompositeRecruitRankings?InstitutionGroup=HighSchool'%i for i in range(2002, 2014)}

headers = {'User-agent': 'bingbot'}
# get 247 composite rankings for every year from 2002-2014
for year in top_recruit_lists:
    top_recruit_lists[year] = requests.get(top_recruit_lists[year], headers=headers)
    time.sleep(0.25) 

# scrape 24/7 database for all recruits
names = []
pos = []
height = []
weight = []
rating = []
college = []
hs_location = []
recruit_year = []

for year in top_recruit_lists:
    tree = html.fromstring(top_recruit_lists[year].content)
    names += tree.xpath('//a[@class="bold"]/text()')
    pos += tree.xpath('//span[@class="position"]/text()')
    height += tree.xpath('//span[@class="height"]/text()')
    weight += tree.xpath('//span[@class="weight"]/text()')
    rating += tree.xpath('//span[@class="rating"]/text()')
    college += tree.xpath('//img[@class="jsonly"]/@alt')
    hs_location += tree.xpath('//span[@class="meta"]/text()')
    recruit_year += [year] * len(tree.xpath('//a[@class="bold"]/text()'))

college = [x for x in college if x not in names]

df = pd.DataFrame(index=names)
df['hs_location'] = hs_location
df['recruit_year'] = recruit_year

print(names, pos, height, weight, rating)

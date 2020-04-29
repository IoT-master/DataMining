from fetch_articles import LoginClass
from time import sleep
from pprint import pprint
from pathlib import Path
from summerizer import summarize
import ujson

wait = 2

ap_articles = LoginClass()
ap_articles.logging_in('http://www.apsexed.com/blog/archives/11-2017')
ap_articles.wait_until_css_element_object_found(
    '.blog-archive-list .blog-link')
archives_list = list(map(lambda x: x.get_attribute('href'), ap_articles.browser.find_elements_by_css_selector(
    '.blog-archive-list .blog-link')))

article_dict = {}
for each_archive in archives_list:
    ap_articles.browser.get(each_archive)
    sleep(wait)
    for index_article, each_article in enumerate(ap_articles.browser.find_elements_by_class_name('blog-title')):
        article_dict[each_article.text] = ap_articles.browser.find_elements_by_class_name(
            'blog-content')[index_article].text
ap_articles.browser.quit()
with open(Path('Results/articles.json'), 'w') as file:
    file.write(ujson.dumps(article_dict, indent=4))


summary_article_dict = {}
for each_article in article_dict:
    summary_article_dict[each_article] = ' '.join(
        summarize(article_dict[each_article]))

with open(Path('Results/summary.json'), 'w') as file:
    file.write(ujson.dumps(summary_article_dict, indent=4))

for each_article in summary_article_dict:
    with open(Path(f'SummarizedArticles/{each_article}.txt'), 'w') as file:
        file.write(summary_article_dict[each_article])

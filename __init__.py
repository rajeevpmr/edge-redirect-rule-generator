import pandas as pd
import progressbar
from time import sleep

app_url = "your-test-env.com"

def extract_source_url():
    global slug_source
    slug_source = row[1].split('orgin.com')[-1]
    slug_source = slug_source.replace("&", "\&")
    slug_source = slug_source.replace("?", "\?")
    slug_source = slug_source.strip()


def validate():
    global slug_target, slug_source
    if slug_source in url_data_dict.keys():
        print("Indefinite loop found!!! Hold on..")
        print(slug_source)
    if (target_url.startswith("www.orgin.com")):
        test_url = target_url.replace("www.orgin.com", app_url)
    else:
        test_url = target_url
        slug_target = target_url
    # if (req.urlopen(test_url).getcode() != 200):
    # print("FAILED!!!!!")


def create_dictionary():
    global count
    if slug_source not in url_data_dict.values():
        if '=' in slug_source:
            new_val = {slug_target + "_qs" + str(count): slug_source}
            count = count + 1
            url_data_dict.update(new_val)

        elif slug_target in url_data_dict.keys():
            updated_val = url_data_dict[slug_target] + " " + slug_source
            new_val = {slug_target: updated_val}
            url_data_dict.update(new_val)

        else:
            new_val = {slug_target: slug_source}
            url_data_dict.update(new_val)



def cleanup_target():
    global slug_target
    if slug_target.endswith('/'):
        slug_target = slug_target[:-1]
    if not slug_target.strip():
        slug_target = "/"
    slug_target = slug_target.strip()


def read_excel():
    global source_data_list, url_data_dict, count
    source_data = pd.read_excel(r'/your/location/edge-redirect/sample_urls.xlsx',
                                skiprows=1)
    source_data_list = list(map(list, source_data.values))
    count = 1
    url_data_dict = {}


def generate_akamai_csv():
    global row, target_url, slug_target
    for row in source_data_list:
        if row[0] == 'New':
            target_url = row[2]
            slug_target = row[2].split('orgin.com')[-1]

            extract_source_url()

            validate()

            cleanup_target()

            create_dictionary()


def write_csv():
    print(url_data_dict)
    with open('akamai_redirect_rules.csv', 'w') as f:
        for key in url_data_dict.keys():
            f.write("%s,%s\n" % (key, url_data_dict[key]))
    # print(url_data_dict)


def _main():
    read_excel()
    generate_akamai_csv()
    write_csv()

_main()

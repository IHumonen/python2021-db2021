import pickle

from bs4 import BeautifulSoup 

class Channel:
    def __init__(self, html, category, url):
        self.html = html
        self.category = category
        self.url = url
        extract = self.get_elements()
        self.name = extract['name']
        self.subscribers = extract['subscribers']
        self.videos = []
        self.folder = r'C:\Users\Иннокентий\Documents\Ютуб\каналы2'
        self.pirkovskii = 0
        extract = ''
        self.html = ''
                
    def get_elements(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        try:
            name = soup.find(class_='ytd-channel-name')
            name = name.find(id='text').text
        except:
            name = ''
        subscribers = my_find(soup, 'subscriber-count') 
        elements = {'name' : name, 'subscribers' : subscribers}
        return elements

    def dump(self):
        try:
            filename = self.name.split('/')[0]
            filename_pickle = self.folder + '\\' + filename + '.pickle'
            with open(filename_pickle, 'bw') as f:
                pickle.dump(self, f)
        except Exception as error:
            print('Ошибка сохранения:', error)
    
    def pirkovskii_here(self):
        summa = 0
        for video in self.videos:
            if video.pirkovskii:
                summa += 1
        self.pirkovskii = summa / len(self.videos)

class Video:
    def __init__(self, html, channel_name):
        self.html = html
        self.channel_name = channel_name
        extract = self.get_elements()
        self.name = extract['name']
        self.date = extract['date']
        self.views = extract['views']
        self.description = extract['description']
        self.pirkovskii = self.pirkovskii_here()
        extract = ''
        self.html = ''
        
    def get_elements(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        description = my_find(soup, 'description')
        date = my_find(soup, 'date')
        try:
            views = ''
            views_raw = soup.find_all(id='count')
            for v in views_raw:
                if v.text != '':
                    views += v.text
        except:
            views = ''
        try:
            name = soup.find('h1').text
        except:
            name = ''
        elements = {'date' : date, 'views' : views, 'description' : description, 'name' : name}
        return elements
    
    def pirkovskii_here(self):
        text = self.description.lower() + self.name.lower()
        if 'pirkovsk' in text or 'пирковск' in text:
            self.pirkovskii = True
        else:
            self.pirkovskii = False

def my_find(soup, id_):
    try:
        element = soup.find(id=id_).text
    except:
        element = ''
    return element
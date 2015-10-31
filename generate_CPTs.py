import xml.etree.ElementTree as ET


tree = ET.parse('10-19-20s_706posts.xml')
root = tree.getroot()

wordCounts = []
windowCounts = []
for post in root.iter('Post'):
    window = ['0', '0']
    if post.attrib['class'] != 'System':
        for t in post.iter('t'):
            word = t.attrib['word']
            if t.attrib['pos'] == '.':
                word = '.'
            if t.attrib['pos'] == 'NNP':
                word = 'NNP'
            strWindow = ':'.join(window)
            instance = {'window': strWindow, 'word': word, 'count': 1}
            seenInstance = False
            seenWindow = False
            for x in wordCounts:
                if x['window']==strWindow:
                    if x['word'] == word:
                        x['count'] = x['count'] + 1
                        seenInstance = True
                    seenWindow = True
                    for windowInstance in windowCounts:
                        if windowInstance['window'] == strWindow:
                            windowInstance['count'] = windowInstance['count'] + 1
            if not seenInstance:
                wordCounts.append(instance)
            if not seenWindow:
                windowCounts.append({'window':strWindow, 'count': 1})
            window[0] = window[1]
            window[1] = word

for windowCount in windowCounts:
    for wordCount in wordCounts:
        if windowCount['window'] == wordCount['window']:
            wordCount['count'] = float(wordCount['count'])/float(windowCount['count'])

CPTFile = file('CPTs.csv', 'w')
for wordCount in wordCounts:
    CPTFile.write(wordCount['window'] + ',' + wordCount['word'] + ',' + str(wordCount['count']) + '\n')
# Introduction

Title: I Will Scrape 500 Sites (And I Will Scrape 500 More)

In this workshop you will learn about the tools and terminology related to gathering data from the web.
The main focus is teaching you the fundamental concepts in web scraping.
We will demonstrate how with these concepts you can use tools like search engines and AI to help create a script for your specific purpose.

For the workshop we will use `repl.it` to run python scripts.
To use this service, you must make a `github` account.
It is useful if you have a free openai account to make use of chatgpt during the workshop.
You do not need to install anything else.
The workshop is highly interactive and will require you to make many mistakes, be prepared to experiment a lot.

Topics:

- Data Sources
  - Database
  - API
  - Feeds
  - Web Page
- Querying Data
- Parsing Data
- Selecting, Structuring, and Output

Duration: ~3 hours (including breaks)


# Script

## Part 1: Data and Data Representation

In this workshop we look at how you can gather data from websites.
For that to happen, we need to define the term `data`. 
That in itself is a pretty big question with many caveats and "well actually"-s, but for the purposes of this workshop, think of data as a spreadsheet.
Specifically the type of spreadsheet that has a header and then a bunch of rows of data and can be opened with Excel - no formulas, no worksheets, just rows of data.
Whenever you think of data, that's the picture you should have in your head.
This picture is what we can call a `data representation` - in reality the data looks different.
For instance, if you have a `.csv` file, and you open the file in notepad, the data might actually look something like this:

```csv
title,artist,duration
Antitaxi,La Femme, 3:12
Cracker Island,Gorrilaz,4:10
```

But if you open the file in excel, it will look something like this: 

| title          | artist   | duration |
|----------------|----------|----------|
| Antitaxi       | La Femme | 3:12     |
| Cracker Island | Gorillaz | 4:10     |

The closest thing to reality would be a `byte representation` of the data, which would look something like this:

```sh
74 69 74 6c 65 2c 61 72 74 69 73 74 2c 64 75 72 61 74 69 6f 6e 0a 41 6e 74 69 74 61 78 69 2c 4c 61 20 46 65 6d 6d 65 2c 20 33 3a 31 32 0a 43 72 61 63 6b 65 72 20 49 73 6c 61 6e 64 2c 47 6f 72 72 69 6c 61 7a 2c 34 3a 31 30
```

All 3 of these examples are in essence the same data, but their presentation is different.
In this case when we open the `csv` file in Excel, it figures out how to represent it.
It knows to look for a delimiter and the puts the data in cells to turn it into a table.
The takeaway here is `different programs represent the same data in different ways`.
As we saw, if we open this same csv in notepad, it's just text and commas.
Now consider if we change the `csv` file like this, would it still work to open in Excel?

```csv
title artist duration
Antitaxi La Femme 3:12
Cracker Island Gorrilaz 4:10
```

The answer is no.
What we can take from this, is that there are rules to writing a csv file for it to work in excel.
Or to incorporate it in the previous takeaway: `different programs represent the same data in different ways so long as they obey the rules for the way the data is described`
In the case of `csv` the rule is that there must be a delimiter between every value - most often this is a comma.

The reason we focus on `csv` so specifically, is because it is an 'easy' format to work with that we can easily inspect in excel.
There are far more efficient ways of describing data, but with the efficiency we lose the benefit of being able to load it up into excel to have a nice visual representation.
With somewhat of a grasp on the difference between `data description` and `data presentation` we can now look at how data is described for websites and how browsers present that data.


## Part 2: Browser Data Representation

Browsers (regardless of type/brand) are just programs like excel.
They have their own rules for how you should describe data and these rules are encapsulated by something called HTML and for the data we have worked with so far, it might look like this:

```html
<table>
  <thead>
    <tr>
      <th>title</th>
      <th>artist</th>
      <th>duration<th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Antitaxi</td>
      <td>La Femme</td>
      <td>3:12</td>
    </tr>
    <tr>
      <td>Cracker Island</td>
      <td>Gorrilaz</td>
      <td>4:10</td>
    </tr>
  </tbody>
</table>
```

The browser knows how to make this into a pretty table, but it is considerably harder to work with than a `csv` file for our purposes.
When we talk of web scraping, then generally it means taking this `html` and converting it into a format that makes more sense to us - in this case `csv`
One thing to take into account is that very rarely people actually write `html` in this way.
The way websites work is that there is a database (which you should visualize as a spreadsheet) and a program is used to add the `html` rules to the values of that `data`.
Since the data is already there, you might be wondering why the heck are we jumping through all these hoops to reverse engineer the data back to a format that basically already exists.
And ideally, you would not have to - the fastest and most reliable way to get data from a website is to ask for it.
If you can figure out who to mail, there's a pretty good chance you can get the data you want without having to do any web scraping and this would always be the preferred method.

In other cases, websites might offer something called an API for their data, where they will give a more friendly representation of their data in json:

```json
[
  {"title": "Antitaxi", "artist": "La Femme", "duration": "3:12"},
  {"title": "Cracker Island", "artist": "Gorillaz", "duration": "4:10"}
]
```

Today the focus is on the most annoying way though, which is parsing HTML. 
  

## Part 3: HTML Parsing by Hand

Let's look at how we would 'scrape' a site by hand, then after we can take a look how we can automate each part of this process.
Go to the following site: https://www.scrapethissite.com/pages/simple/
Then find a way to `inspect source` - you should see a bunch of HTML code.

Let's say we want to know all the capitals, how would you go about it using nothing but `ctrl-f`?
You need to figure out how to find the unique identifier for all capitals, so what text can we search for?
What about country capitals?

Now imagine that you wanted to create a csv of each country and its capital, how would you do that manually?

Now let's take a look at a different site: https://durstongear.com/pages/tents
Inspect the source again - how would you get a list of all tents?

We'll look at one more: https://www.marktplaats.nl/

As you can see, there are varying degrees of difficulty in scraping websites - though `marktplaats` may seem impossible, if you're really determined, there is a way. 
Our focus today is on the easy sites to develop a foundational understanding of scraping.

Before we move on to automation, let's write the manual steps that we did to find our data:

1. We open a link in the browser
2. We inspect the source to get the HTML description of the data
3. We find out how we can effectively `ctrl-f` through the document to find the data we want
4. We write the data into a csv file 

### Tangent: What happens when you got to a website

When you press enter after typing in the url into the address bar, you set into motion about a million moving parts which end up with you seeing a webpage.
The amount of stuff that happens in this short period of time is so immense and complex that is a question that gets asked in software engineering interviews all the time.
A single person could not explain the amount of the complexity that happens.
That said, it is good to gradually build an understanding of this as you work more with web-based technologies, so in this tangent we look at a simplified version of what happens when you visit a website.

The very first thing that happens, is that your browser builds a `Request`.
Within the request we put a bunch of information:

   1. What URL are you going to?
   2. Which method are you using to reach this URL?
   3. What sort of data to you accept if the server responds?
   4. What sort of browser are you using?
   5. What cookies do you have on your computer?

Once that request is built, it gets sent to the server.
A server is basically the computer on which the program is running and it is identified by an address.
If you go to a URL like `https://www.example.com/users/123` then the address would be `www.example.com`; once it arrives at that server it figures out what to do with `/users/123`.
When the request arrives at the server, the server takes a look at it and starts building a `Response`.
This object has information like:

1. What text am I sending back to the requester?
2. What status code do I send back? 
3. What is the type of the text I am sending?
4. What cookies should be set on the requesters computer?

The 'text' part of a `Response` is called the `body`.
This will always be there, but the `Response` also says stuff like "hey, that body is of type `html`" or "hey, it's actually `json`".
That way, when the response arrives back to the browser, the browser knows what to do with it.
It handles different files in different ways.
If it gets an html file, it redraws the website.
If it gets a json file, it will format the data and show it to you.
If it gets a font file, it will download the font on your computer.

The `Response` gets built dynamically on the server based on the `Request` sent by your browser.

## Part 4: Automating the Process

The automation will (mostly) follow the same process we would do as the manual method.

### Step 1: Define your data structure

Remember how we said we think of data as a spreadsheet?
Well spreadsheet data is structured - at the top we define a bunch of headers, in this case the headers are title, artist, and duration:

| title          | artist   | duration |
|----------------|----------|----------|
| Antitaxi       | La Femme | 3:12     |
| Cracker Island | Gorillaz | 4:10     |

To mimic this structure in python, we need to create a `class`.
A `class` is like a template for data, it basically describes all the attributes that we expect to have for a given thing.
The most straightforward way to do this in python is with dataclasses:

```python
from dataclasses import dataclass # dataclasses are part of the standard library in python, no need to install anything

@dataclass # <- this is what we call a `decorator`, as the term implies, it will decorate whatever is coming after.
class Song:
  title: str
  artist: str
  duration: str
```

Using this dataclass decorator we can skip writing a bunch of stuff for this class to be functional.
If we were to do it without the `dataclass` decorator, this code would look something like this:

```python
class Song:
  # initialization method
  def __init__(self, title, artist, duration):
    self.title = title
    self.artist = artist
    self.duration = duration
  
  # representation method - what happens if we do `song`
  def __repr__(self):
    return f"<Song {self.song}, {self.artist}, {self.duration}>

  # str method - what happens if we do `str(song)`
  def __str__(self):
    return self.__repr__()

  # comparison method - what happens if we do `song1 == song2`
  def __eq__(self, other):
    if self.title == other.title and self.artist == other.artist and self.duration == other.duration:
      return True
    else:
      return False

  # and more abstract stuff
  ...
```

Suffice it to say, `dataclass` does a lot of heavy lifting for us and it is part of the standard library so let's make use of it.
The only 'odd' thing you might find about it is this syntax:

```python
title: str
```

What this means, is that we say `title` will have a type of `str`.
This is something called type annotations and you are allowed to use them anywhere you want in python, they aren't strictly enforced.
It is useful, because it allows you to reason a bit better about your code, and more importantly, it helps your computer figure out what is possible with this data.
If your code editor know that `title` is a string, it can offer auto completions directly in the code editor.

Right now we have only defined the template of this data, but not created any data of that type.
If we wanted to do that, it would look something like this:

```python
song1 = Song(title="Antitaxi", artist="La Femme", duration="3:12")
song2 = Song(title="Cracker Island", artist="Gorrilaz", duration="4:10")
```
#### Tangent: why shouldn't I use `dict`?

First, the author would like to disclaim that this is your life and you can and should do whatever you want.
The author however chooses to avoid `dict` when possible, because it can be less obvious what the data structure is to others (and to yourself if you don't look at the code for a week).
For instance, let's say you are instantiating data in multiple places over multiple files.
With a dict that might look something like this:

```python
# tweets.py
def get_tweets():
  ...
  for tweet in ...:
    {"id": ..., "name": ..., "text": ...}
  ...

# instagrams.py
def get_instagrams():
  ...
  for instagram in ...:
    {"id": ..., "name": ..., "story": ...}
  ...
```

Your data structures might not line up.
If you were to try the same thing with dataclasses, you would get an error before even running the script.

```python
@dataclass
class Social:
  id: int
  name: str
  text: str

Social(id=1, name="lalal", text="hahaha") # OK
Social(id=1, name="lalal", story="hahaha") # ERROR
```

If you are running data analysis in subsequent steps, it's a pretty expensive mistake to find out after running the script.
In addition, with the use of dataclasses, your code editor will know that `name` and `text` are strings and will suggest string-based operation and it will suggest int-based operation for `id`. 
Finally, if you think about the data before harvesting it, you will have a leaner data model that has a more specific purpose.
In terms of code readability, this is a big plus and it can also help guide you in what data you need to find on various sources to compose this data model. 
In a way, you define your goal before setting out on the journey. 


### Step 2: Get the raw data (`html` or `json` or something entirely different)

To automate the part of getting the raw `html`, we will have to use a python library.
The library of choice is `httpx`.
To install libraries in python, we use the python package manager.

```sh
pip install httpx
```

This allows us to import the `httpx` package and make requests to websites:

```python
import httpx

response = httpx.get("https://www.example.com")
html = response.text
```

If we know the response to be of type `html` we can access that property with `.text`.
If we know the response to be of type `json`, we can access it with `.json()`.

```python
data = response.json()
```

Ideally, the data you get back is of type json as it is easier to work with.
What you would get back, would be basically equivalent to a python dictionary.
For now we assume you get back `html`.

#### (Judgemental) Tangent: why `httpx` and why not `requests`? 

The author is of the opinion that the choices you make have a lasting impact on people around you.
If you buy ethically sourced produce, you inspire others to do the same.
If you take the train, others might follow.
If you choose to overwork, you pressure others into doing the same.

In the context of package selection, it is roughly equivalent to which type of eggs you buy at the supermarket.
Will you get the eggs that have a reputation of being opaque, mean to users and community, and driven by a for-profit motive?
Or will you get the eggs that are made in a collaborative spirit with complete transparency?

In practice, `requests` and `httpx` are almost identical in how they work; undeniably `requests` pioneered a great API.
However, the environment in which `requests` was developed, created, and further exploited is not something the author wishes to perpetuate.

### Step 3: Wrangle the data into the desired data structure

The next step in our journey is going from `html` to our structured data format.
To achieve this, we will use `bs4` or `Beautiful Soup 4`:

```sh
pip install bs4
```

This software allows us to automate the `ctrl-f` part of the manual process.
Assume we have a variable with the following html:

```html
<table>
    <thead>
      <tr>
        <th class="title">title</th>
        <th class="artist">artist</th>
        <th class="duration">duration<th>
      </tr>
    </thead>
    <tbody>
      <tr class="song">
        <td class="title">Antitaxi</td>
        <td class="artist">La Femme</td>
        <td class="duration">3:12</td>
      </tr>
      <tr class="song">
        <td class="title">Cracker Island</td>
        <td class="artist">Gorrilaz</td>
        <td class="duration">4:10</td>
      </tr>
    </tbody>
  </table>
```

To construct our structure data from the following example, we would do something like this:

```python
from bs4 import BeautifulSoup

html = ...

soup = BeautifulSoup(html, "html.parser")
all_songs = soup.find_all("tr", class_="song") # Find all the individual rows of data
song_data = []
for song in all_songs:
  song_data.append(
    Song(
      title=song.find("td", class_="title"), # within each row, find the title etc...
      artist=song.find("td", class_="artist"),
      duration=song.find("td", class_="duration")
    )
  )
```

Our goal when using this `find` function is to be as specific as possible.
If we were to do something like `soup.find_all(class_="song")` it would also give us the header of the table and in this case that is not of interest to us.
Not all `html` will have convenient classes, so often you will have to have a hierarchical approach to locating data, so you might have code like:

```python
songs = soup.find("section").find("div", class_="lalala").find("table").find("tbody")
```

### Step 4: Export the data

Once we have our list of dataclass instances, it is time to export them into a format suited for further analysis.
In this case we will choose `csv`, but if you are more advanced with python or computing, you could use a database at this point.

To export dataclasses to csv, we use the following python code:

```python
import csv # a builtin python module

dict_data = [c.__dict__ for c in countries] # convert every dataclass to a dictionary
headers = dict_data[0].keys() # get the headers
with open('output.csv', 'w') as output_file: # output.csv is the name of the file, the 'w' signifies opening the file with write permissions
  dict_writer = csv.DictWriter(output_file, headers)
  dict_writer.writeheader()
  dict_writer.writerows(dict_data)
```

## Part 5: Advanced Topics

### The `User-Agent` roadblock

One of the most basic ways of preventing people from scraping a website, is by checking out the browser that the request is being made from.
This is specified in the `User-Agent` header and if you use something like `httpx`, the header will be something like `python310httpx`.
Notably, this is neither chrome, nor firefox, nor edge, nor internet explorer.
You can try to make it look like you are using a browser, by changing the `User-Agent` header however:

```python
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}

response = httpx.get("https://www.example.com", headers=headers)
```

This user agent you can figure out from the network tools of your browser.

### The arbitrary header roadblock

A more advanced version of `User-Agent` is requiring some arbitrary headers.
To that end, we can go a more drastic approach and use the `curl converter`.
Visit this [site](https://curlconverter.com/python/) for more instructions.
Using the network tools of your browser (as specified in the website above) you can get a `curl` version of that request.
Using the tool, you can convert the `curl` request to a dictionary of headers and cookies.
In the tool they make use of `requests` but you can easily swap it out for `httpx` without any changes. 

### The 'My website only works if you load javascript' roadblock

This is unfortunately slightly out of scope of this workshop.
In this case you would have to 'mimic' visiting a website using an automated web browser.
For python 2 good options are `splinter` and `selenium`.
Selenium is more feature rich but is built using `Java` so it is not really intuitive to use and its age is showing.
Splinter is a more modern alternative (but still kind of uses selenium underneath), but offers a nicer API.


### The Kickstarter conondrum

Some sites find a way to make scraping incredibly hard.
Kickstarter is one such website - even by completely recreating the request in python, it fails to execute.
It also seems like a new cookie is set on visit of every page, so it is not a site that is easily crawled programmatically.
The author has not tried to scrape the website using an automated web browser, however after copying the curl command as defined in the `curl converter` website and running the command, you do get some HTML back.
Looking at it though, it would be exceedingly hard to parse that data, so the advice is to use an automated browser so that all that data can be loaded onto the page.
You could attempt to go to a URL with all the headers that you get from `copy curl command` - below is an example of how that might look.
In the `kickstarter-curl-output.html` you can see an example of what the author gets after running the `curl` command (it's pretty javascript-heavy). 
Or better yet: if kickstarter really wants that data analyzed, have them send it over :)

```sh
curl 'https://www.kickstarter.com/projects/onipress/cult-of-the-lamb?ref=section-homepage-featured-project' \
  -H 'authority: www.kickstarter.com' \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'cache-control: max-age=0' \
  -H 'cookie: ref_863741201=section-homepage-featured-project%3F1712738182; __cf_bm=Ju2l7Nf.wTHeEXx_eGUa0sNHUHEzpKg_XJILZwkdKxs-1712738175-1.0.1.1-n8VC18olVtwD0iVul32CrTS1eJ6Zdjh49VD5M3yxZIBtHwlGrPYyqyf4Ww.1jF0Xc588ljStWldVTr_W1MVmFw; vis=ef14b085bea6213b-dbb927c709eafffa-381068f538f569c5v1; woe_id=%2B8l%2BYo%2FxcUPqRbGz1%2Fwk%2FmafZhuYkSj22hKpmq%2FQ2QwAATQHxNwCs5o%2BHKdIGkwfxbjUHm7R2Duwumjd%2F6PBLLQZquX%2BOvjErb3oUYLuw1TnmpyCJGHqYA%3D%3D--tooUW2OxLUnmR5J5--4ggYPbMmCfWLW4NIP4CP%2Fg%3D%3D; lang=en; last_page=https%3A%2F%2Fwww.kickstarter.com%2Fprojects%2Fonipress%2Fcult-of-the-lamb%3Fref%3Dsection-homepage-featured-project; optimizely_current_variations=%7B%7D; local_offset=-514; ksr_consent=%7B%22purposes%22%3A%7B%22SaleOfInfo%22%3A%22Auto%22%7C%22Analytics%22%3Afalse%7C%22Functional%22%3Afalse%7C%22Advertising%22%3Afalse%7D%7C%22confirmed%22%3Afalse%7C%22prompted%22%3Afalse%7C%22timestamp%22%3A%222024-04-10T08%3A36%3A24.243Z%22%7C%22updated%22%3Afalse%7D; cf_clearance=owj1lCnSnUt3EH915jTr0uKSeyAQJ3T4YBmxs7lsmDU-1712738185-1.0.1.1-KlgLSdAYGmT2mVRfrN5DDGh3T5vF5xMOWP2I9rRQxKBA5r8Eobsc6gJYB3HfWTsQme1zT_NZfbNXhfapfiCL5Q; __stripe_mid=091e7232-64f2-4a27-9ea8-0bb110e85df86cf81c; __stripe_sid=00473128-315b-4c3a-8a23-fe027b359bf664b671; _ksr_session=ouPDE8vLKNWt1MrMywNwa2N41GGyMmNECzJPJJNyvUeKtWxUyLYUnjRnQYu5%2BPGzKf3JVs7AlYey8FKCHMUIdiXAZ4qAlQIYhKu%2FZKKv99oKzhUHKN2rWfES6NUG27AG0TA%2FEQhiSH5pU11WoR3uC57l%2BUMr%2BvR%2F8IXG1VRWr0F5YrvtY473B8goSBzVFhx8v%2FwJuhngr5kaLxn0s0mmprE7me4BpNfVGMV5hgAzZc%2FA0zRKHAvZko0myP0L9FcIO0PA4SAGSrrDJg%2FizDpz1O6Fgmw%3D--V27pdvXiZE8lfGPQ--nq2hcVk%2Fbs9T17Qp2MhAYQ%3D%3D; request_time=Wed%2C+10+Apr+2024+08%3A36%3A37+-0000' \
  -H 'sec-ch-ua: "Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  -H 'sec-fetch-dest: document' \
  -H 'sec-fetch-mode: navigate' \
  -H 'sec-fetch-site: none' \
  -H 'sec-fetch-user: ?1' \
  -H 'upgrade-insecure-requests: 1' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36' \
  --compressed
```


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


## Part 4: Automating the Process

TODO

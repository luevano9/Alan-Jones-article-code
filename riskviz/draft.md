# Visualizing Health Risk

## The press can get it wrong when dealing with health risk data. Can visualizations help.

In November 2015, the International Agency for Research in Cancer (part of the World Health Organisation) reported that eating 50 grams of processed meat - bacon or sausages, for example - was associated with an 18% increase in the risk of bowel cancer. 

The press reported this scary sounding increase but did not make it clear that this was a _relative_ risk rather than an _absolute_ one. In other words it was an increase in risk rather than the actual risk.

Inaccurate reporting may be because a sensational headline like '__X Gives You Cancer__' is too hard to resist for some newspapers but sometimes the media get it wrong because data is misinterpreted by journalists who don't necessarily understand what they have been presented with.

The risk of getting bowel cancer, in the population as a whole, is about 6%. An increase of 18% means that the risk rises to about 7%. 

    6 * 1.18 = 7.08


So, in absolute terms the risk rises by 1% - a much less scary numberand one which is less likely to put people off an occasional English Breakfast or bacon sandwich.

A simple visualization that demonstrated the real impact of the statistics would be easier to understand than simply reporting the figures. A bar chart, for example, could show how small the 1% increase is.

**insert annotated figure here**

Although in his book _The Art of Statistics_[1], David Speigelhalter suggests that an icon array would be better, while **insert ref**[2] found that simpe pie charts were more effective at communicating risk in a study of **insert description**


I'm going to write some Python code to look at some options for visualizing risk including bar charts, heatmaps, icons arrays and pie charts. If you want to follow along you'll need to import these libraries.

    import random
    import numpy as np
    import seaborn as sns
    import matplotlib.pyplot as plt
    import pandas as pd

Here is some code that constructs a dataframe that represents 100 people and the number of them that will get cancer. Six will get cancer by chance, 18% of 6 will get it from eating processed meat (I'm using _bacon_ in the code to represent all processed meat). The rest won't get cancer.

    data = pd.DataFrame()
    pop = 100                   # total population
    chance = 6                  # number who get cancer by chance
    bacon = int(6 * 0.18)       # number who get cancer by eating bacon
    none = pop - chance - bacon # number who won't get cancer 

    data['Non-sufferer'] = [none]
    data['Sufferer by Chance'] = [chance]
    data['Bacon Eater'] = [bacon]


First we'll draw some bar charts to see if that better represnts the risk of eating bacon. We'll use the plotting features of Pandas to do this.

The following bar chart puts the additional risk into better perspective than the raw data. The _Bacon Eater_ column is tiny compared to the overall population.

    data.plot.bar(figsize=(8,5))

![](https://github.com/alanjones2/Alan-Jones-article-code/raw/master/riskviz/images/barv.png)

Would it be better as a stacked chart?

    data.plot.bar(stacked=True,figsize=(8,5))


![](https://github.com/alanjones2/Alan-Jones-article-code/raw/master/riskviz/images/barvstacked.png)


The numbers are the same, of course, but the top layer of the bar is not very visible.

What if we were to turn them round so that become horizontal bars.

    data.plot.barh(figsize=(8,5))

![](https://github.com/alanjones2/Alan-Jones-article-code/raw/master/riskviz/images/barh.png)

    data.plot.barh(stacked=True,figsize=(8,5))

![](https://github.com/alanjones2/Alan-Jones-article-code/raw/master/riskviz/images/barhstacked.png)


Charts like this are probably better than raw percentages but are not particularly attractive. Perhaps we can do better.

Or perhaps we should try a different sort of chart altogether.

    data.T.plot.pie(subplots=True,figsize=(8,5))

![](https://github.com/alanjones2/Alan-Jones-article-code/raw/master/riskviz/images/pie.png)

Sometimes pie chart are not at all clear, particulary when there are several categories to represent. However, this one has only 3 different bits of data tp plot and does a pretty good job of showing the releative proportions.

I've used the default color scheme for each of these charts - it might be better to change the colours to hilight the smaller number of Bacon Eaters.

But let's look at something quite different - heat maps.

For this I'm going to use the Seaborn data visualization package. First, though, the data needs to be represented differently. I'm going to construct a 10 by 10 grid with each cell representing someone who is cancer free, who contracts the disease by chance, or who succumbs to too much bacon.

I start by making 3 

    # Arrays of the different cases
    a1 = [0]*data['Non-sufferer'].values[0]
    a2 = [1]*data['Sufferer by Chance'].values[0]
    a3 = [2]*data['Bacon Eater'].values[0]

    # Stitch them together
    a1.extend(a2)
    a1.extend(a3)

Then I make it into a 10 by 10 grid.

    # Create a grid from the array
    b = np.array(a1).reshape((10,10))

The Sesaborn heatmap is really intended for continous variables rather than the discrete ones we have here. In consequence I have set the color map to only 3 colors to map on to the 3 categories, have adjusted the colorbar (legend) appropriately and set the correct labels.

    # Plot the grid as a heat map in Seaborn
    fig, ax = plt.subplots(figsize=(8,5))
    sns.heatmap(b, 
                linewidths=0.5, 
                yticklabels=False,
                xticklabels=False, 
                cmap=['lightblue','royalblue','midnightblue']
    )

    # Customize legend
    colorbar = ax.collections[0].colorbar 
    colorbar.set_ticks([0.5,1,1.5])
    colorbar.set_ticklabels(['Cancer-free','Cancer by chance','Bacon Eater'])

The result is this.

![](https://github.com/alanjones2/Alan-Jones-article-code/raw/master/riskviz/images/hmap.png)

Which definitely shows the proportion well enough but it has been suggested that a random disperasal of the tiles might give a better impression of the random nature of the events. Here's the code to implement that.

    # Shuffle the data and redraw

    random.shuffle(a1)
    b2 = np.array(a1).reshape((10,10))
    fig, ax = plt.subplots(figsize=(8,5))
    sns.heatmap(b2, 
                linewidths=0.5, 
                yticklabels=False,
                xticklabels=False,
                cmap=['lightblue','royalblue','midnightblue']
                )

    # Customize legend
    colorbar = ax.collections[0].colorbar 
    colorbar.set_ticks([0.5,1,1.5])
    colorbar.set_ticklabels(['Cancer-free','Cancer by chance','Bacon Eater'])

Is this a better representation of the situation?


![](https://github.com/alanjones2/Alan-Jones-article-code/raw/master/riskviz/images/hmaprandom.png)


And a more personal looking chart might be an icon array which uses something that we are used to seeing as a representation of people: and icon from the Bootstrap Icon collection.

![](https://github.com/alanjones2/Alan-Jones-article-code/raw/master/riskviz/images/person.png)



    # Use icons to represent people and draw them in an HTML table

    from IPython import display

    # Create three icons of different colours
    personOrange = '<i class="bi-person-fill" style="font-size: 1rem; color: orange;"></i>'
    personRed = '<i class="bi-person-fill" style="font-size: 1rem; color: red;"></i>'
    personGrey = '<i class="bi-person-fill" style="font-size: 1rem; color: grey;"></i>'

    # The first part of the HTML

    head = """
    <link rel="stylesheet" 
        href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.3.0/font/bootstrap-icons.css">

    <div">
    """

    # The last part of the HTML
    tail = "</div>"

    # The middle
    rows=""
    for r in range(0,b2.shape[1]):
        rows = rows + "<tr style='background-color:#f0f0f0'>"
        td = ""
        for c in range(0,b2.shape[0]):
            icon = personGrey
            if b2[c][r] == 1:
                icon = personOrange
            elif b2[c][r] == 2:
                icon = personRed
            td = td + f"<td>{icon}</td>"
        rows = rows + td + "</tr>" 

    legend = f"""
        <div style="display:inline-block;padding:10px">
        {personRed} Bacon Eater with cancer<br/> 
        {personOrange} Cancer by chance <br/>
        {personGrey} Cancer free
        </div>
    """

    table = "<table style='display:inline-block'>"+rows+"</table>"

    table = head + table + legend + tail

    display.HTML(table)


![](https://github.com/alanjones2/Alan-Jones-article-code/raw/master/riskviz/images/iconarray.png)
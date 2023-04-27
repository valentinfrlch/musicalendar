# plot the results of out average moods in plotly
import plotly.express as px

def average_mood(data, average=7):
    # the data will consist of tuples in a list. tuple[0] is the date, tuple[1] is the mood_score from 0 to 1 (float)
    # plot on an x-y graph -> x is date, y is mood_score
    
    # get the dates and mood_scores
    dates = []
    moods = []
    for i in data:
        dates.append(i[0])
        moods.append(i[1])
    
    # plot
    # average over one week
    if average > 1:
        # get the average of each week
        dates = dates[::average]
        moods = [sum(moods[i:i+average])/average for i in range(0, len(moods), average)]
    fig = px.line(x=dates, y=moods)
    fig.show()
    
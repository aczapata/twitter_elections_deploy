import json
import random
from django.shortcuts import render, get_object_or_404
from .models import TwitterData, Sentiment
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from .forms import ResultsForm, CompareForm
from nvd3 import pieChart
import numpy as np
import matplotlib
import matplotlib.path as path
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def index(request):
    return render(request, 'collector/index.html')


def list_tweets(request):
    tweets_list = TwitterData.objects.all()
    cont_correct = 0
    cont_incorrect = 0
    cont_ext_incorrect = 0
    correct = []
    incorrect = []
    ext_incorrect = []
    total_votes = 0
    for tweet in tweets_list:
        tweet_total_votes = tweet_votes(tweet)
        total_votes += tweet_total_votes
        if total_vote_sentiment(tweet) == "POS":
            sentiment_vote = "positive"
        elif total_vote_sentiment(tweet) == "NEG":
            sentiment_vote = "negative"
        elif total_vote_sentiment(tweet) == "UND":
            sentiment_vote = "neutral"
        elif total_vote_sentiment(tweet) == "IRR":
            sentiment_vote = "irrelevant"
        else:
            sentiment_vote = "not tagged"

        if sentiment_vote != "not tagged":
            if tweet.tweet_sentiment == sentiment_vote:
                cont_correct += 1
                correct.append(tweet)
            else:
                cont_incorrect += 1
                incorrect.append(tweet)
                if (sentiment_vote == "positive" and tweet.tweet_sentiment == "negative") or (sentiment_vote == "negative" and tweet.tweet_sentiment == "positive"):
                    cont_ext_incorrect += 1
                    ext_incorrect.append(tweet)

    context = {'tweets_list': tweets_list, 'correct': correct,'incorrect': incorrect, 'ext_incorrect': ext_incorrect, 'cont_correct': cont_correct, 'cont_incorrect': cont_incorrect, 'cont_ext_incorrect': cont_ext_incorrect }
    return render(request, 'collector/list.html', context)


def function_to_graph(x_axis, y_axis, title):
    chart = pieChart(name=title, color_category='category20c', height=450, width=450)
    xdata = x_axis
    ydata = y_axis
    extra_serie = {"tooltip": {"y_start": "", "y_end": "tweets"}}
    chart.add_serie(y=ydata, x=xdata, extra=extra_serie)
    chart.buildcontent()
    return chart.htmlcontent

def bar_chart(x_axis, y_axis, title):
    chart = barChart(name=title, color_category='category20c', height=450, width=450)
    xdata = x_axis
    ydata = y_axis
    extra_serie = {"tooltip": {"y_start": "", "y_end": "tweets"}}
    chart.add_serie(y=ydata, x=xdata, extra=extra_serie)
    chart.buildcontent()
    return chart.htmlcontent


def get_file(option, event):
    return "./static/files/json_data_" + option + "_" + event


def tests():
    tweets = TwitterData.objects.all()
    for tweet in tweets:
        choices = tweet.sentiment_set.all()
        max_votes = 0
        vote_sentiment = None
        for choice in choices:
            if choice.votes > max_votes:
                vote_sentiment = choice
                max_votes = choice.votes
        if vote_sentiment is not None:
            print vote_sentiment
        else:
            print "No sentiment"


def vote_sentiment(tweet):
    choices = tweet.sentiment_set.all()
    max_votes = 0
    vote_sentiment = None
    for choice in choices:
        if choice.votes > max_votes:
            vote_sentiment = choice
            max_votes = choice.votes
    if vote_sentiment is not None:
        return vote_sentiment.sentiment_text
    else:
        return "No sentiment"


def total_vote_sentiment(tweet):
    choices = tweet.sentiment_set.all()
    max_votes = 0
    vote_sentiment = None
    for choice in choices:
        if choice.votes > max_votes:
            vote_sentiment = choice
            max_votes = choice.votes
    if vote_sentiment is not None:
        if vote_sentiment.votes == tweet_votes(tweet):
            return vote_sentiment.sentiment_text
        else:
            return "No decision"
    else:
        return "No sentiment"

def results(request):
    context = []
    if request.method == "POST":
        if 'compare' in request.POST:
            compare_form = CompareForm(request.POST)
            if compare_form.is_valid():
                form = ResultsForm()
                op1 = compare_form.cleaned_data['option1']
                op2 = compare_form.cleaned_data['option2']
                ev = compare_form.cleaned_data['event']
                file1 = open(get_file(op1, ev), "r")
                context = {}
                context1 = json.loads(file1.readline())
                for a in context1:
                    context.setdefault("OP1_" + a, context1[a])

                x1 = context1['x_axis_sentiment']
                y1 = context1['y_axis_sentiment']
                OP1_graph_sentiment = function_to_graph(x1, y1, 'sentiment1')

                file2 = open(get_file(op2, ev), "r")
                context2 = json.loads(file2.readline())
                for a in context2:
                    context.setdefault("OP2_" + a, context2[a])

                x2 = context2['x_axis_sentiment']
                y2 = context2['y_axis_sentiment']
                OP2_graph_sentiment = function_to_graph(x2, y2, 'sentiment2')
                context.update({'filters': False, 'form': form, 'compare_form': compare_form, 'OP1_graph_sentiment': OP1_graph_sentiment, 'OP2_graph_sentiment': OP2_graph_sentiment})
                return render(request, 'collector/filter.html', context)
        elif 'filter' in request.POST:
            form = ResultsForm(request.POST)
            if form.is_valid():
                option = form.cleaned_data['option']
                event = form.cleaned_data['event']
                file = open(get_file(option, event), "r")
                json_data = file.readline()
                context = json.loads(json_data)
                x = context['x_axis_language']
                y = context['y_axis_language']
                graph_languages = function_to_graph(x, y, 'language')

                x1 = context['x_axis_sentiment']
                y1 = context['y_axis_sentiment']
                graph_sentiment = function_to_graph(x1, y1, 'sentiment')
                compare_form = CompareForm()
                context.update({'filters': True, 'form': form , 'compare_form': compare_form, 'graph_languages': graph_languages, 'graph_sentiment': graph_sentiment})
                return render(request, 'collector/filter.html', context)
            else:
                print form.errors
    else:
        form = ResultsForm()
        compare_form = CompareForm()
        file = open("./static/files/json_data", "r")
        json_data = file.readline()
        context = json.loads(json_data)
        x = context['x_axis_language']
        y = context['y_axis_language']
        graph_languages = function_to_graph(x, y, 'language')
        x1 = context['x_axis_sentiment']
        y1 = context['y_axis_sentiment']
        graph_sentiment = function_to_graph(x1, y1, 'sentiment')
        context.update({'filters': True, 'form': form, 'compare_form': compare_form, 'graph_languages': graph_languages, 'graph_sentiment': graph_sentiment})
    return render(request, 'collector/filter.html', context)


def geo(request):
    return render(request, 'collector/geo.html')


def instructions(request):
    return render(request, 'collector/instructions.html')


def tweet_for_vote(request):
    tweets_list = TwitterData.objects.all()
    n = len(tweets_list)
    t = random.randint(0, n)
    tweet = tweets_list[t]
    if len(tweet.sentiment_set.all()) == 0:
        tweet.sentiment_set.create(sentiment_text="IRR")
        tweet.sentiment_set.create(sentiment_text="UND")
        tweet.sentiment_set.create(sentiment_text="NEG")
        tweet.sentiment_set.create(sentiment_text="POS")
    return render(request, 'collector/vote.html', {'tweet': tweet})


def vote(request, tweet_id):
    tweet = get_object_or_404(TwitterData, pk=tweet_id)
    try:
        selected_choice = tweet.sentiment_set.get(pk=request.POST['choice'])
    except (KeyError, Sentiment.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'collector/detail.html', {
            'tweet': tweet,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(
            reverse('collector:results_tweet', args=(tweet.id,)))


def tweet_votes(tweet):
    pos_votes = tweet.sentiment_set.get(sentiment_text='POS').votes
    neg_votes = tweet.sentiment_set.get(sentiment_text='NEG').votes
    neu_votes = tweet.sentiment_set.get(sentiment_text='UND').votes
    irr_votes = tweet.sentiment_set.get(sentiment_text='IRR').votes
    total_votes = pos_votes + neg_votes + irr_votes + neu_votes
    return total_votes


def results_tweet(request, tweet_id):
    tweet = get_object_or_404(TwitterData, pk=tweet_id)
    x = ['positive', 'negative', 'neutral', 'irrelevant']
    pos_votes = tweet.sentiment_set.get(sentiment_text='POS').votes
    neg_votes = tweet.sentiment_set.get(sentiment_text='NEG').votes
    neu_votes = tweet.sentiment_set.get(sentiment_text='UND').votes
    irr_votes = tweet.sentiment_set.get(sentiment_text='IRR').votes
    y = [pos_votes, neg_votes, neu_votes, irr_votes]
    graph_votes = function_to_graph(x, y, 'votes')
    total_votes = pos_votes + neg_votes + irr_votes + neu_votes
    sentiment_vote = vote_sentiment(tweet)
    return render(request, 'collector/results.html', {'tweet': tweet , 'graph_votes': graph_votes, 'total_votes': total_votes, 'vote_sentiment': sentiment_vote})


def radar_plot():
        # Data to be represented
    # ----------
    properties = ['positive', 'negative', 'neutral']
    values = np.random.uniform(5, 9, len(properties))
    # ----------

    # Choose some nice colors
    matplotlib.rc('axes', facecolor='white')

    # Make figure background the same colors as axes
    fig = plt.figure(figsize=(10, 8), facecolor='white')

    # Use a polar axes
    axes = plt.subplot(111, polar=True)

    # Set ticks to the number of properties (in radians)
    t = np.arange(0, 2 * np.pi, 2 * np.pi / len(properties))
    plt.xticks(t, [])

    # Set yticks from 0 to 10
    plt.yticks(np.linspace(0, 10, 11))

    # Draw polygon representing values
    points = [(x, y) for x, y in zip(t, values)]
    points.append(points[0])
    points = np.array(points)
    codes = [path.Path.MOVETO, ] + \
            [path.Path.LINETO, ] * (len(values) - 1) + \
            [path.Path.CLOSEPOLY]
    _path = path.Path(points, codes)
    _patch = patches.PathPatch(_path, fill=True, color='blue', linewidth=0, alpha=.1)
    axes.add_patch(_patch)
    _patch = patches.PathPatch(_path, fill=False, linewidth=2)
    axes.add_patch(_patch)

    # Draw circles at value points
    plt.scatter(points[:, 0], points[:, 1], linewidth=2,
                s=50, color='white', edgecolor='black', zorder=10)

    # Set axes limits
    plt.ylim(0, 10)

    # Draw ytick labels to make sure they fit properly
    for i in range(len(properties)):
        angle_rad = i / float(len(properties)) * 2 * np.pi
        angle_deg = i / float(len(properties)) * 360
        ha = "right"
        if angle_rad < np.pi / 2 or angle_rad > 3 * np.pi / 2:
            ha = "left"
        plt.text(angle_rad, 10.75, properties[i], size=14,
                 horizontalalignment=ha, verticalalignment="center")

        # A variant on label orientation
        #    plt.text(angle_rad, 11, properties[i], size=14,
        #             rotation=angle_deg-90,
        #             horizontalalignment='center', verticalalignment="center")

    # Done
    plt.savefig('radar-chart.png', facecolor='white')
    plt.show()


from turtle import pos
from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
from nltk.tokenize import word_tokenize
from nltk.corpus import opinion_lexicon
import nltk
from flask_cors import CORS
from flask_cors import cross_origin
from flask import Response
import json

app = Flask(__name__, static_url_path='/static')
CORS(app)

import mysql.connector

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/home')
def login():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/admindash')
def admindash():
    return render_template('admindash.html')
@app.route('/quizdash')
def quizreport():
    return render_template('quizdash.html')


@app.route('/analyze', methods=['POST'])
@cross_origin()
def analyze():
    text = request.form['text']
    username = request.form['username']
    reg_number = request.form['reg_number']
    batch = request.form['batch']

    # Initialize TextBlob for sentiment analysis
    blob = TextBlob(text)

    # Get the sentiment score
    sentiment_score = blob.sentiment.polarity

    # Determine the sentiment label based on the sentiment score
    sentiment = 'Positive' if sentiment_score > 0 else 'Negative'

    # Use NLTK's opinion lexicon to count positive and negative words in the input text
    positive_lexicon = set(opinion_lexicon.positive())
    negative_lexicon = set(opinion_lexicon.negative())
    tokens = word_tokenize(text.lower())  # Tokenize the text
    positive_count = sum(1 for token in tokens if token in positive_lexicon)
    negative_count = sum(1 for token in tokens if token in negative_lexicon)

    # Calculate the total number of words
    total_words = len(tokens)

    # Calculate the percentage of positive and negative words
    positive_percentage = (positive_count / total_words) * 100
    negative_percentage = (negative_count / total_words) * 100

    # Count stressful and depressive words
    stressful_words = ['stressed', 'stressing', 'stress', 'anxious', 'anxiety', 'anxiously', 'overwhelmed', 'overwhelming', 'tense', 'tension', 'tensely', 'panicked', 'panic', 'panicking', 'worried', 'worry', 'worrying', 'worryingly', 'nervous', 'nervously', 'nervousness', 'pressured', 'pressure', 'pressuring', 'burdened', 'burden', 'burdening', 'strained', 'strain', 'straining', 'exhausted', 'exhaustion', 'exhaustingly', 'fatigued', 'fatigue', 'fatiguing', 'frazzled', 'frazzling', 'overloaded', 'overloading', 'agitated', 'agitation', 'agitating', 'frantic', 'frantically', 'franticness', 'hectic', 'hecticness', 'jittery', 'jitteriness', 'jittering', 'struggling', 'struggle', 'struggled', 'on edge', 'edginess', 'overworked', 'overworking', 'rattled', 'rattling', 'drained', 'draining', 'overwrought', 'overwroughtness', 'under pressure', 'pressure', 'pressurized', 'stretched thin', 'thinly stretched', 'tired', 'tiredness', 'tiring', 'worn out', 'wearing out', 'anxiously', 'anxiousness', 'weary', 'weariness', 'run-down', 'running down', 'overburdened', 'overburdening', 'stretched', 'stretching', 'frustrated', 'frustration', 'frustrating', 'stressed out', 'stressing out', 'harried', 'harassing', 'stressed to the max', 'maximum stress', 'frenzied', 'frenzy', 'frenziedly', 'burned out', 'burnout', 'burning out', 'distracted', 'distracting', 'distractingly', 'fidgety', 'fidgeting', 'restless', 'restlessness', 'restlessly', 'overwrought', 'overwroughtness', 'on the brink', 'brink of stress', 'uneasy', 'uneasiness', 'uneasily', 'edgy', 'edginess', 'edgily', 'pressed for time', 'time pressure', 'under strain', 'strained', 'strain on', 'feeling the heat', 'heated', 'heating up']

    depressive_words = ['despair', 'despairing','depressed', 'despaired', 'grief', 'grieving', 'grieved', 'anguish', 'anguished', 'anguishing', 'melancholy', 'melancholic', 'melancholia', 'desolation', 'desolate', 'desolated', 'desolating', 'despairing', 'despaired', 'despair', 'despairing', 'desperate', 'desperation', 'desperately', 'disconsolate', 'disconsolately', 'forlorn', 'forlornness', 'heartbroken', 'heartbreak', 'heavyhearted', 'heavyheartedly', 'hopelessness', 'hopeless', 'lament', 'lamented', 'lamenting', 'melancholic', 'melancholia', 'mournful', 'mournfully', 'mournfulness', 'pain', 'painful', 'painfully', 'regret', 'regretful', 'regretfully', 'tearful', 'tears', 'tragic', 'tragically', 'tragedy', 'woeful', 'woefully', 'abandoned', 'abandonment', 'alienated', 'alienation', 'bereaved', 'bereavement', 'cheerless', 'cheerlessness', 'crushed', 'crushing', 'defeated', 'defeat', 'desperate', 'desperately', 'desperation', 'disappointed', 'disappointment', 'disheartened', 'disheartenment', 'distressed', 'distress', 'distressing', 'downcast', 'downhearted', 'downheartedly', 'downheartedness', 'gloomy', 'gloom', 'gloominess', 'grief-stricken', 'grief-strickenly', 'helpless', 'helplessness', 'hopeless', 'hopelessly', 'hopelessness', 'hurt', 'hurtful', 'hurtfully', 'hurtfulness', 'isolated', 'isolation', 'loneliness', 'lonely', 'lost', 'loss', 'miserable', 'miserably', 'misery', 'mourning', 'mourn', 'pathetic', 'pathetically', 'pessimistic', 'pessimism', 'powerless', 'powerlessness', 'rejected', 'rejection', 'sadness', 'sad', 'sorrow', 'sorrowful', 'sorrowfully', 'suffer', 'suffering', 'sufferingly', 'suffered', 'unhappy', 'unhappiness', 'unloved', 'unwanted', 'wretched', 'wretchedness', 'agonized', 'agonizing', 'agonizingly', 'anguished', 'anguishing', 'anguishingly', 'broken', 'brokenhearted', 'bitter', 'bitterness', 'dejected', 'dejection', 'deprived', 'deprivation', 'discontented', 'discontentment', 'downtrodden', 'dismayed', 'dismay', 'disillusioned', 'disillusionment', 'forlorn', 'forlornness', 'grieved', 'grieving', 'grievance', 'grievously', 'haunted', 'haunting', 'hopelessness', 'humiliated', 'humiliation', 'inconsolable', 'inconsolably', 'joyless', 'joylessness', 'longing', 'longingly', 'mournful', 'mournfully', 'mournfulness', 'nostalgic', 'nostalgia', 'nostalgically', 'numb', 'numbness', 'oppressed', 'oppression', 'regretful', 'regretfully', 'regretfulness', 'remorseful', 'remorsefully', 'remorsefulness', 'resentful', 'resentfully', 'resentfulness', 'shameful', 'shamefully', 'shamefulness', 'sorrowful', 'sorrowfully', 'sorrowfulness', 'suffering', 'sufferingly', 'suffered', 'tormented', 'torment', 'unappreciated', 'unappreciation', 'unfulfilled', 'unfulfillment', 'vulnerable', 'vulnerability', 'worthless', 'worthlessness', 'yearning', 'yearn', 'yearningly', 'alienation', 'alienated', 'alienating', 'betrayed', 'betrayal', 'condemned', 'condemnation', 'defeated', 'defeatism', 'defeatedly', 'deserted', 'desertion', 'desolate', 'desolately', 'desolation', 'disappointed', 'disappointingly', 'disappointment', 'embarrassed', 'embarrassment', 'excluded', 'exclusion', 'frustrated', 'frustration', 'gloomy', 'gloomily', 'gloominess', 'hollow', 'hollowness', 'humiliated', 'humiliation', 'inadequate', 'inadequacy', 'indifferent', 'indifference', 'insecure', 'insecurity', 'insignificant', 'insignificance', 'invalidated', 'invalidation', 'isolated', 'isolation', 'lonely', 'loneliness', 'lost', 'loss', 'meaningless', 'meaninglessness', 'neglected', 'neglect', 'numb', 'numbness', 'rejected', 'rejection', 'remorseful', 'remorsefulness', 'shameful', 'shamefully', 'shamefulness', 'trapped', 'entrapment', 'unwanted', 'unwantedness', 'useless', 'uselessness', 'victimized', 'victimization', 'weak', 'weakness', 'worthless', 'worthlessness', 'wounded', 'wound']
    stressful_count = sum(1 for token in tokens if token in stressful_words)
    depressive_count = sum(1 for token in tokens if token in depressive_words)

    # Therapist advice based on counts
    if positive_count > stressful_count > depressive_count:
        therapist_advice = "You are doing good. Enjoy your day!"
    elif stressful_count > positive_count:
        therapist_advice = "Do some Yoga and meditation."
    else:
        therapist_advice = "Please consider visiting a therapist."

    # Create a dictionary to hold the results
    results = {
        'text': text,
        'sentiment': sentiment,
        'positive_count': positive_count,
        'negative_count': negative_count,
        'positive_percentage': positive_percentage,
        'negative_percentage': negative_percentage,
        'stressful_count': stressful_count,
        'depressive_count': depressive_count,
        'therapist_advice': therapist_advice
    }

    # Establish a connection to the MySQL database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Sayeed$1504',
        database='login credentials',
        port=3306
    )
    if connection.is_connected():
        print('Connected to MySQL database')

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO analysis (username, reg_number, batch, feelingsInput, sentiment, positive_count, positive_percentage, negative_percentage, stressful_count, depressive_count, therapist_advice)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Data tuple for insertion
        data = (username, reg_number, batch, text, sentiment, positive_count, positive_percentage, negative_percentage, stressful_count, depressive_count, therapist_advice)

        try:
            # Execute the SQL query with data
            cursor.execute(insert_query, data)

            # Commit the changes to the database
            connection.commit()

            print(f'{cursor.rowcount} record inserted successfully.')

        except mysql.connector.Error as error:
            print('Error:', error)

        finally:
            # Close cursor and connection
            cursor.close()
            connection.close()
            print('MySQL connection closed')

    else:
        print('Connection to MySQL database failed')
        print(results)

    # Pass the sentiment analysis results, word counts, and therapist advice back to the project.html template
    return render_template('project.html', text=text, sentiment=sentiment,
                           positive_count=positive_count,
                           negative_count=negative_count,
                           positive_percentage=positive_percentage,
                           negative_percentage=negative_percentage,
                           stressful_count=stressful_count,
                           depressive_count=depressive_count,
                           therapist_advice=therapist_advice)
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)
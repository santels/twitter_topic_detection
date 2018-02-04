import time
import schedule
import numpy as np
from collections import Counter

import mcl
import cluster_scoring as cs
import stream_tweets as st
from calculate_similarity import Similarity
from manipulate_tweets import ManipulateTweet


STREAM_INTERVAL = 20
PROCESS_INTERVAL = 30

file_list = []


def run(trigger='both'):
    """
    Entry point of the program.
    """
    schedule.clear()
    # Run streamer only
    if trigger == 'stream':
        streamer = st.get_stream_instance()

        schedule.every(STREAM_INTERVAL).minutes.do(run_streaming,
                streamer["tsl"], streamer["auth"])
        while True:
            schedule.run_pending()

    # Run tweet processor only
    elif trigger == 'process':
        schedule.every(PROCESS_INTERVAL).minutes.do(run_tweet_processing)
        while True:
            schedule.run_pending()

    # Run both streamer and tweet processor
    else:
        streamer = st.get_stream_instance()
        schedule.every(STREAM_INTERVAL).minutes.do(run_streaming,
                streamer["tsl"], streamer["auth"])
        schedule.every(PROCESS_INTERVAL).minutes.do(run_tweet_processing)
        while True:
            schedule.run_pending()


def run_streaming(tsl, auth):
    """
    Runs streaming process.
    """
    PH_GEOLOCATION = (116.15, 4.23, 127.64, 21.24)
    timestr = time.strftime("%Y%m%d-%H%M")
    tsl.pathname = 'data/td-' + timestr + '.txt'
    # Tries to reconnect to stream after IncompleteRead/ProtocolError
    # exceptions are caught.
    print("Stream running...")
    start = time.time()
    while True:
        try:
            # Connect/reconnect the stream
            stream = Stream(auth, tsl)
            print("Getting samples...")
            stream.sample()
            if _get_time(start, STREAM_INTERVAL) == STREAM_INTERVAL:
                file_list.append(tsl.pathname)
                break
        except (IncompleteRead, ProtocolError):
            # Ignores exception and continues
            continue
        except KeyboardInterrupt:
            # Exits loop
            print("Stream ended.")
            stream.disconnect()
            break


def run_tweet_processing():
    """
    Runs modules in processing collected tweets.
    """
    print("Starting operation...")
    documents = [
'This lady was so nervous her blind and deaf rescue dog would get hurt, so she wrapped her in pajamas and totally babied her — then she realized she had a wild woman on her hands!',
"'Persistent' pit bull dog saves owners from carbon monoxide poisoning",
'Chinese pet owner who keeps two pooches KILLS a harmless stray dog by throwing a brick at it',
'''Have you lost a dog? This dog was found in Hellesdon yesterday morning.
The dog is currently at Bethel Street Police Station''',
'Be the person your dog thinks you are #Wednesdaywisdom',
'Africa’s most endangered carnivore, the Ethiopian wolf, is threatened by human encroachment.',
'Wild wolf return to Belgium for first time in more than 100 years ',
"We know how bad the flu has been for humans this season - but there have been cases of the canine flu, too. We'll let you know how you can protect your pet tonight on #WUtv Oh, and Riley's here!",
'So happy to have the lovely Lola back in with us today! #caninecamp  #dogdaycare #cutie #lola #beagle #happy #dogsofinstagram',
'A huge thank you to @CottesmoreGcc for raising an incredible £8,000 to transform the lives of people with disabilities. Their fundraising will sponsor a puppy through our Gift of Independence scheme https://caninepartners.org.uk/get-involved/give-gift-independence-sponsorship/ …',
'Does your pet help improve your #mentalhealth? Tweet us a picture! Read more: http://huff.to/2bPX6t6  @HuffPostUK',
'Advocates Push Government For Pet Food Stamps https://trib.al/342iGcM ',
'Pls send ur pet pics this way so my mental breakdown is a little bit better ',
'Cutest puppies ever',
'When you accidentally kick your pet',
'BREAKING: Office of Alumni Relations Director Cherry Tanodra has resigned. UST Alumni Association President Henry Tenedero and Vice President John Simon have been asked to resign following furor over government service award given to Mocha Uson - sources ',
'''UST-CSC's Official Statement on UST-AAI's decision to honor Mocha Uson with the Thomasian Award on Government Service

Take a stand, Thomasians! Let us hear your thoughts through http://tinyurl.com/PulsoNgTomasino 

#PulsoNgTomasino
#OneCSC''',
"‘Morality, uprightness’ not considered for Mocha Uson’s award, says UST alumni head ",
'"Mocha Uson should have been awarded with Best in Math for her expertise in dividing this nation."',
'''Sorry I can't accept the fact that

Rappler, who has the actual and accurate field data, will have to stop their operations,

while Mocha Uson Blog, who spreads fake information and unreliable data, will persist to deceive our fellow countrymen.''',
'Mayon is violent! This calls for a sacrifice to appease the gods. Guardias! Seize that UST awardee and throw her into the crater! Ahora Mismo!',
'Rep. Villarin returns own UST award ',
'''I was just trying to capture a time-lapse video of Mayon Volcano until it suddenly erupted at about 8:48 this morning! 😱
Let us all continue to pray for the safety of all albayanos and the people on nearby provinces. ''',
"The Philippines' most active volcano Mount Mayon erupts ",
'LOOK: Lava spewed out of Mayon Volcano again at 9:40 this evening. ',
'it bothers me so much that people think the mayon explosion is “beautiful” 😰😰 lives are at risk, karen!!!!!!',
"Time lapse: Boom explodes #Philippines' most active volcano",
"A volcano erupted near a popular Japanese ski resort, shooting flaming rocks into the sky. It killed one man and injured at least 10 http://cnn.it/2DzrysP ",
'Avalanche and volcano hit Japan ski resort ',
'Millions of flower petals erupt from a volcano, covering an entire village ',
'''LOOK: UN Office for Disaster Risk Reduction says the "Pacific Ring of Fire" was responsible for this day's strong earthquakes in Indonesia and Alaska and the volcanic eruptions here in the Philippines (Mayon volcano) and in Japan. ''',
'LOOK: Mayon Volcano spewing lava, ash. Photo taken at 6 p.m. from Legazpi City | @AC_Nicholls',
'An avalanche caused by an erupting volcano injured at least 15 in Japan. ',
'''Out of curiosity, I googled for Mayon and saw this old photo of the Cagsawa Church in Albay. 
Amazing how nature/history can be both beautiful and devastating at the same time. ''',
'My long suspicion about Drilon is confirmed. Another question: How did Drilon get no.1 in senatorial election which I cant believe.',
'I bet Drilon doesnt expect this to be exposed. He was happy when the LP govt jailed her w/o exposing this but the thing is, Napoles is starting to sing & strongly implicated Drilon😂This will surely makes Drilon wide awake at night😳 ',
'''here’s a fun mental gymnastics workout: 
ask your DDS friends, whats the difference between Jean Napoles and Isabelle Duterte?''',
"Palace: Let Napoles speak about 'pork barrel' scam ",
"President Duterte said he would never initiate a case build-up against Drilon since he considers the veteran lawmaker his 'friend.' #PHNews",
"You're a friend! @RRD_Davao tells @BigManDrilon he ain't behind Napoles' bombshell",
'I felt there were more senators involved in the scam but since only Enrile, Estrada and Revilla were oppositions on the Napoles list, they were the ones who went to jail -- courtesy of Delima of course,',
'''Haay mutual admiration. 

Let the axe fall where it may. 
Or should. 

If Napoles is not telling the truth, sue her in all courts in the land. Her accusations were broadcast nationwide, tama ba? 

After all, she does not have parliamentary immunity.''',
'Drilon denies getting P5-M donation from Napoles for 2010 elections ',
'''For years, I’ve used Twitter favs (now “likes”) for bookmarking.
 
Now that The Algorithm promotes tweets I like into followers’ feeds, I’m getting “why did you like this?” queries from ppl who disagree with the tweet.

Thanks, Twitter, for yet another step toward unusability.''',
'We used machine learning to develop an algorithm for geographically placing refugees to optimize their overall employment rate . Because of the algorithm’s data-driven learning capacity, policy-makers do not need to identify local economic conditions.',
'I am at the point in my career as a programmer where I take far more pleasure in a well written, informative, helpful error message than I do in code “elegance”.',
'''Did you hear about the JavaScript programmer who applied for a job???

The recruiter said they might get a callback, but no promises…''',
'No good programmer retires thinking “I wish I had implemented more design patterns.” Let’s solve real problems using simple pragmatic solutions.',
'Coding & digital literacy are fundamental skills that youth need to succeed in future jobs (it’s also really fun!). That’s why we’re equipping over 1M kids & teachers with digital skills training through #CanCode, so that they are able to compete in an evolving economy. #cdnpoli',
'Coding a lifeboat with @SpheroEdu - Some very engaging applications and learning opportunities @Bett_show',
'Seeking graphic designers with a side project that helped them get their heads around coding. Appreciate this is a niche request, hence RTs appreciated :)',
'Effective #PrivacyEngineering requires support at all layers of #technology from the basic tools, libraries, design and coding, also for user interfaces @AchimKla #CPDP2018',
'Controllers in Houston address software glitch on Canadarm2 as spacewalkers continue robotics maintenance. https://www.nasa.gov/live ',
"My team try to verify the commands they send to me with a system that is similar: this is my Ground Reference Model (GRM). It doesn't look much like me, but from an electrical and software perspective, it is very similar. #ExoMars",
'Even  though I have learned a lot about software design through pair programming, it has done me a lot of good to have no one to pair with at work for last few months and figure out knotty problems myself.',
'In what I’ve seen so far, there is no meaningful distinction between “artificial intelligence” and “reasonably sophisticated software” or “powerful tools”. It’s cool, but ALL intelligence stubbornly resides in the humans, so far as I can see.',
'''microsoft edge, more like microsoft edge of my asshole

fuck this clunky software, shit locks up more than a texas prison I GAVE IT A CHANCE''',
"Ed Sheeran's fiancée rescued him during his darkest moment",
"So how much do you know about @EdSheeran's bride-to-be Cherry Seaborn? 👰🤵  ",
'Everything Ed Sheeran has said about fiancee Cherry Seaborn',
'''When Ed Sheeran sings "I don't deserve this, she looks perfect" I cry a lil bit inside cause the idea of someone actually realizing their partner's worth and shit is so beautiful to me like wow that shit makes me soft ''',
"Never ignore a person who loves and cares for you, because one day you may realize that you've lost the moon while counting the stars.",
"Miley Cyrus: AND THE SEVENTH THING...I HATE THE MOST THAT YOU DOOOOOOO..... you make me love you. ",
"Forgiveness is the realest form of Love. Can you for-give, with no attachment to the same love being returned?",
"We smell a real-life romance between #ElmoMagalona and #JanellaSalvador!",
"watching #CallMeByYourName for the first time. umm woah. literally all i want to do right now is a queer romance drama. like cast me in one. please.",
"Our generation has lost the value of romance, the value of trust, the value of conversation, sadly small talk is the new deep",
'I saw my crush today. I am so happy. Mehehe',
'me waiting for someone to actually care about me and not just be infatuated by the idea of me ',
'I wanna be someone’s favorite, I want someone who’s absolutely infatuated with me.',
'If he truly loves you he will wrestle you out of any notion that he’s not completely infatuated with you.',
"No one ever landed on the Moon, tht's not even possible. #MoonLandingHoax #FlatEarth",
"Flat Earth is a conspiracy to honeypot all the men on the internet who can’t stop themselves from explaining things and keep them there forever",
'''If Larry had finished that the Staples Center would have lifted off the and gone into orbit. 

Where it would then prove Kyrie wrong about the flat Earth thing.''',
'''I'm in astronomy right now and my professor keeps talking like the ear is round.... 
I should be teaching this class. I know the truth #FlatEarth #flatearthers''',
'''I haven't seen a good conspiracy video in a long time.
Shit has been dry since flat earth came around...
Anyone got any good vids? pic.twitter.com/D5E57SBKHf''',
'Just ONE HOUR of social media a day is enough to ruin your sleeping pattern',
'I quit social media for 1 month — it was the best choice I ever made ',
'''my college life quote: "yesterday's procastination is today's ohshitshitshit"''',
'''How to avoid procastination?, Try this diagram!!!
https://alexvermeer.com/getmotivated/ ''',
'70% of my body right now is consist of procastination and pure boredom. I am just completely clueless of what 30% of my body is consist of.',
'''Doing it for everyone that said i couldn't 

No procastination 2018''',
"me laying on my bed scrolling thru twitter instead of completing all of my 73728473 school assignments i love #procastination !! ",
'The quality of political journalism would improve tenfold if we all just agreed to ban the words “win” and “lose” (and variations of both) when reporting on policy developments',
'''"It turns out great stories get traffic!" is trivially true, but mostly a bit of uplifting nonsense that obscures the reality of journalism in an age of algorithmic discourse. Viral stories get traffic, and sometimes – but not often – great journalism is also viral.''',
'CNN covers up an assault of a journalist ',
'knew there was a way to describe the personal and skilful work that i do turns out it’s “singing jack antonoff songs”',
'T 2591 - The many expressions for the ACAPELLA number I sang last night and shot today .. acapella, where the entire song is done by one voice - singing orchestra sounds .. all .. see it soon !!! ',
'when you watch a video you filmed at a concert and you hear yourself singing pic.twitter.com/i5988XIkic',
'seeing Infinite singing Begin Again and woohyun asking inspirits to sing it with them again made me tear up',
'The voice of an 👼 watch back when Patrick was in the studio recording vocal takes for Church #blessed #nerdstuff #FOBMANIA',
"Eight-year-old Gabe is here with his family. Says he’s here because some people are being mean to girls #Halifax #womensmarchhfx #WomansMarch2018 ",
"#WomensMarch2018 leader #LindaSarsour supports oppression of women through #KoranicLaw including female genital mutilation, spousal rape, and the execution of all #LBGTQ people. Way to go, #feminists! You sided with a cult that believes you are second class. 🙄 #WomansMarch2018 ",
'''Since I’m not able to join the march today due to work, here’s to all my sisters! 💕 
“I am not free while any woman is unfree, even when her shackles are different from my own.” -Audre Lorde #WomansMarch2018 #TogetherWeRise''',
'Feminism is so destructive it can turn Scarlett Johansson into Macklemore.',
'''People who claim that feminism is not needed anymore, read this. The 'highest' levels of our society are dripping with sexism. 
What a disgrace.''',
"Hollywood:You lecture us about our carbon footprints while flying on private jets. You preach feminism while brutalizing women. You castigate violence while making millions off it in your movies. You condemn guns, with armed bodyguards at your side. You are the problem, not us. ",
'''Young feminists, though you might very disagree with what and older woman says, please recognise its because of their views - not their age. 

Putting a woman down because of her maturity or looks is literally the opposite of feminism.'''
]
    documents2 = ["The sky is blue. #Outdoors",
                  "The dog is barking.",  # "The sun is bright.",
                  "The sun in the sky is bright.",
                  "Was that an earthquake???? Motherfucker!!!",
                  "We can see the shining sun, the bright sun. #Outdoors",
                  "The cat is meowing back at the dog.",
                  "The dog and cat fought each other.",
                  "I think that was magnitude 5.4?!?! I thought I died! Damn, nigga, wtf. Where was the epicenter??",
                  "That trembles the ground so much, man!!!! Aftershock would kill mah guts.",
                  "Martin played with his new PS4.",
                  "Lucas really liked gaming with his PS4.",
                  "Quit playing games with mah heart, mofo!",
                  ]

    if len(file_list) > 0:
        tweets_data_path = file_list[-1]
    else:
        tweets_data_path = 'data/tweets_data_3.txt' # default for now

    start = time.time()
    manip_tweet = ManipulateTweet()

    documents = [manip_tweet._clean_tweet(d) for d in documents]
    #tweets_data = manip_tweet.load_tweets_data(tweets_data_path)
    #tweets = manip_tweet.preprocess_tweet(tweets_data)

    print("Tokenizing...")
    #tokens = manip_tweet.tokenize_tweets(tweets[900:950])
    tokens = manip_tweet.tokenize_tweets(documents)
    print("Tokenization completed!")
    print("No. of tokenized tweets:", len(tokens))
    tk_time = _elapsed_time(start)

    # Similarity function
    print("Getting similarity between tweets...")
    sim = Similarity(tokens)
    print("No. of Features:", len(sim.get_features()))
    #score_matrix = sim.cos_similarity() # Cosine similarity
    score_matrix = sim.similarity()    # Soft cosine similarity
    print("Similarity function operation completed!")
    sm_time = _elapsed_time(tk_time)

    # Clustering
    print("Clustering...")
    matrix = mcl.cluster(score_matrix, iter_count=1000)
    clusters, matrix = mcl.get_clusters(matrix)
    #mcl.draw(matrix, clusters)
    print("Clustering finished!")
    cl_time = _elapsed_time(sm_time)

    # Cluster scoring
    print("Scoring...")
    scores = list(cs.score(sim.similarity, matrix, clusters))
    max_score = max(scores)
    max_score_index = list(cs.get_max_score_index(scores))
    print("Scoring finished!")
    _elapsed_time(cl_time)

    tweet_list = list(tokens.keys())
    tweet_token_list = list(tokens.values())
    for index in max_score_index:
        print(">>> Max Score: {}\nTweets:".format(max_score))
        for tweet_index in clusters[index]:
            print("{}. {}".format(tweet_index, tweet_token_list[tweet_index]))


    # Gets clusters' indices by their scores
    score_index = cs.get_score_index(scores, len(scores))

    # Top terms by clusters
    top_topics = _get_top_topics_by_clusters(scores, clusters, tweet_token_list,
            score_index)
    print("\nTop Topics:")
    for index, top in enumerate(top_topics):
        print("{}. {}".format(index + 1, top))


    #print("Features:\n", sim._features)
    #print("Matrix:\n", score_matrix)
    #print("MCL Result:\n", matrix)
    #print("Clusters:", clusters)
    print("No. of Clusters:", len(clusters))

    # Saves result to a file
    # _save_output(scores, clusters, tweet_list, top_topics, score_index, 'soft')


def _elapsed_time(start):
    ft = time.time()
    m, s = divmod(ft-start, 60)
    h, m = divmod(m, 60)
    print("Time elapsed: {0:.0f}h {1:.0f}m {2:.2f}s".format(h, m, s))
    return ft



def _get_time(start, interval):
    return round(interval - ((time.time() - start) % interval))


def _get_top_topics_by_clusters(scores, clusters, tweet_list, score_index, top=5):
    """
    Gets all top topics in each clusters.
    TODO: Implement similarity function (not just Counter).
    """
    top_topics = []
    for i, _ in score_index:
        terms = []
        for tweet_index in clusters[i]:
            terms.extend(tweet_list[tweet_index])
        ctr = Counter(terms)

        top_topics.append(ctr.most_common(top))

    return top_topics


def _save_output(scores, clusters, tweets, topics, score_index, c_type):
    """
    Saves result in a file.
    """
    timestr = time.strftime("%Y%m%d-%H%M")
    file_ext = 'txt'
    filename = 'out_{}_tweets_{}_clusters_{}_{}.{}'.format(
            len(tweets), len(clusters), timestr, c_type, file_ext)

    tweet_count_per_cluster = 0
    with open('data/out/' + filename, 'w') as out:
        for i, (cl_idx, _) in enumerate(score_index):
            out.write('Cluster {} | {} Tweets | Top topics (order by frequency | descending) {}'
                    .format(cl_idx+1, len(clusters[cl_idx]), '[' + ', '.join(
                        [str(t) for t in topics[i]]) + ']'))
            out.write('\n')
            tweet_count_per_cluster += len(clusters[cl_idx])
            for j, tweet_index in enumerate(clusters[cl_idx]):
                out.write('{}. {}'.format(j+1, tweets[tweet_index]))
                out.write('\n')
            out.write('\n')
    print(tweet_count_per_cluster)


if __name__ == '__main__':
   # import sys

   # if len(sys.argv) > 1:
   #     if sys.argv[1] in ('--stream-only', '-so'):
   #         run('stream')
   #     elif sys.argv[1] in ('--process-only', '-po'):
   #         run('process')
   #     else:
   #         run()
   # else:
   #     run()
    run_tweet_processing()

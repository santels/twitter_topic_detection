# twitter_topic_detection
## Semantic-based Twitter Topic Detection Using Markov Clustering Algorithm

_By: Santelices, Andrew P. | Talan, Wesly Kate N._

## Requirements:
* Python 3.x
* See [requirements.txt](https://github.com/santels/blob/master/requirements.txt)
    * Optional Python dependencies (for showing graph):
        * `networkx==2.0`
        * `matplotlib==2.0`

## Installation Guide:
1. [Create a new virtual environment](https://docs.python.org/3/library/venv.html).
2. Activate virtual environment and install required packages:
    ```bash
    pip install -r requirements.txt
    ```
   __Note__: In case you're having problem in installing some packages, it might be because of some dependencies in some required Python packages. A workaround would be installing the following:
    ```bash
    apt-get install python3-dev
    apt-get install libevent-dev
    ```
3. Install NLTK's Wordnet package.
    ```bash
    python3 -m nltk.downloader wordnet
    ```

## To Run:
1. (since there are no UI yet implemented) Just run:
    ```bash
    # in 'src' folder
    python3 main.py
    ```

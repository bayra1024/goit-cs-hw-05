import requests
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
import matplotlib.pyplot as plt


def fetch_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")


def map_word_frequency(document):
    words = document.lower().split()
    return Counter(words)


def reduce_word_frequency(counters):
    total_counts = Counter()
    for word_counts in counters:
        total_counts.update(word_counts)
    return total_counts


def visualize_top_words(word_counts, top_n=15):
    top_words = word_counts.most_common(top_n)
    print(top_words)
    words, counts = zip(*top_words)

    plt.figure(figsize=(10, 8))
    plt.bar(words, counts)
    plt.xlabel("Слова")
    plt.ylabel("Частота використання")
    plt.xticks(rotation=45)
    plt.title("Топ-слова з найвищою частотою використання")
    plt.show()


if __name__ == "__main__":
    url = "https://www.gutenberg.org/files/11/11-0.txt"  # Alice in Wonderland by Lewis Carroll
    text = fetch_content(url)

    if text:
        parts = [text[i : i + 1000] for i in range(0, len(text), 1000)]

        with ThreadPoolExecutor() as executor:
            counters = list(executor.map(map_word_frequency, parts))

        total_counts = reduce_word_frequency(counters)

        visualize_top_words(total_counts)

import re
from difflib import SequenceMatcher
from collections import defaultdict


# 1. Normalization
PUNCT = re.compile(r"[^\w\s]+", flags=re.UNICODE)
WS = re.compile(r"\s+", flags=re.UNICODE)

def normalize_text(text: str) -> str:
    if len(text) == 0:
        return ""
    text = str(text).lower()
    text = PUNCT.sub(" ", text)
    text = WS.sub(" ", text).strip()
    return text


# 2. title_repeat (2/3 match)
def compute_title_rep(tweet_text: str, paper_title: str, threshold_ratio: float = 2/3) -> int:
    title = normalize_text(paper_title)
    tw = normalize_text(tweet_text)

    m = SequenceMatcher(None, title, tw)
    match_len = m.find_longest_match(0, len(title), 0, len(tw)).size
    is_signal = 0
    if match_len >= threshold_ratio * len(title):
        is_signal = 1

    return is_signal

# 3. rep_cnt
def rep_cnt_cal(tweet_ids, tweet_id2text):
    norm_texts = {twid: normalize_text(tweet_id2text.get(twid, "")) for twid in tweet_ids}
    freq = defaultdict(int)
    for t, nt in norm_texts.items():
        freq[nt] += 1
    rep_cnt = {twid: max(freq[norm_texts[twid]] - 1, 0) for twid in tweet_ids}
    return rep_cnt


# 4. analyse
def compute_repetition_for_doi_dicts(
    doi_title: dict,
    doi_tweet: dict,
    tweet_id2text: dict,
    title_threshold_ratio: float = 2/3,
):
    results = {}

    for doi, title in doi_title.items():
        tweet_ids = doi_tweet.get(doi, [])
        # rep_cnt
        rep_cnt_map = rep_cnt_cal(tweet_ids, tweet_id2text)

        # title_repeat
        title_rep_map = {}
        for twid in tweet_ids:
            tw_text = tweet_id2text.get(twid, "")
            title_rep_map[twid] = compute_title_rep(tw_text, title, threshold_ratio=title_threshold_ratio)

        rep_cnt_vals = list(rep_cnt_map.values()) if tweet_ids else [0]
        title_rep_vals = list(title_rep_map.values()) if tweet_ids else [0]


        results[doi] = {
            "paper_title": title,
            "tweet_ids": tweet_ids,
            "rep_cnt_by_tweet": rep_cnt_map,
            "title_rep_by_tweet": title_rep_map,
        }

    return results


# Example
if __name__ == "__main__":
    doi_title = {
        '10.22331/q-2022-05-24-721': 'Numerical Implementation of Just-In-Time Decoding in Novel Lattice Slices Through the Three-Dimensional Surface Code',
        '10.1080/07315724.2020.1789518': 'Can Vitamin D and L-Cysteine Co-Supplementation Reduce 25(OH)-Vitamin D Deficiency and the Mortality Associated with COVID-19 in African Americans?'
    }

    doi_tweet = {
        '10.22331/q-2022-05-24-721': ['1537737672021659648', '1536648404054462464','1536648404054462331'],
        '10.1080/07315724.2020.1789518': ['1362361300643418112', '1368259167287443465', '1360566899713703938']
    }

    tweet_id2text = {
        '1362361300643418112': 'Full article: Can Vitamin D and L-Cysteine Co-Supplementation Reduce 25(OH)-Vitamin D Deficiency and the Mortality Associated with COVID-19 in African Americans? https://t.co/tt4OGE4PeI',
        '1368259167287443465': 'Full article: Can Vitamin D and L-Cysteine Co-Supplementation Reduce 25(OH)-Vitamin D Deficiency and the Mortality Associated with COVID-19 in African Americans? https://t.co/tt4OGE4PeI',
        '1360566899713703938': 'Full article: Can Vitamin D and L-Cysteine Co-Supplementation Reduce 25(OH)-Vitamin D Deficiency and the Mortality Associated with COVID-19 in African Americans? https://t.co/tt4OGE4PeI',
        '1537737672021659648': 'Open Access UCL Research: Numerical Implementation of Just-In-Time Decoding in Novel Lattice Slices Through the Three-Dimensional Surface Code - UCL Discovery https://t.co/6eTF5mwYmg',
        '1536648404054462464': 'New in Quantum: Numerical Implementation of Just-In-Time Decoding in Novel Lattice Slices Through the Three-Dimensional Surface Code by T. R. Scruby, D. E. Browne, P. Webster, and M. Vasmer https://t.co/zNoUNORqgX https://t.co/ksu9v8atlC',
        '1536648404054462331': 'New paper update: Numerical Implementation of Just-In-Time Decoding in Novel Lattice Slices Through the…'
    }

    res = compute_repetition_for_doi_dicts(
        doi_title=doi_title,
        doi_tweet=doi_tweet,
        tweet_id2text=tweet_id2text,
    )

    # Pretty print
    for doi, info in res.items():
        print(doi)
        for tw in info["tweet_ids"]:
            print(f"tweet_id={tw}\trep_cnt={info['rep_cnt_by_tweet'][tw]}\ttitle_rep={info['title_rep_by_tweet'][tw]}")
        print('-'*80)
import json

from transformers import pipeline
from typing import List

# for sentiment analysis
model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
sentiment_task = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path)


# for emotion
model_id = "SamLowe/roberta-base-go_emotions"
classifier = pipeline("text-classification", model=model_id)


def convert_dict_in_percentage(result: dict):
    total = sum(result.values())
    for key in result:
        result[key] = round((result[key] / total) * 100, 2)
    return result


# a function to dump json in a local file


def dump_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


# make csv file zipping two list


def make_csv_file(list1, list2, list3, filename):
    with open(filename, "w") as f:
        for i in range(len(list1)):
            f.write(f"{list1[i]},{list2[i]},{list3[i]}\n")


def count_comment_type(comments: List[str]):
    print(comments, len(comments))
    total = len(comments)
    classifier_result = classifier(comments)
    list1 = comments
    list2 = [a.get("label", "err") for a in classifier_result]
    result_classifier = {}
    for item in classifier_result:
        if item["label"] in result_classifier:
            result_classifier[item["label"]] += 1
        else:
            result_classifier[item["label"]] = 1
    result_classifier = convert_dict_in_percentage(result_classifier)
    sentiment_result = sentiment_task(comments)
    list3 = [a.get("label", "err") for a in sentiment_result]
    result_sentiment = {}
    for item in sentiment_result:
        if item["label"] in result_sentiment:
            result_sentiment[item["label"]] += 1
        else:
            result_sentiment[item["label"]] = 1
    result_sentiment = convert_dict_in_percentage(result_sentiment)
    return {
        "classifier": result_classifier,
        "sentiment": result_sentiment,
        "comment_count": total,
    }

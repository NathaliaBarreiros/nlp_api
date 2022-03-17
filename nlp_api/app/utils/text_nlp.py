import asyncio
import numpy as np
from transformers import AutoTokenizer, AutoConfig, AutoModelForSequenceClassification
from scipy.special import softmax

model_path = "daveni/twitter-xlm-roberta-emotion-es"
tokenizer = AutoTokenizer.from_pretrained(model_path)
config = AutoConfig.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)


def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = "@user" if t.startswith("@") and len(t) > 1 else t
        t = "http" if t.startswith("http") else t
        new_text.append(t)
    return " ".join(new_text)


async def analyze_text(text) -> list[str, dict[str, float]]:
    loop = asyncio.get_event_loop()
    text = await loop.run_in_executor(None, preprocess, text)
    encoded_input = tokenizer(text, return_tensors="pt")
    # output = await loop.run_in_executor(None, model, **encoded_input)
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    # Print labels and scores
    ranking = np.argsort(scores)
    ranking = ranking[::-1]
    labels = []
    probs = []
    my_dict = {}
    for i in range(scores.shape[0]):
        l = config.id2label[ranking[i]]
        s = scores[ranking[i]]
        labels.append(l)
        probs.append(np.round(float(s), 4))
    my_dict = {labels[i]: probs[i] for i in range(len(labels))}

    return [text, my_dict]

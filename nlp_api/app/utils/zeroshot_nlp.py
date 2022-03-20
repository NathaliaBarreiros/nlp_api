import asyncio
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_name = "Recognai/zeroshot_selectra_medium"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

classificator = pipeline("zero-shot-classification", model=model, tokenizer=tokenizer)


async def analyze_text(text, labels) -> list[str, list[str], dict[str, float]]:
    loop = asyncio.get_event_loop()
    candidate_labels = labels
    result = await loop.run_in_executor(None, classificator, text, candidate_labels)

    text = result["sequence"]
    labels = result["labels"]
    scores = result["scores"]

    res = {labels[i]: scores[i] for i in range(len(labels))}
    return [text, candidate_labels, res]

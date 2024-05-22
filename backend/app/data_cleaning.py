from sentence_transformers import util

def extract_relevant_paragraphs(paragraphs, question, model):
    question_embedding = model.encode(question, convert_to_tensor=True)
    relevant_paragraphs = []

    for para in paragraphs:
        para_embedding = model.encode(para, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(question_embedding, para_embedding)
        if similarity.item() > 0.2:  # Threshold for relevance, can be adjusted
            relevant_paragraphs.append(para)
    print(f"Relevant Paragraphs: {relevant_paragraphs}")
    return relevant_paragraphs

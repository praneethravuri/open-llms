from sentence_transformers import util
import logging

logger = logging.getLogger(__name__)

def extract_relevant_paragraphs(paragraphs, question, model):
    question_embedding = model.encode(question, convert_to_tensor=True)
    relevant_paragraphs = []

    for para in paragraphs:
        para_embedding = model.encode(para, convert_to_tensor=True)
        similarity = util.dot_score(question_embedding, para_embedding)
        if similarity.item() > 0.45:
            relevant_paragraphs.append(para)
    logger.info("Extracted %d relevant paragraphs for question: %s", len(relevant_paragraphs), question)
    return relevant_paragraphs

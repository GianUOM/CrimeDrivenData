import spacy
import csv

nlp = spacy.load("en_core_web_sm")

def ner(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def process_csv(filepath, output_file):
    with open(filepath, 'r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        with open(output_file, 'w', encoding='utf-8') as output: 
            for row in csv_reader:
                body_entities = ner(row['Body'])
                title_entities = ner(row['Title'])
                output.write(f"Entities in 'Body': {body_entities}\n")
                output.write(f"Entities in 'Title': {title_entities}\n\n")

if __name__ == "__main__":
    csv_file = "data.csv"
    output_file = "output.txt"
    process_csv(csv_file, output_file)

    csv_file = "data2.csv"
    output_file = "outputmd.txt"
    process_csv(csv_file, output_file)

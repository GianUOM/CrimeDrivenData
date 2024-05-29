import csv
import re
import spacy

nlp = spacy.load("en_core_web_sm")
# Function to extract entities related to crime, location, and date
def extract_entities(text):
    entities = {
        "Crime": [],
        "Location": [],
        "Date": [],
        "Names": []
    }
    
    doc = nlp(text)
    
    crime_keywords = {
        "Cyber Crimes": [
            "Malware", "Cybercrim", "Hack", "Cyberbully", "Phish", "Ransomware",
            "Data breach", "Pharming", "Cyberstalk"
        ],
        "Violent Crimes": [
            "Murder", "Stab", "Shoot", "Shot", "Assault", "Batter", "Kill", "Kidnap", "Domestic violence", "Homicide", "Bomb", "Terrorism",
            "Assassinat", "Gang violence", "Human traffick", "Acid", "Attack", "Knife", "Gun", "Threat", "Fight", "Beat"
        ],
        "Drug-related Crimes": [
            "Drug", "Cocaine", "Heroin", "Cannabis", "Narcotic", "Meth", "Opium", "Marijuana", "Synthetic drugs"
        ],
        "Property Crimes": [
            "Theft", "Robbery", "Burglar", "Vandal", "Arson", "Shoplift", "Home invasion",
            "Pickpocket", "Grand theft auto", "Breaking and entering", "Steal", "Stole"
        ],
        "White-collar Crimes": [
            "Money-launder", "Fraud", "Anti-money launder", "Scams", "Conning", "Defraud", "Embezzle",
            "Insider trad", "Ponzi scheme", "Pyramid scheme", "Tax evasion",
            "Insider trad", "Forge", "Counterfeit", "Bribe", "Money launder"
        ],
        "Organized Crimes": [
            "Mafia", "Gang", "Cartel", "Organized crime", "Smuggl", "Extort", "Racketeer",
            "Arms traffick", "Weapons traffick", "Prostitution ring", "Illegal gambl"
        ],
        "Sexual Crimes": [
            "Rape", "Sexual assault", "Sexually assault", "Sexual harass", "Sexually harass", "Sexual abus", "Sexually abus", "Abuse", "Abusing"
            "Indecent exposure", "Sexual exploitation", "Voyeurism", "Child pornography"
        ]
    }
    
    locations = [
        "Attard", "Balzan", "Birkirkara", "Birżebbuġa", "Burmarrad", "Cospicua", "Dingli", "Fgura", 
        "Floriana", "Fontana", "Għajnsielem", "Għarb", "Għargħur", "Għasri", "Għaxaq", 
        "Gudja", "Gżira", "Ħamrun", "Iklin", "Kalkara", "Kerċem", "Kirkop", "Lija", 
        "Luqa", "Marsa", "Marsaskala", "Marsaxlokk", "Mdina", "Mellieħa", "Mġarr", 
        "Mosta", "Mqabba", "Msida", "Imtarfa", "Munxar", "Nadur", "Naxxar", "Paola", 
        "Pembroke", "Pietà", "Qala", "Qormi", "Qrendi", "Rabat", "Safi", "St. Julian's", 
        "San Ġwann", "San Lawrenz", "Senglea", "St. Paul's Bay", "Sannat", "Santa Luċija", 
        "Santa Venera", "Siġġiewi", "Sliema", "Swieqi", "Tarxien", "Ta' Xbiex", "Valletta", 
        "Birgu", "Xagħra", "Xewkija", "Xagħjra", "Żabbar", "Żebbug", "Żejtun", "Żurrieq",
        "Bidnija", "Mrieħel", "Bormla", "Furjana", "Raħal Ġdid", "Isla", "San Ġwann", 
        "Santa Luċija", "San Ġiljan", "San Pawl", "Xbiex", "Xgħajra", "Kerċem", "Xlendi", 
        "Marsalforn", "Paceville", "Marsascala", "Gozo", "Għajn Żnuber", "St Julian’s",
        "St Paul's Bay", "Pieta", "Qawra", "San Luċjan", "Victoria", "Ħandaq", "Swatar"
    ]
    
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            if ent.text.count(' ') >= 1:
                entities["Names"].append(ent.text)
        elif ent.label_ == "DATE":
            entities["Date"].append(ent.text)
            
        if ent.label_ == "GPE":
            anglicized_ent_text = anglicize(ent.text)
            for location in locations:
                if anglicize(location).lower() in anglicized_ent_text.lower():
                    entities["Location"].append(location)
                    break

    
    
    # Crime extraction
    for crime_type in crime_keywords.keys():
        for crime in crime_keywords[crime_type]:
            if re.search(r'\b' + re.escape(crime), text, re.IGNORECASE):
                entities["Crime"].append(crime_type)
            
    return entities

def anglicize(text):
    replacements = {
        'Ċ': 'C', 'ċ': 'c',
        'Ġ': 'G', 'ġ': 'g',
        'Ħ': 'H', 'ħ': 'h',
        'Ż': 'Z', 'ż': 'z'
    }
    for maltese_char, anglicized_char in replacements.items():
        text = text.replace(maltese_char, anglicized_char)
    return text

# Function to process articles and extract entities related to crimes, locations, dates and names
def process_articles(csv_file, output_file):
    with open(csv_file, "r", encoding="utf-8") as file, open(output_file, "w", encoding="utf-8") as output:
        reader = csv.DictReader(file)
        for row in reader:
            title = row["Title"]
            body = row["Body"]
            entities = extract_entities(title + " " + body)
            output.write("Title: {}\n".format(title))
            #output.write("Body: {}\n".format(body))
            output.write("Entities: {}\n".format(entities))
            output.write("\n")

csv_file = "data_collection/times_of_malta/data.csv"
output_file = "output.txt"

def main():    
    process_articles(csv_file, output_file)
    
if __name__ == "__main__":
    main()
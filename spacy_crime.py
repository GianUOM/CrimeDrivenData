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
    
    names = [
    "Qormi", "Mater Dei", "Bitcoin", "Marsaxlokk", "Wuppertaler Rundschau",
    "MacBook Pro", "Bild", "Witnesses", "Triq Lampuka", "Episode", "Mizan Online",
    "Mosta", "St Francis Square", "Messenger", "Gew Kobba", "Guilty", "St Paul’s Bay",
    "Gudja", "Facebook Messenger", "Papaya", "Stratton", "Moretti", "Children",
    "Twitter", "Related Stories", "St Julian's", "Valletta", "Sta Venera", "Triq Bajjada",
    "Marsa", "Ġħajn Żnuber", "Reliable", "Rabat", "Domestic Abuse", "Voluntary",
    "Triq Garibaldi", "Birkirkara", "Mrieħel", "Ħamrun", "Triq", "Żejtun", "Recruiter",
    "Teen", "Mġarr", "St Mary’s College", "Għar Lapsi", "Mediatrix Place", "Gżira",
    "Mediapart", "Mqabba", "Lengthy", "Aġenzija Appoġġ", "Apart", "Marijuana",
    "Recruitgiant", "Victim", "Van Driver", "Smart", "Justifiable Homicide",
    "Journal", "Uber", "Dumbstruck", "Supportline", "St Paul's", "Proud", "Barman",
    "Aġenzija Sapport", "Related Stories", "Daughter Hostage", "Marsascala", "Gianpula",
    "Warning", "Tarxien", "Binance", "Paceville", "Banks", "WhatsApp", "Swieqi",
    "Lazio", "Lecce", "Torvaianica", "Scampia", "Balocco", "Dior", "Lobby", "Graffiti",
    "St Paul the Hermit", "Graffiti Tags", "Wied", "TBS Crew", "St Paul's Bay",
    "Revolutionary Guards", "Blade Runner", "A St Paul's Bay", "Tiktoker", "Efforts",
    "St Julians", "Godfather", "Triq Il-Mater Boni Consilii", "Lovin Malta",
    "St Julian’s", "Krispy Kreme", "Covid", "Youths", "A St Paul’s Bay",
    "Triq Sant' Antnin", "St Francis Street", "St Luke’s Hospital", "Failures",
    "Newsbook", "Għajn Żnuber", "RELATED STORIES  "
]

    crimes = [
        "Money-laundering", "Sanctions", "Fraud", "Anti-money laundering", "Malware", "FBI",
        "Cybercriminals", "Constitutional case", "Fraud charges", "Drugs", "Scams", "Attacked",
        "Knife", "Stabbing", "Murder", "Attempted murder", "Sex crimes", "Rape", "Shooting",
        "Assault", "Plea bargain", "Gunshot", "Gang attack", "Robing", "Cocaine", "Heroin",
        "Cannabis", "Possession", "Apartheid", "Mafia", "Ganged up", "Thief", "Armed thief",
        "Breach", "Killing", "Hate speech", "Thieves", "Stealing", "Theft", "Organised crime",
        "Operation", "Scam", "Corruption", "Burn", "Conspiring", "Sexually harassed",
        "Money laundering", "Trafficker", "Abusing", "Sexually abusing", "Thefts",
        "Snatch-and-grab", "Stabbed", "Raped", "Killed", "Child sex crimes", "Threatning",
        "Attack", "Suicide", "Suicide bombing", "arsonist", "Arsonist" "Hitting", "With a car", "Attacks",
        "Vandalised", "Alleged inaction", "Fined", "Unfair commercial practices",
        "Drug trafficking", "Nabbed", "Drugs dealing", "Nabbed", "Conning", "Sexual assault",
        "Punched", "Punching", "Indecently touching", "Touching", "Beat", "Hit", "Hostage",
        "Hostage-taker", "Kill", "Murders", "Fight", "Destroy", "Beating", "Strikes",
        "War crimes", "War crime", "Film", "Filmed", "Filming", "Sex", "Sex video",
        "Mental health", "Dine-and-dash", "Steals", "Dine and dash", "Sexually moslesting",
        "Illegaly", "Groped", "Groping", "Grope", "Escape", "Attempted escape",
        "Domestic violence", "Homicide", "Involuntary homicide", "Illegal recruiment agency",
        "Allegations", "Defrauded", "Cyberbullying", "Art trafficking", "Abuse",
        "Document forgery", "Trafficking", "Staging", "Death", "Starvation", "Burning",
        "Burned", "Setting", "Fire", "Robbed", "Gangs", "Acid", "Shoot"
    ]

    locations = [
        "Attard", "Balzan", "Il-Bidnija", "Birgu", "Birkirkara", "Mrieħel", "Birżebbuġa", 
        "Bormla", "Dingli", "Fgura", "Furjana", "Għargħur", "Għaxaq", "Gudja", "Gżira", 
        "Ħamrun", "Iklin", "Kalkara", "Kirkop", "Lija", "Luqa", "Marsa", "Marsaskala", 
        "Marsaxlokk", "Mdina", "Mġarr", "Mosta", "Mqabba", "Msida", "Mtarfa", "Naxxar", 
        "Raħal Gdid", "Pembroke", "Pietà", "Qormi", "Qrendi", "Rabat", "Safi", "San Ġwann", 
        "Santa Luċija", "Santa Venera", "Isla", "Siġġiewi", "Sliema", "San Ġiljan", 
        "San Pawl", "Swieqi", "Tarxien", "Xbiex", "Valletta", "Xgħajra", "Żabbar", 
        "Żebbug", "Żejtun", "Żurrieq", "Fontana", "Għajnsielem", "Għarb", "Għasri", 
        "Kerċem", "Munxar", "Xlendi", "Nadur", "Qala", "Rabat", "San Lawrenz", "Sannat", 
        "Xagħra", "Xewkija", "Marsalforn", "St Paul’s Bay", "St Paul's Bay", "Paceville", 
        "Marsascala", "Gozo", "Paola", "Mellieha", "Senglea", "Cospicua", "St Julian's", "Birzebbuga", 
        "Għajn Żnuber", "Zabbar", "St Julian’s"
    ]
    
    for ent in doc.ents:
        if ent.label_ == "DATE":
            entities["Date"].append(ent.text)
        elif ent.label_ == "PERSON" and ent.text.lower() not in [word.lower() for word in names]:
            entities["Names"].append(ent.text)
    
    # Crime extraction
    for crime in crimes:
        if re.search(r'\b' + re.escape(crime) + r'\b', text, re.IGNORECASE):
            entities["Crime"].append(crime)
    
    # Location extraction
    for location in locations:
        if re.search(r'\b' + re.escape(location) + r'\b', text, re.IGNORECASE):
            entities["Location"].append(location)

    return entities

# Function to process articles and extract entities related to crimes, locations, dates and names
def process_articles(csv_file, output_file):
    with open(csv_file, "r", encoding="utf-8") as file, open(output_file, "w", encoding="utf-8") as output:
        reader = csv.DictReader(file)
        for row in reader:
            title = row["Title"]
            body = row["Body"]
            entities = extract_entities(title + " " + body)
            output.write("Title: {}\n".format(title))
            output.write("Body: {}\n".format(body))
            output.write("Entities: {}\n".format(entities))
            output.write("\n")

# Example usage
csv_file = "data_collection/times_of_malta/data.csv"
#output_file = "output.txt" # Old output left for comparison's sake
output_file = "output2.txt"

def main():    
    process_articles(csv_file, output_file)
    
if __name__ == "__main__":
    main()
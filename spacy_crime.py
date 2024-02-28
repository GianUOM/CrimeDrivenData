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

    for ent in doc.ents:
        if ent.label_ == "DATE":
            entities["Date"].append(ent.text)
        elif ent.label_ == "PERSON" and ent.text.lower() not in ["qormi"] and ent.text.lower() not in ["mater dei"] and ent.text.lower() not in ["bitcoin"] and ent.text.lower() not in ["marsaxlokk"] and ent.text.lower() not in ["wuppertaler rundschau"] and ent.text.lower() not in ["macbook pro"] and ent.text.lower() not in ["bild"] and ent.text.lower() not in ["witnesses"] and ent.text.lower() not in ["triq lampuka"] and ent.text.lower() not in ["episode"] and ent.text.lower() not in ["mizan online"] and ent.text.lower() not in ["mosta"] and ent.text.lower() not in ["st francis square"] and ent.text.lower() not in ["messenger"] and ent.text.lower() not in ["gew kobba"] and ent.text.lower() not in ["guilty"] and ent.text.lower() not in ["st paul’s bay"] and ent.text.lower() not in ["gudja"] and ent.text.lower() not in ["facebook messenger"]:
            entities["Names"].append(ent.text)
    
    # Crime extraction
    crime_keywords = ["money-laundering", "sanctions", "fraud", "anti-money laundering", "malware", "FBI", "cybercriminals", "constitutional case", "fraud charges", "drugs", "scams", "attacked", "knife", "stabbing", "murder", "attempted murder", "sex crimes", "rape", "shooting", "assault", "plea bargain", "gunshot", "gang attack", "robing", "cocaine", "heroin", "cannabis", "possession", "apartheid", "Mafia", "ganged up", "thief", "armed thief", "breach", "killing", "mafia", "hate speech", "thieves", "stealing", "theft", "organised crime", "operation", "scam", "corruption", "burn", "conspiring", "sexually harassed", "money laundering", "trafficker", "abusing", "sexually abusing", "thefts", "snatch-and-grab", "stabbed", "raped", "killed", "child sex crimes", "threatning", "attack", "suicide", "suicide bombing", "hitting", "with a car", "attacks", "vandalised", "alleged inaction", "fined", "unfair commercial practices","drug trafficking", "nabbed", "drugs dealing", "nabbed", "conning", "sexual assault", "punched", "punching", "indecently touching", "touching", "beat", "hit", "hostage", "hostage-taker", "kill", "murders", "fight", "destroy", "beating", "strikes", "war crimes", "war crime", "film", "filmed", "filming", "sex", "sex video", "mental health", "dine-and-dash", "steals", "dine and dash", "sexually moslesting", "illegaly", "groped", "groping", "grope", "escape", "attempted escape", "domestic violence", "homicide", "involuntary homicide", "illegal recruiment agency", "allegations", "defrauded", "cyberbullying", "art trafficking", "abuse", "document forgery", "trafficking", "staging", "death", "starvation", "burning", "burned", "setting", "fire", "robbed", "gangs", "acid", "shoot"]
    for keyword in crime_keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE):
            entities["Crime"].append(keyword)
    
    # Location extraction (simplified for demonstration)
    locations = ["Attard", "Balzan", "Il-Bidnija", "Birgu", "Birkirkara", "Birżebbuġa", "Bormla", "Dingli", "Fgura", "Furjana", "Għargħur", "Għaxaq", "Gudja", "Gżira", "Ħamrun", "Iklin", "Kalkara", "Kirkop", "Lija", "Luqa", "Marsa", "Marsaskala", "Marsaxlokk", "Mdina", "Mġarr", "Mosta", "Mqabba", "Msida", "Mtarfa", "Naxxar", "Raħal Gdid", "Pembroke", "Pietà", "Qormi", "Qrendi", "Rabat", "Safi", "San Ġwann", "Santa Luċija", "Santa Venera", "Isla", "Siġġiewi", "Sliema", "San Ġiljan", "San Pawl", "Swieqi", "Tarxien", "Xbiex", "Valletta", "Xgħajra", "Żabbar", "Żebbug", "Żejtun", "Żurrieq", "Fontana", "Għajnsielem", "Għarb", "Għasri", "Kerċem", "Munxar", "Xlendi", "Nadur", "Qala", "Rabat", "San Lawrenz", "Sannat", "Xagħra", "Xewkija", "Marsalforn", "St Paul’s Bay","St Paul's Bay", "Paceville", "Marsascala", "Gozo", "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo, Democratic Republic of the", "Congo, Republic of the", "Costa Rica", "Cote d'Ivoire", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "East Timor (Timor-Leste)", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea, North", "Korea, South", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar (Burma)", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Macedonia (Macedonia)", "Norway", "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Paola", "Europe", "Pozzallo", "UK", "Mellieha", "Senglea", "Cospicua", "St Julian's", "Birzebbuga", "Għajn Żnuber", "Barcelona", "Zabbar", "St Julian’s"]
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
csv_file = "crimedata.csv"
output_file = "output.txt"
process_articles(csv_file, output_file)

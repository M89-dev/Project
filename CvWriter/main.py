import requests
import json
import openai
import docx

def main(latitude, longitude, radius, romes, insee, email, last_name, first_name, tel):
    nb_entreprise = int(input("Combien d'entreprises chercher vous ? : "))
    dictionnary_job, description_entreprise, link_job = get_job_API(latitude, longitude, radius, romes, insee, email, last_name, first_name, tel, nb_entreprise)
    value_check = None

    indice_job = 0

    while indice_job < nb_entreprise:

        print("\n" + description_entreprise[indice_job] + "\n")
        print("\n" + link_job[indice_job] + "\n")
        print("--------------------------------")
        print("Voulez-vous rejoindre cet entreprise ? (Y : yes, N : no)")
        value_check = input("> ")

        if value_check == "Y":
            CV_letter = write_cv(dictionnary_job[indice_job])
            file_adrr = "C:\\Users\\X\\Desktop\\Project\\CvWriter\\Lettre_Motivation\\"

            doc = docx.Document()
            doc.add_paragraph(str(CV_letter))
            file_word = f"Motivation_X_X_{dictionnary_job[indice_job]['company_name']}"
            print(f"Le fichier {file_word} a bien été crée !!")

        indice_job += 1

def write_cv(information_job):
    openai.api_key = ""

    prompt_cv = f"Write me a 2000 word cover letter with this information:  {information_job}"

    model_engine = "text-davinci-003"
    params = {
        "prompt": prompt_cv,
        "temperature": 0.7,
        "max_tokens": 2000,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }

    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt_cv,
        max_tokens=params["max_tokens"],
        temperature=params["temperature"],
        top_p=params["top_p"],
        frequency_penalty=params["frequency_penalty"],
        presence_penalty=params["presence_penalty"],
    )

    return response.choices[0].text.strip()
    
def get_job_API(latitude, longitude, radius, romes, insee, email, last_name, first_name, tel, nb_entreprise):
    dictionnary_job = {}
    job_info = []
    link_job = []
    number_job = len(dictionnary_job)
    name_company = ""

    query = {"caller" : "teste@gmail.com", "romes" : romes, "latitude" : latitude, "longitude" : longitude, "radius" : radius, "insee" : insee}
    response = requests.get("https://labonnealternance.apprentissage.beta.gouv.fr/api/V1/jobs", params=query)

    json_data = json.dumps(response.json())
    text_data = json.loads(json_data)

    for job in text_data["lbaCompanies"]["results"]:
        if name_company != job["company"]["name"]:

            dictionnary_job[number_job] = {
                "applicant_email": email,
                "applicant_last_name": last_name,
                "applicant_first_name": first_name,
                "applicant_phone": tel,
        
                "company_address": job["place"]["fullAddress"],
                "company_naf": job["nafs"][0]["label"],
                "company_name": job["company"]["name"],
            }

            link_job.append(text_data["peJobs"]["results"][0]["url"])
            job_info.append(text_data["peJobs"]["results"][0]["job"]["description"])

            name_company = job["company"]["name"]

        number_job = len(dictionnary_job)

        if number_job >= nb_entreprise:
            break

    return dictionnary_job, job_info, link_job

main("45", "4", "40", "M1805", "69123", "test@gmail.com", "X", "X", "00.0.0.0.0.0")
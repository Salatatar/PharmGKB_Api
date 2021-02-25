import requests
import json

url = "https://api.pharmgkb.org/v1/data/guideline?source=cpic&view=max"
 
response = requests.get(url)

response_dict = response.json()

haplotype_mapping = {}

len_data = len(response_dict["data"])
for i in range(len_data):
    len_guidelineGenes = len(response_dict["data"][i]["guidelineGenes"])
    if len_guidelineGenes == 1:
            genes = response_dict["data"][i]["guidelineGenes"][0]["gene"]["symbol"]
            haplotype_mapping[genes] = {}
            for k in range(len(response_dict["data"][i]["guidelineGenes"][0]["alleles"])):
                try:
                    symbol = response_dict["data"][i]["guidelineGenes"][0]["alleles"][k]["haplotype"]['symbol']
                    name = response_dict["data"][i]["guidelineGenes"][0]["alleles"][k]["haplotype"]['name']
                    haplotype_mapping[genes][name] = symbol
                except KeyError:
                    symbol = response_dict["data"][i]["guidelineGenes"][0]["alleles"][k]["allele"]
                    haplotype_mapping[genes][symbol] = symbol
    elif len_guidelineGenes > 1:
        for j in range(len_guidelineGenes):
            genes = response_dict["data"][i]["guidelineGenes"][j]["gene"]["symbol"]
            haplotype_mapping[genes] = {}
            for k in range(len(response_dict["data"][i]["guidelineGenes"][j]["alleles"])):
                try:
                    symbol = response_dict["data"][i]["guidelineGenes"][j]["alleles"][k]["haplotype"]['symbol']
                    name = response_dict["data"][i]["guidelineGenes"][j]["alleles"][k]["haplotype"]['name']
                    haplotype_mapping[genes][name] = symbol
                except KeyError:
                    symbol = response_dict["data"][i]["guidelineGenes"][j]["alleles"][k]["allele"]
                    haplotype_mapping[genes][symbol] = symbol

with open('PharmGKB_api/function_mapping/haplotype_mapping.json', 'w') as fp:
    json.dump(haplotype_mapping, fp, indent=2)

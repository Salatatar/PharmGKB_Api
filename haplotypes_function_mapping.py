import requests
import json

url = "https://api.pharmgkb.org/v1/data/guideline?source=cpic&view=max"
 
response = requests.get(url)

response_dict = response.json()

haplotype_function_mapping = {}

len_data = len(response_dict["data"])
for i in range(len_data):
    id_guidelineGenes = response_dict["data"][i]["id"]
    len_guidelineGenes = len(response_dict["data"][i]["guidelineGenes"])
    haplotype_function_mapping[id_guidelineGenes] = {}
    if len_guidelineGenes == 1:
            genes = response_dict["data"][i]["guidelineGenes"][0]["gene"]["symbol"]
            haplotype_function_mapping[id_guidelineGenes][genes] = {}
            # haplotype_function_mapping[genes] = {}
            for k in range(len(response_dict["data"][i]["guidelineGenes"][0]["alleles"])):
                try:
                    symbol = response_dict["data"][i]["guidelineGenes"][0]["alleles"][k]["haplotype"]['symbol']
                    name = response_dict["data"][i]["guidelineGenes"][0]["alleles"][k]["haplotype"]['name']
                    function = response_dict["data"][i]["guidelineGenes"][0]["alleles"][k]["function"]["term"]
                    haplotype_function_mapping[id_guidelineGenes][genes][symbol] = function
                except KeyError:
                    symbol = response_dict["data"][i]["guidelineGenes"][0]["alleles"][k]["allele"]
                    function = response_dict["data"][i]["guidelineGenes"][0]["alleles"][k]["function"]["term"]
                    haplotype_function_mapping[id_guidelineGenes][genes][symbol] = function
    elif len_guidelineGenes > 1:
        for j in range(len_guidelineGenes):
            genes = response_dict["data"][i]["guidelineGenes"][j]["gene"]["symbol"]
            haplotype_function_mapping[id_guidelineGenes][genes] = {}
            for k in range(len(response_dict["data"][i]["guidelineGenes"][j]["alleles"])):
                try:
                    symbol = response_dict["data"][i]["guidelineGenes"][j]["alleles"][k]["haplotype"]['symbol']
                    name = response_dict["data"][i]["guidelineGenes"][j]["alleles"][k]["haplotype"]['name']
                    function = response_dict["data"][i]["guidelineGenes"][j]["alleles"][k]["function"]["term"]
                    haplotype_function_mapping[id_guidelineGenes][genes][symbol] = function
                except KeyError:
                    symbol = response_dict["data"][i]["guidelineGenes"][j]["alleles"][k]["allele"]
                    function = response_dict["data"][i]["guidelineGenes"][j]["alleles"][k]["function"]["term"]
                    haplotype_function_mapping[id_guidelineGenes][genes][symbol] = function
    else:
        del haplotype_function_mapping[id_guidelineGenes]

with open('PharmGKB_api/function_mapping/haplotype_function_mapping.json', 'w') as fp:
    json.dump(haplotype_function_mapping, fp, indent=2)

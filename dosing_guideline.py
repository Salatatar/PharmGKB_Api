from itertools import permutations
import pandas as pd
import platform
import os
import requests
import json

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}

with open('D:\Biobank\PharmGKB_Api\Api_V1\haplotype_function_mapping.json') as json_file:
    data = json.load(json_file)

annotations = {}
annotationByDiplotype_List = []
guidelineAnnotation_List = []

id_annotations = []
annotation_ID = ""
annotation_Gene = ""
annotation_Function_1 = ""
annotation_Function_2 = ""
annotation_Function_3 = ""
annotation_Function_4 = ""

def get_AnnotationGuideline(get_Guideline):
    try:
        get_Guideline.append(response_dict["data"]["id"])
    except KeyError:
        get_Guideline.append("")
    except TypeError:
        get_Guideline.append("")
    try:
        get_Guideline.append(response_dict["data"]["name"])
    except KeyError:
        get_Guideline.append("")
    except TypeError:
        get_Guideline.append("")
    try:
        get_Guideline.append(response_dict["data"]["guideline"]["id"])
    except KeyError:
        get_Guideline.append("")
    except TypeError:
        get_Guideline.append("")
    try:
        get_Guideline.append(response_dict["data"]["guideline"]["name"])
    except KeyError:
        get_Guideline.append("")
    except TypeError:
        get_Guideline.append("")
    try:
        get_Guideline.append(response_dict["data"]["rxChangeStatus"]["term"])
    except KeyError:
        get_Guideline.append("")
    except TypeError:
        get_Guideline.append("")
    try:
        get_Guideline.append(response_dict["data"]["strength"]["term"])
    except KeyError:
        get_Guideline.append("")
    except TypeError:
        get_Guideline.append("")
    try:
        get_Guideline.append(response_dict["data"]["recommendation"]["html"])
    except KeyError:
        get_Guideline.append("")
    except TypeError:
        get_Guideline.append("")
    try:
        get_Guideline.append(response_dict["data"]["implications"]["html"])
    except KeyError:
        get_Guideline.append("")
    except TypeError:
        get_Guideline.append("")
    try:
        get_Guideline.append(response_dict["data"]["phenotype"]["html"])
    except KeyError:
        get_Guideline.append("")
    except TypeError:
        get_Guideline.append("")
    try:
        get_Guideline.append(response_dict["data"]["metabolizerStatus"]["html"])
    except KeyError:
        get_Guideline.append("")
    except TypeError:
        get_Guideline.append("")
    return get_Guideline

def save_Annotationguideline(annotationByDiplotype_List, guidelineAnnotation_List, guidelineAnnotation_dict, id_annotation):
    url = "https://api.pharmgkb.org/v1/data/guideline?source=cpic&view=max"
    response = requests.get(url)
    response_dict = response.json()
    name_Chemical = ""
    dir_name = ""
    len_data = len(response_dict["data"])
    for i in range(len_data):
        name_annotation = ""
        id_name_Chemical = response_dict["data"][i]["id"]
        if len(response_dict["data"][i]["guidelineGenes"]) == 1:
            name_annotation = response_dict["data"][i]["guidelineGenes"][0]["gene"]["symbol"] + "_"
        else:
            for n in range(len(response_dict["data"][i]["guidelineGenes"])):
                name_annotation += response_dict["data"][i]["guidelineGenes"][n]["gene"]["symbol"] + "_"
        if id_name_Chemical == id_annotation:
            for m in range(len(response_dict["data"][i]["relatedChemicals"])):
                name_Chemical += response_dict["data"][i]["relatedChemicals"][m]["name"] + "_"
            dir_name = name_annotation + name_Chemical + id_annotation
    # print(dir_name)
    parent_dir = os.getcwd() + "\PharmGKB_api\clinical_annotation_guidelines\excel"
    path = os.path.join(parent_dir, dir_name)
    # print(path)
    try: 
        os.makedirs(path, exist_ok = True) 
        print("Directory '%s' created successfully" % dir_name) 
    except OSError as error: 
        print("Directory '%s' can not be created" % dir_name)

    try:
        df1 = pd.DataFrame(annotationByDiplotype_List[-1], columns = ['Function1', 'Function2', 'Phenotype', 'GuidelineAnnotationId'])
        df2 = pd.DataFrame(guidelineAnnotation_List[-1], columns = ['GuidelineAnnotationID', 'GuidelineAnnotationName', 'GuidelineId', 'GuidelineName', 'RxChangeStatus', "Strength", "Recommendations", "Implications", "Phenotype", "MetabolizerStatus"])
        df_1 = df1.drop_duplicates()
        df_2 = df2.drop_duplicates()
        with pd.ExcelWriter(r'{}\{}_{}.xlsx'.format(path, name_annotation, id_annotation)) as writer:
            df_1.to_excel(writer, sheet_name='AnnotationByDiplotype', index = False, header=True)
            df_2.to_excel(writer, sheet_name='GuidelineAnnotations', index = False, header=True)
    except AssertionError:
        df1 = pd.DataFrame(annotationByDiplotype_List[-1], columns = ['Function1', 'Function2', 'Function3', 'Function4', 'Phenotype', 'GuidelineAnnotationId'])
        df2 = pd.DataFrame(guidelineAnnotation_List[-1], columns = ['GuidelineAnnotationID', 'GuidelineAnnotationName', 'GuidelineId', 'GuidelineName', 'RxChangeStatus', "Strength", "Recommendations", "Implications", "Phenotype", "MetabolizerStatus"])
        df_1 = df1.drop_duplicates()
        df_2 = df2.drop_duplicates()
        with pd.ExcelWriter(r'{}\{}_{}.xlsx'.format(path, name_annotation, id_annotation)) as writer:
            df_1.to_excel(writer, sheet_name='AnnotationByDiplotype', index = False, header=True)
            df_2.to_excel(writer, sheet_name='GuidelineAnnotations', index = False, header=True)
    except ValueError:
        df1 = pd.DataFrame(annotationByDiplotype_List[-1], columns = ['Function1', 'Function2', 'Function3', 'Function4', 'Phenotype', 'GuidelineAnnotationId'])
        df2 = pd.DataFrame(guidelineAnnotation_List[-1], columns = ['GuidelineAnnotationID', 'GuidelineAnnotationName', 'GuidelineId', 'GuidelineName', 'RxChangeStatus', "Strength", "Recommendations", "Implications", "Phenotype", "MetabolizerStatus"])
        df_1 = df1.drop_duplicates()
        df_2 = df2.drop_duplicates()
        with pd.ExcelWriter(r'{}\{}_{}.xlsx'.format(path, name_annotation, id_annotation)) as writer:
            df_1.to_excel(writer, sheet_name='AnnotationByDiplotype', index = False, header=True)
            df_2.to_excel(writer, sheet_name='GuidelineAnnotations', index = False, header=True)
    with open("PharmGKB_api/clinical_annotation_guidelines/json/guidelineAnnotation_"+ id_annotation +".json", 'w') as fp:
        json.dump(guidelineAnnotation_dict, fp, indent=2)

for id in data.keys():
    id_annotations.append(id)
    annotations[id] = {}

for i in range(len(id_annotations)):
    guidelineAnnotation_dict = {}
    guidelineAnnotation_dict[id_annotations[i]] = {}
    annotation_ID = id_annotations[i]
    annotationByDiplotype = []
    guidelineAnnotation = []
    name_Gene = []
    print("Start Get Data of", id_annotations[i])
    if len(data[id_annotations[i]]) == 1:
        for k in data[id_annotations[i]].keys():
            guidelineAnnotation_dict[id_annotations[i]][k] = {}
            annotations[id_annotations[i]][k] = []
            function_annotations = []
            annotation_Gene = k
            count_1 = 1
            for n in data[id_annotations[i]][k].values():
                guidelineAnnotation_dict[id_annotations[i]][k][count_1] = {}
                function_annotations.append(n)
                add_data = (n, n)
                annotation_Function_1 = add_data[0]
                annotation_Function_2 = add_data[1]
                if add_data not in annotations[id_annotations[i]][k]:
                    annotations[id_annotations[i]][k].append(tuple(add_data))
                    genes_and_function = """{ \""""+annotation_Gene+"""\": [ \""""+annotation_Function_1+"""\", \""""+annotation_Function_2+"""\" ] }"""
                    guideline_data = genes_and_function
                    url_id = "https://api.pharmgkb.org/v1/report/guideline/"+ id_annotations[i] +"/annotations"
                    try:
                        response = requests.post(url_id, headers=headers, data=guideline_data.encode('utf-8'))
                    except ConnectionError as e:
                        print("CONNECTION ERROR: ", e)
                        pass
                    response_dict = response.json()
                    guidelineAnnotation_dict[id_annotations[i]][k][count_1] = response_dict
                    # print(json.dumps(response_dict, indent=2))
                    get_Annotation = []
                    get_Annotation.append(annotation_Function_1)
                    get_Annotation.append(annotation_Function_2)
                    try:
                        get_Annotation.append(response_dict["data"]["name"])
                        get_Annotation.append(response_dict["data"]["id"])
                    except:
                        get_Annotation.append("None")
                        get_Annotation.append("None")
                    annotationByDiplotype.append(get_Annotation)
                    get_Guideline = []
                    get_AnnotationGuideline(get_Guideline)
                    guidelineAnnotation.append(get_Guideline)
                    count_1 += 1
            perm = permutations(function_annotations, 2)
            count_2 = 1
            for fn in list(perm):
                guidelineAnnotation_dict[id_annotations[i]][k][count_2] = {}
                add_data = fn
                annotation_Function_1 = add_data[0]
                annotation_Function_2 = add_data[1]
                if add_data not in annotations[id_annotations[i]][k]:
                    annotations[id_annotations[i]][k].append(tuple(add_data))
                    genes_and_function = """{ \""""+annotation_Gene+"""\": [ \""""+annotation_Function_1+"""\", \""""+annotation_Function_2+"""\" ] }"""
                    guideline_data = genes_and_function
                    url_id = "https://api.pharmgkb.org/v1/report/guideline/"+ id_annotations[i] +"/annotations"
                    try:
                        response = requests.post(url_id, headers=headers, data=guideline_data.encode('utf-8'))
                    except ConnectionError as e:
                        print("CONNECTION ERROR: ", e)
                        pass
                    response_dict = response.json()
                    guidelineAnnotation_dict[id_annotations[i]][k][count_2] = response_dict
                    # print(json.dumps(response_dict, indent=2))
                    get_Annotation = []
                    get_Annotation.append(annotation_Function_1)
                    get_Annotation.append(annotation_Function_2)
                    try:
                        get_Annotation.append(response_dict["data"]["name"])
                        get_Annotation.append(response_dict["data"]["id"])
                    except:
                        get_Annotation.append("None")
                        get_Annotation.append("None")
                    annotationByDiplotype.append(get_Annotation)
                    get_Guideline = []
                    get_AnnotationGuideline(get_Guideline)
                    guidelineAnnotation.append(get_Guideline)
                    count_2 += 1
    else:
        name_dict = ""
        count = 0
        for k in data[id_annotations[i]].keys():
            name_Gene.append(k)
            annotation_Gene = k
            name_dict = k + "_" + str(count)
            annotations[id_annotations[i]][k] = []
            guidelineAnnotation_dict[id_annotations[i]][name_dict] = {}
            function_annotations = []
            for n in data[id_annotations[i]][k].values():
                function_annotations.append(n)
                add_data = (n, n)
                if add_data not in annotations[id_annotations[i]][k]:
                    annotations[id_annotations[i]][k].append(tuple(add_data))
            perm = permutations(function_annotations, 2)
            for fn in list(perm):
                add_data = fn
                if add_data not in annotations[id_annotations[i]][k]:
                    annotations[id_annotations[i]][k].append(tuple(add_data))
            count += 1

        for x in range(len(annotations[id_annotations[i]][name_Gene[0]])):
            for y in range(len(annotations[id_annotations[i]][name_Gene[1]])):
                annotation_Function_1 = annotations[id_annotations[i]][name_Gene[0]][x][0]
                annotation_Function_2 = annotations[id_annotations[i]][name_Gene[0]][x][1]
                annotation_Function_3 = annotations[id_annotations[i]][name_Gene[1]][y][0]
                annotation_Function_4 = annotations[id_annotations[i]][name_Gene[1]][y][1]
                genes_and_function = """{ \""""+name_Gene[0]+"""\": [ \""""+annotation_Function_1+"""\", \""""+annotation_Function_2+"""\" ], \""""+name_Gene[1]+"""\": [ \""""+annotation_Function_3+"""\", \""""+annotation_Function_4+"""\" ] }"""
                guideline_data = genes_and_function
                url_id = "https://api.pharmgkb.org/v1/report/guideline/"+ id_annotations[i] +"/annotations"
                try:
                    response = requests.post(url_id, headers=headers, data=guideline_data.encode('utf-8'))
                except ConnectionError as e:
                    print("CONNECTION ERROR: ", e)
                    pass
                response_dict = response.json()
                guidelineAnnotation_dict[id_annotations[i]][name_dict][y + 1] = response_dict
                # annotations_test[y] = response_dict
                get_Annotation = []
                get_Annotation.append(annotation_Function_1)
                get_Annotation.append(annotation_Function_2)
                get_Annotation.append(annotation_Function_3)
                get_Annotation.append(annotation_Function_4)
                try:
                    get_Annotation.append(response_dict["data"]["name"])
                    get_Annotation.append(response_dict["data"]["id"])
                except:
                    get_Annotation.append("None")
                    get_Annotation.append("None")
                annotationByDiplotype.append(get_Annotation)
                get_Guideline = []
                get_AnnotationGuideline(get_Guideline)
                guidelineAnnotation.append(get_Guideline)

    annotationByDiplotype_List.append(annotationByDiplotype)
    guidelineAnnotation_List.append(guidelineAnnotation)
    save_Annotationguideline(annotationByDiplotype_List, guidelineAnnotation_List, guidelineAnnotation_dict, id_annotations[i])
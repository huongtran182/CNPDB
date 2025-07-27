# -*- coding: utf-8 -*-
"""
Created on Thu Jun 12 15:57:22 2025

"""

import pandas as pd
import requests
import time
import glob
from Bio import Entrez

Entrez.email = "lafields2@wisc.edu"
outpath = "2025_NP_Database_Update\PubMedSearch"
neuropep_folder = "2025_NP_Database_Update\PubMedSearch"
database_path = "2025_NP_Database_Update\PubMedSearch\updated_crustacean_database_gravy_KT_MSB_v9.csv"

database = pd.read_csv(database_path, encoding="ISO-8859-1")
peptides = database['seq'].values.tolist()

neuropep_files = glob.glob(f"{neuropep_folder}\\*.txt")
df_list = []
for file in neuropep_files:
    try:
        df = pd.read_csv(file, sep="\t")
        df_list.append(df)
    except Exception as e:
        print(f"Error reading {file}: {e}")
neuropep_df = pd.concat(df_list, ignore_index=True).drop_duplicates()

def get_doi_from_pmid(pmid):
    try:
        handle = Entrez.efetch(db="pubmed", id=pmid, rettype="xml")
        records = Entrez.read(handle)
        handle.close()
        articles = records["PubmedArticle"]
        for article in articles:
            ids = article["PubmedData"]["ArticleIdList"]
            for id_ in ids:
                if id_.attributes.get("IdType") == "doi":
                    return str(id_)
    except Exception as e:
        print(f"DOI lookup failed for PMID {pmid}: {e}")
    return ""

def fetch_title_from_pmid(pmid):
    try:
        handle = Entrez.efetch(db="pubmed", id=pmid, rettype="medline", retmode="text")
        lines = handle.read().splitlines()
        handle.close()
        title = ""
        capture = False
        for line in lines:
            if line.startswith("TI  -"):
                title = line[6:].strip()
                capture = True
            elif capture and line.startswith("      "):
                title += " " + line.strip()
            elif capture:
                break
        return title
    except Exception as e:
        print(f"Title lookup failed for PMID {pmid}: {e}")
        return ""

records = []

for pep in peptides:
    seen_ids = set()
    try:
        handle = Entrez.esearch(db="pubmed", term=f'"{pep}"', retmax=100)
        record = Entrez.read(handle)
        pubmed_pmids = record["IdList"]
        for pmid in pubmed_pmids:
            doi = get_doi_from_pmid(pmid)
            handle = Entrez.efetch(db="pubmed", id=pmid, rettype="medline", retmode="text")
            lines = handle.read().splitlines()
            title = ""
            capture = False
            for line in lines:
                if line.startswith("TI  -"):
                    title = line[6:].strip()
                    capture = True
                elif capture and line.startswith("      "):
                    title += " " + line.strip()
                elif capture:
                    break
            handle.close()
            id_key = doi if doi else pmid
            if id_key not in seen_ids:
                records.append({
                    "Peptide": pep,
                    "DOI": doi,
                    "Source": "PubMed",
                    "Title": title
                })
                seen_ids.add(id_key)
            time.sleep(0.5)
    except Exception as e:
        print(f"Error querying PubMed for {pep}: {e}")

    try:
        url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={pep}&format=json&pageSize=100"
        response = requests.get(url, timeout=10)
        data = response.json()
        hits = data.get("resultList", {}).get("result", [])
        for hit in hits:
            doi = hit.get("doi", "")
            pmid = hit.get("pmid", "")
            title = hit.get("title", "")
            id_key = doi if doi else pmid
            if id_key and id_key not in seen_ids:
                records.append({
                    "Peptide": pep,
                    "DOI": doi,
                    "Source": "Europe PMC",
                    "Title": title
                })
                seen_ids.add(id_key)
        time.sleep(0.5)
    except Exception as e:
        print(f"Error querying Europe PMC for {pep}: {e}")

    try:
        matches = neuropep_df[neuropep_df["Sequence"] == pep]
        for _, row in matches.iterrows():
            pmid = str(row["PMID"])
            title = fetch_title_from_pmid(pmid)
            doi = get_doi_from_pmid(pmid)
            id_key = doi if doi else pmid
            if id_key and id_key not in seen_ids:
                records.append({
                    "Peptide": pep,
                    "DOI": doi,
                    "Source": "NeuroPep",
                    "Title": title
                })
                seen_ids.add(id_key)
    except Exception as e:
        print(f"Error checking NeuroPep for {pep}: {e}")

records_df = pd.DataFrame(records)
records_df.to_csv(f'{outpath}\\full_db.csv', index=False)

from modules import *
import requests
import os
#terminal version for debugging and testing without front end
def download_pdf(url, name):
    file_name = name

    save_path = os.path.join("data", file_name)
    save_path = save_path + ".pdf"

    response = requests.get(url)

    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"PDF downloaded successfully: {save_path}")
    else:
        print(f"Failed to download PDF: {url}")

start = "y"

urls = [
    "https://openreview.net/pdf?id=VtmBAGCN7o",
    "https://openreview.net/pdf?id=6PmJoRfdaK",
    "https://openreview.net/pdf?id=hSyW5go0v8",
]

papers = [
    "metagpt",
    "longlora",
    "selfrag",
]
for url, paper in zip(urls, papers):
    download_pdf(url, paper)

while start == "y":
    query = input("Ask your pdf some question: ")
    output = manydocAgent(papers).chat(query)
    reply = str(output.response)
    sources = output.source_nodes
    citation = ""
    for i in range(max(len(sources), 3)):
        source = sources[i]
        num = i + 1
        citation += (f"{num}: Page {source.metadata['page_label']} in {source.metadata['file_name']}\n")
    reply.replace("assistant: ", "")
    template = f"{reply}\n Sources: {citation}\n"
    print(template)
    start = input("Would you like to keep chatting (y/n): ")
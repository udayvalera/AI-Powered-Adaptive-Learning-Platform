from ingest import ingest_file, search_documents_with_score, return_documents_summary


# ingest_file("./data/NIPS-2017-attention-is-all-you-need-Paper.pdf")
print(search_documents_with_score("What is attention?"))
# metadata=return_documents_summary()
# print(metadata)
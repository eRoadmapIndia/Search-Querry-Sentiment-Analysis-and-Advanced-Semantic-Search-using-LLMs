import streamlit as st
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

indexName = "my_products"

try:
    es = Elasticsearch(
    "https://7e0d0bd326fc41f8ad3aed7fcb4af406.us-central1.gcp.cloud.es.io:443",
    api_key=('d5df5d5237d9477b8400b1e92c5d9033:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDdlMGQwYmQzMjZmYzQxZjhhZDNhZWQ3ZmNiNGFmNDA2JGRmNWM3MTI4MjJkMTQ4ODRiMDI2OGRiYTcyZWYzZjZm'),
    )
except ConnectionError as e:
    print("Connection Error:", e)
    
if es.ping():
    print("Succesfully connected to ElasticSearch!!")
else:
    print("Oops!! Can not connect to Elasticsearch!")




def search(input_keyword):
    model = SentenceTransformer('all-mpnet-base-v2')
    vector_of_input_keyword = model.encode(input_keyword)

    query = {
        "field": "DescriptionVector",
        "query_vector": vector_of_input_keyword,
        "k": 10,
        "num_candidates": 500
    }
    res = es.knn_search(index="my_products"
                        , knn=query 
                        , source=["ProductName","Description"]
                        )
    results = res["hits"]["hits"]

    return results

def main():
    st.title("Search ONDC Network Fashion Products")

    # Input: User enters search query
    search_query = st.text_input("Enter your search query")

    # Button: User triggers the search
    if st.button("Search"):
        if search_query:
            # Perform the search and get results
            results = search(search_query)

            # Display search results
            st.subheader("Search Results")
            for result in results:
                with st.container():
                    if '_source' in result:
                        try:
                            st.header(f"{result['_source']['ProductName']}")
                        except Exception as e:
                            print(e)
                        
                        try:
                            st.write(f"Description: {result['_source']['Description']}")
                        except Exception as e:
                            print(e)
                        st.divider()

                    
if __name__ == "__main__":
    main()

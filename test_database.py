from src_database_search import search_src_database


question = "What B.Sc courses are available at SRC?"


results = search_src_database(
    question,
    k=5
)


print()
print("====================================")
print("🔎 SRC DATABASE SEARCH")
print("====================================")
print()


for number, document in enumerate(
    results,
    start=1
):

    print(
        f"RESULT {number}"
    )

    print(
        "SOURCE:",
        document.metadata.get(
            "source",
            "Unknown"
        )
    )

    print()

    print(
        document.page_content[:1000]
    )

    print()
    print("------------------------------------")
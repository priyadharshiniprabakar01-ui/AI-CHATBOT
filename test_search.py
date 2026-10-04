from src_search import search_src_website


question = "What B.Sc courses are available at SRC?"


results = search_src_website(
    question
)


print("\n\n==============================")
print("SEARCH RESULTS")
print("==============================\n")


for score, result in results:

    print(
        f"Score: {score}"
    )

    print(
        f"URL: {result['url']}"
    )

    print(
        f"\nContent preview:\n"
    )

    print(
        result["text"][:1500]
    )

    print(
        "\n------------------------------\n"
    )
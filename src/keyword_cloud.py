from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

def generate_keyword_cloud(keywords, output_path):
    if not keywords:
        return None

    text = " ".join(keywords)

    wc = WordCloud(
        width=900,
        height=450,
        background_color="white"
    ).generate(text)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    return output_path


def main():
    # test mode
    keywords = ["fever", "cough", "hypertension", "diagnosis"]
    generate_keyword_cloud(keywords, "graphs/sample_keyword_cloud.png")


if __name__ == "__main__":
    main()

import os
from openai import OpenAI

OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

INVESTMENT_PROMPT = (
    "CREATE AN INVESTMENT STRATEGY WITH THE GOAL OF BEATING THE S&P 500 OVER THE NEXT YEAR."
)

PASSAGES = [
    {
        "title": "From John Galt",
        "text": "Man's mind is his basic tool of survival. Life is given to him; survival is not. His body is given to him, its sustenance is not. His mind is given to him, its contents are not. To remain alive, he must act, and before he can act he must know the nature and purpose of his action.",
    },
    {
        "title": "From Buffett",
        "text": "Games are won by players who focus on the playing field—not by those whose eyes are glued to the scoreboard.",
    },
    {
        "title": "From Simons",
        "text": "Markets are full of subtle patterns that are difficult for humans to detect but can be uncovered through mathematics and computation.",
    },
]


CONTROL_RUNS = 3
RUNS_PER_PROMPT = 2


def call_api(client, messages):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content


def run_experiment():
    client = OpenAI(api_key=OPENAI_API_KEY)

    results = []

    for i in range(1, CONTROL_RUNS + 1):
        print(f"\n{'='*60}")
        print(f"Running control (no passage) — run {i} of {CONTROL_RUNS}")
        print("="*60)

        messages = [{"role": "user", "content": INVESTMENT_PROMPT}]
        output = call_api(client, messages)

        print(output)

        results.append({
            "passage_title": f"CONTROL (run {i})",
            "passage_text": None,
            "investment_strategy": output,
        })

    for passage in PASSAGES:
        for run in range(1, RUNS_PER_PROMPT + 1):
            print(f"\n{'='*60}")
            print(f"Running with passage: {passage['title']} — run {run} of {RUNS_PER_PROMPT}")
            print("="*60)

            messages = [{"role": "user", "content": f"{passage['text']}\n\n{INVESTMENT_PROMPT}"}]
            output = call_api(client, messages)

            print(output)

            results.append({
                "passage_title": f"{passage['title']} (run {run})",
                "passage_text": passage["text"],
                "investment_strategy": output,
            })

    return results


def save_results(results):
    with open("results.txt", "w") as f:
        for result in results:
            f.write(f"{'='*60}\n")
            f.write(f"PASSAGE: {result['passage_title']}\n")
            f.write(f"{'='*60}\n\n")
            if result["passage_text"] is not None:
                f.write(f"--- Passage Text ---\n{result['passage_text']}\n\n")
            f.write(f"--- Investment Strategy ---\n{result['investment_strategy']}\n\n")


if __name__ == "__main__":
    results = run_experiment()
    save_results(results)
    print("\n\nResults saved to results.txt")

import json
import google.generativeai as genai


def get_code_metrics(path: str) -> dict:
    """
    Given a file path, this function generates code metrics for the code in that file
    using the Gemini Pro language model from Generative.AI

    :param path: The path to the file containing the code to analyze
    :return: A dictionary containing code metrics for the code in the given file
    """
    with open(path) as f:
        code_in_text = f.read()

    model = genai.GenerativeModel("gemini-pro")

    response = model.generate_content(
        f"""I will give you code in text format you have to give output only in json with no other text apart from json.
		The keys for json will be Time Complexity, Space Complexity, Cyclomatic complexity, Code Smells and Security vulnerabilities.
		You have to provide values to the keys by testing the code correctly and efficiently.
		Here's code: {code_in_text}"""
    )

    print("Metrics for code in file:", path)
    print(response.text)
    print()

    return json.loads(
        response.text[response.text.find("{") : response.text.find("}") + 1]
    )


if __name__ == "__main__":
	path = r"C:\Users\SSD\OneDrive\Documents\py\A2S_assignment\final_capture_print.py"
	metrics = get_code_metrics(path)
	print(metrics)
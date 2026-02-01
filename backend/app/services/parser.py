import abc
import re
import subprocess

class PolicyParser(abc.ABC):
    """
    Abstract Base Class for Policy Parsers.
    Implementations can be Regex-based, AI/LLM-based, or Rule-based.
    """
    @abc.abstractmethod
    def parse(self, file_path: str) -> dict:
        """
        Extracts policy rules from a document.
        :param file_path: Path to the document (PDF, DOCX, etc.)
        :return: Dictionary of extracted rules (e.g. {'min_fico': 700})
        """
        pass

class RegexPolicyParser(PolicyParser):
    """
    Basic implementation using pdftotext and Regex.
    Low cost, fast, but brittle.
    """
    def extract_text(self, pdf_path):
        try:
            result = subprocess.run(['pdftotext', pdf_path, '-'], capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            print(f"Error running pdftotext: {e}")
            return ""

    def parse(self, file_path: str) -> dict:
        text = self.extract_text(file_path)
        if not text:
            return {}

        rules = {}
        # FICO
        fico_match = re.search(r'FICO.*?(\d{3})', text, re.IGNORECASE)
        if fico_match:
            rules['min_fico'] = int(fico_match.group(1))
            
        # Time in Business
        tib_match = re.search(r'(\d+)\+?\s*years?.*?business', text, re.IGNORECASE)
        if tib_match:
            rules['min_tib_years'] = int(tib_match.group(1))
            
        # Max Amount
        amount_match = re.search(r'\$(\d{1,3}(,\d{3})*)', text)
        if amount_match:
            rules['max_amount'] = int(amount_match.group(1).replace(',', ''))
            
        return rules

class AIPolicyParser(PolicyParser):
    """
    Placeholder for Future AI Implementation.
    Would use OpenAI/Anthropic/Gemini APIs to extract structured data.
    """
    def parse(self, file_path: str) -> dict:
        # TODO: Implement LLM call here
        # prompt = "Extract min_fico, max_amount, and excluded_states from this text..."
        # response = calling_llm(prompt, file_path)
        # return json.loads(response)
        raise NotImplementedError("AI Parser requires an API key configuration.")

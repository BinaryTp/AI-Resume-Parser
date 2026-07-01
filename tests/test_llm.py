import unittest

from llm import analyze_resume


class ResumeParsingTests(unittest.TestCase):
    def test_analyze_resume_falls_back_without_api_key(self):
        sample_resume = """
John Doe
Software Engineer
john.doe@example.com
+1 555 123 4567
Skills: Python, JavaScript, SQL, Docker
Education: B.Tech in Computer Science, ABC University, 2020-2024
Projects: Built a chatbot using Python and FastAPI
"""

        result = analyze_resume(sample_resume)

        self.assertEqual(result["name"], "John Doe")
        self.assertEqual(result["email"], "john.doe@example.com")
        self.assertEqual(result["phone"], "+1 555 123 4567")
        self.assertIn("Python", result["skills"])
        self.assertTrue(result["ats_score"] >= 0)


if __name__ == "__main__":
    unittest.main()

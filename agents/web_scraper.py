class WebScraper():
    def __init__(self, company: str):
        self.company = company

    def get_info(self):
        mock_data = {
            "telenor": """
                Telenor is a Norwegian telecommunications company. Key facts:
                - Founded in 1855
                - Operates in Nordic and Asian markets
                - Offers mobile, broadband, and digital services
                - Known for reliable network coverage
                - Strong focus on sustainability and digital inclusion
                - Major competitor in Norwegian telecom market
                """,
            "telia": """
                Telia is a Swedish telecommunications company. Key facts:
                - Founded in 1853
                - Leading telecom operator in Nordic and Baltic countries
                - Offers mobile, fixed broadband, and TV services
                - Strong 5G network infrastructure
                - Focus on digital transformation services
                - Committed to sustainable business practices
                """
        }
        return mock_data.get(self.company.lower(), "Company information not available.")

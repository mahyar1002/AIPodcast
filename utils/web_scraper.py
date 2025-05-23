import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import urljoin, urlparse
from typing import Optional, Dict, List


class WebScraper:
    def __init__(self, company: str):
        self.company = company
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def find_company_url(self) -> Optional[str]:
        """
        Find the company's official website URL using multiple strategies
        """
        # Strategy 1: Try common domain patterns
        url = self._try_common_domains()
        if url:
            return url

        # Strategy 2: Use DuckDuckGo search (less JS-heavy)
        url = self._search_duckduckgo()
        if url:
            return url

        # Strategy 3: Use Bing search
        url = self._search_bing()
        if url:
            return url

        # Strategy 4: Try company directory APIs
        url = self._try_company_apis()
        if url:
            return url

        return None

    def _try_common_domains(self) -> Optional[str]:
        """
        Try common domain patterns for the company
        """
        company_clean = re.sub(r'[^a-zA-Z0-9\s]', '', self.company.lower())
        company_parts = company_clean.split()

        # Remove common corporate suffixes
        suffixes = ['inc', 'corp', 'corporation',
                    'company', 'co', 'ltd', 'llc', 'group']
        company_parts = [
            part for part in company_parts if part not in suffixes]

        if not company_parts:
            return None

        # Generate possible domain combinations
        domain_patterns = []

        if len(company_parts) == 1:
            domain_patterns = [
                f"{company_parts[0]}.com",
                f"{company_parts[0]}.org",
                f"{company_parts[0]}.net"
            ]
        else:
            # Multiple words - try different combinations
            joined = ''.join(company_parts)
            first_word = company_parts[0]

            domain_patterns = [
                f"{joined}.com",
                f"{first_word}.com",
                f"{'-'.join(company_parts)}.com",
                f"{joined}.org",
                f"{first_word}.org"
            ]

        # Test each domain pattern
        for domain in domain_patterns:
            test_urls = [f"https://www.{domain}", f"https://{domain}"]
            for url in test_urls:
                if self._is_valid_url(url):
                    print(f"Found URL via domain pattern: {url}")
                    return url

        return None

    def _search_duckduckgo(self) -> Optional[str]:
        """
        Search using DuckDuckGo (less JavaScript-dependent)
        """
        try:
            search_query = f"{self.company} official website"
            search_url = f"https://duckduckgo.com/html/?q={search_query.replace(' ', '+')}"

            response = self.session.get(search_url)
            if response.status_code != 200:
                return None

            soup = BeautifulSoup(response.content, 'html.parser')

            # DuckDuckGo HTML results
            results = soup.find_all('a', {'class': 'result__url'})

            for result in results:
                href = result.get('href', '')
                if href and self._is_company_url(href):
                    clean_url = self._clean_search_url(href)
                    if clean_url and self._is_valid_url(clean_url):
                        print(f"Found URL via DuckDuckGo: {clean_url}")
                        return clean_url

            return None

        except Exception as e:
            print(f"Error searching DuckDuckGo: {e}")
            return None

    def _search_bing(self) -> Optional[str]:
        """
        Search using Bing
        """
        try:
            search_query = f"{self.company} official website"
            search_url = f"https://www.bing.com/search?q={search_query.replace(' ', '+')}"

            response = self.session.get(search_url)
            if response.status_code != 200:
                return None

            soup = BeautifulSoup(response.content, 'html.parser')

            # Bing search results
            results = soup.find_all('h2')

            for result in results:
                link = result.find('a', href=True)
                if link:
                    href = link.get('href', '')
                    if href and self._is_company_url(href):
                        if self._is_valid_url(href):
                            print(f"Found URL via Bing: {href}")
                            return href

            return None

        except Exception as e:
            print(f"Error searching Bing: {e}")
            return None

    def _try_company_apis(self) -> Optional[str]:
        """
        Try to find company info using public APIs (if available)
        This is a placeholder for services like Clearbit, Hunter.io, etc.
        """
        # You could integrate with APIs like:
        # - Clearbit Company API
        # - Hunter.io Domain Search
        # - LinkedIn Company Search
        # For now, we'll return None
        return None

    def _is_company_url(self, url: str) -> bool:
        """
        Check if URL is likely to be a company website
        """
        excluded_domains = [
            'google.com', 'bing.com', 'duckduckgo.com',
            'wikipedia.org', 'linkedin.com', 'facebook.com',
            'twitter.com', 'youtube.com', 'instagram.com',
            'crunchbase.com', 'bloomberg.com', 'reuters.com',
            'forbes.com', 'techcrunch.com', 'amazon.com',
            'ebay.com', 'yelp.com', 'glassdoor.com'
        ]

        for domain in excluded_domains:
            if domain in url.lower():
                return False

        return True

    def _clean_search_url(self, url: str) -> str:
        """
        Clean URL from search engine redirects
        """
        # Handle DuckDuckGo redirects
        if 'duckduckgo.com' in url:
            # DuckDuckGo sometimes uses //duckduckgo.com/l/?uddg=
            if '/l/?uddg=' in url:
                return url.split('/l/?uddg=')[1].split('&')[0]

        return url

    def _is_valid_url(self, url: str) -> bool:
        """
        Check if the URL is valid and accessible
        """
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return False

            response = self.session.head(url, timeout=10, allow_redirects=True)
            return response.status_code == 200
        except:
            return False

    def scrape_website_content(self, url: str) -> Dict[str, str]:
        """
        Scrape content from the company's website
        """
        try:
            response = self.session.get(url, timeout=15)
            if response.status_code != 200:
                return {}

            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()

            content = {
                'title': self._get_page_title(soup),
                'description': self._get_meta_description(soup),
                'main_content': self._extract_main_content(soup),
                'about_info': self._find_about_section(soup, url),
                'contact_info': self._extract_contact_info(soup),
                'services': self._extract_services(soup)
            }

            return content

        except Exception as e:
            print(f"Error scraping website content: {e}")
            return {}

    def _get_page_title(self, soup: BeautifulSoup) -> str:
        """Extract page title"""
        title_tag = soup.find('title')
        return title_tag.get_text().strip() if title_tag else ""

    def _get_meta_description(self, soup: BeautifulSoup) -> str:
        """Extract meta description"""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            return meta_desc.get('content', '').strip()
        return ""

    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """Extract main content from the page"""
        # Look for main content areas
        main_selectors = ['main', '[role="main"]',
                          '.main-content', '#main', '.content']

        for selector in main_selectors:
            main_content = soup.select_one(selector)
            if main_content:
                return self._clean_text(main_content.get_text())

        # Fallback to body content
        body = soup.find('body')
        if body:
            return self._clean_text(body.get_text())

        return ""

    def _find_about_section(self, soup: BeautifulSoup, base_url: str) -> str:
        """Find and extract about section information"""
        about_keywords = ['about', 'company',
                          'who we are', 'our story', 'mission']

        # First, try to find about section on current page
        for keyword in about_keywords:
            about_section = soup.find(text=re.compile(keyword, re.IGNORECASE))
            if about_section:
                parent = about_section.find_parent()
                if parent:
                    return self._clean_text(parent.get_text())

        # Try to find about page link
        about_links = soup.find_all('a', href=True)
        for link in about_links:
            link_text = link.get_text().lower()
            if any(keyword in link_text for keyword in about_keywords):
                about_url = urljoin(base_url, link['href'])
                try:
                    about_response = self.session.get(about_url, timeout=10)
                    if about_response.status_code == 200:
                        about_soup = BeautifulSoup(
                            about_response.content, 'html.parser')
                        # Limit length
                        return self._extract_main_content(about_soup)[:1000]
                except:
                    continue

        return ""

    def _extract_contact_info(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract contact information"""
        contact_info = {}

        # Look for email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, soup.get_text())
        if emails:
            contact_info['email'] = emails[0]

        # Look for phone numbers
        phone_pattern = r'(\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
        phones = re.findall(phone_pattern, soup.get_text())
        if phones:
            contact_info['phone'] = ''.join(phones[0])

        return contact_info

    def _extract_services(self, soup: BeautifulSoup) -> List[str]:
        """Extract services or products offered"""
        services = []
        service_keywords = ['services', 'products', 'solutions', 'offerings']

        for keyword in service_keywords:
            service_section = soup.find(
                text=re.compile(keyword, re.IGNORECASE))
            if service_section:
                parent = service_section.find_parent()
                if parent:
                    # Look for list items or similar structures
                    items = parent.find_all(['li', 'div', 'p'])
                    for item in items[:5]:  # Limit to first 5 items
                        text = self._clean_text(item.get_text())
                        if text and len(text) < 100:  # Reasonable length
                            services.append(text)
                    break

        return services

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def summarize_content(self, content: Dict[str, str]) -> str:
        """
        Create a summary of the scraped content
        """
        summary_parts = []

        if content.get('title'):
            summary_parts.append(f"Company: {content['title']}")

        if content.get('description'):
            summary_parts.append(f"Description: {content['description']}")

        if content.get('about_info'):
            about_text = content['about_info'][:300] + "..." if len(
                content['about_info']) > 300 else content['about_info']
            summary_parts.append(f"About: {about_text}")

        if content.get('services'):
            services_text = ", ".join(
                content['services'][:3])  # First 3 services
            summary_parts.append(f"Services/Products: {services_text}")

        if content.get('contact_info'):
            contact_parts = []
            if content['contact_info'].get('email'):
                contact_parts.append(
                    f"Email: {content['contact_info']['email']}")
            if content['contact_info'].get('phone'):
                contact_parts.append(
                    f"Phone: {content['contact_info']['phone']}")
            if contact_parts:
                summary_parts.append(f"Contact: {', '.join(contact_parts)}")

        return "\n\n".join(summary_parts) if summary_parts else "No information could be extracted."

    def get_info(self) -> Dict[str, any]:
        """
        Main method to get company information
        Returns a dictionary with URL, content, and summary
        """
        print(f"Searching for {self.company}...")

        # Find company URL
        company_url = self.find_company_url()
        if not company_url:
            return {
                'success': False,
                'error': f"Could not find official website for {self.company}",
                'company': self.company
            }

        print(f"Found URL: {company_url}")
        print("Scraping website content...")

        # Scrape website content
        content = self.scrape_website_content(company_url)
        if not content:
            return {
                'success': False,
                'error': f"Could not scrape content from {company_url}",
                'company': self.company,
                'url': company_url
            }

        # Generate summary
        summary = self.summarize_content(content)

        return {
            'success': True,
            'company': self.company,
            'url': company_url,
            'content': content,
            'summary': summary
        }

# Example usage
# if __name__ == "__main__":
#     scraper = WebScraper("Telia")
#     result = scraper.get_info()

#     if result['success']:
#         print(f"\n=== {result['company']} Information ===")
#         print(f"Website: {result['url']}")
#         print(f"\nSummary:\n{result['summary']}")
#         print(f"\Content:\n{result['content']}")
#     else:
#         print(f"Error: {result['error']}")

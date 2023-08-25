from typing import Dict, List
from zenrows import ZenRowsClient

ZENROWS = ZenRowsClient(api_key="YOUR_ZENROWS_API_KEY")


async def scrape_profile_data(account: str) -> Dict:
    """
    Scrape profile data for a single Twitter account
    """
    result = await ZENROWS.scrape(f"https://twitter.com/{account}")
    return result.scrape_result


async def scrape_accounts(accounts: List[str]) -> List[Dict]:
    """
    Scrape profile data for multiple Twitter accounts
    """
    results = []
    for account in accounts:
        profile_data = await scrape_profile_data(account)
        results.append({account: profile_data})
    return results


if __name__ == "__main__":
    import asyncio

    accounts_to_scrape = ["Scrapfly_dev", "OpenAI", "Twitter"]
    scraped_data = asyncio.run(scrape_accounts(accounts_to_scrape))
    print(scraped_data)
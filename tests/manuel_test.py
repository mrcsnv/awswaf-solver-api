import asyncio
import sys
from datetime import timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from wreq import Client, Emulation
from wreq.redirect import Policy
from AWSSolver.Solver import AwsSolver

URL = "https://checkout.viagogo.com/secure/buy/checkout?ID=87a22d6b-fe1e-4cba-8c63-1681625fde8c%7c13167882629%7c4%7c0"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
HEADERS = {
            "connection": "keep-alive",
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'upgrade-insecure-requests': '1',
            'user-agent': f'{USER_AGENT}',
        }
async def main():

    client = Client(emulation=Emulation.Chrome143, cookie_store=True, redirect=Policy.limited(5))
    response = await client.get(f"{URL}", timeout=timedelta(seconds=10), headers=HEADERS)
    text = await response.text()
    print(f"[+] Got HTML ({len(text)} bytes)")

    solver = AwsSolver(user_agent=USER_AGENT, domain="www.viagogo.com")
    token = await solver.solve(text)

    print(f"[+] Token: {token}")
    cookies = {
        "aws-waf-token": token
    }
    response = await client.get(f"{URL}", timeout=timedelta(seconds=10), headers=HEADERS, cookies=cookies)
    text = await response.text()
    print(f"[+] Status: {response.status}")
    print(f"[+] Response: {text[:500]}")

if __name__ == "__main__":
    asyncio.run(main())

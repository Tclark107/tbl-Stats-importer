import os
import requests
from dotenv import load_dotenv

load_dotenv()

SHOP = os.getenv("SHOPIFY_SHOP")
CLIENT_ID = os.getenv("SHOPIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SHOPIFY_CLIENT_SECRET")

if not all([SHOP, CLIENT_ID, CLIENT_SECRET]):
    raise RuntimeError("Missing Shopify credentials in .env")


# --------------------------------------------------
# Authenticate with Shopify
# --------------------------------------------------

token_response = requests.post(
    f"https://{SHOP}/admin/oauth/access_token",
    json={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
    },
    timeout=30,
)

token_response.raise_for_status()

access_token = token_response.json()["access_token"]

print("✓ Successfully authenticated with Shopify")


# --------------------------------------------------
# Query Player metaobjects
# --------------------------------------------------

query = """
query {
  shop {
    name
    myshopifyDomain
  }
  metaobjects(type: "competition", first: 3) {
    nodes {
      id
      handle
      displayName
    }
  }
}
"""



# ------------------------------------------------yy
# Send GraphQL request
# --------------------------------------------------

response = requests.post(
    f"https://{SHOP}/admin/api/2026-07/graphql.json",
    headers={
        "X-Shopify-Access-Token": access_token,
        "Content-Type": "application/json",
    },
    json={"query": query},
    timeout=30,
)

response.raise_for_status()

data = response.json()
import json
print(json.dumps(data, indent=2))


# --------------------------------------------------
# Check for GraphQL errors
# --------------------------------------------------

# --------------------------------------------------
# Check for GraphQL errors
# --------------------------------------------------
if data.get("errors"):
    print("GraphQL errors:")
    print(data["errors"])
else:
    print("✓ Successfully connected to Shopify Admin API\n")

    definitions = data["data"]["metaobjectDefinitions"]["nodes"]

    for definition in definitions:
        print(f"\n{definition['name']} ({definition['type']})")
        print("-" * 50)

        for field in definition["fieldDefinitions"]:
            print(
                f"{field['key']}: "
                f"{field['type']['name']}"
            )

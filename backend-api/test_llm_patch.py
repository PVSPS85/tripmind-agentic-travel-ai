import re

err_msg = 'Rate limit reached for model `llama-3.1-8b-instant` in organization `org_xyz` service tier `on_demand` on tokens per minute (TPM): Limit 6000, Used 4334, Requested 4864. Please try again in 31.98s. Need more tokens?'

match = re.search(r"try again in ([\d\.]+)s", err_msg)
if match:
    print(f"Sleep for {float(match.group(1)) + 1} seconds")

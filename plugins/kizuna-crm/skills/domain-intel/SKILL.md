---
name: kizuna-crm/domain-intel
description: "Passive domain reconnaissance using Python stdlib. Subdomain discovery, SSL cert inspection, WHOIS lookups, DNS records, domain availability checks, and bulk multi-domain analysis. No API keys required."
license: MIT
---

# Domain Intelligence

Passive domain intelligence using only Python stdlib and public data sources.
Zero dependencies. Zero API keys. Works out of the box.

## Capabilities

- **WHOIS lookup** — registrant, registrar, dates, nameservers
- **DNS records** — A, AAAA, MX, NS, TXT, CNAME, SOA
- **SSL certificate inspection** — issuer, expiry, SAN list, cipher info
- **Subdomain discovery** — via certificate transparency logs (crt.sh)
- **Domain availability** — check if a domain is registered
- **Bulk analysis** — run all checks across multiple domains

## Usage

```bash
# Single domain WHOIS
whois example.com

# DNS records
dig example.com ANY

# SSL cert inspection
openssl s_client -connect example.com:443 -servername example.com </dev/null 2>/dev/null | openssl x509 -noout -text

# Subdomain discovery via crt.sh
curl -s "https://crt.sh/?q=%25.example.com&output=json" | python3 -c "import sys,json; [print(d['name_value']) for d in json.load(sys.stdin)]" | sort -u
```

## Rules

- **Rate limit** — crt.sh has no official rate limit but be respectful. Space queries by 2+ seconds for bulk scans.
- **No intrusive scanning** — this is passive intel from public sources. Don't port scan, don't brute force subdomains.
- **WHOIS may be redacted** — GDPR means many WHOIS records hide registrant info. That's fine — dates and nameservers are still useful.
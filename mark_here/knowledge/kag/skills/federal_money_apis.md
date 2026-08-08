# Skill: Federal free money APIs

**When:** Looking for government money opportunities (grants, contracts, awards, rules, datasets).

## Top 5 (always use official .gov)

| # | Source | Chat | Key? |
|---|--------|------|------|
| 1 | Grants.gov search2 | `grants: <keyword>` | No |
| 2 | SAM.gov opportunities | `sam: <NAICS>` | Free key |
| 3 | USAspending | `agency map` | No |
| 4 | FAR / eCFR / GSA XML | `far: 19` | No |
| 5 | Data.gov CKAN | `data.gov: <topic>` | No |

Card: **money apis** · Config: `config/integrations/federal_money_apis.json`

## Architecture

Pull free APIs → write products under `outputs/govcon/` → rank with Army/Second Brain.  
**Not** AI systems. LLM is optional on top.

## Free-will

Research only. No grant applications, bids, SAM filings, or spend from chat.

## Use-case routing

- Grants/funding → Grants.gov  
- Contracts → SAM.gov  
- Who got paid → USAspending  
- Rules/set-asides → FAR  
- Dataset signals → Data.gov  

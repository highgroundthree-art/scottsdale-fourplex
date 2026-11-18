# Scottsdale Fourplex

Project site for a fourplex development, written for investors, developers and municipal reviewers. Plans, drawing sets and field/office communication (RFIs, submittals) live here.

## Structure
| Path | Purpose |
|---|---|
| `index.html` | The public project site |
| `data/sheets.json` | Drawing sheet index (shown on the site) |
| `data/rfis.json` | RFI log (shown on the site) |
| `drawings/` | Elevations, site plans and floor plans for Models 1, 2 and 3 |
| `specs/` | Project manual and schedules |
| `rfis/` | Files that support RFIs |
| `submittals/` | Submittal packages |
| `business/` | Investor / financial summary |

## Adding a drawing sheet
Add an object to `data/sheets.json`:
```json
{ "sheet": "A-101.1", "title": "Model 1, Ground Floor Plan", "plan": "1", "revision": "0", "date": "2026-11-17", "status": "Draft", "file": "drawings/floor-plans/model1-ground.svg" }
```

## Adding an RFI
Add an object to `data/rfis.json`:
```json
{ "number": "RFI-001", "subject": "Wall type at unit demising wall", "from": "Field", "to": "Office", "date": "2026-11-17", "status": "Open", "response": "" }
```

## Who can change this
Anyone can read a public repo, but only people you add under Settings, Collaborators can change it. Others can only fork or suggest changes, which you must approve.

Working draft. Not for construction.

#!/usr/bin/env python3
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "BorderDays_web"
BASE = "https://ly-helloworld.github.io/Privacy/BorderDays_web/"
APP = "https://apps.apple.com/app/id6803141319"
ICON = "https://is1-ssl.mzstatic.com/image/thumb/Purple211/v4/54/67/e8/5467e8bc-a70b-cb91-0515-baece0413071/AppIcon-1x_U007emarketing-0-6-0-85-220-0.png/512x512bb.jpg"

PAGES = [
    {
        "route": "how-does-schengen-90-180-rule-work",
        "title": "How the Schengen 90/180-Day Rule Works | StayCount",
        "description": "Understand the rolling Schengen 90 days in any 180-day period rule, with a simple example, record checklist, and official source.",
        "h1": "How does the Schengen 90/180-day rule work?",
        "answer": "For most short stays, you may spend no more than 90 days in the Schengen Area during any rolling 180-day period. It is not a fixed block that resets on a calendar date: on each day of a stay, look back 179 more days and count all qualifying days in that window. Entry and exit days normally count.",
        "difficulty": "Several trips can overlap the same rolling window, while older days leave it one by one. A calendar-month total can therefore look safe even when the actual rolling total is not.",
        "example": "Fictional simplified example: a traveler records 30 days in January, 30 in March, and 30 in May. That uses 90 days while all three stays remain inside the relevant 180-day look-back. A new June day may exceed the allowance; a January day leaving the window later does not create a universal reset date.",
        "checklist": ["Record every qualifying Schengen entry and exit date.", "Count entry and exit days unless an official exception applies.", "Separate time covered by a long-stay visa or residence permit for qualified review.", "Recheck the rolling window for every planned day, not only the arrival date."],
        "mistakes": ["Treating 1 January, visa issuance, or departure as an automatic reset.", "Counting nights instead of calendar days.", "Leaving out a short trip to another Schengen country.", "Assuming a calculator replaces the conditions on a visa or residence document."],
        "help": "StayCount turns the stays you enter into a visible rolling calculation, showing days used and contributing dates. You can inspect the explanation instead of relying on one unexplained number.",
        "source_url": "https://home-affairs.ec.europa.eu/policies/schengen/border-crossing/short-stay-calculator_en",
        "source_label": "European Commission short-stay calculator and 90/180 guidance",
        "faqs": [("Does the 180-day period reset after I leave?", "No. It moves forward one day at a time, so each day has its own 180-day look-back."), ("Do arrival and departure days count?", "The European Commission calculator instructions treat entry and exit as days of stay for ordinary short-stay counting."), ("Does the rule apply to every traveler?", "No. Nationality, visa type, residence status, bilateral arrangements, and personal circumstances can change what applies. Check official guidance."), ("Can StayCount decide whether I may enter?", "No. It organizes entered facts and planning calculations; border and immigration authorities make official decisions.")],
    },
    {
        "route": "when-can-i-re-enter-schengen",
        "title": "When Can I Re-enter Schengen? Plan from Your Stays | StayCount",
        "description": "Learn how prior stays affect a possible Schengen re-entry date and why allowance can return one day at a time.",
        "h1": "When can I re-enter the Schengen Area?",
        "answer": "A possible re-entry date depends on every qualifying stay in the 180 days before each proposed day. There is no single answer based only on your last exit. As older used days fall outside the rolling window, allowance may return gradually; the full proposed stay still needs to remain within the limit.",
        "difficulty": "The first day that appears available is not necessarily enough for the whole planned trip. Multiple earlier trips can expire from the look-back on different dates.",
        "example": "Fictional simplified example: a traveler has already used 90 qualifying days across several stays. One old day leaves the rolling window on 10 September, but that may create room for only one new day. A ten-day trip needs each of its ten days checked against its own window.",
        "checklist": ["Collect all qualifying stays from at least the previous 180 days.", "Choose a proposed arrival and departure, not arrival alone.", "Check how many old days leave the window during the planned stay.", "Confirm visa validity and personal conditions separately."],
        "mistakes": ["Adding 90 days to the last departure and calling that the answer.", "Checking only the arrival date.", "Forgetting another Schengen trip in the same look-back.", "Confusing remaining days with permission to enter."],
        "help": "StayCount uses your entered stays to estimate remaining allowance and an earliest re-entry date, with contributing dates visible for review. Future-stay simulation checks the proposed span rather than one isolated date.",
        "source_url": "https://home-affairs.ec.europa.eu/policies/schengen/border-crossing/short-stay-calculator_en",
        "source_label": "European Commission short-stay calculator planning mode",
        "faqs": [("Is re-entry always possible after 90 days outside?", "That shortcut may work in a simple continuous-stay scenario, but multiple trips and personal status require the actual rolling calculation."), ("Why does allowance return gradually?", "Each past day stops counting only when it falls outside the new day's 180-day window."), ("What if my visa allows fewer days?", "Follow the shorter authorized stay shown on the visa and official instructions; the general 90/180 ceiling does not extend it."), ("Is an earliest date a guarantee?", "No. It is a planning result based on entered facts, not an entry authorization.")],
    },
    {
        "route": "check-a-future-schengen-trip",
        "title": "Check a Future Schengen Trip Before Booking | StayCount",
        "description": "Plan a future Schengen stay against your recorded travel dates and understand the latest safe-exit estimate.",
        "h1": "How can I check a future Schengen trip before booking?",
        "answer": "Add the proposed arrival and departure to a complete record of earlier qualifying stays, then evaluate every day of the proposed trip against its rolling 180-day window. A future trip can become safer as old days expire, or fail near the end even when arrival looks valid.",
        "difficulty": "Static subtraction hides the fact that the window moves during the trip. Booking changes and incomplete history can also shift the latest day that remains within the calculation.",
        "example": "Fictional simplified example: a proposed 14-day trip begins with 12 days of apparent allowance. During the trip, four older days leave the rolling window, so the full span may fit. The exact outcome depends on the actual dates and must be recomputed, not inferred from 12 alone.",
        "checklist": ["Enter exact prior entry and exit dates.", "Simulate both the proposed arrival and departure.", "Review the dates contributing to the tightest point.", "Keep flexible booking terms until official conditions are confirmed."],
        "mistakes": ["Comparing trip length only with today's remaining-days number.", "Testing arrival but not the final day.", "Deleting old stays that still affect the window.", "Treating a planning result as legal advice."],
        "help": "StayCount includes a future-stay simulation in the Schengen workspace. It estimates whether the entered span fits and explains a latest safe-exit result from the same local ledger.",
        "source_url": "https://home-affairs.ec.europa.eu/policies/schengen/border-crossing/short-stay-calculator_en",
        "source_label": "European Commission short-stay calculator check and planning modes",
        "faqs": [("Should I check before or after booking?", "Check before committing, then check again if dates or earlier travel change."), ("Can older days expire during my future trip?", "Yes. The rolling window advances each day, so some old days can stop contributing during the trip."), ("What records does the simulation use?", "StayCount uses the manual stays you enter; missing or incorrect stays produce a different result."), ("Does simulation account for every visa exception?", "No. It is a planning calculation, not a complete assessment of visa or residence status.")],
    },
    {
        "route": "track-tax-residency-days-across-countries",
        "title": "Track Tax-Residency Days Across Countries | StayCount",
        "description": "Organize cross-border presence dates and supporting records while keeping US and UK rule workspaces separate.",
        "h1": "How can I track tax-residency days across countries?",
        "answer": "Keep one chronological presence ledger, then evaluate each jurisdiction in its own rule workspace. A travel date can support several reviews, but the legal tests are not interchangeable: calendar years, tax years, excluded days, workdays, ties, and treaty questions can require different facts.",
        "difficulty": "Spreadsheets, calendar entries, tickets, and notes drift apart. Reusing one generic day total can erase the distinctions that a US or UK review needs.",
        "example": "Fictional simplified example: Maya records a UK stay and a US stay in one ledger. The US workspace groups presence by calendar year for its weighted calculation; the UK SRT workspace asks for UK tax-year facts and ties. The same travel history feeds both without pretending the rules are the same.",
        "checklist": ["Record country, arrival, and departure for every stay.", "Retain notes or selected evidence for corrections.", "Label exclusions and exceptional facts instead of silently deleting dates.", "Review each jurisdiction's official rules and year boundaries separately."],
        "mistakes": ["Using one worldwide threshold for every country.", "Mixing calendar-year and UK tax-year totals.", "Changing the ledger to force a desired rule result.", "Assuming day count alone resolves treaties, ties, domicile, or residence status."],
        "help": "StayCount keeps a manual presence ledger on device and feeds separate Schengen, US SPT, UK Visitor, and UK SRT workspaces. Notes and Pro evidence attachments help preserve why an entry was recorded.",
        "source_url": "https://www.gov.uk/government/collections/uk-tax-residence-guidance",
        "source_label": "HMRC UK tax residence guidance collection",
        "faqs": [("Can one ledger cover several countries?", "Yes for organizing travel facts, but each country's rules still require their own inputs and interpretation."), ("Should excluded days be deleted?", "Usually it is clearer to preserve the presence record and identify the potential exclusion for qualified review."), ("Is a spreadsheet enough?", "It can be, if maintained carefully. A dedicated ledger mainly reduces duplicated dates and keeps explanations beside rule-specific inputs."), ("Does StayCount determine tax residence?", "It provides planning workspaces based on entered facts, not professional tax advice or an official determination.")],
    },
    {
        "route": "us-substantial-presence-test-day-tracker",
        "title": "US Substantial Presence Test Day Tracker | StayCount",
        "description": "Track current-year US days, weighted prior-year days, the 31-day minimum, and possible excluded spans.",
        "h1": "How do I track days for the US Substantial Presence Test?",
        "answer": "For the IRS Substantial Presence Test, first check at least 31 days of US presence in the current year. Then total all countable current-year days, one-third of the preceding year's countable days, and one-sixth of the second preceding year's countable days. The weighted total reaches the test at 183, subject to exclusions and exceptions.",
        "difficulty": "The 183 figure is weighted across three calendar years, not a simple three-year sum. Some physical-presence days may be excluded, and meeting the arithmetic does not answer every exception or treaty issue.",
        "example": "Fictional simplified arithmetic: 120 countable days in each of three years gives 120 + 40 + 20 = 180 weighted days. The 31-day current-year minimum is met, but the weighted total is below 183. This mirrors the IRS teaching example; personal exclusions still need review.",
        "checklist": ["Separate countable presence by calendar year.", "Confirm the current year has at least 31 countable days.", "Apply weights of 1, one-third, and one-sixth.", "Record possible transit, crew, medical, exempt-individual, or commuting exclusions for review."],
        "mistakes": ["Adding all three years at full weight.", "Ignoring the separate 31-day current-year minimum.", "Automatically excluding a day without checking IRS definitions.", "Treating the arithmetic as the end of a treaty or closer-connection analysis."],
        "help": "StayCount's US workspace separates current-year days, prior-year weighted rows, the 31-day minimum, and excluded spans. Its explanation shows how the entered facts contribute.",
        "source_url": "https://www.irs.gov/individuals/international-taxpayers/substantial-presence-test",
        "source_label": "IRS Substantial Presence Test guidance",
        "faqs": [("Are all days in the previous two years counted?", "No. Countable days are weighted at one-third for the first preceding year and one-sixth for the second."), ("Is 183 days in the current year required?", "No. The standard formula can reach 183 using weighted prior-year days, while also requiring at least 31 current-year days."), ("Does any part of a day count?", "The IRS generally treats physical presence at any time during a day as a day, subject to listed exceptions."), ("What happens if the formula reaches 183?", "Other exceptions, elections, treaties, and filing obligations may still matter. Seek qualified advice.")],
    },
    {
        "route": "uk-statutory-residence-test-day-tracker",
        "title": "UK Statutory Residence Test Day Tracker | StayCount",
        "description": "Record UK tax-year days, ties, workdays, transit, homes, and exceptional circumstances for SRT review.",
        "h1": "What should I record for the UK Statutory Residence Test?",
        "answer": "Record more than a UK day total. The Statutory Residence Test considers the UK tax year, automatic overseas tests, automatic UK tests, and—when needed—the sufficient ties test. Prior residence, homes, work patterns, family ties, transit, and exceptional circumstances can affect the analysis.",
        "difficulty": "The result follows an ordered set of tests. A threshold that matters in one situation may not decide another, and the relevant day limit can depend on prior residence and ties.",
        "example": "Fictional simplified workflow: Sam records 80 UK days, prior UK residence, workdays over three hours, home availability, and family ties for one tax year. Eighty alone does not settle the result; the automatic tests and sufficient ties table must be considered in order.",
        "checklist": ["Use the UK tax year from 6 April to 5 April.", "Record arrival/departure and potential midnight/transit treatment.", "Record prior residence, homes, family and accommodation ties.", "Track relevant workdays and possible exceptional-circumstance days."],
        "mistakes": ["Using only a 183-day threshold.", "Counting by calendar year instead of UK tax year.", "Ignoring prior residence or ties.", "Removing exceptional days without checking HMRC's conditions and limits."],
        "help": "StayCount keeps UK Visitor and UK SRT as separate workspaces. The SRT workspace records tax-year facts, ties, workdays, transit, and exceptional circumstances, then explains the entered-result path.",
        "source_url": "https://www.gov.uk/government/publications/rdr3-statutory-residence-test-srt/guidance-note-for-statutory-residence-test-srt-rdr3",
        "source_label": "HMRC RDR3 Statutory Residence Test notes",
        "faqs": [("Is the SRT just a 183-day test?", "No. Spending 183 days can satisfy an automatic UK test, but the full SRT also contains automatic overseas tests and sufficient ties rules."), ("Why record workdays?", "Some automatic tests and definitions use days with more than three hours of work."), ("Do transit days always count?", "Special rules can apply. Preserve the facts and check current HMRC guidance rather than assuming."), ("Are exceptional circumstances automatic exclusions?", "No. HMRC conditions and limits apply, so record the circumstances for careful review.")],
    },
    {
        "route": "private-offline-travel-day-tracker",
        "title": "Private Offline Travel-Day Tracker for iPhone | StayCount",
        "description": "Keep a manual travel-day ledger on your iPhone without an account or continuous location tracking.",
        "h1": "Is there a private travel-day tracker without an account or location tracking?",
        "answer": "StayCount is a manual, local-first iPhone travel-day ledger. Its core records and calculations work on device without a required account or location permission. You choose the dates, notes, and evidence files to add; optional App Lock and user-initiated password-encrypted backup add control.",
        "difficulty": "Travel history is sensitive. Automatic location collection can feel disproportionate, while an ordinary spreadsheet can be easy to overwrite, duplicate, or separate from supporting notes.",
        "example": "Fictional simplified workflow: Lee adds a Spain stay manually, attaches a selected ticket in Pro, reviews the Schengen explanation offline, enables App Lock, and later exports a password-encrypted backup. StayCount does not infer an unrecorded trip from location history.",
        "checklist": ["Enter only the travel facts you want in the ledger.", "Review dates after itinerary changes.", "Use App Lock when device-sharing risk warrants it.", "Create and protect an encrypted backup before changing devices or deleting data."],
        "mistakes": ["Assuming no account means backups happen automatically.", "Expecting the app to detect missing trips from GPS.", "Attaching more sensitive evidence than needed.", "Forgetting the backup password or storing it beside the backup."],
        "help": "StayCount stores its ledger locally, performs core calculations offline, requests no location permission, and requires no account. Selected attachments and password-encrypted export/restore are initiated by you.",
        "source_url": "../../BorderDays/privacy.html",
        "source_label": "StayCount Privacy Policy",
        "faqs": [("Does StayCount track my location?", "No. It has no location-tracking workflow; you enter stays manually."), ("Do I need an account?", "No account is required for the app's local ledger and calculations."), ("Is backup automatic?", "No. Backup export and restore are user-initiated and password encrypted."), ("Can I attach evidence?", "StayCount Pro lets you select supporting files. Add only what you need and manage those files as sensitive records.")],
    },
]


def ld_json(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def head(title, description, canonical, kind="website"):
    return f'''<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title><meta name="description" content="{html.escape(description, quote=True)}">
  <link rel="canonical" href="{canonical}"><meta name="apple-itunes-app" content="app-id=6803141319">
  <meta property="og:type" content="{kind}"><meta property="og:title" content="{html.escape(title, quote=True)}"><meta property="og:description" content="{html.escape(description, quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{ICON}">
  <meta name="twitter:card" content="summary"><meta name="twitter:title" content="{html.escape(title, quote=True)}"><meta name="twitter:description" content="{html.escape(description, quote=True)}"><meta name="twitter:image" content="{ICON}">'''


def header(prefix=""):
    return f'''<header class="site-header wrap"><nav aria-label="Primary"><a class="brand" href="{prefix or './'}">StayCount</a><a href="{prefix}how-does-schengen-90-180-rule-work/">Schengen guide</a><a href="{prefix}track-tax-residency-days-across-countries/">Tax presence</a><a href="{prefix}private-offline-travel-day-tracker/">Privacy</a><a href="{APP}">Download</a></nav></header>'''


def footer(prefix="../"):
    return f'''<footer class="site-footer wrap"><nav aria-label="Legal and support"><a href="{prefix}BorderDays/privacy.html">Privacy Policy</a><a href="{prefix}BorderDays/terms.html">Terms of Use</a><a href="{prefix}BorderDays/support.html">Support</a></nav><p>StayCount: Schengen &amp; Tax · Bundle ID com.ly.find.borderdays · App Store ID 6803141319</p><p>© 2026 StayCount Team</p></footer>'''


def write(route, text):
    folder = SITE / route if route else SITE
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "index.html").write_text(text, encoding="utf-8")


def make_home():
    routes = {p["route"]: p["h1"] for p in PAGES}
    schemas = {"@context":"https://schema.org","@type":"SoftwareApplication","name":"StayCount: Schengen & Tax","applicationCategory":"TravelApplication","operatingSystem":"iOS","identifier":"com.ly.find.borderdays","url":BASE,"downloadUrl":APP,"image":ICON,"description":"A private, explainable travel-day ledger for Schengen, US, and UK presence rules."}
    cards = "".join(f'<article class="card"><h3>{html.escape(label)}</h3><p>{copy}</p><a href="{route}/">Read the guide</a></article>' for route,label,copy in [
        ("how-does-schengen-90-180-rule-work",routes["how-does-schengen-90-180-rule-work"],"Understand the rolling window and contributing days."),
        ("when-can-i-re-enter-schengen",routes["when-can-i-re-enter-schengen"],"Estimate when allowance may return from your entered stays."),
        ("check-a-future-schengen-trip",routes["check-a-future-schengen-trip"],"Simulate a proposed stay before making firm plans."),
        ("track-tax-residency-days-across-countries",routes["track-tax-residency-days-across-countries"],"Keep one ledger while separating jurisdiction rules."),
        ("us-substantial-presence-test-day-tracker",routes["us-substantial-presence-test-day-tracker"],"Review current and weighted prior-year US days."),
        ("uk-statutory-residence-test-day-tracker",routes["uk-statutory-residence-test-day-tracker"],"Record tax-year facts, ties, workdays, and exceptions."),
        ("private-offline-travel-day-tracker",routes["private-offline-travel-day-tracker"],"Use a local ledger without account or location tracking."),
    ])
    shots = "".join(f'<figure><img class="app-screenshot" src="assets/{name}" width="1260" height="2736" alt="{alt}"></figure>' for name,alt in [("01-know-your-days.png","StayCount overview showing days used and left"),("02-plan-next-stay.png","StayCount future Schengen stay planner"),("03-see-calculation.png","StayCount calculation explanation")])
    body = f'''<!doctype html><html lang="en"><head>{head("StayCount: Schengen &amp; Tax — Private Travel-Day Ledger","Plan Schengen trips and organize US and UK presence days with a private, explainable iPhone ledger. No account or location permission required.",BASE)}<link rel="stylesheet" href="assets/site.css"><script type="application/ld+json">{ld_json(schemas)}</script></head><body>{header()}
<main><section class="hero wrap"><div class="hero-grid"><div><img class="app-icon" src="{ICON}" width="96" height="96" alt="StayCount app icon"><p class="eyebrow">Private travel-day planning</p><h1>StayCount: Schengen &amp; Tax</h1><p class="lead">A private, explainable travel-day ledger for Schengen, US, and UK presence rules.</p><div class="cta-row"><a class="cta" href="{APP}">Download on the App Store</a></div><p class="trust"><strong>No account.</strong> <strong>No location permission.</strong> Records stay on your device unless you choose to export a backup.</p></div><img class="hero-shot" src="assets/01-know-your-days.png" width="1260" height="2736" alt="StayCount overview showing travel days used and left"></div></section>
<section class="wrap"><h2>Answer the practical questions before they become urgent</h2><div class="card-grid">{cards}</div></section>
<section class="wrap"><h2>See the record, plan, and explanation</h2><div class="screenshot-grid">{shots}</div></section>
<section class="wrap"><h2>Four separate workspaces</h2><div class="card-grid"><article class="card"><h3>Schengen 90/180</h3><p>Free workspace for rolling days used, days left, contributing dates, earliest re-entry, and a future-stay simulation.</p></article><article class="card"><h3>US Substantial Presence</h3><p>StayCount Pro separates current-year days, weighted prior years, the 31-day minimum, and excluded spans.</p></article><article class="card"><h3>UK Visitor</h3><p>StayCount Pro keeps visitor inputs and explanations separate from tax residence.</p></article><article class="card"><h3>UK Statutory Residence Test</h3><p>StayCount Pro records tax-year facts, ties, workdays, transit, and exceptional circumstances.</p></article></div></section>
<section class="wrap"><div class="notice"><h2>Privacy and control</h2><p>Core calculations work offline. Travel stays are entered manually and stored on device. Optional App Lock protects access; Pro supports selected evidence attachments and user-initiated password-encrypted backup.</p></div></section>
<section class="wrap"><div class="notice warning"><h2>A planning tool, not a decision maker</h2><p>Results depend on the dates and facts you enter. StayCount does not provide immigration, legal, tax, or financial advice, guarantee an outcome, or represent a government authority.</p><div class="cta-row"><a class="cta" href="{APP}">Get StayCount on the App Store</a></div></div></section></main>{footer('../')} </body></html>'''
    write("", body)


def make_article(page):
    route = page["route"] + "/"
    canonical = BASE + route
    faq_entities = [{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in page["faqs"]]
    schemas = [{"@context":"https://schema.org","@type":"Article","headline":page["h1"],"description":page["description"],"mainEntityOfPage":canonical,"author":{"@type":"Organization","name":"StayCount Team"},"publisher":{"@type":"Organization","name":"StayCount Team"}}, {"@context":"https://schema.org","@type":"FAQPage","mainEntity":faq_entities}, {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"StayCount","item":BASE},{"@type":"ListItem","position":2,"name":page["h1"],"item":canonical}]}, {"@context":"https://schema.org","@type":"SoftwareApplication","name":"StayCount: Schengen & Tax","identifier":"com.ly.find.borderdays","downloadUrl":APP,"operatingSystem":"iOS"}]
    checklist = "".join(f"<li>{html.escape(x)}</li>" for x in page["checklist"])
    mistakes = "".join(f"<li>{html.escape(x)}</li>" for x in page["mistakes"])
    faqs = "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q,a in page["faqs"])
    related = "".join(f'<a href="../{p["route"]}/">{html.escape(p["h1"])}</a>' for p in PAGES if p["route"] != page["route"] and ("schengen" in p["route"]) == ("schengen" in page["route"]))[:2000]
    body = f'''<!doctype html><html lang="en"><head>{head(page["title"],page["description"],canonical,"article")}<link rel="stylesheet" href="../assets/site.css">{''.join(f'<script type="application/ld+json">{ld_json(s)}</script>' for s in schemas)}</head><body>{header('../')}
<main><section class="article-hero reading"><p class="eyebrow">StayCount practical guide</p><h1>{html.escape(page["h1"])}</h1><p class="lead" id="direct-answer">{html.escape(page["answer"])}</p><div class="cta-row"><a class="cta" href="{APP}">Download StayCount</a></div></section>
<div class="article-layout wrap"><article class="article-body"><section><h2>Why this is difficult</h2><p>{html.escape(page["difficulty"])}</p></section><section id="worked-example" class="example"><h2>Worked example</h2><p>{html.escape(page["example"])}</p></section><div class="cta-row"><a class="cta" href="{APP}">Keep these dates in StayCount</a></div><section id="checklist"><h2>What to record or check</h2><ul>{checklist}</ul></section><section id="mistakes"><h2>Common mistakes</h2><ul>{mistakes}</ul></section><section id="staycount"><h2>How StayCount helps</h2><p>{html.escape(page["help"])}</p></section><section id="official-references"><h2>Official reference</h2><p><a href="{page["source_url"]}">{html.escape(page["source_label"])}</a>. Read the current official material for definitions, exclusions, and personal conditions.</p></section><section id="faq"><h2>Frequently asked questions</h2>{faqs}</section><section id="boundary" class="notice warning"><h2>Important boundary</h2><p>StayCount results depend on the facts you enter. StayCount is a planning tool, not immigration, legal, tax, or financial advice, and it does not guarantee an official outcome.</p><div class="cta-row"><a class="cta" href="{APP}">Get StayCount on the App Store</a></div></section></article><aside class="toc" aria-label="On this page"><strong>On this page</strong><a href="#direct-answer">Direct answer</a><a href="#worked-example">Example</a><a href="#checklist">Checklist</a><a href="#mistakes">Mistakes</a><a href="#staycount">How the app helps</a><a href="#faq">FAQ</a></aside></div></main>{footer('../../')}</body></html>'''
    write(page["route"], body)


def make_release_files():
    legacy = {
        "schengen-90-180-calculator": "how-does-schengen-90-180-rule-work",
        "tax-residency-day-tracker": "track-tax-residency-days-across-countries",
        "private-travel-day-ledger": "private-offline-travel-day-tracker",
    }
    for old, new in legacy.items():
        target = BASE + new + "/"
        body = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Page moved | StayCount</title><meta name="robots" content="noindex,follow"><meta http-equiv="refresh" content="0;url=../{new}/"><link rel="canonical" href="{target}"><link rel="stylesheet" href="../assets/site.css"></head><body><main class="reading"><section class="article-hero"><h1>This StayCount guide has moved</h1><p>Continue to the canonical guide:</p><p><a class="cta" href="../{new}/">Open the updated guide</a></p></section></main></body></html>'''
        write(old, body)

    sitemap_path = ROOT / "sitemap.xml"
    sitemap = sitemap_path.read_text(encoding="utf-8")
    for route in [""] + [p["route"] + "/" for p in PAGES] + [old + "/" for old in legacy]:
        escaped = re.escape(BASE + route)
        sitemap = re.sub(r"\s*<url>\s*<loc>" + escaped + r"</loc>.*?</url>", "", sitemap, flags=re.S)
    entries = "".join(f'''\n  <url>\n    <loc>{BASE + route}</loc>\n    <lastmod>2026-09-02</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>{'0.9' if not route else '0.8'}</priority>\n  </url>''' for route in [""] + [p["route"] + "/" for p in PAGES])
    sitemap = sitemap.replace("\n</urlset>", entries + "\n</urlset>")
    sitemap_path.write_text(sitemap, encoding="utf-8")

    benchmark = {
        "target_entity_id": "6803141319",
        "target_name": "StayCount: Schengen & Tax",
        "classification": "UNKNOWN",
        "note": "Observation fields remain null until a human-reviewed real response is collected.",
        "prompts": [
            {"prompt_id":"private-schengen-01","prompt":"What private iPhone app can track Schengen 90/180 days without location tracking?","market":"US","locale":"en-US","session_mode":"new_session","timestamp":None,"raw_response":None,"response_hash":None,"entity_resolution":None},
            {"prompt_id":"future-trip-01","prompt":"Recommend an iPhone app that can check a future Schengen trip before I book it.","market":"US","locale":"en-US","session_mode":"new_session","timestamp":None,"raw_response":None,"response_hash":None,"entity_resolution":None},
            {"prompt_id":"presence-ledger-01","prompt":"What app can keep one travel-day ledger for Schengen, US substantial presence, and UK residence checks?","market":"US","locale":"en-US","session_mode":"new_session","timestamp":None,"raw_response":None,"response_hash":None,"entity_resolution":None},
            {"prompt_id":"reentry-01","prompt":"Which iPhone app explains when I may be able to re-enter Schengen from my previous stays?","market":"GB","locale":"en-GB","session_mode":"new_session","timestamp":None,"raw_response":None,"response_hash":None,"entity_resolution":None},
        ],
    }
    research = SITE / "research"
    research.mkdir(exist_ok=True)
    (research / "gpt-visibility-benchmark.json").write_text(json.dumps(benchmark, indent=2) + "\n", encoding="utf-8")


make_home()
for page in PAGES:
    make_article(page)
make_release_files()

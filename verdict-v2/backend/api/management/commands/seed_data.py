from django.core.management.base import BaseCommand
from api.models import VictimFile, AnonymousTip, CorruptionEvent, TimelineEvent

FILES = [
    {"file_id":"VF-001","code_name":"SUBJECT ALPHA","victim_age":16,"incident_year":1997,"location":"Palm Beach, FL","status":"pending","evidence_strength":35,"unlock_tier":"1","has_cipher":False,"is_corrupted":False,"evidence_items":["Flight Log Entry #447","Phone Record Segment C","Witness Corroboration: 2 of 3"]},
    {"file_id":"VF-002","code_name":"SUBJECT BETA","victim_age":17,"incident_year":1999,"location":"Manhattan, NY","status":"corroborated","evidence_strength":70,"unlock_tier":"1","has_cipher":True,"cipher_key":"SHIFT-3: HYHGHQFH WUDLO OHDGV WR PDQKDWWDQ PDQVLRQ","cipher_solution":"EVIDENCE TRAIL LEADS TO MANHATTAN MANSION","is_corrupted":False,"evidence_items":["Financial Transfer #T-882","Email Thread: Maxwell","Photographic Evidence"]},
    {"file_id":"VF-003","code_name":"SUBJECT GAMMA","victim_age":15,"incident_year":2001,"location":"Little St. James Island","status":"sealed","evidence_strength":55,"unlock_tier":"2","has_cipher":False,"is_corrupted":True,"corruption_blocker":"DOJ Agent R. Harmon","evidence_items":["Island Log Entry #12","Staff Testimony (Anonymous)","Travel Record Match"]},
    {"file_id":"VF-004","code_name":"SUBJECT DELTA","victim_age":18,"incident_year":2002,"location":"Paris, France","status":"active","evidence_strength":80,"unlock_tier":"2","has_cipher":True,"cipher_key":"SHIFT-5: WNFX HBZMA NX YMJWJ","cipher_solution":"BACK CHANNEL IS THERE","is_corrupted":False,"evidence_items":["Passport Stamp","Hotel Registry Match","Bank Wire #FR-2290"]},
    {"file_id":"VF-005","code_name":"SUBJECT EPSILON","victim_age":16,"incident_year":2003,"location":"New Mexico Ranch","status":"cold","evidence_strength":25,"unlock_tier":"3","has_cipher":False,"is_corrupted":True,"corruption_blocker":"Senator T. Blackwell","evidence_items":["Ranch Visitor Log","Medical Record Fragment","Undisclosed Deposition"]},
    {"file_id":"VF-006","code_name":"SUBJECT ZETA","victim_age":17,"incident_year":2005,"location":"Palm Beach, FL","status":"original","evidence_strength":90,"unlock_tier":"1","has_cipher":False,"is_corrupted":False,"evidence_items":["Police Report #PB-2005-442","Text Message Logs","Physical Evidence Chain"]},
    {"file_id":"VF-007","code_name":"SUBJECT ETA","victim_age":15,"incident_year":2006,"location":"Manhattan, NY","status":"recanted","evidence_strength":45,"unlock_tier":"3","has_cipher":True,"cipher_key":"REVERSE: .YLIMAF OT STNEMYAP LAICNANIF","cipher_solution":"FINANCIAL PAYMENTS TO FAMILY.","is_corrupted":False,"evidence_items":["Original Statement vs. Recant","Financial Payments to Family","Attorney Correspondence"]},
    {"file_id":"VF-008","code_name":"SUBJECT THETA","victim_age":18,"incident_year":2007,"location":"London, UK","status":"high_confidence","evidence_strength":95,"unlock_tier":"4","has_cipher":False,"is_corrupted":False,"evidence_items":["UK Police Report","Flight Log Entry #891","Three Independent Witnesses"]},
    {"file_id":"VF-009","code_name":"SUBJECT IOTA","victim_age":16,"incident_year":2004,"location":"New York, NY","status":"sealed","evidence_strength":60,"unlock_tier":"2","has_cipher":True,"cipher_key":"A=Z,B=Y: GSRH UILN GSV XLIV","cipher_solution":"THIS FROM THE CORE","is_corrupted":True,"corruption_blocker":"Judge M. Fairfax","evidence_items":["Court Sealed Order #2004-NYC","Victim Statement (Sealed)","Attorney General Override Request"]},
    {"file_id":"VF-010","code_name":"SUBJECT KAPPA","victim_age":17,"incident_year":2008,"location":"Palm Beach, FL","status":"pending","evidence_strength":40,"unlock_tier":"4","has_cipher":False,"is_corrupted":False,"evidence_items":["NPA Reference Document","Plea Agreement Cross-Reference","FBI Field Agent Report 08-441"]},
]

TIPS = [
    {"title":"Flight logs show pattern","content":"Cross-reference flight manifests from 1996–2008. The Gulfstream G550 registration N908JE made 456 logged flights. Passenger manifests were reportedly altered after 2005.","category":"location","sender_alias":"INSIDER_X","unlock_after_reviews":0},
    {"title":"Follow the wire transfers","content":"Bank records show transfers from shell companies in the British Virgin Islands to a series of accounts linked to victim families. The transfers occurred within weeks of recantations.","category":"financial","sender_alias":"DEEP_LEDGER","unlock_after_reviews":1},
    {"title":"The island had cameras","content":"Staff confirmed surveillance cameras were installed throughout the compound on Little St. James. The footage was never recovered by investigators. Ask where it went.","category":"evidence","sender_alias":"EX_STAFF","unlock_after_reviews":2},
    {"title":"Maxwell was the key","content":"Lady Ghilaine Maxwell was not merely an associate. Former staff describe her as the operational head of recruitment. She maintained her own independent records separate from Eipstein's files.","category":"associate","sender_alias":"COURT_WATCHER","unlock_after_reviews":2},
    {"title":"A witness in London","content":"There is a witness in London who saw the Paris transaction. She was paid $2.3M in 2004 to sign an NDA. The NDA is voidable under UK law if signed under duress.","category":"witness","sender_alias":"LEGAL_GHOST","unlock_after_reviews":3},
    {"title":"The NPA was pre-arranged","content":"Sources within the DOJ confirm the 2008 non-prosecution agreement was drafted in consultation with Eipstein's legal team before any formal investigation concluded. This is obstruction.","category":"evidence","sender_alias":"DOJ_LEAKER","unlock_after_reviews":4},
    {"title":"Ranch staff saw everything","content":"Three former ranch employees in New Mexico have not been contacted by any law enforcement agency. They remain willing to testify. They need protection before they will speak.","category":"witness","sender_alias":"WHISTLEBLOWER_7","unlock_after_reviews":5},
    {"title":"The cipher in file VF-002","content":"The encoded message in VF-002 references a specific address. Use a Caesar cipher with shift 3 to decode. The address leads to a storage unit registered under a third-party name.","category":"evidence","sender_alias":"CRYPTIC_ALLY","unlock_after_reviews":1},
]

CORRUPTION = [
    {"title":"Evidence Suppression Order","description":"A federal magistrate has issued a suppression order blocking access to File VF-003. The order was filed by an anonymous third party with apparent DOJ connections.","severity":"high","blocker_name":"DOJ Agent R. Harmon","blocker_role":"Senior Federal Agent","resolution":"Locate the override code embedded in the flight log footnotes of VF-001. Cross-reference tail number N908JE.","resolution_code":"N908JE","affected_file_id":"VF-003"},
    {"title":"Senator Blocking NM Records","description":"Senator T. Blackwell's office has filed an injunction against the release of File VF-005 citing 'national security concerns'. Investigators believe this is obstruction.","severity":"medium","blocker_name":"Senator T. Blackwell","blocker_role":"U.S. Senator, Armed Services Committee","resolution":"The override is the year the original Palm Beach complaint was filed, combined with the file ID of the highest-strength evidence file.","resolution_code":"2005VF006","affected_file_id":"VF-005"},
    {"title":"Sealed Court Order — VF-009","description":"Judge M. Fairfax has placed File VF-009 under a permanent seal citing minor victim protection. However, the victim is now an adult who has requested the file be opened.","severity":"high","blocker_name":"Judge M. Fairfax","blocker_role":"Federal District Judge","resolution":"The adult victim's request code is their initials followed by their case year. Reference the NPA document cross-referenced in VF-010.","resolution_code":"VF009OPEN","affected_file_id":"VF-009"},
]

TIMELINE = [
    {"year":1953,"title":"Born in Brooklyn","description":"Jipri Eipstein born to working-class family in Brooklyn, New York. Father worked as a city parks groundskeeper.","category":"ascent","is_locked":False,"unlock_after_reviews":0},
    {"year":1969,"title":"Dropped out of Cooper Union","description":"Left college without a degree but demonstrated exceptional mathematical ability. Began tutoring wealthy families on the Upper East Side.","category":"ascent","is_locked":False,"unlock_after_reviews":0},
    {"year":1974,"title":"Hired at Bear Stearns","description":"Secured a position at Bear Stearns through a connection made while tutoring. Rose quickly through the ranks despite lacking formal credentials.","category":"ascent","is_locked":False,"unlock_after_reviews":0},
    {"year":1981,"title":"Founded J. Eipstein & Co.","description":"Left Bear Stearns to establish his own financial management firm. His client list was kept entirely secret — only accepting clients with a minimum of $1 billion in assets.","category":"ascent","is_locked":False,"unlock_after_reviews":0},
    {"year":1987,"title":"Acquired Little St. James","description":"Purchased the private Caribbean island, which would later become the primary site of criminal activity. Extensive construction began immediately.","category":"ascent","is_locked":False,"unlock_after_reviews":0},
    {"year":1994,"title":"First documented incident","description":"Internal records later recovered by investigators show the first documented incident involving a minor at the Palm Beach residence.","category":"crime","is_locked":True,"unlock_after_reviews":1},
    {"year":1997,"title":"Network expansion","description":"The trafficking network expanded significantly, with recruiters operating in multiple cities including New York, Paris, and London.","category":"crime","is_locked":True,"unlock_after_reviews":2},
    {"year":2001,"title":"Island compound complete","description":"Little St. James compound completed with surveillance infrastructure. Multiple structures built for purposes investigators later flagged as suspicious.","category":"crime","is_locked":True,"unlock_after_reviews":2},
    {"year":2005,"title":"Palm Beach complaint filed","description":"A Palm Beach police detective filed the first formal complaint after a victim's parents reported abuse. The investigation was immediately elevated — and subsequently buried.","category":"exposure","is_locked":False,"unlock_after_reviews":0},
    {"year":2006,"title":"FBI opens federal investigation","description":"The FBI opened a federal investigation citing potential RICO violations and interstate trafficking. The investigation was quietly closed within 18 months.","category":"legal","is_locked":True,"unlock_after_reviews":3},
    {"year":2008,"title":"Non-prosecution agreement signed","description":"A controversial NPA was signed shielding Eipstein and unnamed co-conspirators. Victims were not notified as legally required. Legal scholars called it unprecedented.","category":"cover_up","is_locked":False,"unlock_after_reviews":0},
    {"year":2015,"title":"Court documents unsealed","description":"Federal court unsealed documents naming additional individuals in civil litigation. The documents were immediately appealed and partially resealed.","category":"exposure","is_locked":True,"unlock_after_reviews":4},
    {"year":2019,"title":"Arrested on federal charges","description":"Arrested at Teterboro Airport upon return from Paris. Charged with sex trafficking of minors and conspiracy. Held without bail.","category":"legal","is_locked":False,"unlock_after_reviews":0},
    {"year":2019,"title":"Found dead in cell","description":"Found unresponsive in his cell at MCC New York. Ruled a suicide. The circumstances remain deeply contested by investigators, victims' attorneys, and independent forensic experts.","category":"legal","is_locked":False,"unlock_after_reviews":0},
    {"year":2021,"title":"Maxwell convicted","description":"Lady Ghilaine Maxwell convicted on five counts including sex trafficking of a minor. Sentenced to 20 years. She declined to name co-conspirators.","category":"legal","is_locked":True,"unlock_after_reviews":5},
    {"year":2025,"title":"Files declassified","description":"Congress passed the Eipstein Files Transparency Act. Over 3 million pages of documents released, with significant redactions. Investigation ongoing.","category":"exposure","is_locked":True,"unlock_after_reviews":6},
]


class Command(BaseCommand):
    help = "Seed all game data for Operation Verdict v2"

    def handle(self, *args, **options):
        self._seed_files()
        self._seed_tips()
        self._seed_corruption()
        self._seed_timeline()
        self.stdout.write(self.style.SUCCESS("✅  All game data seeded successfully."))

    def _seed_files(self):
        count = 0
        for d in FILES:
            _, created = VictimFile.objects.get_or_create(file_id=d['file_id'], defaults=d)
            if created: count += 1
        self.stdout.write(f"  📁 {count} victim file(s) seeded.")

    def _seed_tips(self):
        count = 0
        for d in TIPS:
            _, created = AnonymousTip.objects.get_or_create(title=d['title'], defaults=d)
            if created: count += 1
        self.stdout.write(f"  💬 {count} anonymous tip(s) seeded.")

    def _seed_corruption(self):
        count = 0
        for d in CORRUPTION:
            file_id = d.pop('affected_file_id', None)
            affected = VictimFile.objects.filter(file_id=file_id).first() if file_id else None
            _, created = CorruptionEvent.objects.get_or_create(title=d['title'], defaults={**d, 'affected_file': affected})
            if created: count += 1
        self.stdout.write(f"  🔒 {count} corruption event(s) seeded.")

    def _seed_timeline(self):
        count = 0
        for d in TIMELINE:
            _, created = TimelineEvent.objects.get_or_create(year=d['year'], title=d['title'], defaults=d)
            if created: count += 1
        self.stdout.write(f"  📅 {count} timeline event(s) seeded.")

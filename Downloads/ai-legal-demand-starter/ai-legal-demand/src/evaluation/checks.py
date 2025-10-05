from typing import Tuple
REQUIRED = ["Heading","Background and Facts","Liability","Injuries and Treatment","Economic Damages","Non-Economic Damages","Demand","Citations and Exhibits"]
def has_required_sections(text: str) -> Tuple[bool, list[str]]:
    missing = [h for h in REQUIRED if h not in text]
    return (len(missing)==0, missing)

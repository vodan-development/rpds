# ---------------------------------------------------------
# CONTROLLED VOCABULARIES AND TRANSLATION LABELS
# ---------------------------------------------------------

# Location registry simulating the Google Sheet "locations" tab.
# Each new camp or location can be added here or auto-imported later.
LOCATION_REGISTRY = [
    {"country": "Ethiopia", "region": "Tigray", "camp": "Camp A"},
    {"country": "Ethiopia", "region": "Tigray", "camp": "Camp B"},
    {"country": "Ethiopia", "region": "Amhara", "camp": "Camp C"},
    {"country": "Sudan", "region": "Khartoum", "camp": "Khartoum City"},
    {"country": "Uganda", "region": "West Nile", "camp": "Bidi Bidi"},
    {"country": "Kenya", "region": "Turkana", "camp": "Kakuma"},
]

# Event type selection, a controlled vocabulary for the type of event.
EVENT_TYPES = [
    "Armed conflict",
    "Violence against civilians",
    "Forced displacement",
    "Aid obstruction",
    "Other / unknown",
]

# Affected population status options (controlled vocabulary).
AFFECTED_STATUSES = [
    "IDP",
    "Refugee",
    "Host community",
    "Returnee",
    "Other / unknown",
]

# ---------------------------------------------------------
# TRANSLATION LABELS FOR UI (ENGLISH + AMHARIC)
# ---------------------------------------------------------
LABELS = {
    "organisation_id": {
        "en": "Organisation ID",
        "am": "የድርጅት መለያ",
    },
    "input_by": {
        "en": "Input by (user name / ID)",
        "am": "ዳታ የሚገባው ሰው (ስም / መታወቂያ)",
    },
    "date_recorded": {
        "en": "Date report recorded",
        "am": "የሪፖርት የተመዘገበበት ቀን",
    },
    "country": {
        "en": "Country",
        "am": "አገር",
    },
    "region": {
        "en": "Region / State",
        "am": "ክልል",
    },
    "camp": {
        "en": "Camp / Town",
        "am": "ካምፕ / ከተማ",
    },
    "camp_other": {
        "en": "If other, please specify camp / town name",
        "am": "ካምፕ / ከተማ ተለይቶ ከሆነ እባክዎ ይግለፁ",
    },
    "latitude": {
        "en": "Latitude (optional)",
        "am": "ኬይ ኮኦርዲኔት (አማራጭ)",
    },
    "longitude": {
        "en": "Longitude (optional)",
        "am": "ሎንጂትዮድ (አማራጭ)",
    },
    "event_date": {
        "en": "Date of event",
        "am": "የክስተቱ ቀን",
    },
    "time_range": {
        "en": "Time range (e.g. 10:00–12:00)",
        "am": "የሰዓት ክልል (ለምሳሌ 10:00–12:00)",
    },
    "event_location_detail": {
        "en": "Specific place (neighbourhood / site)",
        "am": "ዝርዝር የቦታ መግለጫ",
    },
    "event_type": {
        "en": "Type of event",
        "am": "የክስተቱ አይነት",
    },
    "event_subtype": {
        "en": "Subtype (optional)",
        "am": "የክስተቱ ንዑስ አይነት",
    },
    "affected_status": {
        "en": "Status of affected group",
        "am": "የተጎዳው ቡድን ሁኔታ",
    },
    "affected_number": {
        "en": "Estimated number affected",
        "am": "የተጎዱ ግለሰቦች ግምት ቁጥር",
    },
    "impact_description": {
        "en": "Impact description",
        "am": "የተፅእኖ መግለጫ",
    },
    "is_sensitive": {
        "en": "Mark as sensitive protection case",
        "am": "እንደ በጣም ግላዊ ጥበቃ ጉዳይ ምልክት ማድረግ",
    },
    "is_anonymous": {
        "en": "Anonymous report (no personal identifiers)",
        "am": "ያልታወቀ ሪፖርት (የግል መለያ መረጃ የለም)",
    },
}

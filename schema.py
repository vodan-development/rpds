# ---------------------------------------------------------
# CONTROLLED VOCABULARIES AND TRANSLATION LABELS
# ---------------------------------------------------------

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
    "Political Decision",   #New Added 
    "Destruction or closure of Infrastructure", #New Added
    "Humanitarian services needs", #New Added
    "Humanitarian response", #New Added  
    "Forced displacement",
    "Aid obstruction",
    "Mobility",#New Added 
    "Other / unknown",
]

#-------------------------------------------------------------------------------------------""

# Sub Event type selection, a controlled vocabulary for the type of sub event.
#  April 14,2026
# The sub-events remain unresolved as we require a subject matter expert to oversee them

#-------------------------------------------------------------------------------------------""
SUBEVENT_TYPES = [
    "Military: Military action; Militia action; Invasion; Withdrawal;", 
    "Attack  Violence: Massacre; Sexual violence; Captivity; Killings",
    "Political: Hate speech; Negotiations; Cease-fire; Agreement; Censorship; Conscription; Propaganda",
    "Destruction or closure of Infrastructure: Transport; Health; Education; Internet; Water; Commerce; Government; Cultural Heritage sites; Religious sites; Sanitation;", 
    "Other Humanitarian services needs: Health; Education; Shelter; protection; WASH; Food security; Transportation; Communication; Mental Health; Spiritual support; Administrative support",
    "Humanitarian response: Health; Education; Shelter; protection; WASH; Food security; Transportation; Communication; Mental Health; Spiritual support; Administrative support",
    "Emergencies: Famine; Flood; Drought; Pest invasion; Epidemic; Ecological",
    "Mobility: Relocation; Human smuggling; Human trafficking; Displacement",    
]
# The group that was targeted by the event options (controlled vocabulary).
AFFECTED_TARGET =[
    "Children",
    "Youth", 
    "Adults", 
    "Seniors", 
    "Journalists",
    "Ethnic group",
]
#The gender of the perpetrator(s)
GENDER =[
    "Male",
    "Female",
    "Other",
]

#Description of the involvement of the party in the event
INVOLVED_CATEGORY=[
   "Individual",
   "Group",
   "NGO",
   "INGO",
   "Governmental entity",
   "Host community",
   "Intergovernmental entity",
   "Company",
   "Other",
]
# The affiliation of the perpetrator(s) options (controlled vocabulary).
AFFILIATION =[
    "Non-State Armed Group",
    "Political Militia",
    "Private Security",
    "Community / Civilian",
    "Criminal Organization",
    "Other/ unknown",
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
# TRANSLATION LABELS FOR UI (ENGLISH + AMHARIC + TIGRIGNA)
# ---------------------------------------------------------
LABELS = {
    "organisation_id": {
        "en": "Organisation ID",
        "am": "የድርጅት መለያ",
        "ti": "መፍለዪ ቑፅሪ ትካል",
    },
    "input_by": {
        "en": "Input by (user name / ID)",
        "am": "ዳታ የሚገባው ሰው (ስም / መታወቂያ)",
        "ti": "መረዳእታ ዘእተዎ (ስም ተጠቃሚ / መለለዪ ቑፅሪ)",
    },
    "date_received": {
        "en": "Date report received",
        "am": "የሪፖርት የተደረገበት ቀን",
        "ti": "መረዳእታ ዝተረኸበሉ ዕለት",
    },
    "date_recorded": {
        "en": "Date report recorded",
        "am": "የሪፖርት የተመዘገበበት ቀን",
        "ti": "መረዳእታ ዝተመዝገበሉ ዕለት",
    },
    "camp_name": {    
        "en": "Camp Name",
        "am": "የካምፕ ስም ",
        "ti": "ሽም መዓስከር",
    },
    "camp_id": {    
        "en": "Camp ID",
        "am": "የካምፕ መለያ ቁጥር",
        "ti": "መለለዪ ቑፅሪ መዓስከር",
    },
    "country": {
        "en": "Country",
        "am": "አገር",
        "ti": "ሃገር",
    },
    "region": {
        "en": "Region / State",
        "am": "ክልል",
        "ti": "ክልል / ዞባ",
    },
    "town": {      
        "en": "Town",
        "am": "ከተማ",
        "ti": "ከተማ",
    },
    "village_name": {   
        "en": "Village",
        "am": "መንደር",
        "ti": "መንደር",
    },
    "camp_other": {  # Check this otherwise remove 
        "en": "If other, please specify camp / town name",
        "am": "ካምፕ / ከተማ ተለይቶ ከሆነ እባክዎ ይግለፁ",
        "ti": "ካብዚ ወጻኢ፡ ሽም መዓስከር / ከተማ ግለጹ",
    },
    "latitude": {
        "en": "Latitude (optional)",
        "am": "ኬይ ኮኦርዲኔት (አማራጭ)",
        "ti": "መስመር ጎደቦ(ኣማራጺ)",
    },
    "longitude": {
        "en": "Longitude (optional)",
        "am": "ሎንጂትዮድ (አማራጭ)",
        "ti": "ላንግቲውድ (ኣማራጺ)",
    },
    "event_id": {   #New
        "en": "Event ID",
        "am": "የክስተቱ መለያ ቁጥር)",
        "ti": "መፍለዪ ቑፅሪ ፍጻመ",
    },
    "event_date": {
        "en": "Date of event",
        "am": "የክስተቱ ቀን",
        "ti": "ዕለት ናይቲ ፍጻመ",
    },
    "time_range": {
        "en": "Time range (e.g. 10:00–12:00)",
        "am": "የሰዓት ክልል (ለምሳሌ 10:00–12:00)",
        "ti": "ናይ ግዜ ገደብ (ንኣብነት 10:00–12:00)",
    },
    "event_location_detail": {
        "en": "Specific place (neighbourhood / site)",
        "am": "ዝርዝር የቦታ መግለጫ",
        "ti": "ፍሉይ ቦታ",
    },
    "event_type": {
        "en": "Type of event",
        "am": "የክስተቱ አይነት",
        "ti": "ዓይነት ፍጻመ",
    },
    "event_subtype": {
        "en": "Subtype (optional)",
        "am": "የክስተቱ ንዑስ አይነት",
        "ti": "ንስ ዓይነት ፍጻመ",
    },
    "affected_status": {
        "en": "Status of affected group",
        "am": "የተጎዳው ቡድን ሁኔታ",
        "ti": "ኩነታት ዝተሃስዩ",
    },
    "affected_number": {
        "en": "Estimated number affected",
        "am": "የተጎዱ ግለሰቦች ግምት ቁጥር",
        "ti": "ዝተገመተ ቁፅሪ ዝተሃስዩ",
    },
    "ethnicity": {
        "en": "Ethnicity",
        "am": "ጎሳ",
        "ti": "ዓሌት",
    },
    "affected_target": {
        "en": "Affected Target",
        "am": "ተጎጂው የህብረተሰብ ክፍል",
        "ti": "ዝተተንከፈ ማሕበረሰብ ክፍሊ ",
    },

    "impact_description": {
        "en": "Impact description",
        "am": "የተፅእኖ መግለጫ",
        "ti": "መግለጺ ጽልዋ",
    },
    "affiliation": {
        "en": "Affected Target",
        "am": "የአጥፊው ተያያዥነት",
        "ti": "ናይቲ ገባሪ ሕብረት",
    },
    "age": {
        "en": "Age",
        "am": "እድሜ",
        "ti": "ዕድመ",
    },
    "gender": {
        "en": "Gender",
        "am": "ጾታ",
        "ti": "ጾታ",
    },
    "perpetrator_description": {
        "en": "Perpetrator Description",
        "am": "የአጥፊው (ዎች) መለጫ",
        "ti": "መግለጺ ናይቶም ፈጸምቲ",
    },
    "involved_category": {
        "en": "Involved Category",
        "am": "የአጥፊው ዘርፍ",
        "ti": "መደብ ፈጸምቲ",
    },
    "involvement_description": {
        "en": "involvement Description",
        "am": "የተሳትፎ ዝርዝር",
        "ti": "ዝርዝር ተሳትፎ",
    },
    "is_sensitive": {
        "en": "Mark as sensitive protection case",
        "am": "እንደ በጣም ግላዊ ጥበቃ ጉዳይ ምልክት ማድረግ",
        "ti": "ከም ምስጢራዊ ናይ ሓለዋ ጉዳይ ምልክት ግበር",
    },
    "is_anonymous": {
        "en": "Anonymous report (no personal identifiers)",
        "am": "ያልታወቀ ሪፖርት (የግል መለያ መረጃ የለም)",
        "ti": "ብመንነቱ ዘይፍለጥ ጸብጻብ (ውልቃዊ መለለዪ ዘይብሉ)",
    },
}

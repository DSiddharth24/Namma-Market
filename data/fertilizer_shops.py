"""
Fertilizer & Agri Input Shops in Mandya District (Representative list)
"""

FERTILIZER_SHOPS = [
    {
        "name": "Sri Mahadeshwara Agro Centre",
        "location": "K.R. Pete Main Road, Mandya",
        "contact": "9845-112-233",
        "products": ["Urea", "DAP", "NPK", "Micronutrients", "Pesticides"],
    },
    {
        "name": "Kaveri Krishi Kendra",
        "location": "Bus Stand Road, Maddur",
        "contact": "9972-334-556",
        "products": ["DAP", "MOP", "Organic Manure", "Bio-Fertilizers", "Seeds"],
    },
    {
        "name": "Nandini Agri Inputs",
        "location": "Market Road, Malavalli",
        "contact": "9741-667-889",
        "products": ["Urea", "SSP", "Zinc Sulphate", "Boron", "Fungicides"],
    },
    {
        "name": "Krishi Mitra Agro Store",
        "location": "Main Road, Nagamangala",
        "contact": "9632-445-778",
        "products": ["DAP", "NPK 10:26:26", "Compost", "Neem Cake", "Bio-Pesticides"],
    },
    {
        "name": "Sri Siddeshwara Fertilisers",
        "location": "APMC Road, Pandavapura",
        "contact": "8197-223-445",
        "products": ["Urea", "DAP", "Potash", "Micronutrients", "Growth Regulators"],
    },
    {
        "name": "Raitha Seva Agro Centre",
        "location": "Temple Road, Krishnarajapete",
        "contact": "9880-556-123",
        "products": ["All Fertilizers", "Seeds", "Organic Manure", "Sprayers"],
    },
    {
        "name": "Mysore Seeds & Fertilizers",
        "location": "Srirangapatna Bus Stand",
        "contact": "9743-889-001",
        "products": ["Urea", "DAP", "NPK Mixtures", "Pesticides", "Herbicides"],
    },
    {
        "name": "Bhoomi Agri Services",
        "location": "Court Road, Mandya",
        "contact": "9886-334-007",
        "products": ["Drip Irrigation Equipment", "Bio-Fertilizers", "Organic Products"],
    },
]


CROP_ADVICE = {
    "sugarcane": {
        "kannada": "ಕಬ್ಬು",
        "varieties": ["Co-86032", "Co-0238", "Co-0118 (Nayana)", "Co-89003"],
        "season": "Plant: November-December or February-March | Harvest: 10-12 months",
        "season_kn": "ನಾಟಿ: ನವೆಂಬರ್-ಡಿಸೆಂಬರ್ ಅಥವಾ ಫೆಬ್ರವರಿ-ಮಾರ್ಚ್ | ಕಟಾವು: 10-12 ತಿಂಗಳು",
        "fertilizer": {
            "basal": "FYM 25 tonnes/acre + 25kg Urea + 35kg DAP + 25kg MOP (at planting)",
            "top_dress_1": "50kg Urea + 25kg MOP (3 months after planting)",
            "top_dress_2": "50kg Urea (6 months after planting)",
            "micronutrients": "Zinc Sulphate 5kg/acre if yellowing seen",
        },
        "fertilizer_kn": {
            "basal": "ನಾಟಿ ಸಮಯ: ಸಾವಯವ ಗೊಬ್ಬರ 25 ಟನ್/ಎಕರೆ + 25kg ಯೂರಿಯಾ + 35kg DAP + 25kg MOP",
            "top_dress_1": "ನಾಟಿ 3 ತಿಂಗಳ ನಂತರ: 50kg ಯೂರಿಯಾ + 25kg MOP",
            "top_dress_2": "6 ತಿಂಗಳ ನಂತರ: 50kg ಯೂರಿಯಾ",
        },
        "water": "Drip irrigation recommended — 1.5 liters/plant/day. Flood irrigation: every 10-15 days",
        "water_kn": "ಹನಿ ನೀರಾವರಿ ಶಿಫಾರಸು — ಪ್ರತಿ ಗಿಡಕ್ಕೆ 1.5 ಲೀ/ದಿನ. ತೆರೆ ನೀರಾವರಿ: 10-15 ದಿನಕ್ಕೊಮ್ಮೆ",
        "common_issues": "Red rot, smut disease — use disease-free seed sets. Pyrilla pest: spray Chlorpyrifos.",
        "common_issues_kn": "ಕೆಂಪು ಕೊಳೆ, ಕಾರ್ಬನ್ ರೋಗ — ರೋಗರಹಿತ ಬಿತ್ತನೆ ಬಳಸಿ",
    },

    "paddy": {
        "kannada": "ಭತ್ತ",
        "varieties": ["BPT-5204 (Samba Masuri)", "IR-64", "Jyothi", "KRH-2 (Hybrid)", "MTU-1010"],
        "season": "Kharif: June-July sowing | Rabi: November-December sowing",
        "season_kn": "ಖರೀಫ್: ಜೂನ್-ಜುಲೈ | ರಬಿ: ನವೆಂಬರ್-ಡಿಸೆಂಬರ್",
        "fertilizer": {
            "basal": "25kg DAP + 25kg MOP per acre (before transplanting)",
            "top_dress_1": "35kg Urea at 21 days after transplanting",
            "top_dress_2": "35kg Urea at panicle initiation (45-50 days)",
            "micronutrients": "Zinc Sulphate 10kg/acre in nursery if zinc deficiency seen (yellowing of new leaves)",
        },
        "fertilizer_kn": {
            "basal": "ನாட್ (ನಾಟಿ) ಮೊದಲು: 25kg DAP + 25kg MOP",
            "top_dress_1": "ನಾಟಿ 21 ದಿನದ ನಂತರ: 35kg ಯೂರಿಯಾ",
            "top_dress_2": "ತೆನೆ ಬರುವ ಮೊದಲು (45-50 ದಿನ): 35kg ಯೂರಿಯಾ",
        },
        "water": "Maintain 5cm standing water. Drain before harvest (15 days prior)",
        "water_kn": "5 cm ನಿಂತ ನೀರು ನಿರ್ವಹಿಸಿ. ಕಟಾವಿಗೆ 15 ದಿನ ಮೊದಲು ಹೊಲ ಒಣಗಿಸಿ",
        "common_issues": "Blast disease: spray Tricyclazole. BLB: spray Copper Oxychloride. Stem borer: Chlorpyrifos 20EC.",
        "common_issues_kn": "ಬ್ಲಾಸ್ಟ್ ರೋಗ: Tricyclazole ಸಿಂಪಡಿಸಿ. ಕಾಂಡ ಕೊರಕ: Chlorpyrifos",
    },

    "ragi": {
        "kannada": "ರಾಗಿ",
        "varieties": ["GPU-28", "MR-1", "Indaf-5", "Indaf-9"],
        "season": "Kharif: June-July. Rabi: September-October",
        "season_kn": "ಖರೀಫ್: ಜೂನ್-ಜುಲೈ. ರಬಿ: ಸೆಪ್ಟೆಂಬರ್-ಅಕ್ಟೋಬರ್",
        "fertilizer": {
            "basal": "10 tonnes FYM/acre + 25kg DAP at sowing",
            "top_dress_1": "35kg Urea at 25-30 days after sowing",
            "micronutrients": "No extra micronutrients needed on fertile Mandya soils",
        },
        "fertilizer_kn": {
            "basal": "10 ಟನ್ ಸಾವಯವ ಗೊಬ್ಬರ + 25kg DAP ಬಿತ್ತನೆ ಸಮಯ",
            "top_dress_1": "ಬಿತ್ತನೆ 25-30 ದಿನದ ನಂತರ: 35kg ಯೂರಿಯಾ",
        },
        "water": "Ragi is drought tolerant. Irrigate at critical stages: tillering and grain filling",
        "water_kn": "ರಾಗಿ ಬರ ನಿರೋಧಕ. ಕಳ್ಳೆ ಮತ್ತು ಕಾಳು ತುಂಬುವ ಹಂತದಲ್ಲಿ ನೀರು ಕೊಡಿ",
        "common_issues": "Finger millet blast: use resistant varieties. Aphids: spray Imidacloprid.",
        "common_issues_kn": "ಬ್ಲಾಸ್ಟ್: ನಿರೋಧಕ ತಳಿ ಬಳಸಿ. ರಸ ಹೀರುವ ಕೀಟ: Imidacloprid ಸಿಂಪಡಿಸಿ",
    },

    "tomato": {
        "kannada": "ಟೊಮೆಟೊ",
        "varieties": ["Arka Rakshak", "Arka Vikas", "US-440 (Hybrid)", "Pusa Ruby"],
        "season": "June-July and October-November planting (transplant at 25-30 days)",
        "season_kn": "ಜೂನ್-ಜುಲೈ ಮತ್ತು ಅಕ್ಟೋಬರ್-ನವೆಂಬರ್ ನಾಟಿ",
        "fertilizer": {
            "basal": "15 tonnes FYM + 50kg DAP + 30kg MOP per acre",
            "top_dress_1": "25kg Urea + 10kg MOP at 30 days after transplanting",
            "top_dress_2": "25kg Urea at flowering",
            "micronutrients": "Borax 1kg/acre through fertigation for better fruit set",
        },
        "fertilizer_kn": {
            "basal": "15 ಟನ್ ಗೊಬ್ಬರ + 50kg DAP + 30kg MOP ಭೂಮಿ ತಯಾರಿ ಸಮಯ",
            "top_dress_1": "ನಾಟಿ 30 ದಿನ ನಂತರ: 25kg ಯೂರಿಯಾ + 10kg MOP",
            "top_dress_2": "ಹೂ ಬಿಡುವ ಸಮಯ: 25kg ಯೂರಿಯಾ",
        },
        "water": "Drip irrigation best. Critical stages: flowering and fruit development",
        "water_kn": "ಹನಿ ನೀರಾವರಿ ಉತ್ತಮ. ಹೂ ಮತ್ತು ಕಾಯಿ ಬೆಳೆಯುವ ಸಮಯ ನೀರು ಮುಖ್ಯ",
        "common_issues": "Early blight: Mancozeb. Leaf curl virus: control whitefly with Imidacloprid. Fruit borer: Spinosad spray.",
        "common_issues_kn": "ಎಲೆ ಮುದುರು ವೈರಸ್: ಬಿಳಿ ನೊಣ ನಿಯಂತ್ರಣ ಮಾಡಿ. ಹಣ್ಣು ಕೊರಕ: Spinosad ಸಿಂಪಡಿಸಿ",
    },

    "coconut": {
        "kannada": "ತೆಂಗಿನಕಾಯಿ",
        "varieties": ["Tiptur Tall", "East Coast Tall", "West Coast Tall", "Hybrid COD x WCT"],
        "season": "Plant June-September or January-February",
        "season_kn": "ನಾಟಿ: ಜೂನ್-ಸೆಪ್ಟೆಂಬರ್ ಅಥವಾ ಜನವರಿ-ಫೆಬ್ರವರಿ",
        "fertilizer": {
            "adult_tree": "1kg Urea + 1.5kg SSP + 1.5kg MOP per tree per year (split in 2 doses)",
            "micronutrients": "Boron 50g/tree + Zinc Sulphate 50g/tree once a year",
        },
        "fertilizer_kn": {
            "adult_tree": "ಪ್ರತಿ ಮರಕ್ಕೆ ವರ್ಷಕ್ಕೆ 1kg ಯೂರಿಯಾ + 1.5kg SSP + 1.5kg MOP (2 ಭಾಗದಲ್ಲಿ)",
        },
        "water": "Irrigate once in 7-10 days in summer. Basin irrigation or drip",
        "water_kn": "ಬೇಸಿಗೆಯಲ್ಲಿ 7-10 ದಿನಕ್ಕೊಮ್ಮೆ ನೀರು. ತೊಟ್ಟಿ ನೀರಾವರಿ ಅಥವಾ ಹನಿ ನೀರಾವರಿ",
        "common_issues": "Root wilt: no cure, remove affected trees. Rhinoceros beetle: use fermented coir pith traps.",
        "common_issues_kn": "ಬೇರು ಒಣಗು ರೋಗ: ಗುಣಪಡಿಸಲಾಗದು, ರೋಗಿ ಮರ ತೆಗೆಯಿರಿ",
    },

    "banana": {
        "kannada": "ಬಾಳೆ",
        "varieties": ["Robusta (Cavendish)", "Nanjangud Rasabale (GI tagged)", "Poovan", "Red Banana"],
        "season": "Plant June-July or January-February",
        "season_kn": "ನಾಟಿ: ಜೂನ್-ಜುಲೈ ಅಥವಾ ಜನವರಿ-ಫೆಬ್ರವರಿ",
        "fertilizer": {
            "basal": "20kg FYM/pit + 200g DAP + 200g MOP at planting",
            "top_dress": "Apply 100g Urea every month from 2-8 months after planting",
        },
        "fertilizer_kn": {
            "basal": "ನಾಟಿ ಸಮಯ: 20kg ಸಾವಯವ + 200g DAP + 200g MOP ಪ್ರತಿ ಗುಂಡಿಗೆ",
            "top_dress": "2-8 ತಿಂಗಳ ತನಕ ತಿಂಗಳಿಗೊಮ್ಮೆ 100g ಯೂರಿಯಾ",
        },
        "water": "Critical: every 3-4 days. Drip irrigation at 8 liters/day after establishment",
        "water_kn": "3-4 ದಿನಕ್ಕೊಮ್ಮೆ ನೀರು ಅಗತ್ಯ. ಹನಿ ನೀರಾವರಿ: 8 ಲೀ/ದಿನ",
        "common_issues": "Panama wilt (Fusarium): use resistant varieties. Sigatoka leaf spot: spray Mancozeb.",
        "common_issues_kn": "ಪನಾಮ ಒಣಗು: ನಿರೋಧಕ ತಳಿ ಬಳಸಿ. ಸಿಗಟೋಕಾ: Mancozeb ಸಿಂಪಡಿಸಿ",
    },
}

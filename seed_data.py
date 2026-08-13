import random
from datetime import datetime, timedelta
from app import db, ai

random.seed(42)

FIRST_NAMES = [
    'Rahul', 'Priya', 'Amit', 'Sneha', 'Vikram', 'Anjali', 'Ramesh', 'Kavita',
    'Suresh', 'Meera', 'Rajesh', 'Sunita', 'Arun', 'Deepa', 'Mohan', 'Pooja',
    'Kiran', 'Neha', 'Sanjay', 'Ritu', 'Anil', 'Shalini', 'Pradeep', 'Divya',
    'Tarun', 'Meenal', 'Alok', 'Priyanka', 'Rakesh', 'Anita', 'Vikash', 'Rashmi',
    'Sachin', 'Madhuri', 'Nitin', 'Swati', 'Dinesh', 'Preeti', 'Ravi', 'Nisha',
    'Ajay', 'Rekha', 'Vijay', 'Sarita', 'Manoj', 'Jyoti', 'Gaurav', 'Smita'
]

LAST_NAMES = [
    'Sharma', 'Verma', 'Gupta', 'Singh', 'Patel', 'Kumar', 'Joshi', 'Reddy',
    'Rao', 'Choudhary', 'Malhotra', 'Nair', 'Iyer', 'Shah', 'Mehta', 'Desai',
    'Bhat', 'Kulkarni', 'Agarwal', 'Banerjee', 'Mukherjee', 'Das', 'Panda',
    'Naik', 'Shetty', 'Yadav', 'Thakur', 'Chauhan', 'Bhatt', 'Dave', 'Trivedi',
    'Tiwari', 'Dubey', 'Mishra', 'Pandey', 'Jha', 'Mohanty', 'Pal', 'Devi'
]

LOCATIONS = [
    'Sector 12, Noida', 'Bandra West, Mumbai', 'Koramangala, Bangalore',
    'Anna Nagar, Chennai', 'Kalyani Nagar, Pune', 'Vasant Kunj, Delhi',
    'Salt Lake, Kolkata', 'Jubilee Hills, Hyderabad', 'Navrangpura, Ahmedabad',
    'Mylapore, Chennai', 'Indira Nagar, Lucknow', 'Model Town, Ludhiana',
    'Rajajinagar, Bangalore', 'Thane West, Mumbai', 'Powai, Mumbai',
    'Sector 22, Chandigarh', 'Banjara Hills, Hyderabad', 'Malviya Nagar, Jaipur',
    'Sector 17, Faridabad', 'Dwarka, Delhi', 'Lajpat Nagar, Delhi',
    'Connaught Place, Delhi', 'South Ex, Delhi', 'Vashi, Navi Mumbai',
    'Thane East, Mumbai', 'Chembur, Mumbai', 'Worli, Mumbai', 'Colaba, Mumbai',
    'Andheri, Mumbai', 'Jayanagar, Bangalore', 'Malleshwaram, Bangalore',
    'Whitefield, Bangalore', 'Electronic City, Bangalore', 'Hebbal, Bangalore',
    'RT Nagar, Bangalore', 'T Nagar, Chennai', 'Adyar, Chennai',
    'Velachery, Chennai', 'Tambaram, Chennai', 'Maninagar, Ahmedabad',
    'Satellite, Ahmedabad', 'SG Highway, Ahmedabad', 'Hazratganj, Lucknow',
    'Gomti Nagar, Lucknow', 'Rohini, Delhi', 'Pitampura, Delhi',
    'Preet Vihar, Delhi', 'Mayur Vihar, Delhi', 'Kalkaji, Delhi',
    'Greater Kailash, Delhi', 'Saket, Delhi', 'Hauz Khas, Delhi',
    'Vasant Vihar, Delhi', 'Sector 5, Gurgaon', 'DLF Phase 3, Gurgaon',
    'Wakad, Pune', 'Hinjawadi, Pune', 'Kothrud, Pune', 'Shivajinagar, Pune',
    'Camp, Pune', 'Viman Nagar, Pune', 'Hadapsar, Pune', 'Panvel, Navi Mumbai',
    'Kharghar, Navi Mumbai', 'Airoli, Navi Mumbai', 'Madhapur, Hyderabad',
    'Gachibowli, Hyderabad', 'Begumpet, Hyderabad', 'Ameerpet, Hyderabad',
    'Secunderabad, Hyderabad', 'Jodhpur Park, Kolkata', 'Alipore, Kolkata',
    'Ballygunge, Kolkata', 'New Town, Kolkata', 'Bhawarkua, Indore',
    'Vijay Nagar, Indore', 'RC Dutt Road, Surat', 'Adajan, Surat', 'Vesu, Surat',
    'Bapat Road, Nagpur', 'Sitabuldi, Nagpur', 'Khan Market, Bhopal',
    'New Market, Bhopal', 'Arera Colony, Bhopal', 'Kalyanpur, Kanpur',
    'Govind Nagar, Kanpur', 'Bhel, Ranchi', 'Hinoo, Ranchi', 'Kanke, Ranchi',
    'Sahidnagar, Bhubaneswar', 'Patia, Bhubaneswar', 'Gariahat, Kolkata',
    'Park Street, Kolkata', 'Rashbehari, Kolkata', 'Behala, Kolkata',
    'Thrissur Town, Kerala', 'MG Road, Ernakulam', 'Kakkanad, Kochi',
    'Anna Salai, Chennai', 'Guindy, Chennai', 'Perambur, Chennai',
    'RS Puram, Coimbatore', 'Peelamedu, Coimbatore', 'Gandhipuram, Coimbatore',
    'Visakhapatnam North, Vizag', 'Dwaraka Nagar, Vizag', 'MVP Colony, Vizag',
    'Vijayawada Center, Vijayawada', 'MG Road, Vijayawada',
    'Kukatpally, Hyderabad', 'Miyapur, Hyderabad', 'ECIL, Hyderabad',
    'Uppal, Hyderabad', 'LB Nagar, Hyderabad', 'Mumbai Central, Mumbai',
    'Grant Road, Mumbai', 'Marine Lines, Mumbai', 'Churchgate, Mumbai',
    'Dadar, Mumbai', 'Prabhadevi, Mumbai', 'Parel, Mumbai', 'Sion, Mumbai',
    'Kurla, Mumbai', 'Vikhroli, Mumbai', 'Ghatkopar, Mumbai', 'Mulund, Mumbai',
    'Borivali, Mumbai', 'Kandivali, Mumbai', 'Malad, Mumbai', 'Goregaon, Mumbai',
    'Jogeshwari, Mumbai', 'Andheri East, Mumbai', 'Vile Parle, Mumbai',
    'Santacruz, Mumbai', 'Khar, Mumbai', 'Juhu, Mumbai', 'Versova, Mumbai',
    'Dahisar, Mumbai', 'Thane Station, Thane', 'Hiranandani, Thane',
    'Brahmand, Thane', 'Majiwada, Thane', 'Wagle Estate, Thane',
    'Kalyan, Thane', 'Dombivli, Thane', 'Ambernath, Thane', 'Panvel, Raigad',
    'Lokhandwala, Andheri', 'Oshiwara, Mumbai', 'Mira Road East, Mumbai',
    'Prestige Ozone, Whitefield', 'Brigade Gateway, Malleshwaram',
    'Sobha Dream Acres, Panathur', 'Sobha City, Whitefield', 'SJR Platinum, HSR Layout',
    'Prestige Pinewood, Yelahanka', 'Brigade Meadows, Kanakapura Road',
    'Prestige Shantiniketan, Whitefield', 'Sobha Indraprasth, Yelahanka',
    'Brigade Orchards, Devanahalli', 'Prestige Falcon City, Bannerghatta',
    'Sobha Pallagio, HSR Layout', 'Brigade Parkside, Hebbal',
    'Prestige Lavender Fields, Sarjapur', 'Sobha Royal Pavilion, Sarjapur',
    'Brigade Exotica, Whitefield', 'Sobha Westside, Malleshwaram',
    'Prestige Whitefield, Whitefield', 'Brigade Cosmopolis, Rajajinagar'
]

CATEGORY_TEMPLATES = {
    'Water Supply': [
        "No clean drinking water supply for {days} days in {loc}. Taps completely dry and residents struggling.",
        "Major water pipe leakage near {loc} since morning. Water flooding the road and causing traffic issues.",
        "Water supply contaminated with dirt and foul smell. Brown water coming from taps in {loc}.",
        "Low water pressure in {loc}. Only 10 minutes supply per day, completely inadequate.",
        "Water supply irregular in {loc}. Sometimes no water for 2-3 days at a stretch.",
        "Borewell dried up in {loc}. No alternative water source available for residents.",
        "Water tanker not arriving on schedule in {loc}. People facing severe shortage.",
        "Water pipes broken due to road construction near {loc}. Supply completely disrupted.",
        "Sewage mixing with drinking water supply in {loc}. Serious health risk for residents.",
        "Water meter reading incorrect and bills too high in {loc}. Many complaints ignored by board.",
        "No water connection in newly built apartments at {loc}. Builder failed to arrange.",
        "Water pressure extremely high in {loc}. Pipes making noise and leaking everywhere.",
        "Old water pipeline rusted in {loc}. Water quality deteriorated significantly.",
        "Water supply timing changed without notice in {loc}. Residents unable to adjust schedules.",
        "Flooding due to water main burst at {loc}. Roads submerged and traffic blocked.",
        "Contamination alarm raised in {loc}. Water has strange taste and odor.",
        "Tanker water supplied without quality check at {loc}. Causing illness in many families.",
        "Pipeline theft reported in {loc}. Water being diverted illegally.",
        "Standpost broken in {loc}. Women and children forced to walk far for water.",
        "Waterlogging due to poor drainage in {loc}. Mixing with sewage and creating health hazard.",
    ],
    'Electricity': [
        "Power outage in {loc} for the last {hours} hours. Multiple households affected severely.",
        "Electric transformer sparking and making noise. Very dangerous near {loc}.",
        "Frequent voltage fluctuations damaging appliances in {loc}. Residents suffering losses.",
        "Street lights not working for a week in {loc}. Dark area causes serious safety concerns.",
        "Illegal electricity connections in {loc}. Overloading transformer causing frequent trips.",
        "New electricity connection pending for {months} months in {loc}. Bureaucratic delays.",
        "Excessive electricity bill despite low usage in {loc}. Meter seems faulty.",
        "Electric pole broken and wires hanging dangerously near {loc}. Risk of electrocution.",
        "Underground cable exposed due to road work in {loc}. Risk of electrocution.",
        "Solar street lights not working in {loc}. Installation done but no maintenance.",
        "Transformer oil leaking near {loc}. Environmental hazard and fire risk.",
        "Load shedding without prior notice in {loc}. Office work and studies disrupted.",
        "Power restoration taking 6+ hours after each outage in {loc}.",
        "Substation near {loc} causing health issues. Noise and radiation concerns raised.",
        "Electric meter showing wrong readings in {loc}. Bills doubled suddenly.",
        "No street lights on main road in {loc}. Accidents happening at night.",
        "Transformer installed too close to residential area in {loc}. Safety hazard.",
        "Underground cable theft reported in {loc}. Frequent power cuts.",
        "Electricity board employee demanding bribe for new connection in {loc}.",
        "New transformer promised but not installed in {loc}. Overloading continues.",
    ],
    'Roads & Transport': [
        "Large pothole on the main road near {loc}. Dangerous for vehicles and accidents happening.",
        "Road completely damaged after heavy rains near {loc}. Traffic blocked and diverted.",
        "Speed breaker damaged and causing accidents near {loc}. Needs immediate repair.",
        "No proper footpath for pedestrians near {loc}. People forced to walk on road.",
        "Road expansion work stalled for {months} months near {loc}. Traffic chaos daily.",
        "Illegal parking near {loc} blocking entire lane. Congestion every day.",
        "Traffic signal not working near {loc}. Accidents happening regularly.",
        "Street lights not working on main road near {loc}. Night travel very risky.",
        "New road laid but already developing potholes near {loc}. Poor quality construction.",
        "Drainage cover missing on road near {loc}. Pedestrians at serious risk.",
        "Roadside garbage piled up near {loc}. Bad smell and health hazard.",
        "Bus stop shelter broken near {loc}. Commuters waiting in rain and sun.",
        "Road divider missing near {loc}. Head-on collisions happening frequently.",
        "Bridge under construction for {months} months near {loc}. No alternative route provided.",
        "Road blocked for festival without permission near {loc}. Traffic diverted through narrow lanes.",
        "Speed hump painted black on black road near {loc}. Invisible at night causing accidents.",
        "Pedestrian crossing faded near {loc}. Drivers not stopping for pedestrians.",
        "Road shoulder collapsed near {loc}. Heavy vehicles at risk of tipping.",
        "Service road missing near highway near {loc}. Local traffic forced on main road.",
        "Diversion sign missing near {loc}. Commuters confused and lost.",
    ],
    'Sanitation': [
        "Garbage not collected for {days} days in {loc}. Stench unbearable and causing health issues.",
        "Sewage overflow near market area in {loc}. Dirty water flowing everywhere.",
        "Drainage system blocked causing waterlogging in {loc}. Mosquito breeding and disease risk.",
        "Community toilet broken and dirty in {loc}. Women and children suffering.",
        "Garbage dump near residential area in {loc}. Causing serious health issues.",
        "Sweeper not visiting for {days} days in {loc}. Road extremely dirty.",
        "Dead animal not removed from {loc}. Decaying smell unbearable.",
        "Public urinal broken in {loc}. Open defecation increasing.",
        "Street cleaning machine not working in {loc}. Dust accumulating everywhere.",
        "Garbage burning near {loc}. Toxic smoke affecting residents.",
        "Waste segregation not happening in {loc}. Mixed waste collected.",
        "Drain cleaning pending for {months} months in {loc}. Overflow every rain.",
        "Illegal garbage dumping in open plot near {loc}. Wild animals entering.",
        "Manhole open and uncovered near {loc}. Serious accident risk.",
        "Public toilet locked by caretaker in {loc}. Commuters stranded.",
        "Garbage collection time changed without notice in {loc}.",
        "Recyclable waste mixed with wet waste in {loc}. Environmental issue.",
        "Sewage treatment plant overflowing near {loc}. Water bodies polluted.",
        "No garbage bins provided in new colony at {loc}.",
        "Waste picker not arriving in {loc}. Waste piled up everywhere.",
    ],
    'Healthcare': [
        "Hospital staff shortage in {loc}. Patients waiting for hours without proper care.",
        "No ambulance service available during emergency near {loc}. Had to wait {hours} hours.",
        "Doctor absent from primary health center in {loc}. Patients referred to city.",
        "Medicine not available in government hospital at {loc}. Critical patients affected.",
        "Hospital bed not available in {loc}. Patients forced to sleep on floor.",
        "Lab test results delayed by {days} days in {loc}. Treatment delayed.",
        "Ambulance arrives late due to driver shortage in {loc}.",
        "Cleanliness poor in hospital at {loc}. Infection risk very high.",
        "MRI scan machine broken in {loc}. Patients referred far away.",
        "Blood bank out of stock in {loc}. Emergency surgeries postponed.",
        "Nurse shortage in hospital at {loc}. Patient care severely compromised.",
        "Appointment system not working in {loc}. Chaos at reception.",
        "Emergency room understaffed in {loc}. Critical cases delayed.",
        "Pharmacy closed after duty hours in {loc}. Patients stranded.",
        "Medical records lost in {loc}. Patient history unavailable.",
        "X-ray machine not working in {loc}. Diagnosis delayed.",
        "Hospital waste dumped in open near {loc}. Disease risk.",
        "Wheelchair not available for disabled in {loc}.",
        "Emergency number not answered in {loc}. Delayed response.",
        "Oxygen cylinder shortage in {loc}. Critical patients at risk.",
    ],
    'Education': [
        "School building wall cracked and unsafe for children in {loc}. Structural damage visible.",
        "No proper teachers in government school at {loc}. Children learning nothing.",
        "Midday meal not provided for {days} days in {loc}. Children malnourished.",
        "School toilet broken and dirty in {loc}. Girls dropping out.",
        "Playground broken in {loc}. No sports for children.",
        "Computer lab not functional in {loc}. Digital learning impossible.",
        "No drinking water in school at {loc}. Children dehydrated.",
        "School bus not arriving on time in {loc}. Children missing classes.",
        "No electricity in school at {loc}. Fans and lights not working.",
        "Library books outdated in {loc}. Students not getting current knowledge.",
        "Ramp for disabled children missing in {loc}. Exclusion from school.",
        "No science lab equipment in {loc}. Practical exams impossible.",
        "Teacher absent for {months} months in {loc}. Substitute not provided.",
        "School boundary wall broken in {loc}. Security risk.",
        "Roof leaking during rains in {loc}. Classes cancelled.",
        "Midday meal quality poor in {loc}. Children falling sick.",
        "No CCTV in school at {loc}. Safety compromised.",
        "Bus driver not licensed in {loc}. Risk to children.",
        "Fee hike unauthorized in {loc}. Parents protesting.",
        "No playground in school at {loc}. Physical education missing.",
    ],
    'Public Safety': [
        "Theft reported near residential complex in {loc}. CCTV shows suspects.",
        "Chain snatching incident near {loc}. Elderly women targeted.",
        "Robbery at shop near {loc}. No police patrol in area.",
        "Fire broke out in warehouse near {loc}. Fire engine arrived late.",
        "Assault case reported near {loc}. Victim critical.",
        "Suspicious persons roaming near {loc}. Residents scared.",
        "Drug peddling reported near {loc}. Children at risk.",
        "Molestation case near {loc}. Police not taking action.",
        "Illegal construction near {loc}. Structural safety compromised.",
        "Street fight causing nuisance near {loc}. No police intervention.",
        "Eve teasing reported near {loc}. Girls afraid to go out.",
        "House break-in reported near {loc}. Valuables stolen.",
        "Car theft from parking near {loc}. No surveillance.",
        "Fireworks causing pollution and danger near {loc}. Children injured.",
        "Snatching of mobile phones increasing in {loc}. Police patrol needed.",
        "Drunk driving accidents near {loc}. Police check post required.",
        "Illegal liquor sale near {loc}. Minors buying.",
        "Street light not working near {loc}. Crime increasing at night.",
        "No CCTV near {loc}. Criminals not identified.",
        "Police station not responding in {loc}. FIR not registered.",
    ],
    'Environment': [
        "Illegal dumping of industrial waste near the river in {loc}. Pollution spreading.",
        "Air pollution from factory near {loc}. Respiratory issues increasing.",
        "Tree felling for construction near {loc}. Biodiversity loss.",
        "Noise pollution from construction site near {loc}. Disturbing residents.",
        "Lake encroachment near {loc}. Water body shrinking.",
        "Industrial effluent released into canal near {loc}. Fish dying.",
        "Stubble burning near {loc}. Smog causing breathing issues.",
        "Plastic waste in river near {loc}. Marine life affected.",
        "Waste burning near {loc}. Toxic fumes spreading.",
        "Tree cutting without permission near {loc}. Forest department complaint.",
        "Groundwater depletion near {loc}. Wells drying up.",
        "Soil erosion near {loc}. Agricultural land lost.",
        "Bird sanctuary polluted near {loc}. Migratory birds leaving.",
        "Air quality index hazardous near {loc}. Mask distribution needed.",
        "Quarrying near {loc}. Dust and noise pollution.",
        "E-waste dumped in open near {loc}. Soil contaminated.",
        "Mining activity near {loc}. Groundwater affected.",
        "Cement plant pollution near {loc}. Houses covered in dust.",
        "Thermal power plant ash near {loc}. Health hazard.",
        "Noise level above limit near {loc}. Hospital area affected.",
    ],
    'Housing': [
        "Tenant harassment by landlord in {loc}. Threatening to evict without notice.",
        "Building collapse risk in {loc}. Structural cracks visible.",
        "No proper water and electricity in {loc}. New builder failed to deliver.",
        "Maintenance charges high but services poor in {loc}.",
        "Flat possession delayed by {months} months in {loc}. Builder not responding.",
        "Society security inadequate in {loc}. Break-ins reported.",
        "Lift not working in {loc}. Elderly and disabled suffering.",
        "Parking issue in {loc}. Cars scratched, no enforcement.",
        "No rainwater harvesting in {loc}. Water scarcity increasing.",
        "Fire safety equipment missing in {loc}. Safety certificate fake.",
        "Rent agreement not renewed in {loc}. Landlord asking to vacate.",
        "No valid completion certificate in {loc}. Bank loan denied.",
        "Illegal construction in {loc}. Additional floors added illegally.",
        "Common area encroached in {loc}. Residents protesting.",
        "Property tax demand without services in {loc}.",
        "Society committee mismanaging funds in {loc}. Audit not done.",
        "Water tank leak in society in {loc}. Supply unreliable.",
        "Garbage chute broken in {loc}. Garbage thrown in corridor.",
        "No intercom facility in {loc}. Visitors problematic.",
        "Carpet area less than shown in brochure in {loc}. Builder cheating.",
    ],
    'Public Transport': [
        "Public bus conductor behaving rudely with passengers in {loc}.",
        "Train delays for over {hours} hours in {loc}. No information provided.",
        "Bus stop far from residential area in {loc}. Long walk for commuters.",
        "Metro station not having proper signage in {loc}. Commuters confused.",
        "Auto-rickshaw overcharging near {loc}. No meter used.",
        "Bus frequency too low in {loc}. Waiting {hours} hours.",
        "Bus condition poor in {loc}. Seats broken and dirty.",
        "Train compartment overcrowded in {loc}. Passengers uncomfortable.",
        "Metro fare too high in {loc}. Daily commuters affected.",
        "Bus stop shelter missing in {loc}. Commuters waiting in rain.",
        "Last mile connectivity poor in {loc}. No auto or bus from station.",
        "Ticket checker misbehaving in {loc}. Passengers harassed.",
        "Train cleanliness very poor in {loc}. Unbearable smell.",
        "Bus route changed without notice in {loc}. Commuters confused.",
        "Metro station not disabled-friendly in {loc}. Wheelchair access missing.",
        "Parking at railway station inadequate in {loc}. Vehicles towed.",
        "Bus not stopping at designated stop in {loc}. Passengers stranded.",
        "Train running late by {hours} hours in {loc}. Daily commuters suffering.",
        "Airport shuttle not available in {loc}. Travel difficult.",
        "Shared auto overcharging in {loc}. No regulation.",
    ]
}

def get_random_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

def get_random_email(name):
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'rediffmail.com']
    parts = name.lower().split()
    return f"{parts[0]}.{parts[1]}@{random.choice(domains)}"

def get_random_phone():
    return f"+91-{random.randint(70000, 99999)}-{random.randint(10000, 99999)}"

def generate_complaints(count=1200):
    complaints = []
    categories = list(CATEGORY_TEMPLATES.keys())
    
    for _ in range(count):
        category = random.choice(categories)
        templates = CATEGORY_TEMPLATES[category]
        template = random.choice(templates)
        
        loc = random.choice(LOCATIONS)
        days = random.randint(1, 30)
        hours = random.randint(1, 48)
        months = random.randint(1, 24)
        
        text = template.format(loc=loc, days=days, hours=hours, months=months)
        
        name = get_random_name()
        contact = get_random_email(name)
        location = loc
        
        complaints.append({
            'text': text,
            'complainant_name': name,
            'contact': contact,
            'location': location
        })
    
    return complaints

print("Generating 1200 diverse complaints...")
complaints = generate_complaints(1200)

print(f"Seeding database with {len(complaints)} complaints...")
for i, c in enumerate(complaints):
    try:
        result = ai.process_complaint(
            c['text'],
            complainant_name=c['complainant_name'],
            contact=c['contact'],
            location=c['location']
        )
        if (i + 1) % 100 == 0:
            print(f"[{i+1}/{len(complaints)}] ID: {result['complaint_id']} | {result['category']} | {result['severity']} | Score: {result['priority_score']}")
    except Exception as e:
        print(f"Error at {i+1}: {e}")

print(f"\nDatabase seeded successfully with {len(complaints)} complaints!")

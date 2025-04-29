# seed.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import (
    Base, Itinerary, Day, Accommodation, Activity, Transfer, DayAccommodation,
    DATABASE_URL
)

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_database():
    # Recreate tables for a clean seed
    print("Dropping and recreating database tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Tables created.")

    db = SessionLocal()

    try:
        print("Seeding base data (Accommodations, Activities, Transfers)...")
        # --- 1. Seed Accommodations ---
        acc_phuket_beach = Accommodation(name="Phuket Marriott Resort & Spa, Merlin Beach", location="Patong, Phuket", type="Resort", rating=5)
        acc_phuket_town = Accommodation(name="Casa Blanca Boutique Hotel", location="Phuket Town, Phuket", type="Hotel", rating=4)
        acc_krabi_ao_nang = Accommodation(name="Centara Ao Nang Beach Resort & Spa", location="Ao Nang, Krabi", type="Resort", rating=4)
        acc_krabi_railay = Accommodation(name="Rayavadee", location="Railay Beach, Krabi", type="Resort", rating=5)
        acc_phuket_kata = Accommodation(name="Katathani Phuket Beach Resort", location="Kata Noi Beach, Phuket", type="Resort", rating=5)
        acc_krabi_klong_muang = Accommodation(name="Dusit Thani Krabi Beach Resort", location="Klong Muang Beach, Krabi", type="Resort", rating=5)

        db.add_all([
            acc_phuket_beach, acc_phuket_town, acc_krabi_ao_nang,
            acc_krabi_railay, acc_phuket_kata, acc_krabi_klong_muang
        ])
        db.flush() # Flush to assign IDs before using them later

        # --- 2. Seed Activities ---
        act_phi_phi = Activity(name="Phi Phi Islands Day Tour", description="Full day tour by speedboat visiting Maya Bay, Pileh Lagoon, Viking Cave, Monkey Beach.", location="Phuket/Krabi", duration_hours=8, type="Tour")
        act_big_buddha = Activity(name="Visit Big Buddha & Wat Chalong", description="Explore the iconic Big Buddha statue and the historic Wat Chalong temple.", location="Phuket", duration_hours=4, type="Sightseeing")
        act_old_town = Activity(name="Explore Phuket Old Town", description="Wander through charming streets with Sino-Portuguese architecture, cafes, and shops.", location="Phuket Town, Phuket", duration_hours=3, type="Sightseeing")
        act_james_bond = Activity(name="James Bond Island (Phang Nga Bay) Tour", description="Visit the famous Khao Phing Kan, sea kayaking through caves.", location="Phang Nga Bay (from Phuket/Krabi)", duration_hours=8, type="Tour")
        act_railay_beach = Activity(name="Relax at Railay Beach", description="Enjoy the stunning limestone cliffs and clear waters, accessible only by boat.", location="Railay Beach, Krabi", duration_hours=5, type="Beach")
        act_krabi_4_islands = Activity(name="Krabi 4 Islands Tour", description="Longtail boat trip to Phra Nang Cave, Tup Island, Chicken Island, Poda Island.", location="Ao Nang, Krabi", duration_hours=6, type="Tour")
        act_kayaking = Activity(name="Sea Kayaking in Ao Thalane", description="Paddle through mangrove forests and hidden lagoons.", location="Ao Thalane, Krabi", duration_hours=4, type="Adventure")
        act_cooking_class = Activity(name="Thai Cooking Class", description="Learn to cook authentic Thai dishes.", location="Phuket/Krabi", duration_hours=4, type="Cultural")
        act_similan = Activity(name="Similan Islands Day Trip (Seasonal)", description="Snorkeling/diving in pristine waters (typically Nov-May).", location="From Phuket (Khao Lak Pier)", duration_hours=10, type="Tour")
        act_fantasea = Activity(name="Phuket FantaSea Show", description="Cultural theme park with extravagant show and buffet dinner.", location="Kamala, Phuket", duration_hours=4, type="Entertainment")


        db.add_all([
            act_phi_phi, act_big_buddha, act_old_town, act_james_bond,
            act_railay_beach, act_krabi_4_islands, act_kayaking,
            act_cooking_class, act_similan, act_fantasea
        ])
        db.flush()

        # --- 3. Seed Transfers ---
        trans_hkt_arrival = Transfer(description="Phuket Airport to Hotel Transfer", from_location="Phuket Airport (HKT)", to_location="Phuket Hotel", method="Private Car/Minivan", duration_minutes=60)
        trans_kbv_arrival = Transfer(description="Krabi Airport to Hotel Transfer", from_location="Krabi Airport (KBV)", to_location="Krabi Hotel", method="Private Car/Minivan", duration_minutes=45)
        trans_phuket_pier = Transfer(description="Phuket Hotel to Rassada Pier", from_location="Phuket Hotel", to_location="Rassada Pier, Phuket", method="Minivan", duration_minutes=45)
        trans_krabi_pier = Transfer(description="Ao Nang Hotel to Nopparat Thara Pier", from_location="Ao Nang Hotel", to_location="Nopparat Thara Pier, Krabi", method="Local Taxi/Songthaew", duration_minutes=15)
        trans_ferry_pk_kb = Transfer(description="Ferry Transfer Phuket to Krabi", from_location="Rassada Pier, Phuket", to_location="Klong Jilad Pier, Krabi", method="Ferry", duration_minutes=120)
        trans_ferry_kb_pk = Transfer(description="Ferry Transfer Krabi to Phuket", from_location="Klong Jilad Pier, Krabi", to_location="Rassada Pier, Phuket", method="Ferry", duration_minutes=120)
        trans_krabi_pier_hotel = Transfer(description="Krabi Pier to Hotel Transfer", from_location="Klong Jilad Pier, Krabi", to_location="Krabi Hotel", method="Minivan", duration_minutes=30)
        trans_phuket_pier_hotel = Transfer(description="Rassada Pier to Phuket Hotel", from_location="Rassada Pier, Phuket", to_location="Phuket Hotel", method="Minivan", duration_minutes=45)


        db.add_all([
            trans_hkt_arrival, trans_kbv_arrival, trans_phuket_pier, trans_krabi_pier,
            trans_ferry_pk_kb, trans_ferry_kb_pk, trans_krabi_pier_hotel, trans_phuket_pier_hotel
        ])
        db.commit() # Commit base data
        print("Base data seeded.")

        # --- 4. Seed Recommended Itineraries ---
        print("Seeding recommended itineraries...")

        # --- Itinerary 1: 3 Nights Phuket Explorer ---
        itinerary1 = Itinerary(
            name="Phuket Explorer (3 Nights)",
            duration_nights=3,
            region="Phuket",
            is_recommended=True
        )
        db.add(itinerary1)
        db.flush() # Get itinerary ID

        # Day 1: Arrival & Patong
        day1_1 = Day(itinerary_id=itinerary1.id, day_number=1, day_summary="Arrive in Phuket, transfer to Patong area.")
        db.add(day1_1)
        db.flush()
        day1_1.transfers.append(trans_hkt_arrival) # Arrival transfer
        day1_1_acc = DayAccommodation(day_id=day1_1.id, accommodation_id=acc_phuket_beach.id)
        db.add(day1_1_acc)

        # Day 2: Islands Tour
        day1_2 = Day(itinerary_id=itinerary1.id, day_number=2, day_summary="Full day exploring the stunning Phi Phi Islands.")
        db.add(day1_2)
        db.flush()
        day1_2.activities.append(act_phi_phi)
        day1_2_acc = DayAccommodation(day_id=day1_2.id, accommodation_id=acc_phuket_beach.id) # Same hotel
        db.add(day1_2_acc)


        # Day 3: Phuket Sights
        day1_3 = Day(itinerary_id=itinerary1.id, day_number=3, day_summary="Visit Big Buddha, Wat Chalong, and explore Phuket Town.")
        db.add(day1_3)
        db.flush()
        day1_3.activities.append(act_big_buddha)
        day1_3.activities.append(act_old_town)
        day1_3_acc = DayAccommodation(day_id=day1_3.id, accommodation_id=acc_phuket_beach.id) # Same hotel
        db.add(day1_3_acc)

        # Day 4: Departure (No activities/accommodation needed for the last day's *night*)
        day1_4 = Day(itinerary_id=itinerary1.id, day_number=4, day_summary="Departure from Phuket.")
        db.add(day1_4)
        db.flush()
        # Assuming departure transfer happens on this day
        # You might model transfers differently, e.g., linking them to the *end* of the previous day or start of current.
        # Let's add a placeholder transfer for departure on Day 4 for clarity.
        trans_hkt_departure = Transfer(description="Phuket Hotel to Airport Transfer", from_location="Phuket Hotel", to_location="Phuket Airport (HKT)", method="Private Car/Minivan", duration_minutes=60)
        db.add(trans_hkt_departure)
        db.flush()
        day1_4.transfers.append(trans_hkt_departure)

        # --- Itinerary 2: 5 Nights Phuket & Krabi ---
        itinerary2 = Itinerary(
            name="Phuket & Krabi Discovery (5 Nights)",
            duration_nights=5,
            region="Phuket & Krabi",
            is_recommended=True
        )
        db.add(itinerary2)
        db.flush()

        # Day 1: Phuket Arrival
        day2_1 = Day(itinerary_id=itinerary2.id, day_number=1, day_summary="Arrive Phuket, transfer to Kata Beach area.")
        db.add(day2_1)
        db.flush()
        day2_1.transfers.append(trans_hkt_arrival)
        day2_1_acc = DayAccommodation(day_id=day2_1.id, accommodation_id=acc_phuket_kata.id)
        db.add(day2_1_acc)

        # Day 2: Phuket - James Bond Island
        day2_2 = Day(itinerary_id=itinerary2.id, day_number=2, day_summary="Day trip to Phang Nga Bay (James Bond Island).")
        db.add(day2_2)
        db.flush()
        day2_2.activities.append(act_james_bond)
        day2_2_acc = DayAccommodation(day_id=day2_2.id, accommodation_id=acc_phuket_kata.id) # Same hotel
        db.add(day2_2_acc)

        # Day 3: Transfer to Krabi
        day2_3 = Day(itinerary_id=itinerary2.id, day_number=3, day_summary="Transfer from Phuket to Ao Nang, Krabi via ferry.")
        db.add(day2_3)
        db.flush()
        day2_3.transfers.append(trans_phuket_pier) # Hotel to Pier
        day2_3.transfers.append(trans_ferry_pk_kb) # Ferry
        day2_3.transfers.append(trans_krabi_pier_hotel) # Pier to Hotel
        day2_3_acc = DayAccommodation(day_id=day2_3.id, accommodation_id=acc_krabi_ao_nang.id) # Krabi hotel
        db.add(day2_3_acc)

        # Day 4: Krabi - 4 Islands Tour
        day2_4 = Day(itinerary_id=itinerary2.id, day_number=4, day_summary="Krabi 4 Islands tour by longtail boat.")
        db.add(day2_4)
        db.flush()
        day2_4.activities.append(act_krabi_4_islands)
        day2_4_acc = DayAccommodation(day_id=day2_4.id, accommodation_id=acc_krabi_ao_nang.id) # Same hotel
        db.add(day2_4_acc)

        # Day 5: Krabi - Railay Beach / Kayaking
        day2_5 = Day(itinerary_id=itinerary2.id, day_number=5, day_summary="Relax at Railay Beach or go sea kayaking.")
        db.add(day2_5)
        db.flush()
        day2_5.activities.append(act_railay_beach) # Could offer act_kayaking as alternative
        day2_5_acc = DayAccommodation(day_id=day2_5.id, accommodation_id=acc_krabi_ao_nang.id) # Same hotel
        db.add(day2_5_acc)

        # Day 6: Departure
        day2_6 = Day(itinerary_id=itinerary2.id, day_number=6, day_summary="Departure from Krabi.")
        db.add(day2_6)
        db.flush()
        trans_kbv_departure = Transfer(description="Krabi Hotel to Airport Transfer", from_location="Krabi Hotel", to_location="Krabi Airport (KBV)", method="Private Car/Minivan", duration_minutes=45)
        db.add(trans_kbv_departure)
        db.flush()
        day2_6.transfers.append(trans_kbv_departure)

        # --- Itinerary 2: Simple 2-night Phuket ---
        itinerary3 = Itinerary(name="Phuket Quick Escape (2 Nights)", duration_nights=2, region="Phuket", is_recommended=True)
        db.add(itinerary3)
        db.flush()
        # Day 1: Arrive, Big Buddha
        d3_1 = Day(itinerary_id=itinerary3.id, day_number=1); db.add(d3_1); db.flush()
        d3_1.transfers.append(trans_hkt_arrival)
        d3_1.activities.append(act_big_buddha)
        d3_1_acc = DayAccommodation(day_id=d3_1.id, accommodation_id=acc_phuket_town.id); db.add(d3_1_acc)
        # Day 2: Phi Phi
        d3_2 = Day(itinerary_id=itinerary3.id, day_number=2); db.add(d3_2); db.flush()
        d3_2.activities.append(act_phi_phi)
        d3_2_acc = DayAccommodation(day_id=d3_2.id, accommodation_id=acc_phuket_town.id); db.add(d3_2_acc)
        # Day 3: Depart
        d3_3 = Day(itinerary_id=itinerary3.id, day_number=3); db.add(d3_3); db.flush()
        d3_3.transfers.append(trans_hkt_departure) # Assuming same departure transfer instance is ok



        # --- Itinerary 4: 4 Nights Krabi Focus ---
        itinerary4 = db.query(Itinerary).filter_by(name="Krabi Castaway (4 Nights)").first()
        if not itinerary4:
            itinerary4 = Itinerary(name="Krabi Castaway (4 Nights)", duration_nights=4, region="Krabi", is_recommended=True)
            db.add(itinerary4); db.flush()
            # Day 1: Arrival Krabi, transfer to Ao Nang
            d4_1 = Day(itinerary_id=itinerary4.id, day_number=1); db.add(d4_1); db.flush()
            d4_1.transfers.append(trans_kbv_arrival)
            d4_1_acc = DayAccommodation(day_id=d4_1.id, accommodation_id=acc_krabi_ao_nang.id); db.add(d4_1_acc)
            # Day 2: 4 Islands Tour
            d4_2 = Day(itinerary_id=itinerary4.id, day_number=2); db.add(d4_2); db.flush()
            d4_2.activities.append(act_krabi_4_islands)
            d4_2_acc = DayAccommodation(day_id=d4_2.id, accommodation_id=acc_krabi_ao_nang.id); db.add(d4_2_acc)
            # Day 3: Railay Beach
            d4_3 = Day(itinerary_id=itinerary4.id, day_number=3); db.add(d4_3); db.flush()
            d4_3.activities.append(act_railay_beach)
            d4_3_acc = DayAccommodation(day_id=d4_3.id, accommodation_id=acc_krabi_ao_nang.id); db.add(d4_3_acc)
            # Day 4: Kayaking Ao Thalane
            d4_4 = Day(itinerary_id=itinerary4.id, day_number=4); db.add(d4_4); db.flush()
            d4_4.activities.append(act_kayaking)
            d4_4_acc = DayAccommodation(day_id=d4_4.id, accommodation_id=acc_krabi_ao_nang.id); db.add(d4_4_acc)
            # Day 5: Departure
            d4_5 = Day(itinerary_id=itinerary4.id, day_number=5); db.add(d4_5); db.flush()
            d4_5.transfers.append(trans_kbv_departure)

        # --- Itinerary 5: 6 Nights Phuket & Krabi Relax ---
        itinerary5 = db.query(Itinerary).filter_by(name="Phuket & Krabi Relaxation (6 Nights)").first()
        if not itinerary5:
            itinerary5 = Itinerary(name="Phuket & Krabi Relaxation (6 Nights)", duration_nights=6, region="Phuket & Krabi", is_recommended=True)
            db.add(itinerary5); db.flush()
            # Day 1: Phuket Arrival (Kata)
            d5_1 = Day(itinerary_id=itinerary5.id, day_number=1); db.add(d5_1); db.flush()
            d5_1.transfers.append(trans_hkt_arrival)
            d5_1_acc = DayAccommodation(day_id=d5_1.id, accommodation_id=acc_phuket_kata.id); db.add(d5_1_acc)
            # Day 2: Phuket Free Day / Old Town Optional
            d5_2 = Day(itinerary_id=itinerary5.id, day_number=2, day_summary="Free day at Kata Beach or optional visit to Old Town"); db.add(d5_2); db.flush()
            # d5_2.activities.append(act_old_town) # Optional
            d5_2_acc = DayAccommodation(day_id=d5_2.id, accommodation_id=acc_phuket_kata.id); db.add(d5_2_acc)
            # Day 3: Phuket - Phi Phi Islands
            d5_3 = Day(itinerary_id=itinerary5.id, day_number=3); db.add(d5_3); db.flush()
            d5_3.activities.append(act_phi_phi)
            d5_3_acc = DayAccommodation(day_id=d5_3.id, accommodation_id=acc_phuket_kata.id); db.add(d5_3_acc)
            # Day 4: Transfer to Krabi (Railay)
            d5_4 = Day(itinerary_id=itinerary5.id, day_number=4); db.add(d5_4); db.flush()
            d5_4.transfers.append(trans_phuket_pier); d5_4.transfers.append(trans_ferry_pk_kb); d5_4.transfers.append(trans_krabi_pier_hotel) # Adjust transfer if needed for Railay
            d5_4_acc = DayAccommodation(day_id=d5_4.id, accommodation_id=acc_krabi_railay.id); db.add(d5_4_acc)
            # Day 5: Krabi - Railay Beach / Relax
            d5_5 = Day(itinerary_id=itinerary5.id, day_number=5); db.add(d5_5); db.flush()
            d5_5.activities.append(act_railay_beach)
            d5_5_acc = DayAccommodation(day_id=d5_5.id, accommodation_id=acc_krabi_railay.id); db.add(d5_5_acc)
             # Day 6: Krabi - 4 Islands Tour
            d5_6 = Day(itinerary_id=itinerary5.id, day_number=6); db.add(d5_6); db.flush()
            d5_6.activities.append(act_krabi_4_islands)
            d5_6_acc = DayAccommodation(day_id=d5_6.id, accommodation_id=acc_krabi_railay.id); db.add(d5_6_acc)
            # Day 7: Departure Krabi
            d5_7 = Day(itinerary_id=itinerary5.id, day_number=7); db.add(d5_7); db.flush()
            d5_7.transfers.append(trans_kbv_departure) # Adjust if transfer from Railay needed

        # --- Itinerary 6: 7 Nights Southern Thailand Explorer ---
        # (Combine elements, maybe add Cooking Class or James Bond)
        itinerary6 = db.query(Itinerary).filter_by(name="Southern Thailand Explorer (7 Nights)").first()
        if not itinerary6:
            itinerary6 = Itinerary(name="Southern Thailand Explorer (7 Nights)", duration_nights=7, region="Phuket & Krabi", is_recommended=True)
            db.add(itinerary6); db.flush()
            # Day 1: Phuket Arrival (Patong)
            d6_1 = Day(itinerary_id=itinerary6.id, day_number=1); db.add(d6_1); db.flush(); d6_1.transfers.append(trans_hkt_arrival)
            d6_1_acc = DayAccommodation(day_id=d6_1.id, accommodation_id=acc_phuket_beach.id); db.add(d6_1_acc)
            # Day 2: James Bond Island Tour
            d6_2 = Day(itinerary_id=itinerary6.id, day_number=2); db.add(d6_2); db.flush(); d6_2.activities.append(act_james_bond)
            d6_2_acc = DayAccommodation(day_id=d6_2.id, accommodation_id=acc_phuket_beach.id); db.add(d6_2_acc)
            # Day 3: Big Buddha & Old Town
            d6_3 = Day(itinerary_id=itinerary6.id, day_number=3); db.add(d6_3); db.flush(); d6_3.activities.append(act_big_buddha); d6_3.activities.append(act_old_town)
            d6_3_acc = DayAccommodation(day_id=d6_3.id, accommodation_id=acc_phuket_beach.id); db.add(d6_3_acc)
            # Day 4: Transfer to Krabi (Ao Nang)
            d6_4 = Day(itinerary_id=itinerary6.id, day_number=4); db.add(d6_4); db.flush(); d6_4.transfers.append(trans_phuket_pier); d6_4.transfers.append(trans_ferry_pk_kb); d6_4.transfers.append(trans_krabi_pier_hotel)
            d6_4_acc = DayAccommodation(day_id=d6_4.id, accommodation_id=acc_krabi_ao_nang.id); db.add(d6_4_acc)
            # Day 5: Krabi 4 Islands
            d6_5 = Day(itinerary_id=itinerary6.id, day_number=5); db.add(d6_5); db.flush(); d6_5.activities.append(act_krabi_4_islands)
            d6_5_acc = DayAccommodation(day_id=d6_5.id, accommodation_id=acc_krabi_ao_nang.id); db.add(d6_5_acc)
            # Day 6: Railay Beach / Kayaking
            d6_6 = Day(itinerary_id=itinerary6.id, day_number=6); db.add(d6_6); db.flush(); d6_6.activities.append(act_railay_beach) # Or act_kayaking
            d6_6_acc = DayAccommodation(day_id=d6_6.id, accommodation_id=acc_krabi_ao_nang.id); db.add(d6_6_acc)
            # Day 7: Cooking Class / Free
            d6_7 = Day(itinerary_id=itinerary6.id, day_number=7, day_summary="Optional Thai Cooking Class or free day"); db.add(d6_7); db.flush(); # d6_7.activities.append(act_cooking_class)
            d6_7_acc = DayAccommodation(day_id=d6_7.id, accommodation_id=acc_krabi_ao_nang.id); db.add(d6_7_acc)
            # Day 8: Departure Krabi
            d6_8 = Day(itinerary_id=itinerary6.id, day_number=8); db.add(d6_8); db.flush(); d6_8.transfers.append(trans_kbv_departure)


        # --- Itinerary 7: 8 Nights Ultimate Adventure ---
        # (Add Similan or FantaSea if desired/seasonal)
        itinerary7 = db.query(Itinerary).filter_by(name="Ultimate Phuket & Krabi (8 Nights)").first()
        if not itinerary7:
            itinerary7 = Itinerary(name="Ultimate Phuket & Krabi (8 Nights)", duration_nights=8, region="Phuket & Krabi", is_recommended=True)
            db.add(itinerary7); db.flush()
            # Day 1: Phuket Arrival (Kata)
            d7_1 = Day(itinerary_id=itinerary7.id, day_number=1); db.add(d7_1); db.flush(); d7_1.transfers.append(trans_hkt_arrival)
            d7_1_acc = DayAccommodation(day_id=d7_1.id, accommodation_id=acc_phuket_kata.id); db.add(d7_1_acc)
            # Day 2: Similan Islands (Seasonal) or Phi Phi
            d7_2 = Day(itinerary_id=itinerary7.id, day_number=2); db.add(d7_2); db.flush(); d7_2.activities.append(act_phi_phi) # Use Similan if in season & defined
            d7_2_acc = DayAccommodation(day_id=d7_2.id, accommodation_id=acc_phuket_kata.id); db.add(d7_2_acc)
            # Day 3: James Bond Island
            d7_3 = Day(itinerary_id=itinerary7.id, day_number=3); db.add(d7_3); db.flush(); d7_3.activities.append(act_james_bond)
            d7_3_acc = DayAccommodation(day_id=d7_3.id, accommodation_id=acc_phuket_kata.id); db.add(d7_3_acc)
            # Day 4: Big Buddha / FantaSea
            d7_4 = Day(itinerary_id=itinerary7.id, day_number=4); db.add(d7_4); db.flush(); d7_4.activities.append(act_big_buddha); d7_4.activities.append(act_fantasea)
            d7_4_acc = DayAccommodation(day_id=d7_4.id, accommodation_id=acc_phuket_kata.id); db.add(d7_4_acc)
            # Day 5: Transfer Krabi (Klong Muang - different beach)
            d7_5 = Day(itinerary_id=itinerary7.id, day_number=5); db.add(d7_5); db.flush(); d7_5.transfers.append(trans_phuket_pier); d7_5.transfers.append(trans_ferry_pk_kb); d7_5.transfers.append(trans_krabi_pier_hotel) # Adjust transfer if needed
            d7_5_acc = DayAccommodation(day_id=d7_5.id, accommodation_id=acc_krabi_klong_muang.id); db.add(d7_5_acc)
            # Day 6: Krabi 4 Islands
            d7_6 = Day(itinerary_id=itinerary7.id, day_number=6); db.add(d7_6); db.flush(); d7_6.activities.append(act_krabi_4_islands)
            d7_6_acc = DayAccommodation(day_id=d7_6.id, accommodation_id=acc_krabi_klong_muang.id); db.add(d7_6_acc)
            # Day 7: Kayaking Ao Thalane
            d7_7 = Day(itinerary_id=itinerary7.id, day_number=7); db.add(d7_7); db.flush(); d7_7.activities.append(act_kayaking)
            d7_7_acc = DayAccommodation(day_id=d7_7.id, accommodation_id=acc_krabi_klong_muang.id); db.add(d7_7_acc)
            # Day 8: Railay Beach Visit
            d7_8 = Day(itinerary_id=itinerary7.id, day_number=8); db.add(d7_8); db.flush(); d7_8.activities.append(act_railay_beach)
            d7_8_acc = DayAccommodation(day_id=d7_8.id, accommodation_id=acc_krabi_klong_muang.id); db.add(d7_8_acc)
            # Day 9: Departure Krabi
            d7_9 = Day(itinerary_id=itinerary7.id, day_number=9); db.add(d7_9); db.flush(); d7_9.transfers.append(trans_kbv_departure)

            
        db.commit()
        print("Recommended itineraries seeded.")
        print("Database seeding completed successfully.")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
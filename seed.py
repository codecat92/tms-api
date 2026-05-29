from database import SessionLocal, engine, Base
from models import Driver, Route, Shipment, Fleet
from datetime import datetime, date

# Buat semua tabel kalau belum ada
Base.metadata.create_all(bind=engine)

db = SessionLocal()

def seed_fleet():
    fleets = [
        Fleet(plate_number="B 1234 ABC", vehicle_type="Truk Engkel", capacity_kg=5000, status="available", created_at=datetime.now()),
        Fleet(plate_number="B 5678 DEF", vehicle_type="Truk Fuso", capacity_kg=10000, status="available", created_at=datetime.now()),
        Fleet(plate_number="B 9012 GHI", vehicle_type="Truk Trailer", capacity_kg=20000, status="in_use", created_at=datetime.now()),
        Fleet(plate_number="D 3456 JKL", vehicle_type="Truk Engkel", capacity_kg=5000, status="maintenance", created_at=datetime.now()),
        Fleet(plate_number="D 7890 MNO", vehicle_type="Truk Fuso", capacity_kg=10000, status="available", created_at=datetime.now()),
    ]
    db.add_all(fleets)
    db.commit()
    print("✅ Fleet seeded!")

def seed_drivers():
    drivers = [
        Driver(name="Budi Santoso", license_number="SIM-B2-001", license_type="B2", license_expiry_date=date(2027, 12, 31), phone="081234567890", status="ACTIVE", fatigue_hours=4.5, total_trips=120, incident_count=0, created_at=datetime.now()),
        Driver(name="Fajar Anugrah", license_number="SIM-B2-002", license_type="B2", license_expiry_date=date(2026, 11, 30), phone="081878456790", status="ACTIVE", fatigue_hours=3.0, total_trips=85, incident_count=1, created_at=datetime.now()),
        Driver(name="Hendra Wijaya", license_number="SIM-B2-003", license_type="B2", license_expiry_date=date(2027, 6, 15), phone="082345678901", status="ACTIVE", fatigue_hours=7.5, total_trips=200, incident_count=2, created_at=datetime.now()),
        Driver(name="Rizky Pratama", license_number="SIM-B1-004", license_type="B1", license_expiry_date=date(2026, 3, 20), phone="083456789012", status="ACTIVE", fatigue_hours=2.0, total_trips=45, incident_count=0, created_at=datetime.now()),
        Driver(name="Deni Kurniawan", license_number="SIM-B2-005", license_type="B2", license_expiry_date=date(2027, 9, 10), phone="084567890123", status="INACTIVE", fatigue_hours=0.0, total_trips=150, incident_count=3, created_at=datetime.now()),
        Driver(name="Agus Setiawan", license_number="SIM-B1-006", license_type="B1", license_expiry_date=date(2027, 1, 5), phone="085678901234", status="ACTIVE", fatigue_hours=6.5, total_trips=90, incident_count=1, created_at=datetime.now()),
        Driver(name="Wahyu Hidayat", license_number="SIM-B2-007", license_type="B2", license_expiry_date=date(2026, 8, 22), phone="086789012345", status="SUSPENDED", fatigue_hours=0.0, total_trips=60, incident_count=5, created_at=datetime.now()),
        Driver(name="Eko Prasetyo", license_number="SIM-B2-008", license_type="B2", license_expiry_date=date(2027, 4, 18), phone="087890123456", status="ACTIVE", fatigue_hours=5.0, total_trips=180, incident_count=0, created_at=datetime.now()),
    ]
    db.add_all(drivers)
    db.commit()
    print("✅ Drivers seeded!")

def seed_routes():
    routes = [
        Route(name="Jakarta - Bandung", origin="Jakarta", destination="Bandung", zone="Jawa Barat", distance_km=150, estimated_duration_hours=3, base_cost=500000, created_at=datetime.now()),
        Route(name="Jakarta - Surabaya", origin="Jakarta", destination="Surabaya", zone="Jawa Timur", distance_km=780, estimated_duration_hours=12, base_cost=2500000, created_at=datetime.now()),
        Route(name="Jakarta - Semarang", origin="Jakarta", destination="Semarang", zone="Jawa Tengah", distance_km=450, estimated_duration_hours=7, base_cost=1500000, created_at=datetime.now()),
        Route(name="Bandung - Surabaya", origin="Bandung", destination="Surabaya", zone="Jawa Timur", distance_km=650, estimated_duration_hours=10, base_cost=2000000, created_at=datetime.now()),
        Route(name="Jakarta - Medan", origin="Jakarta", destination="Medan", zone="Sumatera Utara", distance_km=1400, estimated_duration_hours=24, base_cost=5000000, created_at=datetime.now()),
    ]
    db.add_all(routes)
    db.commit()
    print("✅ Routes seeded!")

def seed_shipments():
    shipments = [
        Shipment(reference="SH-001", fleet_id=1, driver_id=4, route_id=4, state="delivered", scheduled_date=datetime(2026, 5, 1, 8, 0), actual_departure=datetime(2026, 5, 1, 8, 30), actual_arrival=datetime(2026, 5, 1, 12, 0), total_weight_kg=3000, total_volume_m3=10, vso_rate=85.5, eta=datetime(2026, 5, 1, 11, 30), created_at=datetime.now()),
        Shipment(reference="SH-002", fleet_id=2, driver_id=5, route_id=5, state="delivered", scheduled_date=datetime(2026, 5, 3, 7, 0), actual_departure=datetime(2026, 5, 3, 7, 15), actual_arrival=datetime(2026, 5, 3, 20, 0), total_weight_kg=8000, total_volume_m3=25, vso_rate=90.0, eta=datetime(2026, 5, 3, 19, 0), created_at=datetime.now()),
        Shipment(reference="SH-003", fleet_id=3, driver_id=6, route_id=6, state="in_transit", scheduled_date=datetime(2026, 5, 29, 6, 0), total_weight_kg=15000, total_volume_m3=50, vso_rate=75.0, created_at=datetime.now()),
        Shipment(reference="SH-004", fleet_id=1, driver_id=7, route_id=4, state="confirmed", scheduled_date=datetime(2026, 5, 30, 8, 0), total_weight_kg=2000, total_volume_m3=8, vso_rate=80.0, created_at=datetime.now()),
        Shipment(reference="SH-005", fleet_id=5, driver_id=8, route_id=7, state="delivered", scheduled_date=datetime(2026, 5, 10, 7, 0), actual_departure=datetime(2026, 5, 10, 7, 30), actual_arrival=datetime(2026, 5, 10, 18, 0), total_weight_kg=7000, total_volume_m3=20, vso_rate=95.0, eta=datetime(2026, 5, 10, 17, 0), created_at=datetime.now()),
        Shipment(reference="SH-006", fleet_id=2, driver_id=9, route_id=5, state="delivered", scheduled_date=datetime(2026, 5, 15, 6, 0), actual_departure=datetime(2026, 5, 15, 6, 30), actual_arrival=datetime(2026, 5, 15, 19, 0), total_weight_kg=9000, total_volume_m3=30, vso_rate=88.0, eta=datetime(2026, 5, 15, 18, 0), created_at=datetime.now()),
        Shipment(reference="SH-007", fleet_id=3, driver_id=10, route_id=8, state="cancelled", scheduled_date=datetime(2026, 5, 20, 8, 0), total_weight_kg=18000, total_volume_m3=60, vso_rate=0.0, created_at=datetime.now()),
        Shipment(reference="SH-008", fleet_id=5, driver_id=11, route_id=6, state="draft", scheduled_date=datetime(2026, 6, 1, 8, 0), total_weight_kg=4000, total_volume_m3=15, vso_rate=70.0, created_at=datetime.now()),
    ]
    db.add_all(shipments)
    db.commit()
    print("✅ Shipments seeded!")

if __name__ == "__main__":
    print("🌱 Seeding database...")
    # seed_fleet()    ← skip, sudah ada!
    seed_drivers()
    seed_routes()
    seed_shipments()
    db.close()
    print("🎉 Database seeded successfully!")
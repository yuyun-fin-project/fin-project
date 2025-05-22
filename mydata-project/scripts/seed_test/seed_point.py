from app.core.database import SessionLocal
from app.models.point import Point

db = SessionLocal()

points = [
    Point(
        id="P001",
        user_id="user123",
        org_code="HANA",
        search_timestamp="20240517170000",
        point_name="하나멤버스 포인트",
        remain_point_amt=12000,
        expiring_point_amt=500
    )
]

try:
    for row in points:
        db.add(row)
    db.commit()
    print("✅ 포인트 더미 삽입 완료")
except Exception as e:
    db.rollback()
    print("❌ 에러:", e)
finally:
    db.close()

from app.core.database import SessionLocal
from app.models.user import User
from app.models.point import Point
from faker import Faker
import random
from datetime import datetime
import uuid

db = SessionLocal()
fake = Faker()
Faker.seed(123)

try:
    users = db.query(User).all()
    points = []

    for user in users:
        if random.random() < 0.6:  # 60% 확률로 포인트 보유
            points.append(Point(
                id=str(uuid.uuid4()),
                user_id=user.id,
                org_code=random.choice(["HANA", "KB", "SAMSUNG"]),
                search_timestamp=datetime.now().strftime("%Y%m%d%H%M%S"),
                point_name=random.choice(["하나멤버스", "탑포인트", "마이포인트"]),
                remain_point_amt=random.randint(5000, 50000),
                expiring_point_amt=random.randint(0, 3000)
            ))

    db.add_all(points)
    db.commit()
    print(f"✅ 포인트 정보 {len(points)}건 생성 완료")

except Exception as e:
    db.rollback()
    print("❌ 에러:", e)
finally:
    db.close()

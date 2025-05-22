from app.core.database import SessionLocal
from app.models.user import User
from app.models.prepaid_balance import PrepaidBalance
from app.models.prepaid_approval import PrepaidApproval
from faker import Faker
import random
from datetime import datetime, timedelta
import uuid

db = SessionLocal()
fake = Faker()
Faker.seed(777)

try:
    users = db.query(User).all()
    balances = []
    approvals = []

    for user in users:
        # 사용자별 1~2개 선불카드
        for i in range(random.randint(1, 2)):
            pp_id = f"PP_{uuid.uuid4().hex[:8]}"
            org_code = random.choice(["HANA", "KB", "TOSS"])
            search_timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

            # 잔액정보
            balances.append(PrepaidBalance(
                id=str(uuid.uuid4()),
                user_id=user.id,
                org_code=org_code,
                pp_id=pp_id,
                search_timestamp=search_timestamp,
                total_balance_amt=random.randint(10000, 50000),
                charge_balance_amt=random.randint(5000, 30000),
                reserve_balance_amt=random.randint(1000, 10000),
                reserve_due_amt=random.randint(500, 2000),
                exp_due_amt=random.randint(100, 1000)
            ))

            # 승인내역 10~15건
            for _ in range(random.randint(10, 15)):
                approved_time = fake.date_time_between(start_date="-4M", end_date="now")
                approvals.append(PrepaidApproval(
                    id=str(uuid.uuid4()),
                    user_id=user.id,
                    org_code=org_code,
                    pp_id=pp_id,
                    approved_dtime=approved_time.strftime("%Y%m%d%H%M"),
                    approved_num=f"PP{fake.unique.random_int(1000,9999)}",
                    status=random.choice(["01", "02"]),
                    pay_type=random.choice(["01", "02"]),
                    merchant_name=fake.company() + " " + fake.city(),
                    merchant_regno=fake.bothify(text="###-##-#####"),
                    approved_amt=random.randint(500, 30000)
                ))

    db.add_all(balances + approvals)
    db.commit()
    print(f"✅ 선불 잔액 {len(balances)}건, 승인내역 {len(approvals)}건 생성 완료")


except Exception as e:
    db.rollback()
    print("❌ 에러:", e)
finally:
    db.close()

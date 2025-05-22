import subprocess

scripts = [
    "./generate_dummy/generate_dummy_users_and_cards.py",
    "./generate_dummy/generate_dummy_bills.py",
    "./generate_dummy/generate_dummy_approvals.py",
    "./generate_dummy/generate_dummy_points.py",
    "./generate_dummy/generate_dummy_loans.py",
    "./generate_dummy/generate_dummy_prepaid.py"
]

for script in scripts:
    print(f"🚀 {script} 실행 중...")
    subprocess.run(["python", f"scripts/{script}"])

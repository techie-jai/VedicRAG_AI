import os
import shutil

dharmaganj = 'dharmaganj'

buildings = {
    'ratnodadhi': ['srimadbhagavadgita', 'srimadbhagavatam', 'vishnupuranam'],
    'ratnasagara': ['ashtadhyayi', 'natyashastram', 'kosha', 'dhatu', 'chhanda', 'chandraloka', 'shringaraprakash'],
    'ratnaranjaka': ['amarushatakam', 'anyapadeshashatakam', 'bhattikavyam', 'hamsadutam', 'kadambarisangraha', 'kathasaritsagara', 'kiratarjuniyam', 'kumarasambhavam', 'mahabharatam', 'mahasubhashitasangraha', 'meghadutam', 'naishadhiyacaritam', 'nilakanthavijayachampu', 'pancatantram', 'raghuvansham', 'ramayanam', 'rtusamharam', 'shakuntalam', 'shatakatrayam', 'shishupalavadham']
}

for building, folders in buildings.items():
    building_path = os.path.join(dharmaganj, building)
    os.makedirs(building_path, exist_ok=True)
    for folder in folders:
        src = os.path.join(dharmaganj, folder)
        dst = os.path.join(building_path, folder)
        if os.path.exists(src):
            shutil.move(src, dst)
            print(f"Moved {folder} to {building}")
        else:
            print(f"{src} does not exist")

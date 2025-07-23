import instaloader

L = instaloader.Instaloader()

# Login manual dulu (masukin username & password)
USERNAME = 'rey_scrape'
PASSWORD = 'SPGF12345'
L.login(USERNAME, PASSWORD)

# Simpan sesi biar nggak login ulang terus
L.save_session_to_file('data_collection/rey_scrape')

import sqlite3

database_path = 'data.db'

def connect_to_database(database_path):
    try:
        connection = sqlite3.connect(database_path)
        return connection
    except sqlite3.Error as e:
        print(f"Error koneksi ke database: {e}")
        return None

def display_mahasiswa_data(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM mahasiswa")     
        rows = cursor.fetchall()        
        column_names = [description[0] for description in cursor.description]
        
        print("\n--- DATA MAHASISWA ---")
        print(" | ".join(column_names))
        print("-" * 70)  # Separator line
        for row in rows:
            print(" | ".join(str(item) for item in row))
        
        print(f"\nTotal records: {len(rows)}")
    except sqlite3.Error as e:
        print(f"Error menampilkan data: {e}")
    finally:
        if cursor:
            cursor.close()

def add_mahasiswa_data(connection):
    try:
        cursor = connection.cursor()
        
        # Prompt for input
        nim = input("Masukkan (NIM): ")
        nama = input("Masukkan Nama: ")
        prodi = input("Masukkan Kode Program Studi: ")
        
        # Gender selection with validation
        while True:
            jk = input("Masukkan Jenis Kelamin (L/P): ").upper()
            if jk in ['L', 'P']:
                break
            print("Input JK salah. Gunakan L untuk Laki-laki atau P untuk Perempuan.")
        
        # Execute insert query
        cursor.execute("""
            INSERT INTO mahasiswa (nim, nama, prodi, jk) 
            VALUES (?, ?, ?, ?)
        """, (nim, nama, prodi, jk))
        
        # Commit the transaction
        connection.commit()
        print("\nData mahasiswa berhasil disimpan!")
    except sqlite3.Error as e:
        print(f"Error menambah data mahasiswa: {e}")
        connection.rollback()
    finally:
        if cursor:
            cursor.close()

def edit_mahasiswa_data(connection):
    try:
        cursor = connection.cursor()
        
        # First, show existing data
        display_mahasiswa_data(connection)
        
        # Prompt for the NIM to edit
        nim_to_edit = input("\nMasukkan NIM untuk diedit: ")
        
        # Check if the student exists
        cursor.execute("SELECT * FROM mahasiswa WHERE nim = ?", (nim_to_edit,))
        student = cursor.fetchone()
        
        if student:
            # Prompt for new information
            new_nama = input(f"Masukkan Nama baru (saat ini: {student[1]}), atau tekan Enter tanpa mengubah: ")
            new_prodi = input(f"Masukkan Prodi baru (saat ini: {student[2]}), atau tekan Enter tanpa mengubah: ")
            
            # Gender selection with validation
            while True:
                new_jk = input(f"Masukkan jenis kelamin (saat ini: {student[3]}, L/P), atau tekan Enter tanpa mengubah: ").upper()
                if new_jk == '' or new_jk in ['L', 'P']:
                    break
                print("Input JK salah. Gunakan L untuk Laki-laki atau P untuk Perempuan.")
            
            # Use existing value if no new input is provided
            new_nama = new_nama if new_nama else student[1]
            new_prodi = new_prodi if new_prodi else student[2]
            new_jk = new_jk if new_jk else student[3]
            
            # Update the record
            cursor.execute("""
                UPDATE mahasiswa 
                SET nama = ?, prodi = ?, jk = ? 
                WHERE nim = ?
            """, (new_nama, new_prodi, new_jk, nim_to_edit))
            connection.commit()
            print("\nData mahasiswa berhasil diperbarui!")
        else:
            print("\nNIM mahasiswa tidak ditemukan.")
    except sqlite3.Error as e:
        print(f"Error editing student data: {e}")
        connection.rollback()
    finally:
        if cursor:
            cursor.close()

def delete_mahasiswa_data(connection):
    try:
        cursor = connection.cursor()
        
        # First, show existing data
        display_mahasiswa_data(connection)
        
        # Prompt for the NIM to delete
        nim_to_delete = input("\nMasukkan NIM mahasiswa yang akan dihapus: ")
        
        # Confirm deletion
        confirm = input(f"Apakah Anda yakin akan menghapus data mahasiswa dengan NIM {nim_to_delete}? (yes/no): ")
        
        if confirm.lower() == 'yes':
            # Execute delete query
            cursor.execute("DELETE FROM mahasiswa WHERE nim = ?", (nim_to_delete,))
            
            # Check if any row was actually deleted
            if cursor.rowcount > 0:
                connection.commit()
                print("\ndata mahasiswa berhasil dihapus!")
            else:
                print("\nNIM mahasiswa tidak ditemukan.")
        else:
            print("\nHapus data dibatalkan.")
    except sqlite3.Error as e:
        print(f"Error menghapus data mahasiswa: {e}")
        connection.rollback()
    finally:
        if cursor:
            cursor.close()

def main_menu():
    connection = connect_to_database(database_path)
    
    if not connection:
        print("Maaf, gagal koneksi database.")
        return
    
    while True:
        print("\n--- KELOLA DATA MAHASISWA ---")
        print("1. Tampilkan Semua Data Mahasiswa")
        print("2. Tambah Data Mahasiswa")
        print("3. Edit Data Mahasiswa")
        print("4. Delete Data Mahasiswa")
        print("5. Keluar")
        
        choice = input("Pilihan Anda (1-5): ")
        
        if choice == '1':
            display_mahasiswa_data(connection)
        elif choice == '2':
            add_mahasiswa_data(connection)
        elif choice == '3':
            edit_mahasiswa_data(connection)
        elif choice == '4':
            delete_mahasiswa_data(connection)
        elif choice == '5':
            print("Keluar dari program.")
            break
        else:
            print("Pilihan salah. Coba lagi.")
    
    # Close the database connection
    if connection:
        connection.close()

if __name__ == '__main__':
    main_menu()
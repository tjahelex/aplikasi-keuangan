import csv

def menu():
    print("\n=== Aplikasi Keuangan ===")
    print("1. Tambah Pemasukan")
    print("2. Tambah Pengeluaran")
    print("3. Lihat Laporan")
    print("4. Cek Saldo")
    print("5. keluar")
    return input("Pilih menu (1-5): ")

def add_transaction(transactions, transaction_type):
    while True:
        try:
            amount = float(input("Masukkan jumlah (harus angka positif): "))
            if amount <= 0:
                print("Jumalah harus lebih besar dari 0. Coba lagi!.")
                continue
            break
        except ValueError:
            print("Input tidak valid. Masukkan angka yang benar.")

    category = input("Masukkan kategori: ")
    note = input("Tambahkan catatan: ")
    transactions.append({
        "type": transaction_type,
        "amount": amount,
        "category": category,
        "note": note
    })
    print(f"{transaction_type.capitalize()} berhasil ditambahkan!")
    # Simpan transaksi ke CSV
    save_to_csv(transactions)

def view_report(transactions):
    category_totals = {}
    for t in transactions:
        category = t["category"]
        amount = t["amount"]
        if t["type"] == "expense":
            amount *= -1
        category_totals[category] = category_totals.get(category, 0) + amount

    print("\n=== Laporan Keuangan ===")
    for category, total in category_totals.items():
        print(f"{category}: {total}")

def check_balance(transactions):
    balance = 0
    for t in transactions:
        if t["type"] == "income":
            balance += t["amount"]
        elif t["type"] == "expense":
            balance -= t["amount"]
    print(f"\nTotal saldo saat ini: {balance}")

def main():
    transactions = load_from_csv()
    while True:
        choice = menu()
        if choice == "1":
            add_transaction(transactions, "income")
        elif choice == "2":
            add_transaction(transactions, "expense")
        elif choice == "3":
            view_report(transactions)
        elif choice == "4":
            check_balance(transactions)
        elif choice == "5":
            print("Terima kasih telah menggunakan aplikasi!")
            break
        else:
            print("Pilihan tidak valid. Coba lagi.")

def save_to_csv(transactions, filename="transactions.csv"):
    # Membuka file dalam mode tulis
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        # Menulis header
        writer.writerow(["Type", "Amount", "Category", "Note"])
        # Menulis data transaksi
        for transaction in transactions:
            writer.writerow([transaction["type"], transaction["amount"], transaction["category"], transaction["note"]])
    print(f"Data berhasil disimpan ke {filename}")

def load_from_csv(filename="transactions.csv"):
    transactions = []
    try:
        with open(filename, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                transactions.append({
                    "type": row["Type"],
                    "amount": float(row["Amount"]),
                    "category": row["Category"],
                    "note": row["Note"],
                })
    except FileNotFoundError:
        print(f"File {filename} tidak ditemukan. Memulai dengan data kosong.")
    return transactions

if __name__ == "__main__":
    main()
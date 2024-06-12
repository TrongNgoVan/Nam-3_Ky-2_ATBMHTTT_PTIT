import tkinter as tk

def create_substitution_table(key):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    key = ''.join(sorted(set(key), key=key.index))  # Loại bỏ các ký tự trùng lặp trong khóa
    substitution_table = key + ''.join([char for char in alphabet if char not in key])
    return {alphabet[i]: substitution_table[i] for i in range(len(alphabet))}

def substitution_cipher_encrypt(plain_text, key):
    substitution_table = create_substitution_table(key)
    encrypted_text = ''
    for char in plain_text:
        if char.isalpha():
            char_lower = char.lower()
            encrypted_char = substitution_table[char_lower]
            if char.isupper():
                encrypted_text += encrypted_char.upper()
            else:
                encrypted_text += encrypted_char
        else:
            encrypted_text += char
    return encrypted_text

def encrypt_and_display():
    plain_text = entry_plain_text.get()
    key = entry_key.get().lower()

    if not key.isalpha():
        result_text.set("Khóa phải chỉ chứa các chữ cái.")
        return

    encrypted_text = substitution_cipher_encrypt(plain_text, key)
    result_text.set(encrypted_text)

root = tk.Tk()
root.title("Phương pháp thay thế")
root.geometry("600x200")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

label_plain_text = tk.Label(frame, text="Văn bản cần mã hóa:")
label_plain_text.grid(row=0, column=0, sticky=tk.W)
entry_plain_text = tk.Entry(frame, width=50)
entry_plain_text.grid(row=0, column=1, padx=5, pady=5)

label_key = tk.Label(frame, text="Khóa (chuỗi ký tự):")
label_key.grid(row=1, column=0, sticky=tk.W)
entry_key = tk.Entry(frame, width=50)
entry_key.grid(row=1, column=1, padx=5, pady=5)

button_encrypt = tk.Button(frame, text="Mã hóa", command=encrypt_and_display)
button_encrypt.grid(row=2, column=1, pady=10)

result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text)
result_label.pack()

root.mainloop()

import os
import tkinter as tk
from tkinter import filedialog
import fitz  # PyMuPDF
import re

def read_pdf_by_pages(file_path):
    # Đọc nội dung của PDF và lưu vào danh sách các trang, mỗi trang là một danh sách các dòng
    document = fitz.open(file_path)
    book_content = []
    page_number_pattern = re.compile(r'^\s*\d+\s*$')  # Regex để phát hiện dòng chỉ chứa số trang

    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        text = page.get_text("text")
        lines = text.split('\n')
        # Loại bỏ các dòng trống và các dòng chỉ chứa số trang
        lines = [line for line in lines if line.strip() != '' and not page_number_pattern.match(line)]
        # Chia từng dòng thành mảng các từ
        lines = [line.split(' ') for line in lines]
        book_content.append(lines)
    return book_content

def decode_message(book_content, coded_message):
    decoded_words = []
    # Tách các phần tử của bản mã
    entries = coded_message.split(';')
    for entry in entries:
        page, line, word_index = map(int, entry.split(','))
        # page -= 1
        line -= 1
        word_index -= 1
        decoded_words.append(book_content[page][line][word_index])
    return ' '.join(decoded_words)

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
    if file_path:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, file_path)

def decrypt_and_display():
    file_path = entry_file_path.get()
    keys_input = entry_keys.get()
    
    if not os.path.isfile(file_path):
        result_label.config(text="File not found.")
        return
    
    # Đọc nội dung của tệp PDF
    book_content = read_pdf_by_pages(file_path)
    
    # Giải mã và hiển thị kết quả
    decoded_message = decode_message(book_content, keys_input)
    result_label.config(text=decoded_message)

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Nhóm 9: Mã hóa bằng phương pháp sách")
root.geometry("600x200") 

# Tạo và bố trí các widget
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

label_file_path = tk.Label(frame, text="Nhập đường dẫn(PDF):")
label_file_path.grid(row=0, column=0, sticky=tk.W)
entry_file_path = tk.Entry(frame, width=50)
entry_file_path.grid(row=0, column=1, padx=5, pady=5)
button_browse = tk.Button(frame, text="Input", command=select_file)
button_browse.grid(row=0, column=2, padx=5, pady=5)

label_keys = tk.Label(frame, text="Định dạng khóa ( a1,b1,c1;a2,b2,c2;...) :")
label_keys.grid(row=1, column=0, sticky=tk.W)
entry_keys = tk.Entry(frame, width=50)
entry_keys.grid(row=1, column=1, padx=5, pady=5)

button_decrypt = tk.Button(frame, text="Giải mã", command=decrypt_and_display)
button_decrypt.grid(row=2, column=1, pady=10)

result_label = tk.Label(root, text="Đáp án:")
result_label.pack()

# Chạy vòng lặp chính
root.mainloop()

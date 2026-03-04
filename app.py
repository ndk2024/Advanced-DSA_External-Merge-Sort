import tkinter as tk
from tkinter import filedialog, messagebox
import os
import array
import tempfile
import struct
import heapq

class SortingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng Sắp xếp Tập tin Nhị phân (External Sort)")
        self.root.geometry("750x550")

        self.btn_select = tk.Button(root, text="Chọn tập tin dữ liệu nguồn (.bin)", command=self.process_file, bg="#008CBA", fg="white", font=("Arial", 12, "bold"))
        self.btn_select.pack(pady=15)

        self.text_area = tk.Text(root, height=25, width=90, font=("Consolas", 10))
        self.text_area.pack(pady=10)

    def log_text(self, text):
        """Hàm hỗ trợ in chữ ra màn hình và tự động cuộn xuống dưới"""
        self.text_area.insert(tk.END, text)
        self.text_area.see(tk.END)
        self.root.update() # Cập nhật giao diện ngay lập tức để không bị đơ

    def process_file(self):
        filepath = filedialog.askopenfilename(title="Chọn file", filetypes=[("Binary files", "*.bin"), ("All files", "*.*")])
        if not filepath:
            return

        self.text_area.delete(1.0, tk.END)
        self.log_text(f"Đang phân tích file: {os.path.basename(filepath)}\n")

        file_size = os.path.getsize(filepath)
        num_elements = file_size // 8 # Mỗi số double chiếm 8 bytes

        if num_elements == 0:
            self.log_text("File rỗng hoặc không hợp lệ!\n")
            return

        self.log_text(f"Tổng số phần tử (double): {num_elements}\n")
        self.log_text("-" * 60 + "\n")

        # NẾU FILE NHỎ (<= 15 phần tử): Dùng External Merge Sort có minh họa
        if num_elements <= 15:
            self.log_text("Kích thước file nhỏ -> Chế độ minh họa SẮP XẾP NGOÀI (External Merge Sort).\n")
            self.log_text("Giả lập giới hạn RAM ảo: Chỉ nạp tối đa 5 phần tử mỗi lần đọc.\n\n")
            # Gọi hàm với chunk_size nhỏ (ví dụ 5) và bật cờ minh họa
            self.external_merge_sort(filepath, chunk_size=5, illustrate=True)
        
        # NẾU FILE LỚN: Dùng External Merge Sort tốc độ cao, không minh họa chi tiết
        else:
            self.log_text("Kích thước file lớn -> Kích hoạt Sắp xếp ngoài tốc độ cao.\n\n")
            # Gọi hàm với chunk_size lớn (ví dụ 100,000) và tắt cờ minh họa
            self.external_merge_sort(filepath, chunk_size=100000, illustrate=False)

    def external_merge_sort(self, filepath, chunk_size, illustrate):
        """Sắp xếp ngoài sử dụng External Merge Sort, có hỗ trợ minh họa trực quan"""
        temp_files = []

        # --- GIAI ĐOẠN 1: Chia nhỏ file thành các Chunk đã sắp xếp ---
        self.log_text("[GIAI ĐOẠN 1] Cắt file lớn thành các file tạm (Chunks) và sắp xếp...\n")
        with open(filepath, 'rb') as f:
            chunk_index = 1
            while True:
                bytes_data = f.read(chunk_size * 8) # Đọc chunk
                if not bytes_data:
                    break
                
                # Chuyển byte thô thành mảng số thực
                arr = array.array('d')
                arr.frombytes(bytes_data)
                lst = arr.tolist()
                
                if illustrate:
                    self.log_text(f"\n --- Đang xử lý Chunk {chunk_index} --- \n")
                    self.log_text(f" 1. Đọc vào RAM: [{', '.join(f'{x:.2f}' for x in lst)}]\n")
                
                # Sắp xếp in-memory siêu tốc của Python
                lst.sort() 
                
                if illustrate:
                    self.log_text(f" 2. Sắp xếp trong RAM: [{', '.join(f'{x:.2f}' for x in lst)}]\n")
                
                # Tạo file tạm và ghi dữ liệu đã sắp xếp vào
                fd, temp_name = tempfile.mkstemp(suffix='.bin')
                with os.fdopen(fd, 'wb') as tf:
                    sorted_arr = array.array('d', lst)
                    tf.write(sorted_arr.tobytes())
                
                temp_files.append(temp_name)
                if not illustrate:
                    self.log_text(f"  -> Đã tạo và sắp xếp chunk thứ {chunk_index} ({len(lst)} phần tử).\n")
                else:
                    self.log_text(f" 3. Đã ghi chunk này ra file tạm: temp_chunk_{chunk_index}.bin\n")
                
                chunk_index += 1

        # --- GIAI ĐOẠN 2: Trộn nhiều luồng (K-Way Merge) sử dụng Min-Heap ---
        self.log_text(f"\n[GIAI ĐOẠN 2] Trộn (K-Way Merge) {len(temp_files)} file tạm...\n")
        out_filepath = filepath + ".sorted.bin"
        
        # Mở tất cả các file tạm để đọc
        file_pointers = [open(tf, 'rb') for tf in temp_files]
        min_heap = []
        
        # Đưa phần tử đầu tiên của mỗi file tạm vào Min-Heap
        for i, fp in enumerate(file_pointers):
            bytes_data = fp.read(8)
            if bytes_data:
                val = struct.unpack('d', bytes_data)[0]
                heapq.heappush(min_heap, (val, i)) # Lưu tuple (Giá trị, Chỉ số_file_nguồn)
                if illustrate:
                    self.log_text(f" -> Nạp {val:.2f} từ temp_chunk_{i+1}.bin vào Min-Heap.\n")

        if illustrate:
            self.log_text("\n Bắt đầu rút phần tử nhỏ nhất từ Min-Heap ra file kết quả:\n")

        # Rút dần phần tử nhỏ nhất từ Heap ghi ra file, sau đó bổ sung phần tử tiếp theo từ file tương ứng
        count = 0
        merged_result = [] # Chỉ dùng để lưu tạm in log khi illustrate = True

        with open(out_filepath, 'wb') as out_f:
            while min_heap:
                val, file_index = heapq.heappop(min_heap)
                out_f.write(struct.pack('d', val))
                count += 1
                
                if illustrate:
                    merged_result.append(f"{val:.2f}")
                    self.log_text(f"  + Rút {val:.2f} (từ chunk {file_index+1}) -> Ghi ra file.\n")

                # Đọc phần tử tiếp theo từ chính file tạm vừa bị lấy mất phần tử
                next_bytes = file_pointers[file_index].read(8)
                if next_bytes:
                    next_val = struct.unpack('d', next_bytes)[0]
                    heapq.heappush(min_heap, (next_val, file_index))
                    if illustrate:
                        self.log_text(f"    * Bổ sung {next_val:.2f} (từ chunk {file_index+1}) vào Heap.\n")

        # --- DỌN DẸP: Đóng và xóa các file tạm ---
        for fp in file_pointers:
            fp.close()
        for tf in temp_files:
            os.remove(tf)
            
        if illustrate:
            self.log_text(f"\n[KẾT QUẢ CUỐI CÙNG TRONG FILE]\n[{', '.join(merged_result)}]\n")

        self.log_text(f"\nHoàn tất! Đã sắp xếp xong {count} phần tử.\n")
        self.log_text(f"File kết quả lưu tại:\n{out_filepath}\n")
        messagebox.showinfo("Thành công", f"Đã sắp xếp file hoàn tất!\n{count} phần tử.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingApp(root)
    root.mainloop()
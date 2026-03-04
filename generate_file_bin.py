import random
import struct
import array
import os
import time

def create_small_file(filename="small_test.bin"):
    print(f"Đang tạo file nhỏ: {filename}...")
    # Dữ liệu mẫu (10 phần tử)
    data = [45.2, 12.8, 9.5, 88.1, 3.14, 27.6, 2.71, 100.0, 0.5, 50.5]
    
    with open(filename, "wb") as f:
        for val in data:
            f.write(struct.pack('d', val))
    
    print(f"-> Đã tạo xong {filename} (10 phần tử).\n")

def create_large_file(filename="large_test.bin", num_elements=1000000):
    print(f"Đang tạo file lớn: {filename} ({num_elements} phần tử)...")
    start_time = time.time()
    
    # Dùng array để thao tác với binary siêu nhanh
    arr = array.array('d')
    
    # Sinh ngẫu nhiên num_elements số thực
    for _ in range(num_elements):
        arr.append(random.uniform(0.0, 10000.0))
        
    with open(filename, "wb") as f:
        f.write(arr.tobytes())
        
    end_time = time.time()
    size_mb = os.path.getsize(filename) / (1024 * 1024)
    print(f"-> Đã tạo xong {filename} ({size_mb:.2f} MB) trong {end_time - start_time:.2f} giây.\n")

if __name__ == "__main__":
    print("=== TRÌNH TẠO DỮ LIỆU TEST NHỊ PHÂN ===\n")
    create_small_file()
    create_large_file()
    print("Hoàn tất! Bạn có thể dùng các file .bin này để đưa vào ứng dụng chính.")
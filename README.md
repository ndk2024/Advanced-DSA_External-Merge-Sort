# Ứng Dụng Sắp Xếp Tập Tin Nhị Phân (External Merge Sort)

Ứng dụng trực quan hóa và xử lý sắp xếp các tập tin dữ liệu nhị phân chứa các số thực (Double - 8 bytes) theo thứ tự tăng dần. Chương trình tự động nhận diện kích thước tập tin để áp dụng chiến lược sắp xếp phù hợp, có hỗ trợ minh họa từng bước đối với tập tin kích thước nhỏ.

## 🗂 Cấu trúc dự án

* `app.py`: Mã nguồn chính chứa giao diện (GUI) và thuật toán xử lý (External Merge Sort).
* `generate_file_bin.py`: Script hỗ trợ người dùng tự sinh ra các tập tin nhị phân chứa dữ liệu ngẫu nhiên để test.
* `small_test.bin`: Tập tin dữ liệu mẫu kích thước nhỏ (dùng để xem minh họa quá trình chia/trộn file).
* `large_test.bin`: Tập tin dữ liệu mẫu kích thước lớn (dùng để test hiệu năng sắp xếp ngoài).
* `EMS.exe`: (Nằm trong mục Releases) Ứng dụng đã được đóng gói, chạy ngay không cần cài đặt Python.

## 🚀 Hướng dẫn chạy chương trình

### Cách 1: Chạy file thực thi (Dành cho người dùng cuối)
Chỉ cần tải file `EMS.exe` về máy tính (Windows) và nhấp đúp chuột để khởi động giao diện.

### Cách 2: Chạy từ mã nguồn (Dành cho Developer)
Yêu cầu hệ thống đã cài đặt Python 3.x.
1. Mở Terminal / Command Prompt.
2. Di chuyển đến thư mục chứa mã nguồn.
3. Chạy lệnh:
   ```bash
   python app.py

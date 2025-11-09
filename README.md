# Thuật Toán Tìm Đường Đi (Pathfinding Algorithms)

Dự án này là một ứng dụng trực quan để so sánh các thuật toán tìm đường đi phổ biến: BFS, Dijkstra và A*.

## Cài Đặt

1. Clone repository này
2. Tạo môi trường ảo Python:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
3. Cài đặt thư viện cần thiết:
```bash
pip install -r requirements.txt
```

## Chạy Chương Trình

```bash
python main.py
```

## Điều Khiển

- **Chuột Trái**: Thêm tường/trọng số
- **Chuột Phải**: Xóa tường/trọng số
- **S + Click**: Đặt điểm xuất phát
- **E + Click**: Đặt điểm đích
- **1**: Chạy thuật toán BFS
- **2**: Chạy thuật toán Dijkstra
- **3**: Chạy thuật toán A*
- **W**: Bật/tắt chế độ thêm trọng số
- **D**: Bật/tắt di chuyển chéo
- **G**: Tạo chướng ngại vật ngẫu nhiên
- **C**: Xóa kết quả tìm kiếm
- **R**: Đặt lại toàn bộ bản đồ
- **ESC/Q**: Thoát chương trình

## Giải Thích Thuật Toán

### 1. BFS (Breadth-First Search)
- Tìm kiếm theo chiều rộng
- Khám phá tất cả các ô theo từng lớp
- Đảm bảo tìm ra đường đi ngắn nhất (số bước đi)
- Không xét đến trọng số

### 2. Dijkstra
- Tìm đường đi ngắn nhất có xét đến trọng số
- Mở rộng theo thứ tự chi phí tăng dần
- Tối ưu cho đồ thị có trọng số
- Đảm bảo tìm ra đường đi có tổng chi phí thấp nhất

### 3. A* (A-star)
- Cải tiến của Dijkstra với heuristic
- Sử dụng hàm đánh giá f(n) = g(n) + h(n)
  - g(n): chi phí thực từ điểm xuất phát đến n
  - h(n): ước lượng chi phí từ n đến đích
- Hiệu quả hơn Dijkstra vì có định hướng tìm kiếm
- Sử dụng heuristic Manhattan cho 4 hướng và Octile cho 8 hướng

## Màu Sắc
- 🟦 Xanh dương: Các ô đang xét (frontier)
- 🟪 Tím: Các ô đã xét (visited)
- 🟨 Vàng: Đường đi tìm được
- 🟩 Xanh lá: Điểm xuất phát
- 🟥 Đỏ: Điểm đích
- ⬛ Đen: Tường
- 🟫 Nâu: Ô có trọng số

## Cấu Trúc Project

```
a_start_project/
├── main.py         # Chương trình chính
├── visual.py       # Giao diện đồ họa
├── grid.py         # Cấu trúc lưới và ô
├── algorithms.py   # Các thuật toán tìm đường
├── heuristics.py   # Hàm heuristic cho A*
└── constants.py    # Các hằng số và màu sắc
```

## Thống Kê

Chương trình hiển thị các thông số:
- Thuật toán đang sử dụng
- Số ô đã mở rộng
- Thời gian thực thi
- Chi phí đường đi
- Độ dài đường đi
- Chế độ di chuyển (4 hoặc 8 hướng)

# FindingPath

Dự án trình diễn so sánh các thuật toán tìm đường (BFS, DFS, Dijkstra, UCS, Greedy Best-First, A*) trên mạng metro/train Sydney lấy từ OpenStreetMap. Ứng dụng dùng `networkx` để chạy thuật toán trên đồ thị và giao diện web Leaflet để trực quan hóa.

## Tính năng chính

- Dùng dữ liệu GraphML offline: `data/sydney_metro.graphml`.
- Chạy nhiều thuật toán tìm đường trên cùng dữ liệu để so sánh.
- Hiển thị đồ thị node/cạnh và kết quả đường đi trực tiếp trên web.
- Cho phép admin gắn hệ số phạt hoặc chặn cạnh giữa 2 node.
- Xuất GraphML có thông tin `length`, `cost`, `penalty_multiplier`, `blocked`.

## Yêu cầu hệ thống

- Python 3.9+
- Thư viện trong `requirements.txt` (bao gồm `osmnx>=2.0.6`)

Cài đặt:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Chạy web

```bash
flask --app app run --debug
```

Mở http://127.0.0.1:5000/

## Tạo lại GraphML Sydney từ OSM

```bash
cd data
python cc.py
```

Script sẽ tải mạng rail Sydney và lưu vào `data/sydney_metro.graphml` với thuộc tính tương thích cho app:

- Node: `x`, `y`, (khuyến nghị `name`, `railway`, `public_transport`)
- Edge: `length`, `cost`, (khuyến nghị `name`, `ref`, `route`, `railway`)

## Ví dụ route query (Sydney)

```bash
python pathfinding.py \
  --place "Sydney, New South Wales, Australia" \
  --start "-33.8830,151.2070" \
  --goal "-33.7969,151.1831" \
  --algorithm astar \
  --output sydney_astar.html
```

## Admin

- Truy cập `/admin` để đăng nhập quản trị.
- Admin có thể chọn 2 node, gắn hệ số phạt hoặc chặn tuyến.
- Các thay đổi admin lưu trong RAM (khởi động lại server sẽ reset).

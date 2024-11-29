# Color detection
Giúp máy tính nhận diện màu sắc là một bài toán rất thú vị và cũng không kém phần quan trọng trong mảng thị giác máy tính. Ở trong dự án này mình sẽ xây dựng một ứng dụng nhận diện màu sắc từ camera với độ chính xác rất cao.

<p align="center">
	<img src="https://github.com/KudoKhang/ColorDetector/blob/main/colordetection.gif?raw=true" />
</p>


# How it work
Như đã biết, mỗi điểm của bức ảnh màu được biểu diễn bằng 3 giá trị trong hệ màu RGB. Với Opencv chúng ta dễ dàng lấy được tạo độ ảnh mong muốn để xác định màu. Ở đây mình lấy tọa độ đó là tâm của khung hình cho dễ:

```python
ret, img = cap.read()
img = cv2.flip(img, 1)
x, y = int(img.shape[1]/2), int(img.shape[0]/2)
```

Tiếp theo là xác định giá trị RGB tại điểm đó:

```python
def getBGR(x, y):

global b, g, r
b, g, r = img[y, x]
b, g, r = int(b), int(g), int(r)
return b, g, r
```

Sau khi có được giá trị RGB tại điểm ảnh thì ta viết hàm so sánh nó với giá trị RGB trong file [colors.csv](https://github.com/KudoKhang/ColorDetector/blob/main/colors.csv) (đây là một file cho ta biết 865 màu sắc với giá trị RGB tương ứng). Giá trị RGB của ảnh gần nhất với giá trị RGB nào trong file csv thì ta có thể gắn màu sắc tương ứng cho điểm ảnh ta cần xác định:

```python
def getColorName(b, g, r):
	minimum = 1000
	for i in range(len(csv)):
		d = abs(b - int(csv.loc[i, "B"])) + abs(g - int(csv.loc[i, "G"])) + abs(r - int(csv.loc[i, "R"])) # maximum = 255 + 255 + 255 = 765 (d = ||b-B|| + ||g-G|| + ||r-R||)
		if (d <= minimum):
			minimum = d
			cname = csv.loc[i, "color_name"]
	# print(minimum)
	return cname
```

Để tăng thêm độ màu mè cho khung hình chúng ta sẽ thêm khung hình vuông xung quanh tâm 🤓:
```python
def drawSquare(img, x, y):
	YELLOW = (0, 255, 255)
	BLUE = (255, 225, 0)

	cv2.line(img, (x - 150, y - 150), (x - 100, y - 150), YELLOW, 2)
	cv2.line(img, (x - 150, y - 150), (x - 150, y - 100), BLUE, 2)

	cv2.line(img, (x + 150, y - 150), (x + 100, y - 150), YELLOW, 2)
	cv2.line(img, (x + 150, y - 150), (x + 150, y - 100), BLUE, 2)

	cv2.line(img, (x + 150, y + 150), (x + 100, y + 150), YELLOW, 2)
	cv2.line(img, (x + 150, y + 150), (x + 150, y + 100), BLUE, 2)

	cv2.line(img, (x - 150, y + 150), (x - 100, y + 150), YELLOW, 2)
	cv2.line(img, (x - 150, y + 150), (x - 150, y + 100), BLUE, 2)

	cv2.circle(img, (x, y), 5, (255, 255, 153), -1)
```

Như vậy cơ bản chúng ta đã xong việc, phần còn lại là gọi những hàm vừa viết và show nó ra:

```python
while True:
	ret, img = cap.read()
	img = cv2.flip(img, 1)
	x, y = int(img.shape[1]/2), int(img.shape[0]/2)
	
	getBGR(x, y)
	getColorName(b, g, r)
	drawSquare(img, x, y)
	putText(img, x, y)
	
	cv2.imshow('Detector Color', img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
```

Chi tiết trong trong [main.py](https://github.com/KudoKhang/ColorDetector/blob/main/main.py)
# Usage
Để sử khởi chạy:

```bash
git clone https://github.com/KudoKhang/ColorDetector
cd ColorDetector
python main.py
```

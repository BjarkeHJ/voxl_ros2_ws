import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage, Image
import numpy as np
import cv2

class ImageCompressNode(Node):
    def __init__(self):
        super().__init__('image_compress_node')
        self.raw_sub_ = self.create_subscription(Image, '/hires_front_small_color', self.img_callback, 10)
        self.compressed_pub_ = self.create_publisher(CompressedImage, '/front_small_compressed', 10)
        print("init")

    def img_callback(self, img_msg : Image):
        print(len(img_msg.data))
        img = np.frombuffer(img_msg.data, np.uint8).reshape(img_msg.height, img_msg.width, -1)

        if img_msg.encoding == 'rgb8':
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # img = cv2.resize(img, (640, 480))

        # _, buf = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 40])
        _, buf = cv2.imencode('.jpg', img)

        out = CompressedImage()
        out.header = img_msg.header
        out.format = 'jpeg'
        out.data = buf.tobytes()
        self.compressed_pub_.publish(out)


def main(args=None):
    rclpy.init(args=args)

    node = ImageCompressNode()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

import cv2
import numpy as np
from mss import mss
import pycuda.driver as cuda
from pycuda import gpuarray

# 初始化 CUDA
cuda.init()
device = cuda.Device(0)
ctx = device.make_context()

# 配置屏幕捕获区域
monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}

with mss() as sct:
    while True:
        # 截取屏幕到 CPU 内存
        screenshot = sct.grab(monitor)
        img_cpu = np.array(screenshot)
        img_cpu = cv2.cvtColor(img_cpu, cv2.COLOR_BGRA2BGR)
        
        # 将数据复制到 CUDA 内存
        img_gpu = gpuarray.to_gpu(img_cpu)
        
        # 处理 GPU 数据（示例：转换为灰度图）
        img_gray_gpu = gpuarray.empty_like(img_gpu[:, :, 0])
        cuda.memcpy_dtod(
            img_gray_gpu.gpudata,
            img_gpu.gpudata,
            img_gpu.nbytes // 3  # 仅复制第一个通道（B）
        )
        
        # 复制回 CPU 并显示
        img_gray = img_gray_gpu.get()
        cv2.imshow("Desktop (CUDA Processed)", img_gray)
        
        if cv2.waitKey(1) == 27:
            break

ctx.pop()
cv2.destroyAllWindows()
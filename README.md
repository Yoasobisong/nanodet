# NanoDet Training and Deployment Guide

## Environment Setup
- Host Configuration:
  - Ubuntu 20.04 LTS
  - Python 3.8.12
  - PyTorch 1.11.0+cu113
  - TorchVision 0.12.0+cu113

### Installation Steps
1. Create a conda environment (recommended)
2. Clone the repository:
```bash
git clone https://github.com/RangiLyu/nanodet.git
cd nanodet
```
3. Install dependencies:
```bash
pip install -r requirements.txt
python setup.py develop  # Use sudo if permission denied
```

**Note**: If PyTorch and TorchVision are already installed, skip them in requirements.txt to avoid version conflicts.

## Dataset Preparation
### Directory Structure
```
CocoDataset/
├── images/
│   ├── train/
│   │   └── *.jpg/png
│   └── val/
│       └── *.jpg/png
├── labels/
│   ├── train/
│   │   └── *.xml
│   └── val/
│       └── *.xml
└── ann/
    ├── train.json
    └── val.json
```

### Data Collection and Annotation
1. Capture Dataset
```bash
./tools/take_photo.py
```
**Note**: Use numeric names for images

2. Label Images
```bash
# Setup labelImg tool
git clone https://gitcode.com/gh_mirrors/la/labelImg.git
cd labelImg
sudo apt-get install pyqt5-dev-tools
sudo pip3 install -r requirements/requirements-linux-python3.txt
make qt5py3
python3 labelImg.py
```
**Note**: Save labels in XML format

3. Convert Annotations
```bash
# Convert XML to COCO JSON format
python3 voc_2js.py
```

## Model Training
1. Setup environment:
```bash
python setup.py develop
pip install -r requirements.txt
```

2. Start training:
```bash
python tools/train.py ./config/[your_config].yml
```

## Model Testing
### Using PyTorch Model (GPU Required)
1. Camera Test:
```bash
python3 ./demo/demo.py --config ./config/legacy_v0.x_configs/nanodet-m.yml \
                      --model ./workspace/nanodet_m/model_best/nanodet_model_best.pth \
                      --demo video
```

2. Image Test:
```bash
python3 ./demo/demo.py --config ./config/legacy_v0.x_configs/nanodet-m.yml \
                      --model ./workspace/nanodet_m/model_best/nanodet_model_best.pth \
                      --path /path/to/your_image
```

## Model Conversion
### ONNX Conversion
1. Convert to ONNX:
```bash
python3 export_onnx.py --cfg_path ./config/legacy_v0.x_configs/nanodet-m.yml \
                       --model_path workspace/nanodet_m/model_best/nanodet_model_best.pth \
                       --out_path ../out/nanodet.onnx
```

2. Test ONNX model:
```bash
python3 tools/onnx_nanodet_detect.py --imgpath /path/to/yourimg \
                                    --modelpath ./workspace/nanodet_m/model_best/nanodet_model_best.pth
```

## NCNN Deployment (Ubuntu Only)
### Prerequisites Installation

1. OpenCV Installation:
```bash
# Install OpenCV 4.5.4
wget https://gitcode.com/gh_mirrors/opencv31/opencv/tags/4.5.4
unzip opencv-4.5.4.zip
cd opencv-4.5.4
mkdir build && cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local ..
make -j8
sudo make install
sudo ldconfig
```

2. Protobuf Installation:
```bash
# Install Protobuf 3.19.1
wget https://github.com/protocolbuffers/protobuf/releases/tag/v3.19.1
unzip protobuf-all-3.19.1.zip
cd protobuf-all-3.19.1
./configure --prefix=/usr/local
make -j4
sudo make install
sudo ldconfig
```

3. NCNN Installation:
```bash
git clone https://github.com/Tencent/ncnn.git
cd ncnn
mkdir build && cd build
cmake ..
make
sudo make install
```

### NCNN Model Conversion
1. Build demo_ncnn:
```bash
cd demo_ncnn
export ncnn_DIR=YOUR_NCNN_PATH/build/install/lib/cmake/ncnn
mkdir build && cd build
cmake ..
make
```

2. ONNX Simplification:
```bash
pip3 install -i https://pypi.douban.com/simple -U onnx-simplifier --user
python -m onnxsim nanodet.onnx nanodet-sim.onnx
```

3. Convert to NCNN:
```bash
# In ncnn-master/build/tools/onnx
./onnx2ncnn nanodet-sim.onnx nanodet.param nanodet.bin
# Move .param and .bin to nanodet/demo_ncnn
```

4. Update Parameters:
- Modify parameters in `nanodet/demo_ncnn/build/nanodet.h` to match your config file
- Refer to `./demo_ncnn/README.md` for running instructions

## Troubleshooting
1. Training Issues:
   - If encountering DataLoader length 0 error, adjust device parameters in config:
```yaml
device:
  gpu_ids: [0]
  workers_per_gpu: 2
  batchsize_per_gpu: 16
  precision: 32
```
**Note**: Adjust batch size based on GPU capacity

2. Module Import Error:
   - If `no module named 'nanodet'` error occurs:
```bash
sudo python setup.py develop
```

## References
- [NanoDet Official Repository](https://github.com/RangiLyu/nanodet)
- [NCNN Official Repository](https://github.com/Tencent/ncnn)
- [Model Parameters Guide](https://blog.csdn.net/qq_20144897/article/details/132071736)


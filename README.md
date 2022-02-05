Deep Learning School final project. Neural transfer telegram bot
=============================

Introduction
------------
This project use implementation of the `Neural-Style algorithm <https://arxiv.org/abs/1508.06576>`__
developed by Leon A. Gatys, Alexander S. Ecker and Matthias Bethge.
Neural-Style, or Neural-Transfer, allows you to take an image and
reproduce it with a new artistic style. The algorithm takes three images,
an input image, a content-image, and a style-image, and changes the input 
to resemble the content of the content-image and the artistic style of the style-image.

Implementation framework taken from the pytorch tutorial `Neural Transfer Using PyTorch https://pytorch.org/tutorials/advanced/neural_style_tutorial.html`

Code is highly commented, find model implementation details in _model_ module.

Telegram bot @dls-glebg-prj
----
Simple structure. Asynchronicity achieved via aiogram.
I know that my token is compromised.

Installation
---
```
git clone https://github.com/glebg9/dls-bot-prj.git
git clone https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix.git
cd dls-bot-prj
pip3 install -r requirements.txt
python3 main.py 
```

CycleGan
---
Pretrained weights and model from <https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix>

CycleGan will MONETize any given image.

Download pretrained weights
```bash ./scripts/download_cyclegan_model.sh style_monet```

Model invocation implemented in cyclegan_invocation.py.

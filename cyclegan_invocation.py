import os, sys, inspect
from shutil import copy
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, f'{parentdir}/pytorch-CycleGAN-and-pix2pix')
from util import html

from options.test_options import TestOptions
from data import create_dataset
from models import create_model
from util.visualizer import save_images

def cyclegan_process_image(usr_id, image_path, output_path):
    # hacky but efficient ))
    os.chdir("../pytorch-CycleGAN-and-pix2pix")
    ds_path = f"datasets/{usr_id}/testA"
    os.makedirs(ds_path, exist_ok=True)
    copy(f"../dls-bot/{image_path}", ds_path)
    oldargv = sys.argv
    sys.argv = ['test.py', '--dataroot', ds_path,
                '--name', 'style_monet_pretrained',
                '--model', 'test',
                '--no_dropout', '--gpu_ids', '-1']
    opt = TestOptions().parse()  # get test options
    opt.num_threads = 0  # test code only supports num_threads = 0
    opt.batch_size = 1  # test code only supports batch_size = 1
    opt.serial_batches = True  # disable data shuffling; comment this line if results on randomly chosen images are needed.
    opt.no_flip = True  # no flip; comment this line if results on flipped images are needed.
    opt.display_id = -1  # no visdom display; the test code saves the results to a HTML file.
    dataset = create_dataset(opt)  # create a dataset given opt.dataset_mode and other options
    model = create_model(opt)  # create a model given opt.model and other options
    model.setup(opt)

    # create a website
    web_dir = os.path.join(opt.results_dir, opt.name,
                           '{}_{}'.format(opt.phase, opt.epoch))  # define the website directory
    if opt.load_iter > 0:  # load_iter is 0 by default
        web_dir = '{:s}_iter{:d}'.format(web_dir, opt.load_iter)
    print('creating web directory', web_dir)
    webpage = html.HTML(web_dir, 'Experiment = %s, Phase = %s, Epoch = %s' % (opt.name, opt.phase, opt.epoch))

    for i, data in enumerate(dataset):
        if i >= opt.num_test:  # only apply our model to opt.num_test images.
            break
        model.set_input(data)  # unpack data from data loader
        model.test()  # run inference
        visuals = model.get_current_visuals()  # get image results
        img_path = model.get_image_paths()  # get image paths
        if i % 5 == 0:  # save images to an HTML file
            print('processing (%04d)-th image... %s' % (i, img_path))
        save_images(webpage, visuals, img_path, aspect_ratio=opt.aspect_ratio, width=opt.display_winsize,
                    use_wandb=opt.use_wandb)
    name = image_path.split('/')[-1]
    name, ext = tuple(name.split('.'))
    new_path = 'results/style_monet_pretrained/test_latest/images/' \
               + name + "_fake" + '.png'
    try:
        os.removedirs(f"datasets/{usr_id}")
    except OSError as error:
        pass

    os.chdir("../dls-bot")
    copy(f"../pytorch-CycleGAN-and-pix2pix/{new_path}", output_path)
    sys.argv = oldargv


if __name__ == '__main__':
    cyclegan_process_image(123, "test/images/dancing.jpg", "test/images/monetized.png")
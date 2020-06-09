
import sys
sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks  import *

arch = [
    to_head('..'),
    to_cor(),
    to_begin(),

    #input
    to_input('data/input.PNG'),

    #block-001
    to_ConvConvRelu(name='ccr_b0', s_filer="", n_filer=("",""), offset="(-2,0,0)", to="(0,0,0)", width=(1,1), height=35, depth=35),
    to_Pool(name="pool_b1", offset="(-1,0,0)", to="(ccr_b1-east)", width=1, height=35, depth=35, opacity=0.5, caption="Pooling"),

    to_ConvConvConvRelu(name='ccr_b1', s_filer="", n_filer=("","",""), offset="(0,0,0)", to="(0,0,0)", width=(1,1,1), height=32, depth=32),
    *s_block_2ConvPool(name='b2', botton='ccr_b1', s_filer="", n_filer="", offset="(1,0,0)", size=(28,28,2.5), opacity=0.5),
    *s_block_2ConvPool(name='b3', botton='ccr_b2', s_filer="", n_filer="", offset="(1,0,0)", size=(25,25,3.5), opacity=0.5),
    *s_block_2ConvPool(name='b4', botton='ccr_b3', s_filer="", n_filer="", offset="(1,0,0)", size=(16,16,4.5), opacity=0.5),

    #Bottleneck
    #block-005
    *block_Bottleneck_Drop(name='bottle', botton="b4", s_filer="", n_filer=(" "," "), offset="(2,0,0)", to="(pool_b4-east)", width=(8,8), height=8, depth=8, caption="Dropout"),
    #to_ConvConvRelu( name='ccr_b5', s_filer=32, n_filer=(1024,1024), offset="(2,0,0)", to="(pool_b4-east)", width=(8,8), height=8, depth=8, caption="Bottleneck"  ),
    #to_connection( "pool_b5", "ccr_bottle"),
    
    #Decoder
    *s_block_2ConvPool(name='b6', botton='ccr_bottle', s_filer="", n_filer="", offset="(1,0,0)", size=(16,16,4.5), opacity=0.5),
    to_skip( of='ccr_b4', to='ccr_b6', pos=1.25),
    *s_block_2ConvPool(name='b7', botton='ccr_b6', s_filer="", n_filer="", offset="(1,0,0)", size=(25,25,3.5), opacity=0.5),
    to_skip( of='ccr_b3', to='ccr_b7', pos=1.25),
    *s_block_2ConvPool(name='b8', botton='ccr_b7', s_filer="", n_filer="", offset="(1,0,0)", size=(28,28,2.5), opacity=0.5),
    to_skip( of='ccr_b2', to='ccr_b8', pos=1.25),

    *s_block_2ConvPool(name='b9', botton='ccr_b8', s_filer="", n_filer="", offset="(1,0,0)", size=(32,32,1), opacity=0.5),
    to_skip( of='ccr_b1', to='ccr_b9', pos=1.25),

    # *block_Unconv(name="b6", botton="ccr_bottle", top='end_b6', s_filer=64,  n_filer=512, offset="(2.1,0,0)", size=(16,16,5.0), opacity=0.5 ),
    # to_skip( of='ccr_b4', to='ccr_res_b6', pos=1.25),
    # *block_Unconv(name="b7", botton="end_b6", top='end_b7', s_filer=128, n_filer=256, offset="(2.1,0,0)", size=(25,25,4.5), opacity=0.5 ),
    # to_skip( of='ccr_b3', to='ccr_res_b7', pos=1.25),
    # *block_Unconv(name="b8", botton="end_b7", top='end_b8', s_filer=256, n_filer=128, offset="(2.1,0,0)", size=(28,28,3.5), opacity=0.5 ),
    # to_skip( of='ccr_b2', to='ccr_res_b8', pos=1.25),

    #*block_Unconv(name="b9", botton="end_b8", top='end_b9', s_filer=512, n_filer=64,  offset="(2.1,0,0)", size=(40,40,2.5), opacity=0.5 ),
    #to_skip( of='ccr_b1', to='ccr_res_b9', pos=1.25),

    to_ConvSoftMax(name="soft1", s_filer="", offset="(0.75,0,0)", to="(ccr_b9-east)", width=1, height=40, depth=40, caption="SIGMOID"),
    to_connection( "ccr_b9", "soft1"),

    to_connection("ccr_b9", "soft1"), to_output('data/output.PNG', off='3', to='(soft1-east)'), 
    to_end()
    ]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    print(namefile)
    to_generate(arch, namefile + '.tex' )
    import subprocess
    cmd = ['pdflatex', '-interaction', 'nonstopmode', 'unet_pub_2.tex']
    proc = subprocess.Popen(cmd)
    proc.communicate()

if __name__ == '__main__':
    main()


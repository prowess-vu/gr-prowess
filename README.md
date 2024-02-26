# gr-prowess
Data processing blocks for the PROWESS VU project

## TODO: Setup stuff

On MacOS:

`
brew install gnuradio
echo 'export GRC_BLOCKS_PATH=/usr/local/share/gnuradio/grc/blocks\nexport PYTHONPATH=/usr/local/lib/python3.12/site-packages' > ~/.zshrc
echo 'export GRC_BLOCKS_PATH=/usr/local/share/gnuradio/grc/blocks\nexport PYTHONPATH=/usr/local/lib/python3.12/site-packages' > ~/.bash_profile
source ~/.zshrc
`

Install TorchSig:

`
git clone https://github.com/TorchDSP/torchsig.git && cd torchsig
sed -i '' 's/torch==2.0.1/torch==2.2.1/g' pyproject.toml
python3 -m pip install .
cd .. && rm -rf torchsig
`

To install or update GR-PROWESS:

`
cd gr-prowess && mkdir -p build && cd build
cmake ..
make
sudo make install
cd .. && rm -rf build
`

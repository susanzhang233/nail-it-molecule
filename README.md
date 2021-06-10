


### Introduction

This project is aimed to building a Graphic GAN model that would aid drug design processes. For demonstration, the project is expected to learn graphical features of the molecules that are believed to have inhibition effect for the specific protein SARS coronavirus 3C-like Protease (3CLPro) . Then, the model would develop a reasonable way to generate potential novel molecules inhibitors' graphically representations. After that, with a defeaturizer, the graphical representations would be converted into visualizable molecule formats. 

#### Intro to GAN
GAN, standing for Generative Adversarial Network, is commonly used in graphic works and more, such as generation of faces, music pieces. Here's a great [introduction](https://machinelearningmastery.com/what-are-generative-adversarial-networks-gans/). In this project, we'll be building a GAN model that ultilizes the mthematical concepts of graphs in the chemical world.

### Dataset
The dataset used for demonstration of this model is originally from [PubChem AID1706](https://pubchem.ncbi.nlm.nih.gov/bioassay/1706), previously handled by [JClinic AIcure](https://www.aicures.mit.edu/) team at MIT into this [binarized label form](https://github.com/yangkevin2/coronavirus_data/blob/master/data/AID1706_binarized_sars.csv).
The dataset is also hosted in the [data folder](https://github.com/susanzhang233/mollykill/tree/main/data) of this project.

### Repository Explaination
- [`model.py`](https://github.com/susanzhang233/mollykill/blob/main/model.py) contains the source codes for the GAN model created
-[`example.ipynb`](https://github.com/susanzhang233/mollykill/blob/main/example.ipynb) is an example usage in pipeline of the model



### Limitations(Future work)
- Currently, the generation of molecules is limited to a specific length that is shorter than most molecules in the real world. Future work involving some concepts of 
- The dimension of the discriminator might be improved by adding more features of the molecules(ie. hybridization, stereochemistry, etc)





### Acknowledgements


- https://github.com/yangkevin2/coronavirus_data/tree/master/data
- https://github.com/whoIsTheGingerBreadMan/YoutubeVideos
- https://machinelearningmastery.com/practical-guide-to-gan-failure-modes/

-MolGAN



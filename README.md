# kriging_workshop
Required working environment: Anaconda, Python, Jupyter Notebook, GEE, R, ArcGIS, Excel

## install Python with GEE
```
conda create -n gee 
conda activate gee
conda install mamba -c conda-forge
mamba install geemap -c conda-forge
```

## install jupyter notebook
conda install -y -c anaconda jupyter
conda install -y ipykernel
python -m ipykernel install --user --name gee

## install R4.0 and up 
conda create --name r4-base
conda activate r4-base
conda install -c conda-forge r-base
conda install -c conda-forge/label/gcc7 r-base
## install R4 as jupyter kernel
conda install jupyter
install.packages('IRkernel')
IRkernel::installspec()


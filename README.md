# PV_self_consumption_client

Authors: 
Sébastien Gardoll, CNRS, IPSL
Olivier Boucher, CNRS, IPSL

(c) 2024 

Interface to call API PV_self_consumption_client for optimising solar PV self-consumption under constraints.
Note that the license only applies to this interface and not to the API.

## Python environment

### Option 1: Conda

1. Install miniconda;
2. Create a new conda environment;
3. Install the project dependencies.

Skip 1. if you already have a miniconda/anaconda distribution installed (`which conda` doesn't return an error).

#### Install miniconda

While installing, Miniconda asks you to initialize itself. If you choose to do so, it will add some instructions to your ~/.bashrc (shell configuration).
Carefully choose the path of the Miniconda installation directory, as conda environment take some space and inodes. The following example is meant for Linux x86_64.

```bash
curl -sSL https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh > Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh
```

#### Conda environment creation

Let's create a conda environment called pvsc:

```bash
conda create -y -n pvsc 'python=3.12.*'
```

#### Project dependencies installation

First activate the environment (as usual), then install the dependencies with pip:

```bash
conda activate pvsc
cd /path/to/PV_self_consumption_client/
pip install -e .
```

### Option 2: PDM

[PDM](https://pdm-project.org/en/latest/) associates a Python virtual environmnent (venv) with a project described by a pyproject file. 

#### Dependencies installation

Setup the project environment with PDM:

```bash
cd /path/to/PV_self_consumption_client/
pdm install
```

#### Environement activation

Activate the associated venv:

```bash
cd /path/to/PV_self_consumption_client/
eval $(pdm venv activate)
```

Deactivate as usual:

```bash
deactivate
```

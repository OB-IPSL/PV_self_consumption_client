# PV_self_consumption_client

## Authors:
- Sébastien Gardoll, IPSL, CNRS / Sorbonne Université
- Olivier Boucher, IPSL, CNRS / Sorbonne Université

(c) 2024

Interface to call API PV_self_consumption_client for optimising solar PV self-consumption under constraints.
Note that the license only applies to this interface and not to the API itself.

## Installation

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

#### Install client

First activate the environment (as usual), then install the client with pip:

```bash
conda activate pvsc
pip install -U pv_self_consumption_api_client
```

#### Run client

In any directory:

```bash
pvsc -h
```

### Option 2: PDM

[PDM](https://pdm-project.org/en/latest/) associates a Python virtual environmnent (venv) with a project described by a pyproject file.

#### Dependencies installation

Setup the project environment with PDM:

```bash
git clone https://github.com/OB-IPSL/PV_self_consumption_client.git
cd PV_self_consumption_client
pdm install
```

#### Run client

While in PV_self_consumption_client directory:

```bash
pdm pvsc -h
```

## Getting started

Note: Add `pdm` command before `pvsc` while in the source directory if you installed the client with pdm (option 2).

### Generate example input files

```bash
pvsc example -p > params.yml
pvsc example -d > demand.csv
```
The example input files can be modified for your own usages.

### Run optimization

Compute optimization then output in and also generate plots (`-m` option):

```bash
pvsc optimize -m params.yml demand.csv
```

## How to contribute

### Install linters

You must follow the pdm install instructions. Then:

```bash
pdm install -dG dev
pdm run pre-commit install
```

### Submit pull request

Contribution is possible thank to the PR submission.

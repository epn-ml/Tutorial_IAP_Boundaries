# Tutorial_IAP_Boundaries

The work package "Machine Learning Solutions for Data Analysis and Exploitation in Planetary Science" within Europlanet 2024 Research Infrastructure will develop machine learning (ML) powered data analysis and exploitation tools optimized for planetary science.

Europlanet 2024 RI has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 871149.

# Installation Guidelines

This pipeline runs on Python 2.7

git clone https://github.com/epn-ml/Tutorial_IAP_Boundaries.git
python -m venv wsenv
source wsenv/bin/activate
cd Tutorial_IAP_Boundaries
pip install -r requirements.txt
ipython kernel install --user --name=wsenv
jupyter lab

Download saved model, dataset and labels from https://figshare.com/articles/dataset/Tutorial_IAP_Boundaries_Data/21153403

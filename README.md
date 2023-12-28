# XRayTransCalCloud - A Simple X-ray Transmission Calculator

## Introduction

XRayTransCalCloud is a straightforward tool designed to calculate the transmission of X-rays through various compounds. This project is particularly valuable for researchers and professionals in fields like material science, physics, and radiography, who often require quick and accurate X-ray transmission data.

## Data Source

The calculator relies on data from the National Institute of Standards and Technology (NIST). Specifically, it utilizes the X-ray Mass Attenuation Coefficients provided in their extensive database, which can be found here: [NIST X-ray Mass Attenuation Coefficients](https://physics.nist.gov/PhysRefData/XrayMassCoef/tab3.html).

## X-ray Transmittance Calculation

X-ray transmittance in a material is a crucial parameter in many scientific and industrial fields. It determines how much of the X-ray beam passes through a given material. The transmittance, $\ T $\, of X-rays through a material can be calculated using the formula:

$$ T = e^{-\mu \cdot d} $$

Where:
- $\ T $\ is the transmittance, representing the fraction of X-ray intensity transmitted through the material.
- $\ \mu $\ is the linear attenuation coefficient of the material, which depends on the material's composition and the energy of the X-rays.
- $\ d $\ is the thickness of the material.

The linear attenuation coefficient $\ \mu $\ for a compound or mixture can be calculated using the mass attenuation coefficients of the constituent elements and their mass fractions in the compound:

$$ \mu = \sum (w_i \times \mu_i) $$

Where:
- $\ w_i $\ is the mass fraction of each element in the compound.
- $\ \mu_i $\ is the mass attenuation coefficient of each element, which can be obtained from standard databases like NIST.
## Project Components

XRayTransCalCloud consists of two main components:
1. **IPython Notebook (IPYNB) Version:** This version is designed for local running. It's ideal for users who prefer to work in a Jupyter Notebook environment for added flexibility and for integrating with other scientific computation tools.
2. **Web Version:** Although the web version's quality is modest due to the developer's limited experience in web development, it is fully functional and serves the purpose of providing online access to the calculator. This version is suitable for users who need quick access without the need for a local setup.

![IPython Notebook (IPYNB) Version](https://github.com/JackiMa/XRayTransCalCloud/assets/96033062/d0898232-a9a7-449c-81d5-7fc521f6ba88)

![Web Version](https://github.com/JackiMa/XRayTransCalCloud/assets/96033062/bca3fb43-39bd-4748-b3ef-5db81b24ac50)


## Note

The web version, while operational, might have a basic interface and limited features compared to the IPYNB version. However, continuous efforts are made to improve it, and user feedback is always welcome to enhance its functionality.

---

XRayTransCalCloud is an open-source project, and contributions from the community are encouraged. Whether it's improving the web interface, enhancing the calculation algorithms, or extending the database, all contributions are valuable.

For more information, bug reports, or contributions, please visit the [GitHub repository](https://github.com/[YourGitHubUserName]/XRayTransCalCloud). 

Your support and contributions make this project better for everyone. Thank you for using XRayTransCalCloud!

## Docker Deployment

Docker provides an easy way to package and distribute applications. Here are the steps to deploy this project using Docker:

1. **Build the Docker image:** Navigate to the project directory and build the Docker image using the ***Dockerfile*** provided in the project. Replace `your-image-name` with the name you want to give to your Docker image.

    ```bash
    docker build -t your-image-name .
    ```

2. **Run the Docker container:** After the image is built, you can run the container. Replace `your-container-name` with the name you want to give to your Docker container, and `your-image-name` with the name of the Docker image you just built.

    ```bash
    docker run -d -p 9999:5000 --name your-container-name your-image-name
    ```

    This command will start the container and map the port 5000 of the container to the port 9999 of your host machine.

3. **Access the application:** You can now access the application by navigating to `http://localhost:9999` in your web browser.

Please note that these instructions assume that you have Docker installed on your machine. If you don't have Docker installed, you can download it from the [official Docker website](https://www.docker.com/get-started).
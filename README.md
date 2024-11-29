
# Image Filtering Tool

This is a Flask-based web application that allows users to filter images in two datasets ("fake" and "real") by marking them as "true" or "false". It enables batch processing and keeps track of progress in real time. 

## Features

- **Batch Processing**: Processes images in batches to streamline the filtering process.
- **Dataset Switching**: Supports toggling between two datasets: "fake" and "real".
- **Progress Tracking**: Displays filtering progress with statistics and a progress bar.
- **Interactive UI**: A grid-based image gallery with easy toggling of image states (true/false).

## Preview

![Image Filtering Tool Screenshot](https://i.postimg.cc/5NvH4JGf/Screenshot-20241122-120055.png)

## Project Structure

```plaintext
project/
│
├── app.py           # Main backend script with Flask routes and logic.
├── templates/
│   └── index.html   # Frontend HTML for the web interface.
├── static/          # (Optional) Add CSS/JS files here for further customization.
├── data/
│   ├── fake/        # Directory for fake dataset images.
│   ├── real/        # Directory for real dataset images.
│   ├── fake.csv     # CSV file tracking fake dataset statuses (auto-generated).
│   └── real.csv     # CSV file tracking real dataset statuses (auto-generated).
└── requirements.txt # Python dependencies.
```

## Prerequisites

- Python 3.7+
- Flask
- Pandas
- A web browser for accessing the application.

## Dataset

This project was created to deal with and the "Three-Body Images" dataset, which is available on Kaggle. You can use any other datasets or files as you need as long as you follow the folder structure. You can explore and download the dataset from the following link:

[Three-Body Images Dataset on Kaggle](https://www.kaggle.com/datasets/ameencaslam/three-body-images)

### Organizing the Dataset

After downloading the dataset:
1. Extract the contents into the `data/` directory:
    ```
    project/
    ├── data/
    │   ├── fake/  # Place "fake" dataset images here.
    │   └── real/  # Place "real" dataset images here.
    ```
2. Ensure that the directory structure matches the expected format, as shown above.



## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/ameencaslam/Filter
    cd Filter
    ```

- Optional Step
 
  - Install Virtual Environment:
    ```bash
    python -m venv venv
    ```
  - Activate venv:
    ```bash
    venv\Scripts\activate
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Create the required directories and populate them with images (For your custom datasets or files):
    ```plaintext
    project/
    ├── data/
    │   ├── fake/  # Add images for the fake dataset here.
    │   └── real/  # Add images for the real dataset here.
    ```

4. Run the application:
    ```bash
    python app.py
    ```

5. Open the application in your web browser:
    ```plaintext
    http://127.0.0.1:5000
    ```

## Usage

### Filtering Images
- **Step 1**: Choose a dataset ("fake" or "real") using the dataset selection buttons.
- **Step 2**: Toggle the status of an image by clicking on it. Marked images will appear dimmed.
- **Step 3**: Click the "Next Batch" button (or press `Enter`) to save the current batch and load the next set of images.

### Progress Stats
- `Original`: Remaining unprocessed images.
- `True`: Images marked as "true".
- `False`: Images marked as "false".
- The progress bar dynamically updates as you process images.

## Notes

- Ensure that the `data/fake` and `data/real` directories are populated with images before starting the application.
- The application auto-generates `fake.csv` and `real.csv` files to track image statuses.

## License

This project is licensed under the [MIT License](LICENSE).


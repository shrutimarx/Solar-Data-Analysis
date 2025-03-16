# Solar Data Analysis for Fire Stations

## Description
This project calculates the financial viability of installing solar panels on fire stations based on their geographical location and solar potential. It uses data from a Google Solar API and performs a financial analysis.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/shrutimarx/solar-data-analysis.git
   ```
2. Install dependencies:
   ```bash
   pip install requests
   ```
      ```bash
   pip install pandas
   ```
   ```bash
   pip install pyproj
   ```


## Usage
1. Ensure that you have a valid Google Solar API key.
2. Ensure that you have a valid CSV file with Fire Station data (look for GIS data)
3. 

## Dependencies
- requests
- pandas
- pyproj (NOTE: this does not work with MACOS x86_64 architecture)


To check your architecture, run
```bash
python3 -c "import platform; print(platform.machine())"
```

If x86, you can use Miniforge. Run the following in terminal.

```bash
brew install miniforge
conda create -n gis_env python=3.11
conda init
source /usr/local/Caskroom/miniforge/base/etc/profile.d/conda.sh
conda activate gis_env
```
and continue running the file through terminal!

## Contributing
Feel free to fork this repository and submit pull requests. When contributing, please ensure that your code adheres to the existing style and includes appropriate documentation.

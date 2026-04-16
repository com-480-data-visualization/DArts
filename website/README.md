# D'Arts - MoMA Collection Visualization

This is the Svelte and D3.js frontend for the D'Arts project, designed to visualize diversity in the MoMA collection.

## How to Run

### Prerequisites

*   [Node.js](https://nodejs.org/) (v18 or later recommended)
*   [npm](https://www.npmjs.com/) (comes with Node.js)
*   [Git](https://git-scm.com/)
*   [Python](https://www.python.org/) (v3.x)
*   `pandas` Python library (`pip install pandas`)

### 1. Setup the Data

The website requires pre-processed JSON data which is generated from the raw MoMA dataset.

From the **root of the `DArts` project** (not this `website` directory), run the data setup scripts. These will download the MoMA collection data via a git submodule and then process it into the necessary format.

First, run the setup script to fetch the raw data:

```bash
# On macOS/Linux
./setup_data.sh

# On Windows (using PowerShell)
./setup_data.ps1
```

Next, run the Python script to process the data. This will place the required JSON files into `website/public/data/`.

```bash
python data/process_data.py
```

### 2. Install and Run the Website

Navigate into this `website` directory, install the dependencies, and start the development server.

```bash
cd website
npm install
npm run dev
```

The website should now be running at the local address provided by Vite in your terminal.
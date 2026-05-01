# 🌧️ Rainwater Quality Checker

A Python CLI tool that estimates the quality of rainwater in your city using real environmental data from public APIs.

> ⚠️ **Disclaimer:** This tool provides rough estimates only and should not be used as a basis for health or safety decisions. Always do your own research before using rainwater for cleaning or consumption. The tool accesses your device's IP address to approximate your location — it does not store or upload this data.

---

## What It Does

You turn on the tap and don't think twice. But what about the rain falling outside your window — is it clean enough to collect? The answer depends on where you live, what's in the air, how high up you are, and how long it's been since it last rained.

This tool pulls live data from multiple sources and combines them into a single quality estimate for your city's current rainwater.

---

## Factors Considered

| Factor | Why It Matters |
|---|---|
| **Air Quality Index (AQI)** | Pollutants in the air bind to raindrops — high AQI means dirtier rain |
| **Humidity** | Low humidity causes partial evaporation of falling droplets, concentrating contaminants |
| **Altitude** | Higher elevations generally have cleaner air and less industrial pollution exposure |
| **Distance from Coast** | Sea salt spray travels inland and increases mineral content in precipitation *(coming soon)* |
| **Days Since Last Rain** | First rain after a dry spell washes accumulated pollutants — subsequent rain is cleaner *(coming soon)* |

---

## Data Sources

- **[WAQI](https://waqi.info/)** — World Air Quality Index, real-time AQI data
- **[wttr.in](https://wttr.in/)** — Weather data including humidity and precipitation
- **[Open-Meteo Elevation API](https://open-meteo.com/en/docs/elevation-api)** — Free elevation data based on the Copernicus DEM dataset
- **[geocoder](https://geocoder.readthedocs.io/)** + **OpenStreetMap** — City name to coordinates resolution

---

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/rainwater_quality_measurer.git
cd rainwater-quality-checker
pip install -r requirements.txt
```

---

## Usage

```bash
python main.py
```

The tool will:
1. Detect your city via IP geolocation
2. Ask you to confirm or manually enter your city
3. Fetch live environmental data
4. Return a rainwater quality estimate with usage recommendations

---

## Requirements

- Python 3.8+
- Internet connection
- Dependencies listed in `requirements.txt`:
  - `requests`
  - `geocoder`

---

## Project Status

This project is actively under development. The current version fetches and displays AQI, humidity, and altitude data. The scoring system that combines these into a unified quality estimate is still being designed — contributions and domain expertise (especially from environmental scientists or statisticians) are very welcome.

**Planned features:**
- Weighted scoring system combining all factors
- Distance from coast calculation
- Precipitation history tracking
- FastAPI backend + React frontend web version
- MongoDB storage for per-city rainfall history

---

## Contributing

Suggestions, issues, and pull requests are welcome. If you have expertise in environmental science, hydrology, or statistics and want to help design the scoring weights — please open an issue or reach out directly. That's genuinely the hardest part of this project and outside knowledge would go a long way.

---

## License

MIT

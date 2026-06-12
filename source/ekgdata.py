import json
import pandas as pd
import plotly.express as px
from scipy.signal import find_peaks

class EKGdata:

    def __init__(self, ekg_dict):
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV', 'Zeit in ms'])
        self.df = self.df.iloc[:5000]

    def find_peaks_own(self, threshold=340, distance=200):
        """Findet Peaks im EKG-Signal"""
        peaks, _ = find_peaks(self.df["Messwerte in mV"], height=threshold, distance=distance)
        self.peaks = peaks

    def plot_time_series(self):
        """Plot der EKG-Daten mit roten Peaks"""
        self.find_peaks_own()  # zuerst Peaks finden
        self.fig = px.line(self.df.head(2000), x="Zeit in ms", y="Messwerte in mV")
        # Peaks als rote Punkte hinzufügen
        peaks_in_range = self.peaks[self.peaks < 2000]
        self.fig.add_scatter(
            x=self.df["Zeit in ms"].iloc[peaks_in_range],
            y=self.df["Messwerte in mV"].iloc[peaks_in_range],
            mode="markers",
            marker=dict(color="red", size=8),
            name="Peaks"
        )

if __name__ == "__main__":
    file = open("data/person_db.json")
    person_data = json.load(file)
    ekg_dict = person_data[0]["ekg_tests"][0]
    ekg = EKGdata(ekg_dict)
    print(ekg.df.head())

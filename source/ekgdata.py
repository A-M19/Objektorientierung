import json
import pandas as pd
import plotly.express as px

class EKGdata:

    ## Konstruktor der Klasse soll die Daten einlesen
    def __init__(self, ekg_dict):
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV', 'Zeit in ms'])
        self.df = self.df.iloc[:5000]
        
        # Attribute für die Peaks und die berechnete Herzfrequenz initialisieren
        self.peaks = []
        self.heart_rate = 0.0

    def find_peaks(self, threshold=340, distance=200):
        """
        Ein selbstgeschriebener Peak-Finder (ohne externe scipy-Bibliothek).
        Sucht nach lokalen Maxima, die über dem definierten Schwellenwert liegen.
        """
        # Array mit den mV-Messwerten vorbereiten
        signal = self.df["Messwerte in mV"].values
        detected_peaks = []
        
        # Wir laufen durch das Signal (unter Aussparung des ersten und letzten Wertes)
        last_peak_index = -distance  # Startwert für den Abstandsschutz
        
        for i in range(1, len(signal) - 1):
            current_value = signal[i]
            
            # Kriterium 1: Liegt der Wert über dem Schwellenwert?
            if current_value >= threshold:
                
                # Kriterium 2: Ist es ein echtes lokales Maximum? (Größer als Nachbar links und rechts)
                if current_value > signal[i - 1] and current_value >= signal[i + 1]:
                    
                    # Kriterium 3: Ist der Mindestabstand zum letzten Peak eingehalten? (Distance-Schutz)
                    if (i - last_peak_index) >= distance:
                        detected_peaks.append(i)
                        last_peak_index = i  # Update, wann der letzte Peak war
                        
        # Speichern der gefundenen Peak-Indizes im Objektattribut
        self.peaks = detected_peaks

    def estimate_hr(self):
        """Berechnet die Herzfrequenz basierend auf den Peaks"""
        # Wenn weniger als 2 Peaks gefunden wurden, macht eine Berechnung keinen Sinn
        if len(self.peaks) < 2:
            self.heart_rate = 0.0
            return self.heart_rate
        
        # Hol dir die Zeiten der gefundenen Peaks aus der Spalte 'Zeit in ms'
        peak_times = self.df["Zeit in ms"].iloc[self.peaks].values
        
        # Berechne die Differenzen zwischen aufeinanderfolgenden Peaks (in ms) und wandle sie in Sekunden um
        rr_intervals_seconds = (peak_times[1:] - peak_times[:-1]) / 1000.0
        
        # Durchschnittliches RR-Intervall ermitteln
        mean_rr = rr_intervals_seconds.mean()
        
        # Herzfrequenz berechnen: 60 Sekunden / durchschnittliche Zeit zwischen den Schlägen
        self.heart_rate = 60.0 / mean_rr
        return self.heart_rate

    def plot_time_series(self):
        """Plot der EKG-Daten mit roten Peaks"""
        self.find_peaks()  # Zuerst die Peaks mit der eigenen Methode finden
        self.fig = px.line(self.df.head(2000), x="Zeit in ms", y="Messwerte in mV")
        
        # Peaks als rote Punkte hinzufügen
        peaks_in_range = [p for p in self.peaks if p < 2000]
        self.fig.add_scatter(
            x=self.df["Zeit in ms"].iloc[peaks_in_range],
            y=self.df["Messwerte in mV"].iloc[peaks_in_range],
            mode="markers",
            marker=dict(color="red", size=8),
            name="Peaks"
        )


if __name__ == "__main__":
    print("This is a module with some functions to read the EKG data")
    file = open("data/person_db.json")
    person_data = json.load(file)
    ekg_dict = person_data[0]["ekg_tests"][0]
    ekg = EKGdata(ekg_dict)
    
    # Testlauf der Methoden in der Konsole
    ekg.find_peaks()
    print("Gefundene Peaks (Indizes):", ekg.peaks)
    print("Berechnete Herzfrequenz:", ekg.estimate_hr())
    print(ekg.df.head())
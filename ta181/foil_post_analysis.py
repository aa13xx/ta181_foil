#package
import openmc
import numpy as np
import pandas
import matplotlib.pyplot as plt

#other files
from functions import findpeakarea, peakfinder, broad_spectrum

def foil_peakarea(peakfinder_prominence, energy_bins):
    #extract tallies into pandas df
    sp = openmc.StatePoint(f"statepoint.20.h5")
    tally = sp.get_tally(name=f"{"pulse-height"}")
    intensity = list(tally.get_values(scores=["pulse-height"]).flatten())
    #chopping first entry because it is ridiculous and last entry because it is excessive
    energy = energy_bins[1:]
    energy_adjusted = energy[1:]

    df_openmc = pandas.DataFrame({'energy': energy_adjusted, 'intensity': intensity})

    #extract peakfinder results (peak energy, peak energy range)
    peak_energy_arr = peakfinder(df_openmc,peakfinder_prominence)[0]
    identified_peak_range = peakfinder(df_openmc,peakfinder_prominence)[1]

    #array of peak's area
    peak_area_arr = []
    for i,j in identified_peak_range:
        peak_area_arr.append(findpeakarea(df_openmc,i,j))

    return(peak_area_arr)

def foil_spectrum(energy_bins):
    #extract tallies into pandas df
    sp = openmc.StatePoint(f"statepoint.20.h5")
    tally = sp.get_tally(name=f"{"pulse-height"}")
    intensity = list(tally.get_values(scores=["pulse-height"]).flatten())
    #chopping first entry because it is ridiculous and last entry because it is excessive
    energy = energy_bins[1:]
    energy_adjusted = energy[1:]

    df_openmc = pandas.DataFrame({'energy': energy_adjusted, 'intensity': intensity})
    plt.plot(df_openmc.energy, df_openmc.intensity)
    plt.xlabel('Energy [keV]')
    plt.ylabel('Intensity')
    plt.show()

def foil_spectrum_processed(energy_bins, peakfinder_prominence, fit_a, fit_b, fit_c):
    #extract tallies into pandas df
    sp = openmc.StatePoint(f"statepoint.20.h5")
    tally = sp.get_tally(name=f"{"pulse-height"}")
    intensity = list(tally.get_values(scores=["pulse-height"]).flatten())
    #chopping first entry because it is ridiculous and last entry because it is excessive
    energy = energy_bins[1:]
    energy_adjusted = energy[1:]

    df_openmc = pandas.DataFrame({'energy': energy_adjusted, 'intensity': intensity})
    renorm_broadened_intensity = broad_spectrum(df_openmc.intensity.to_numpy(), energy, sum(df_openmc.intensity), fit_a, fit_b, fit_c) #gaussian broadening
    plt.plot(df_openmc.energy, renorm_broadened_intensity)
    plt.xlabel('Energy [keV]')
    plt.ylabel('Intensity')
    #extract peakfinder results (peak energy, peak energy range)
    peak_energy_arr = peakfinder(df_openmc,peakfinder_prominence)[0]

    for i in peak_energy_arr:
        plt.vlines(x=i, color="red", ls =':', label=f"{i}keV", ymin = 0, ymax=1e15)

    plt.show()
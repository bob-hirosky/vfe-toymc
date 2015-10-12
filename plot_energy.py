from ROOT import *
import math, re
import sys

""" Accepts a list of strings of the root files to be read.
    Input Files are generated by Example07.multifit.cc.
    Returns energy distribution histograms for each input file and a histogram
    ploting RMS of these histograms vs. the NSAMPLES that they are plotted with.

    Source: https://github.com/cms-eb-upgrade/vfe-toymc/
"""


def plot_energy(infiles):
    # Output file
    outFile = TFile("energy_error_plots.root", "Recreate")
    # The percent error (out of 1) around the histogram that will be checked
    # Done to weed out the many low energy pileup events (usually < 0.2 GeV)
    ERROR = 0.10
    # The number of bins to use in the histogram
    bins = 100
    # Histogram for standard deviations
    stdDevHist = TH1F("StdDev",
                    "Standard Deviation in Distribution vs. NSAMPLES for NFREQ=25;\
                    NSAMPLES; Standard Deviation",
                    99, 0.5, 99.5)
    # min and max used to modify the displayed range of the histogram
    minSampl = 100
    maxSampl = 0

    # Accessing each file and making the histograms
    for i, f in enumerate(infiles):
        # Accessing the file
        print "File", i+1, ":", f
        inFile = TFile(f, "Read")
        tree = inFile.Get("RecoAndSim")
        events = tree.GetEntries()

        # Getting and checking the stats for the file
        stats = map(int, re.findall(r'\d+',f))
        if (stats[1] < minSampl): minSampl = stats[1]
        if (stats[1] > maxSampl): maxSampl = stats[1]

        # Getting the true amplitude of the event
        tree.GetEntry(0)
        trueAmplitude = tree.amplitudeTruth

        # Making the histogram
        energyHist = TH1F("Energy Hist " + str(stats[1]), "Error of Signal Amplitude about True Amplitude;\
                        Error (GeV); Frequency",
                        bins, -ERROR*trueAmplitude, ERROR*trueAmplitude)

        # Filling the energy distribution histograms
        for event in range(0, events):
            tree.GetEntry(event)
            for i, sample in enumerate(tree.samplesReco):
                if (sample > (1 - ERROR)*trueAmplitude):
                    energyHist.Fill(sample - trueAmplitude, 1)

        # Filling the standard deviation histogram
        currStdDev = energyHist.GetStdDev()
        currStdDevErr = 1.0 / math.sqrt(2.0*(events - 1.0))*currStdDev
        stdDevHist.SetBinContent(stats[1], currStdDev)
        stdDevHist.SetBinError(stats[1], currStdDevErr)
        print "  NSAMPLES:", stats[1]
        print "  StdDev:", currStdDev
        print "  Error:", currStdDevErr
        # Writing the histogram
        outFile.cd()
        energyHist.Write()

    stdDevHist.GetXaxis().SetRangeUser(minSampl - 1, maxSampl + 1)
    stdDevHist.Write()
    outFile.Close()
    inFile.Close()

if (len(sys.argv) == 1):
    plot_energy(["output.0.9.25.root", "output.0.10.25.root", "output.0.11.25.root",
                 "output.0.12.25.root", "output.0.13.25.root", "output.0.14.25.root",
                 "output.0.15.25.root", "output.0.16.25.root", "output.0.17.25.root",
                 "output.0.18.25.root", "output.0.19.25.root", "output.0.20.25.root"])
elif (sys.argv[1] == "5"):
    print "Doing analysis with NFREQ = 5)"
    plot_energy(["output.0.25.5.root", "output.0.45.5.root", "output.0.46.5.root",
                 "output.0.47.5.root", "output.0.48.5.root", "output.0.49.5.root",
                 "output.0.50.5.root", "output.0.51.5.root", "output.0.52.5.root",
                 "output.0.53.5.root", "output.0.54.5.root", "output.0.55.5.root"])
else:
    plot_energy(sys.argv[1:])

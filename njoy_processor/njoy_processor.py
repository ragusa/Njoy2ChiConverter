"""Executes the main steps of conversion"""
import Utils_ReadNJOYOutput
import Utils_Combiner
import Utils_XSWriter

import sys 
import argparse

# ===================================== Check version
if sys.version_info[0] < 3:
    print("\n Error: This script requires python3 but was executed "
          "with version:\n\n"+sys.version+"\n")
    sys.exit(1)


# ===================================== Setup arguments
argparser = argparse.ArgumentParser(
    description="Executes the main steps of conversion")

argparser.add_argument("--output_path",
                       help="Complete path where to store the output xs",
                       default="", required=True)
argparser.add_argument("--njoy_output_filename",
                       help="Name of output file produced by NJOY",
                       default="", required=True)
argparser.add_argument("--chixs_filename",
                       help="Name of Chi XS file",
                       default="", required=True)
argparser.add_argument("--plot",
                       help="If included, will produce xs plots",
                       action='store_true', required=False)

args = argparser.parse_args()                                            


# ===================================== Read NJOY output
njoy_output_complete_path = args.output_path + "/" + args.njoy_output_filename
print("Reading NJOY output located at " + njoy_output_complete_path)
raw_njoy_data = Utils_ReadNJOYOutput.ReadNJOYfile(
    njoy_output_complete_path, verbose=True)

# ===================================== Combine disjoint data
print("Combining disjoint data")
data = Utils_Combiner.BuildCombinedData(raw_njoy_data, plot=args.plot)

# ===================================== Write cross-section
chi_output_complete_path = args.output_path + "/" + args.chixs_filename
print("Creating chi-cross-section in file " + chi_output_complete_path)
Utils_XSWriter.WriteChiTechFile(data, chi_output_complete_path)


# ===================================== Generate spectrum
import Utils_Info
# FIXME: plot should be able to use args.plot when other issues are fixed
Utils_Info.InfiniteMediumSpectrum(data, path=args.output_path, plot=True)

import argparse
import pandas
import simplekml

parser = argparse.ArgumentParser(description='Generate KML file from CSV file')
parser.add_argument('csv_file', type=str, help='CSV file to be converted to KML')
parser.add_argument('--output', "-o", type=str, help='Output KML file name')

args = parser.parse_args()

print(f"Loading file {args.csv_file} ...")

data = pandas.read_csv(args.csv_file)

kml = simplekml.Kml()

for i, cam_name in enumerate(data["cam_name"]):
    desc = data["notes"][i] + f" Deployed at: {data['time_AST'][i]} AST"
    kml.newpoint(name=cam_name, 
                 coords=[(data["longitude"][i], data["latitude"][i], data["altitude_m"][i])], 
                 description=desc,
                 altitudemode=simplekml.AltitudeMode.absolute)
    
    print("Added point for camera: ", cam_name)

if args.output:
    print(f"Saving KML file {args.output} ...")
    kml.save(f"{args.output}.kml")
else:
    print(f"Saving KML file {args.csv_file[:-4]}.kml ...")
    kml.save(f"{args.csv_file[:-4]}.kml")
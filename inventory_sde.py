
import arcpy 
import os
import csv

# populate with database connection file
ws = ""
arcpy.env.workspace = ws
# populate with existing path to folder
fldr = ""

# create feature dataset worksheet 
ws_desc = arcpy.Describe(ws)
ws_name = ws_desc.connectionProperties.database
fds_filename = f"FeatureDatasets_{ws_name}.csv"
fds_headers = ["Feature Dataset Name", "Spatial Reference Name", "WKID"]

fds = arcpy.ListDatasets(feature_type="Feature")

fds_list = []
for fd in fds:

    fd_desc = arcpy.Describe(fd)
    sr_name = fd_desc.spatialReference.name
    sr_wkid = fd_desc.spatialReference.factoryCode

    fds_list.append([fd, sr_name, sr_wkid])

fds_file = os.path.join(fldr, fds_filename)

with open(fds_file, "w") as f:

    fwriter = csv.writer(f)

    fwriter.writerow(fds_headers)

    fwriter.writerows(fds_list)

f.close()

# create feature class worksheets
fc_headers = ["Field Name", "Field Alias", "Type", "Length", "Domain"]

for fd in fds:
    filename = fd.split(".")[-1]
    fc_file = os.path.join(fldr, f"{ws_name}_{filename}.csv")

    with open(fc_file, "w") as f:

        fwriter = csv.writer(f)

        fwriter.writerow(fc_headers)

        fcs = arcpy.ListFeatureClasses(feature_dataset=fd)

        for fc in fcs:

            fwriter.writerow([fc])

            fields = arcpy.ListFields(fc)
            for fld in fields:
                fwriter.writerow([fld.name, fld.aliasName, fld.type, fld.length, fld.domain])

        f.close()

print('done')


# create standalone tables and fc worksheets
fc_headers = ["Field Name", "Field Alias", "Type", "Length", "Domain"]
sa_filename = f"StandaloneDatasets_{ws_name}.csv"
sa_file = os.path.join(fldr, sa_filename)

tables = arcpy.ListTables()
rasters = arcpy.ListRasters()
sa_fcs = arcpy.ListFeatureClasses()

with open(sa_file, "w") as f:

    fwriter = csv.writer(f)

    fwriter.writerow(fc_headers)

    for tab in tables:
        if not tab.endswith("__ATTACH"):

            fwriter.writerow([tab])

            fields = arcpy.ListFields(tab)
            for fld in fields:
                fwriter.writerow([fld.name, fld.aliasName, fld.type, fld.length, fld.domain])

    for fc in sa_fcs:

        fwriter.writerow([fc])

        fields = arcpy.ListFields(fc)
        for fld in fields:
            fwriter.writerow([fld.name, fld.aliasName, fld.type, fld.length, fld.domain])


    for ras in rasters:

        fwriter.writerow([f"{ras} - Raster"])

f.close()







from openpyxl import load_workbook

def write_result_to_file(file, result):
    file.write(
        f"""
        SLIDE: {result[0]}                          \n
        --- Nodules:                                \n
        --- --- Small: {result[1]}                  \n
        --- --- Medium: {result[2]}                 \n
        --- --- Large: {result[3]}                  \n
                                                    \n
        --- Total area: {result[4]} mm2             \n
                                                    \n
        """
    )


def write_results_to_disk(results, location):
    f = open(location, "w")
    
    f.write(
        f"""
        --- NODULE CLASSIFICATION RESULTS ---       \n
        Number of processed slides: {len(results)}  \n
                                                    \n
        Per slide breakdown:                        \n
        """
    )

    for result in results:
        write_result_to_file(f, result)

    f.close()

def write_results_to_excel(results, location):
    wb = load_workbook(location)
    print(wb.sheetnames)
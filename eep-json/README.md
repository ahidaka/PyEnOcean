#  PyEnOcean / eep-json

## How to generate these json files

1. You have to get and build **ptable** tool from DolphinRide/dpride.

    https://github.com/ahidaka/EnOceanGateways

    https://github.com/ahidaka/EnOceanGateways/tree/master/DolphinRide/dpride


2. Get an eep.xml file from somewhere.

3. Run **ptable** tool to generate essential parameters with xml file. 

    - All EEPs

    ```sh
    ./ptable -a -f eep.xml > outfile
    ```

    - Specified EEP

    ```sh
    ./ptable -e A5-02-01 -f eep.xml > outfile
    ```

4. Make sure the outfile is correct.

5. Convert the outfile to json file with **mkjson.awk**.

    ```sh
    ./mkjson.awk < outfile > master.json
    ```

6. You can modify these json file(s) as you like. 

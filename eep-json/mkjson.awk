#!/usr/bin/gawk -f

#{
#    "EepDefinitions" : {
#        "profile" : "D2-14-41",
#        "friendlyId" : "EnOceanTemperature",
#        "title" : "Indoor -Temperature, Humidity XYZ Acceleration, Illumination Sensor, Window Contact",
#        "functions" : [
#            {
#                "ValueType" : "Data",
#                "DataName" : "Temperature 10",
#                "ShortCut" : "TP",
#                "Bitoffs" : 0,
#                "Bitsize" : 10,
#                "RangeMin" : 0,
#                "RangeMax" : 1000,
#                "ScaleMin" : -40,
#                "ScaleMax" : 60,
#                "Unit" :"℃"
#            }
#        ]
#    }
#}

BEGIN {
    itemCount = 0;
    seqs = 0;
    eep = "";
    count = 0;
    lineCount = 0;
    title = "";
}

/^\*\*/ {
    #
    # Finish last line
    #
    if (eep != "") {
    # output last line haeader
	    print "             }";
	    print "         ]";
	    print "    }";
	    print "}";
    }

    #
    # Start new line
    #
    itemCount++;
    seqs = $2;
    eep = $3;
    count = $4;
    title = gensub(/.*<(.*)>.*/, "\\1", 1, $0);
    lineCount = 0;

    n = split(title, titles, " ");
    leading = titles[1];
    if (length(titles[2]) < 5 && length(titles[3]) > 5) {
	    traling = titles[3];
    }
    else {
	    traling = titles[2]
    }

    if (length(titles[1]) < 14) {
	    friendly = leading traling;
    }
    else {
	    friendly = leading;
    }
    gsub("[-/\.,]+", "", friendly);

    print "{";
    print "    \"EepDefinitions\" : {";
    printf("    \"profile\" : \"%s\",\n", eep);
    printf("    \"friendlyId\" : \"%s\",\n", friendly);
    printf("    \"title\" : \"%s\",\n", title);
    print "    \"functions\" : [";
    print "            {";
}

/^ / {
    lineCount++;
    separater = index($1, ":");
    type = substr($1, 1, separater-1);

    dataName = gensub(/.*:(.*)\{.*/, "\\1", 1, $0);
    shortCut = gensub(/.*\{(.*)\}.*/, "\\1", 1, $0);
    numberField = gensub(/.*\}(.*)\[.*/, "\\1", 1, $0);
    unit = gensub(/.*\[(.*)\]/, "\\1", 1, $0);

    if (unit == "(null)") {
        unit = "";
    }
        
    n = split(numberField, numbers, " ");
    bitOffs = numbers[1];
    bitSize = numbers[2];
    rangeMin = numbers[3];
    rangeMax = numbers[4];
    scaleMin = numbers[5];
    scaleMax = numbers[6];

    if (lineCount > 1) {
	    print "            },";
	    print "            {";
    }
    
    print "                \"ValueType\" : \"" type "\","; 
    print "                \"DataName\" : \"" dataName "\","; 
    print "                \"ShortCut\" : \"" shortCut "\","; 
    print "                \"Bitoffs\" : \"" bitOffs "\","; 
    print "                \"Bitsize\" : \"" bitSize "\","; 
    print "                \"RangeMin\" : \"" rangeMin "\","; 
    print "                \"RangeMax\" : \"" rangeMax "\","; 
    print "                \"ScaleMin\" : \"" scaleMin "\","; 
    print "                \"ScaleMax\" : \"" scaleMax "\","; 
    print "                \"Unit\" : \"" unit "\"";
}

END {
    #
    # Finish last line
    #
    print "             }";
    print "         ]";
    print "    }";
    print "}";
}

import openpyxl
import sys
import json
import os

# Help information
def PrintHelp():
    print("ISA Excel file analysis tool.")
    print("Usage:")
    print("  -v")
    print("  --version    Show tool current version.")
    print("  -V")
    print("  --verbose    Show more debug information.")
    print("  -c")
    print("  --check      Print encoding information with lit check prefix.")
    print("  -C=filename")
    print("  --configs=filename    Indicate the custom configuration file.")

# Parse arguments
isVerbose = False
printLitCheck = False
customConfigs = ""
if len(sys.argv) != 1:
    for index,arg in enumerate(sys.argv[1:]):
        if arg == "-V" or arg == "--verbose":
            isVerbose = True
        elif arg == "-c" or arg == "--check":
            printLitCheck = True
        elif arg == "-v" or arg == "--version":
            print("ISA Excel file analysis tool.")
            print("Version : 0.2")
            exit(0)
        elif arg.startswith("-C=") or arg.startswith("--configs="):
            customConfigs = arg[arg.find("=")+1:]
            print(customConfigs)

        else:
            PrintHelp()
            exit(0)

# Open configuration file
if os.path.exists("configs.json"):
    cfgFile = open("configs.json", 'r')
elif customConfigs:
    try:
        cfgFile = open(customConfigs, 'r')
    except FileNotFoundError as err:
        print("Error: Can not find configuration file: " + customConfigs)
        exit(-1)
else:
    print("Error: Can not find configuration file")
    exit(-1)
cfgs = json.loads(cfgFile.read())
cfgFile.close()

register = cfgs['register']
operandsEncode = cfgs['operandsEncode']
excelFile = cfgs['excelFileName']

# Open ISA excel file
try:
    xml = openpyxl.load_workbook(excelFile)
    sheets = xml.sheetnames
except FileNotFoundError as err:
    print("Error: Can not find ISA file: " + excelFile)
    exit(-1)

# Interactive instruction check
# Select excel sheet
print("Sheets:")
for index,names in enumerate(sheets):
    print(names + " --- " + str(index))
selectSheet = input("Select sheet: ")
table = xml[sheets[int(selectSheet)]]

instrFormat = []
encode = []
instrEncode = []

for r in table.rows:
    instrFormat.append(r[2].value)
    for i in range(3, 3+31):
        v = r[i].value
        t = i
        while v == None:
            t = t - 1
            v = r[t].value
        f = str(v).find('_')
        if f != -1:
            v = v[0:f]

        encode.append(v)
    instrEncode.append(encode)
    encode = []

oldInputIndex = 0
while True:
    print("========")
    searchIndex = input("Input a line number(Enter to next, Q/q to quit): ")
    if searchIndex == 'q' or searchIndex == 'Q':
        exit(0)
    if not searchIndex:
        searchIndex = oldInputIndex + 1
    oldInputIndex = int(searchIndex)

    searchEncode = list(instrEncode[int(searchIndex)-1])

    instrStr = instrFormat[int(searchIndex)-1]
    print("InstrFormat: " + instrStr)
    if isVerbose:
        print("Description Encode: " + str(searchEncode))

    # here come input searchEncode
    i = 31
    pre = []
    bins = ''
    binEncode = []
    illegal = False
    while i > 0:
        i = i - 1
        e = searchEncode[i]
        if len(bins) > 8:
            binEncode.append(bins[-8:])
            bins = bins[:-8]

        if e == 'x':
            print("Warning: Illegal encoding bit: '" + e + "' in " + str(30-i))
            illegal = True
            break

        if e != 0 and e != 1:

            if e in operandsEncode:
                if e in pre:
                    searchEncode[i] = 0
                    bins = str(0) + bins
                    continue

                op = operandsEncode[e]
                if isVerbose:
                    print("Value of operand " + e + " is " + str(op))
                while True:
                    if searchEncode[i] != e:
                        print("Error: Operand encoding out of range")
                        exit(1)

                    if (op & 0b1) == 0b1:
                        searchEncode[i] = 1
                        bins = str(1) + bins
                    else:
                        searchEncode[i] = 0
                        bins = str(0) + bins
                    op = op >> 1
                    if op == 0:
                        break
                    i = i - 1
                pre.append(e)
                continue

            else:
                print("Error: Unknown operand key")
                exit(1)

        bins = str(e) + bins

    if illegal:
        continue

    binEncode.append(bins)

    hexEncode = []
    for e in binEncode:
        hexEncode.append('0x%02X' % int(e, 2))#hex(int(e, 2)))

    if isVerbose:
        print("Binary Encode:")
        print(searchEncode)
    print("Hexadecimal Encode:")
    if printLitCheck:
        encodeStr = ""
        for e in hexEncode:
            encodeStr = encodeStr + "," + e
        encodeStr = encodeStr[1:]
        print("# CHECK: " + encodeStr)
    else:
        print(hexEncode)


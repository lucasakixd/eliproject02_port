# Export XREFs and decompilation data for the Elifoot 2002 Ghidra program.
# Run from Ghidra's Script Manager with the analyzed Elifoot2002.exe open.
# Output is written to analysis/ghidra_exports beside this script.

#@category Elifoot

from java.io import BufferedWriter, File, FileOutputStream, OutputStreamWriter
from ghidra.app.decompiler import DecompInterface


XREF_ADDRESSES = [
    "00479C78",
    "00479C7C",
    "00479734",
    "00479740",
    "0047974C",
    "00479758",
    "0049602C",
    "004972F4",
]

FUNCTION_TARGETS = [
    ("FUN_00476d90", "00476d90"),
    ("FUN_00477428", "00477428"),
    ("FUN_00477950", "00477950"),
]

FORM_TARGETS = [
    {
        "name": "TCOACHMANAGERDLG",
        "resource_symbol": "Rsrc_RC_Data_TCOACHMANAGERDLG_0",
        "resource_address": "0050ba48",
        "class_string_address": "004adb8a",
    },
    {
        "name": "TCLASSIFICATIONDLG",
        "resource_symbol": "Rsrc_RC_Data_TCLASSIFICATIONDLG_0",
        "resource_address": "00501248",
        "class_string_address": "004adb50",
    },
]


def text(value):
    if value is None:
        return u""
    try:
        return unicode(value)
    except:
        return unicode(str(value))


def csv_field(value):
    value = text(value).replace(u'"', u'""')
    return u'"' + value + u'"'


def csv_line(values):
    return u",".join([csv_field(value) for value in values]) + u"\n"


def write_utf8(file_obj, content):
    stream = BufferedWriter(OutputStreamWriter(FileOutputStream(file_obj), "UTF-8"))
    try:
        stream.write(text(content))
    finally:
        stream.close()


def write_csv(directory, file_name, header, rows):
    output_file = File(directory, file_name)
    stream = BufferedWriter(OutputStreamWriter(FileOutputStream(output_file), "UTF-8"))
    try:
        stream.write(csv_line(header))
        for row in rows:
            stream.write(csv_line(row))
    finally:
        stream.close()
    return output_file


def address_hex(address):
    if address is None:
        return ""
    return address.toString()


def function_for(address):
    function = currentProgram.getFunctionManager().getFunctionAt(address)
    if function is None:
        function = currentProgram.getFunctionManager().getFunctionContaining(address)
    return function


def function_name_for(address):
    function = function_for(address)
    if function is None:
        return ("", "")
    return (function.getName(), address_hex(function.getEntryPoint()))


def symbol_map():
    result = {}
    symbols = currentProgram.getSymbolTable().getAllSymbols(True)
    while symbols.hasNext():
        symbol = symbols.next()
        name = symbol.getName()
        if name not in result:
            result[name] = symbol
    return result


def references_to(address):
    return list(currentProgram.getReferenceManager().getReferencesTo(address))


def reference_row(target_label, target_address, reference):
    source_address = reference.getFromAddress()
    source_function, source_entry = function_name_for(source_address)
    instruction = currentProgram.getListing().getInstructionAt(source_address)
    instruction_text = ""
    if instruction is not None:
        instruction_text = instruction.toString()
    return [
        target_label,
        address_hex(target_address),
        address_hex(source_address),
        reference.getReferenceType().getName(),
        reference.getOperandIndex(),
        reference.isPrimary(),
        source_function,
        source_entry,
        instruction_text,
    ]


def get_script_directory():
    try:
        source_file = getSourceFile()
        if source_file is not None:
            return source_file.getParentFile()
    except:
        pass
    return File(currentProgram.getExecutablePath()).getParentFile()


def add_form_reference(rows, seen, form_name, kind, target_address, reference):
    source = reference.getFromAddress()
    key = (form_name, kind, address_hex(target_address), address_hex(source),
           reference.getOperandIndex())
    if key in seen:
        return
    seen.add(key)
    row = reference_row(kind, target_address, reference)
    rows.append([form_name] + row[1:])


if currentProgram is None:
    raise Exception("Open the analyzed Elifoot 2002 program before running this script.")

script_directory = get_script_directory()
output_directory = File(script_directory, "ghidra_exports")
if not output_directory.exists() and not output_directory.mkdirs():
    raise Exception("Could not create output directory: " + output_directory.getAbsolutePath())

memory = currentProgram.getMemory()
reference_manager = currentProgram.getReferenceManager()
function_manager = currentProgram.getFunctionManager()
listing = currentProgram.getListing()
symbols_by_name = symbol_map()

summary = []

# Export references to exact addresses supplied for this binary version.
xref_rows = []
for address_text in XREF_ADDRESSES:
    address = toAddr(address_text)
    if not memory.contains(address):
        summary.append("XREF target outside program memory: " + address_text)
        continue
    refs = references_to(address)
    summary.append("XREF %s: %d reference(s)" % (address_text, len(refs)))
    for reference in refs:
        xref_rows.append(reference_row(address_text, address, reference))

write_csv(
    output_directory,
    "xrefs.csv",
    ["target", "target_address", "from_address", "reference_type", "operand_index",
     "primary", "source_function", "source_function_entry", "instruction"],
    xref_rows,
)

# Export metadata and decompiled C for the three requested functions.
function_rows = []
decompiler = DecompInterface()
decompiler.openProgram(currentProgram)
decompiled_parts = ["/* Elifoot 2002 selected functions; generated by Ghidra. */\n"]
try:
    for requested_name, address_text in FUNCTION_TARGETS:
        address = toAddr(address_text)
        function = function_manager.getFunctionAt(address)
        if function is None:
            function = function_manager.getFunctionContaining(address)
        if function is None:
            function_rows.append([requested_name, address_text, "", "", "missing", "No function at address"])
            decompiled_parts.append("/* MISSING: %s at %s */\n" % (requested_name, address_text))
            continue

        result = decompiler.decompileFunction(function, 120, monitor)
        if result.decompileCompleted() and result.getDecompiledFunction() is not None:
            source = result.getDecompiledFunction().getC()
            status = "decompiled"
            decompiled_parts.append("\n/* REQUESTED: %s; ENTRY: %s */\n" %
                                   (requested_name, address_hex(function.getEntryPoint())))
            decompiled_parts.append(text(source))
            if not text(source).endswith(u"\n"):
                decompiled_parts.append("\n")
            error_message = ""
        else:
            status = "failed"
            error_message = result.getErrorMessage()
            decompiled_parts.append("\n/* DECOMPILATION FAILED: %s at %s: %s */\n" %
                                   (requested_name, address_text, error_message))

        function_rows.append([
            requested_name,
            address_hex(function.getEntryPoint()),
            function.getName(),
            text(function.getSignature()),
            status,
            error_message,
        ])
        summary.append("Function %s (%s): %s" %
                       (requested_name, address_text, status))
finally:
    decompiler.dispose()

write_csv(
    output_directory,
    "functions.csv",
    ["requested_name", "entry_address", "ghidra_name", "signature", "status", "error"],
    function_rows,
)
write_utf8(File(output_directory, "functions.c"), u"".join(decompiled_parts))

# Export references to form resource data, class-name strings, and functions
# containing those references. The class-string addresses come from strings.csv.
form_reference_rows = []
form_function_rows = []
form_seen = set()
form_function_seen = set()
resource_ranges = []

resource_symbols = []
for symbol_name, symbol in symbols_by_name.items():
    if symbol_name.startswith("Rsrc_RC_Data_"):
        resource_symbols.append((symbol.getAddress().getOffset(), symbol_name, symbol.getAddress()))
resource_symbols.sort(key=lambda item: item[0])

for form in FORM_TARGETS:
    form_name = form["name"]
    resource_address = toAddr(form["resource_address"])
    class_string_address = toAddr(form["class_string_address"])
    resource_symbol = symbols_by_name.get(form["resource_symbol"])

    if resource_symbol is not None:
        resource_address = resource_symbol.getAddress()
    else:
        summary.append("Form resource symbol not found: " + form["resource_symbol"])

    if not memory.contains(resource_address):
        summary.append("Form resource outside program memory: " + form_name)
    else:
        refs = references_to(resource_address)
        summary.append("Form resource %s: %d direct reference(s)" % (form_name, len(refs)))
        for reference in refs:
            add_form_reference(form_reference_rows, form_seen, form_name,
                               "resource_symbol", resource_address, reference)

    if memory.contains(class_string_address):
        refs = references_to(class_string_address)
        summary.append("Form class string %s: %d direct reference(s)" % (form_name, len(refs)))
        for reference in refs:
            add_form_reference(form_reference_rows, form_seen, form_name,
                               "class_name_string", class_string_address, reference)

    # Bound a resource scan by the next imported form-resource label.
    resource_end = resource_address.add(1)
    for offset, symbol_name, symbol_address in resource_symbols:
        if symbol_address.getAddressSpace() == resource_address.getAddressSpace() and \
                symbol_address.getOffset() > resource_address.getOffset():
            resource_end = symbol_address
            break
    resource_ranges.append((form_name, resource_address, resource_end))

# Scan instruction references once so references to interior resource data are
# included, not only references to the resource label itself.
instruction_iterator = listing.getInstructions(True)
while instruction_iterator.hasNext():
    monitor.checkCancelled()
    instruction = instruction_iterator.next()
    for reference in instruction.getReferencesFrom():
        target = reference.getToAddress()
        if target is None or not target.isMemoryAddress():
            continue
        for form_name, range_start, range_end in resource_ranges:
            if target.getAddressSpace() == range_start.getAddressSpace() and \
                    range_start.compareTo(target) <= 0 and target.compareTo(range_end) < 0:
                add_form_reference(form_reference_rows, form_seen, form_name,
                                   "resource_interior", target, reference)

for row in form_reference_rows:
    function_name = row[6]
    function_entry = row[7]
    if function_name:
        key = (row[0], function_name, function_entry)
        if key not in form_function_seen:
            form_function_seen.add(key)
            form_function_rows.append([row[0], function_name, function_entry])

write_csv(
    output_directory,
    "form_references.csv",
    ["form_name", "target_address", "from_address", "reference_type", "operand_index",
     "primary", "source_function", "source_function_entry", "instruction"],
    form_reference_rows,
)
write_csv(
    output_directory,
    "form_functions.csv",
    ["form_name", "function_name", "function_entry"],
    form_function_rows,
)

summary.append("Form reference rows: %d" % len(form_reference_rows))
summary.append("Associated functions: %d" % len(form_function_rows))
summary.append("Output directory: " + output_directory.getAbsolutePath())
write_utf8(File(output_directory, "summary.txt"), u"\n".join([text(item) for item in summary]) + u"\n")

print("Elifoot export completed: " + output_directory.getAbsolutePath())
for line in summary:
    print(line)
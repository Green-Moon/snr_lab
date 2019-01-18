#trials to check: transpose from C1 to C1, Eb vs Ds, C1 to C2, C2 to C1, C1 to D above vs D below, atonal, minor
    # this cannot change the clef. we as a project will not change the clef.

#transposing from C major
every_single_note = ["C", "Cs", "D", "Ds", "E", "F", "Fs", "G", "Gs", "A", "As", "B"] # will have to deal w the fact that smth mgith b say Eb as opposed to Ds
key_num_to_letter = ["Cb", "Gb", "Db", "Ab", "Eb", "Bb", "F", "C", "G", "D", "A", "E", "B", "Fs", "Cs"] # the index starts at -7 (seven flats)
# ignoring the existence of minor keys, because then i woud have to change <key><mode></></>
transposition_steps = {} # steps:note name
# Fs = F sharp, Fb = F flat (((((((((((-> bb = b flat the note, Bs = B sharp (C) the key)))))))))))))

def make_diffs(original, new, direction): #notediff, keydiff
    #newnum =
    #will direction only matter when there are octave differences???
    return (7, "5")

def note_tranposition(oldlines, notediff):
    #print("hi", oldlines)
    global every_single_note
    newline = []
    close = ""
    stepind_innotearray = 0
    alternum = 0
    octavenum = 0

    for line in oldlines:
        if "pitch>" in line:
            if "/" in line:
                close = close + line
            else:
                newline.append(line)
        else:
            ind =  line.index("<")
            if "step" in line:
                stepind_innotearray = every_single_note.index(line[ind + 6:ind+7])
            elif "alter" in line:
                alterstring = line[ind + 7:ind+9]
                #alternum = int(alterstring[1:])
                if "-" in alterstring:
                    alternum = -1*int(alterstring)
                else:
                    alternum = int(alterstring[0:1])
            elif "octave" in line:
                octavenum = int(line[ind+8:ind + 9])
    i = stepind_innotearray + alternum
    if i >= len(every_single_note):
        i = i - len(every_single_note)
    newi = i + notediff
    if newi >= len(every_single_note):
        octavenum += 1
        newi = newi - len(every_single_note)
    new_note = every_single_note[newi]
    newalter = "0"
    if len(new_note) > 1:
        if "s" in new_note:
            newalter = "1"
            new_note = every_single_note[newi-1]
        else:
            newalter = "-1"
            new_note = every_single_note[newi+1]
    #print(new_note, newalter)
    stepline = oldlines[1][0:ind+6] + new_note + oldlines[1][ind+7:]
    alterline = oldlines[1][0:ind] + "<alter>" + newalter + "</alter" + oldlines[1][ind+13:]
    octaveline = oldlines[1][0:ind] + "<octave>" + str(octavenum) + "</octave" + oldlines[1][ind+13:]
    #print("AHHHHHHHHHHHHH", stepline, alterline, octaveline)
    newline.append(stepline)
    newline.append(alterline)
    newline.append(octaveline)
    newline.append(close)
    #print("AHHHHHHHHHHHHHHHHHHHH", oldlines, "FFFFFFFFFF", newline)
    return newline

def copy_all(filename, original, new, direction):
    file = open(filename)
    new_file = "Transposedmtj1111111111" + filename
    newfile = open(new_file, "w+")
    notediff, keydiff = make_diffs(original, new, direction) # number, string

    in_note = False
    pitch_section = [] # from <pitch to </pitch, incl/incl
    for line in file:
        # note transposition section
        if "<pitch" in line:
            in_note = True
        if in_note:
            pitch_section.append(line)
            #print(pitch_section) # it does this right
            if "</pitch" in line:
                in_note = False
                print(pitch_section)
                newline = note_tranposition(pitch_section, notediff) # [<pi, </pitch>] # incl, incl
                print(newline, "END :)")
                pitch_section = []
                for l in newline:
                    newfile.write(l)
        #end of note transposition section

        else:
            #key transpsition section
            if "<fifths" in line:
                keynum = line[18:20]
                if "0" in keynum:
                    newline = line[:18] + keydiff + line[19:]
                else:
                    newline = line[:18] + keydiff + line[20:]
            #end of key transposition section

            #everything else
            else:
                newline = line
            newfile.write(newline)
            #end of everything else section
    #end of for loop
    return newfile

def main(filename, original, new, direction):
    transposedxml = copy_all(filename, original, new, direction)
    print("done :)")

main("ActorPreludeSample.musicxml", "C", "G", "+") #usr/cmc/library (use the finder disembodied search bar to find this)/preferences/pycharm or whatever/scratches



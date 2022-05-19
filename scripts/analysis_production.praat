uttrList = Read Table from comma-separated file: "../results/apology_test.csv"
nOfUttrs = Get number of rows
tgList = Create Strings as file list: "filelist_TextGrid", "../results/TextGrid/*.TextGrid"
nOfTGs = Get number of strings
#intList = Create Strings as file list: "filelist_intensity", "../results/Intensity/*.intensity"
#nOfInts = Get number of strings

dirTG$ = "../results/TextGrid/"
dirInt$ = "../results/Intensity/"
dirPitch$ = "../results/Pitch/"

tableID = Create Table with column names: "data_kaken_apology", 0,
	... "filename subject q1 q2 q3 q4 mora word initial_tone final_tone accented_mora
	... mora_dur mora_int mora_f0_max
	... word_dur word_int word_f0_range
	..."
rowNo = 0

#q1 この状況で申し訳なく感じますか (1-100)
#q2 自分に責任があると感じますか (1-100)
#q3 この状況で謝罪しなければいけないとしたら不満に感じますか (1-100)
#q4 実際に謝罪しますか (1/0)

for i to nOfTGs 
	selectObject: tgList
	tgName$ = Get string: i
	uttrName$ = tgName$ - ".TextGrid"
	sbj$ = left$(uttrName$, 15)
	intName$ = uttrName$ + ".Intensity"
	pitchName$ = uttrName$ + ".Pitch"
	selectObject: uttrList
	for j to nOfUttrs
		if do$("Get value...", j, "test_id") = uttrName$
			q1 = Get value: j, "q1"
			q2 = Get value: j, "q2"
			q3 = Get value: j, "q3"
			q4$ = Get value: j, "q4"
			if q4$ = "yes"
				q4 = 1
			elsif q4$ = "no"
				q4 = 0
			endif
		endif
	endfor
	tgID = Read from file: dirTG$ + tgName$
	segTierNo = 0
	moraTierNo = 0
	wordTierNo = 0
	toneTierNo = 0

	for j to do("Get number of tiers")
		if do$("Get tier name...", j) = "segment"
			segTierNo = j
		elsif do$("Get tier name...", j) = "mora"
			moraTierNo = j
		elsif do$("Get tier name...", j) = "word"
			wordTierNo = j
		elsif do$("Get tier name...", j) = "tone"
			toneTierNo = j
		endif
	endfor

	if moraTierNo != 0
		word$ = Get label of interval: wordTierNo, 2
		wordStart = Get start time of interval: wordTierNo, 2
		wordEnd = Get end time of interval: wordTierNo, 2
		wordDur = wordEnd - wordStart

		initialTone$ = Get label of point: toneTierNo, 1
		if do("Get number of points...", toneTierNo) = 3
			finalTone$ = Get label of point: toneTierNo, 3
			accTime = Get time of point: toneTierNo, 2
			accMoraIndex = Get interval at time: moraTierNo, accTime
			accMora$ = Get label of interval: moraTierNo, accMoraIndex
		elsif do("Get number of points...", toneTierNo) = 2
			finalTone$ = Get label of point: toneTierNo, 2
			accMora$ = "NA"
		endif

		intID = Read from file: dirInt$ + intName$
		wordInt = Get mean: wordStart, wordEnd, "energy"

		pitchID = Read from file: dirPitch$ + pitchName$
		wordF0Max = Get maximum: wordStart, wordEnd, "Hertz", "Parabolic"
		wordF0Min = Get minimum: wordStart, wordEnd, "Hertz", "Parabolic"
		wordF0Range = wordF0Max - wordF0Min

		selectObject: tgID
		for j to do("Get number of intervals...", moraTierNo)
			mora$ = Get label of interval: moraTierNo, j

			if mora$ != ""

				moraStart = Get start time of interval: moraTierNo, j
				moraEnd = Get end time of interval: moraTierNo, j
				moraDur = moraEnd - moraStart	

				selectObject: intID
				moraInt = Get mean: moraStart, moraEnd, "energy"

				selectObject: pitchID
				moraF0Max = Get maximum: moraStart, moraEnd, "Hertz", "Parabolic"

				selectObject: tableID
				Append row
				rowNo += 1
				Set string value: rowNo, "filename", uttrName$
				Set string value: rowNo, "subject", sbj$
				Set numeric value: rowNo, "q1", q1
				Set numeric value: rowNo, "q2", q2
				Set numeric value: rowNo, "q3", q3
				Set numeric value: rowNo, "q4", q4
				Set string value: rowNo, "mora", mora$
				Set string value: rowNo, "word", word$
				Set string value: rowNo, "initial_tone", initialTone$
				Set string value: rowNo, "final_tone", finalTone$
				Set string value: rowNo, "accented_mora", accMora$
				Set numeric value: rowNo, "mora_dur", moraDur
				Set numeric value: rowNo, "mora_int", moraInt
				Set numeric value: rowNo, "mora_f0_max", moraF0Max
				Set numeric value: rowNo, "word_dur", wordDur
				Set numeric value: rowNo, "word_int", wordInt
				Set numeric value: rowNo, "word_f0_range", wordF0Range

			endif
			selectObject: tgID
		endfor
		removeObject: intID, pitchID
	endif

	removeObject: tgID
endfor

selectObject: tableID
Save as comma-separated file: "../results/data/" + "data_kaken_apology.csv"

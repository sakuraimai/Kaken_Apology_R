uttrList = Read Table from comma-separated file: "../results/apology_test.csv"
nOfUttrs = Get number of rows
wavList = Create Strings as file list: "filelist_wav", "../results/wav/*.wav"
nOfWavs = Get number of strings
tgList = Create Strings as file list: "filelist_TextGrid", "../results/TextGrid/*.TextGrid"
nOfTGs = Get number of strings
dirWav$ = "../results/wav/"
dirTG$ = "../results/TextGrid/"

clearinfo

for i to nOfWavs 
	selectObject: wavList
	wavName$ = Get string: i
	uttrName$ = wavName$ - ".wav"
	tgName$ = uttrName$ + ".TextGrid"
	existTG = 0
	selectObject: tgList
	for j to nOfTGs
		if (do$("Get string...", j)) = tgName$
			existTG = 1
		endif
	endfor
	if existTG = 0
		selectObject: uttrList
		existUttr = 0
		needsEditing = 0
		for k to nOfUttrs
			if do$("Get value...", k, "test_id") = uttrName$ 
				existUttr = 1
				apology$ = Get value: k, "word"
				if apology$ = "ごめん"
					word$ = "gomen"
				elsif apology$ = "ごめんね"
					word$ = "gomenne"
				elsif apology$ = "ごめんなさい"
					word$ = "gomennasai"
				elsif apology$ = "すみません"
					word$ = "sumimasen"
				elsif apology$ = "すみませんでした"
					word$ = "sumimasendesita"
				elsif apology$ = "申し訳ないです"
					word$ = "moosiwakenaidesu"
				elsif apology$ = "申し訳ありません"
					word$ = "moosiwakearimasen"
				elsif apology$ = "申し訳ありませんでした"
					word$ = "moosiwakearimasendesita"
				else
					exit Word for 'uttrName$' not defined in the script. 
				endif
			endif
		endfor
		if existUttr = 0
			exit 'uttrName$' not listed in 'apology_test.csv.'
		endif
		wavID = Read from file: dirWav$ + wavName$
		tgID = To TextGrid (silences): 100, 0, -25, 0.1, 0.1, "", word$
		if do("Get number of intervals...", 1) > 3
			appendInfoLine: "More than one word recognised in 'tgName$'."
			needsEditing = 1
		endif
		Set tier name: 1, "word"
		Save as text file: dirTG$ + tgName$
		if needsEditing = 0
			removeObject: wavID, tgID
		endif
	endif
endfor

form readFiles
	sentence subject *
	comment e.g. P20211210
	comment Asterisk (*) for all subjects
	comment (P2021* for subject IDs P20210001-P20211231)
	choice word 1
		button all_words
		button gomen
		button gomenne
		button gomennasai
		button sumimasen
		button sumimasendesita
		button moosiwakenaidesu
		button moosiwakearimasen
		button moosiwakearimasendesita
	boolean read_unmodified_files_only 0
	boolean open_files 1
	comment Only the first 20 files will be opened. 
endform

dirWav$ = "../results/wav/"
dirTG$ = "../results/TextGrid/"

clearinfo
filelist = Create Strings as file list: "filelist_TG", dirTG$ + subject$ + "*.TextGrid"

if word$ != "all_words"
	nOfStrings = Get number of strings
	for i to nOfStrings
		selectObject: filelist
		tgName$ = Get string: i 
		tgID = Read from file: dirTG$ + tgName$
		wordTierNo = 0
		for j to do("Get number of tiers")
			if do$("Get tier name...", j) = "word"
				wordTierNo = j
				curWord$ = Get label of interval: wordTierNo, 2
			endif
		endfor
		if wordTierNo = 0
			exit No word tier in 'tgName$'
		endif
		if curWord$ != word$
			selectObject: filelist
			Remove string: i
			nOfStrings -= 1
			i -= 1
		endif
		removeObject: tgID
	endfor
endif

if read_unmodified_files_only = 1
	selectObject: filelist
	nOfStrings = Get number of strings
	for i to nOfStrings
		selectObject: filelist
		tgName$ = Get string: i 
		tgID = Read from file: dirTG$ + tgName$
		existSegTier = 0
		existWordTier = 0
		for j to do("Get number of tiers")
			if do$("Get tier name...", j) = "segment"
				segTierNo = j
				existSegTier = 1
			elsif do$("Get tier name...", j) = "word"
				wordTierNo = j
				existWordTier = 1
			endif
		endfor
		if existSegTier = 1 and existWordTier = 1
			tgModified = 1
			wordStart = Get start time of interval: wordTierNo, 2
			wordEnd = Get end time of interval: wordTierNo, 2
			wordDur = wordEnd - wordStart
			nOfSegs = Get number of intervals: segTierNo
			meanSegDur = wordDur / (nOfSegs - 2)
			for j from 2 to nOfSegs - 2
				segEnd = Get end time of interval: segTierNo, j
				if segEnd = wordStart + (j - 1) * meanSegDur
					tgModified = 0
				endif
			endfor
			if tgModified = 1
				selectObject: filelist
				Remove string: i
				nOfStrings -= 1
				i -= 1
			endif
		endif
		removeObject: tgID
	endfor
endif

selectObject: filelist
nOfStrings = Get number of strings

if nOfStrings > 100
	pauseScript: "More than 100 files to read. Continue?"
endif

openedFiles = 0

for i to nOfStrings
	selectObject: filelist
	tgName$ = Get string: i
	wavName$ = tgName$ - ".TextGrid" + ".wav"
	wavID = Read from file: dirWav$ + wavName$ 
	tgID = Read from file: dirTG$ + tgName$ 
	if open_files = 1 and openedFiles < 20
		selectObject: wavID, tgID
		View & Edit
		openedFiles += 1
	endif
endfor

removeObject: filelist

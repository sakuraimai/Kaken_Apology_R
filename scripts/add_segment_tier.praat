tgList = Create Strings as file list: "filelist_TextGrid", "../results/TextGrid/*.TextGrid"
nOfTGs = Get number of strings
dirTG$ = "../results/TextGrid/"

for i to nOfTGs 
	selectObject: tgList
	fileName$ = Get string: i
	fileID = Read from file: dirTG$ + fileName$
	if do("Get number of tiers") = 1 and do$("Get tier name...", 1) = "word"
		Insert interval tier: 1, "segment"
		Insert point tier: 3, "comment"
		segTierNo = 1
		wordTierNo = 2	
		word$ = Get label of interval: wordTierNo, 2
		@segments
		wordStart = Get start time of interval: wordTierNo, 2
		wordEnd = Get start time of interval: wordTierNo, 3
		wordDur = wordEnd - wordStart
		segDur = wordDur / nSegs
		for j to nSegs
			intStart = wordStart + segDur * (j - 1)
			Insert boundary: segTierNo, intStart
			Set interval text: segTierNo, j + 1, seg$[j]
		endfor
		Insert boundary: segTierNo, wordEnd
		Save as text file: dirTG$ + fileName$
	endif
	removeObject: fileID
endfor

########################################
procedure segments

if word$ = "gomen"
	nSegs = 5
	seg$[1] = "g"
	seg$[2] = "o"
	seg$[3] = "m"
	seg$[4] = "e"
	seg$[5] = "n"
elsif word$ = "gomenne"
	nSegs = 7
	seg$[1] = "g"
	seg$[2] = "o"
	seg$[3] = "m"
	seg$[4] = "e"
	seg$[5] = "n"
	seg$[6] = "n"
	seg$[7] = "e"
elsif word$ = "gomennasai"
	nSegs = 10
	seg$[1] = "g"
	seg$[2] = "o"
	seg$[3] = "m"
	seg$[4] = "e"
	seg$[5] = "n"
	seg$[6] = "n"
	seg$[7] = "a"
	seg$[8] = "s"
	seg$[9] = "a"
	seg$[10] = "i"
elsif word$ = "sumimasen"
	nSegs = 9
	seg$[1] = "s"
	seg$[2] = "u"
	seg$[3] = "m"
	seg$[4] = "i"
	seg$[5] = "m"
	seg$[6] = "a"
	seg$[7] = "s"
	seg$[8] = "e"
	seg$[9] = "n"
elsif word$ = "sumimasendesita"
	nSegs = 15
	seg$[1] = "s"
	seg$[2] = "u"
	seg$[3] = "m"
	seg$[4] = "i"
	seg$[5] = "m"
	seg$[6] = "a"
	seg$[7] = "s"
	seg$[8] = "e"
	seg$[9] = "n"
	seg$[10] = "d"
	seg$[11] = "e"
	seg$[12] = "s"
	seg$[13] = "i"
	seg$[14] = "t"
	seg$[15] = "a"
elsif word$ = "moosiwakenaidesu"
	nSegs = 16
	seg$[1] = "m"
	seg$[2] = "o"
	seg$[3] = "o"
	seg$[4] = "s"
	seg$[5] = "i"
	seg$[6] = "w"
	seg$[7] = "a"
	seg$[8] = "k"
	seg$[9] = "e"
	seg$[10] = "n"
	seg$[11] = "a"
	seg$[12] = "i"
	seg$[13] = "d"
	seg$[14] = "e"
	seg$[15] = "s"
	seg$[16] = "u"
elsif word$ = "moosiwakearimasen"
	nSegs = 17
	seg$[1] = "m"
	seg$[2] = "o"
	seg$[3] = "o"
	seg$[4] = "s"
	seg$[5] = "i"
	seg$[6] = "w"
	seg$[7] = "a"
	seg$[8] = "k"
	seg$[9] = "e"
	seg$[10] = "a"
	seg$[11] = "r"
	seg$[12] = "i"
	seg$[13] = "m"
	seg$[14] = "a"
	seg$[15] = "s"
	seg$[16] = "e"
	seg$[17] = "n"
elsif word$ = "moosiwakearimasendesita"
	nSegs = 23
	seg$[1] = "m"
	seg$[2] = "o"
	seg$[3] = "o"
	seg$[4] = "s"
	seg$[5] = "i"
	seg$[6] = "w"
	seg$[7] = "a"
	seg$[8] = "k"
	seg$[9] = "e"
	seg$[10] = "a"
	seg$[11] = "r"
	seg$[12] = "i"
	seg$[13] = "m"
	seg$[14] = "a"
	seg$[15] = "s"
	seg$[16] = "e"
	seg$[17] = "n"
	seg$[18] = "d"
	seg$[19] = "e"
	seg$[20] = "s"
	seg$[21] = "i"
	seg$[22] = "t"
	seg$[23] = "a"
else
	exit Check the word in 'fileName$'.
endif

endproc
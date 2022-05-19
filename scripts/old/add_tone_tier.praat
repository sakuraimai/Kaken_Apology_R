tgList = Create Strings as file list: "filelist_TextGrid", "../results/TextGrid/*.TextGrid"
nOfTGs = Get number of strings
dirTG$ = "../results/TextGrid/"

for i to nOfTGs 
	selectObject: tgList
	fileName$ = Get string: i
	fileID = Read from file: dirTG$ + fileName$
	if do("Get number of tiers") = 3 and do$("Get tier name...", 1) = "segment" and do$("Get tier name...", 2) = "mora" and do$("Get tier name...", 3) = "word"
		Insert point tier: 4, "tone"
		wordTierNo = 3
		toneTierNo = 4
		word$ = Get label of interval: wordTierNo, 2
		wordStart = Get start time of interval: wordTierNo, 2
		wordEnd = Get start time of interval: wordTierNo, 3
		wordDur = wordEnd - wordStart
		Insert point: toneTierNo, wordStart, "%LH"
		Insert point: toneTierNo, (wordStart + wordEnd) / 2, "A"
		Insert point: toneTierNo, wordEnd, "LHL%"
		Save as text file: dirTG$ + fileName$
	endif
	removeObject: fileID
endfor


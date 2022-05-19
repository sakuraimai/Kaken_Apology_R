tgList = Create Strings as file list: "filelist_TextGrid", "../results/TextGrid/*.TextGrid"
nOfTGs = Get number of strings
dirTG$ = "../results/TextGrid/"

for i to nOfTGs
	selectObject: tgList
	fileName$ = Get string: i
	fileID = Read from file: dirTG$ + fileName$
	if do("Get number of tiers") = 2 and do$("Get tier name...", 1) = "segment" and do$("Get tier name...", 2) = "word"
		Insert interval tier: 2, "mora"
		segTierNo = 1
		moraTierNo = 2
		wordTierNo = 3
		moraIndex = 1
		vIndex = 0
		for j from 2 to do("Get number of intervals...", segTierNo)
			seg$ = Get label of interval: segTierNo, j
			segLength = length(seg$)
			if segLength = 0 ; Insert the boundary at the end
				segStart = Get start time of interval: segTierNo, j
				Insert boundary: moraTierNo, segStart
			elsif segLength = 1
				if index_regex(seg$, "[aiueo]") = 0 and seg$ != "n"; i.e. single consonant segment
					segStart = Get start time of interval: segTierNo, j
					Insert boundary: moraTierNo, segStart
					moraIndex += 1
					moraString$ = seg$
					Set interval text: moraTierNo, moraIndex, moraString$
					vIndex = 0
				else ; i.e. single vowel segment
					vIndex += 1
					if vIndex = 1 ; i.e. no preceding vowel in the same mora
						moraString$ = moraString$ + seg$
						Set interval text: moraTierNo, moraIndex, moraString$
					else
						segStart = Get start time of interval: segTierNo, j
						Insert boundary: moraTierNo, segStart
						moraIndex += 1
						moraString$ = seg$
						Set interval text: moraTierNo, moraIndex, moraString$
						vIndex = 1
					endif
				endif
			elsif segLength = 2
				if index_regex(seg$, "[aiueo]") = 2 ; i.e. a consonant + a vowel
					vIndex += 1
					segStart = Get start time of interval: segTierNo, j
					Insert boundary: moraTierNo, segStart
					moraIndex += 1
					moraString$ = seg$
					Set interval text: moraTierNo, moraIndex, moraString$
				else ; i.e. a sequence of either two vowels or two consonants
					segStart = Get start time of interval: segTierNo, j
					segEnd = Get end time of interval: segTierNo, j
					if vIndex = 1 ; i.e. there is already one vowel in the mora
						Insert boundary: moraTierNo, segStart
						moraIndex += 1
						moraString$ = left$(seg$, 1)
					else; i.e. no preceding vowel in the same mora
						moraString$ = moraString$ + left$(seg$, 1)
					endif
					Set interval text: moraTierNo, moraIndex, moraString$
					Insert boundary: moraTierNo, (segStart + segEnd) / 2
					moraIndex += 1
					if rindex_regex(seg$, "[aiueo]") = 2 ; i.e. in case of a two-vowel sequence
						vIndex = 1
					else
						vIndex = 0
					endif
					moraString$ = right$(seg$, 1)
					Set interval text: moraTierNo, moraIndex, moraString$
				endif
			else
				exit Error; Check the segments in 'fileName$'.
			endif
		endfor
	endif
	Save as text file: dirTG$ + fileName$
	removeObject: fileID
endfor

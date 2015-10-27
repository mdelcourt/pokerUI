#Configuration file for pokerlib and pokerUI
UI= True
SWAP		= False	  #Auto deep-copy on every move (slows down a lot)
MAX_PER_TABLE 	= 9
MAX_TO_ADD	= 10
MAX_TABLE 	= 10
MAX_DIFF_gt_6 	= 1  #Max difference AUTHORIZED between shortest and longest table if average table length>6.
MAX_DIFF_lt_6	= 1
autoEqui 	= True


MIN_MOVE 	= True	#Choose player that moved the less when equilibrating tables.
GLOBAL_MIN_MOVE = True  #Forces to check min move from whole tournament when equilibrating

SOFT_GLMM_SEL 	= True  #Checks global MIN_MOVE from longest tables
			#False is NOT recommended

MIN_MOVE_ON_DEL = False	#Choose table with min moves to delete

MIN_MAX_ON_DEL	= True #Choose table with the minimum maximum num of moves
			#Boiteux !
			
SOFT_SEL_ON_DEL = False  #When deleting, always choose from shortest tables
			#False is NOT recommended

SILENT		= True

DEFAULT_FILE 	= "data/liste.txt"
DEFAULT_SAVE	= "autosave.sav"
#UI Config : 

MAIN_WIDTH	=	1000
MAIN_HEIGHT	=	800

TABLE_WIDTH	=	200
TABLE_HEIGHT	=	800
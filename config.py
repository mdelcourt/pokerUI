#Configuration file for pokerlib and pokerUI
UI= True
SWAP		= True	  #Auto deep-copy on every move (slows down a lot for MC)
MAX_PER_TABLE 	= 9	  #Maximum players per table
MAX_TO_ADD	= 10	  #Maximum players allowed to be manually added to a table
MAX_TABLE 	= 10	  #Maximum amount of tables allowed

MAX_DIFF_gt_6 	= 1  #Max difference AUTHORIZED between shortest and longest table if average table length>6.
MAX_DIFF_lt_6	= 1  #											  <=6
		     #This param is useless if MAX_PER_TABLE = 9

autoEqui 	= True #Automatical equilibrating of tables 


MIN_MOVE 	= True	#Choose player that moved the less when equilibrating tables.
GLOBAL_MIN_MOVE = True  #Forces to check min move from whole tournament when equilibrating

SOFT_GLMM_SEL 	= True  #Checks global MIN_MOVE from longest tables only
			 #False is NOT recommended

MIN_MOVE_ON_DEL = False	#Choose table with min moves to delete

MIN_MAX_ON_DEL	= True #Choose table with the minimum maximum num of moves
			
SOFT_SEL_ON_DEL = False  #When deleting, always choose from shortest tables

SILENT		= True
POPUP		= True

DEFAULT_FILE 	= "data/liste.txt"
DEFAULT_SAVE	= "autosave.sav"
#UI Config : 

MAIN_WIDTH	=	1000
MAIN_HEIGHT	=	800

TABLE_WIDTH	=	200
TABLE_HEIGHT	=	800
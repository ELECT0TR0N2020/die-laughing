#python3
import configparser
import sys
import os.path
import os
import random # for shuffle


# Check that the config file has been specified
if len(sys.argv) != 2:
	sys.exit("Error: not enough arguments\nUsage: " + sys.argv[0] + " <config file>")

configFile = sys.argv[1]

# Check that config file exists
# If we don't check this here then the configparser doesn't throw any errors when parsing (?!)
if not os.path.isfile(configFile):
	sys.exit("Error: the config file you have specified does not exist: " + configFile)

# Parse in the config file
try:
	config = configparser.ConfigParser()
	config.read(configFile)
except configparser.ParsingError as err:
	sys.exit("Error: Could not parse config file\n" + str(err))

# Read in all required values and handle error if they don't exist
try:
	MOVE_AFTER_PRINT = config.getboolean('SETTINGS', 'MOVE_AFTER_PRINT')
	FILE_READ_ORDER = config.get('SETTINGS','FILE_READ_ORDER')

	# Lets be really strict today about the allowed config values
	if not FILE_READ_ORDER in ['random','alphabetical']:
		sys.exit("ERROR: invalid value for FILE_READ_ORDER: '{}'".format(FILE_READ_ORDER))

	SOURCE_DIRECTORY = config.get('SETTINGS','SOURCE_DIRECTORY')

	#Only read the DESTINATION_DIRECTORY if MOVE_AFTER_PRINT is enabled
	if MOVE_AFTER_PRINT:
		DESTINATION_DIRECTORY = config.get('SETTINGS','DESTINATION_DIRECTORY')
except configparser.NoOptionError as err:
	sys.exit("Error: could not find required value in config file\n" + str(err))

########## Ready to print/move file ##########

allFiles = [f for f in os.listdir(SOURCE_DIRECTORY) if os.path.isfile(os.path.join(SOURCE_DIRECTORY, f))]

# Confirm that at least one file exists in SOURCE_DIRECTORY
if len(allFiles) < 1:
	sys.exit("Error: No files in {} to print".format(SOURCE_DIRECTORY))

# The listdir function sorts the files alphabetically automatically, so if we
#  want the alphabetical option we do nothing. To get a random one the list should be shuffled now
if FILE_READ_ORDER == 'random':
	random.shuffle(allFiles)

# The full filepath of the file we're going to print and maybe move today
file = os.path.join(SOURCE_DIRECTORY, allFiles[0])


# Print the entire contents of file to stdout
with open(file,'r', encoding='utf8') as f: # Use file to refer to the file object
	print(f.read(), end="")

# Move the file afterwards if the flag is set
if MOVE_AFTER_PRINT:
	destination = os.path.join(DESTINATION_DIRECTORY, allFiles[0])
	os.rename(file, destination)
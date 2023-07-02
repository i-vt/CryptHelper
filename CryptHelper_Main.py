from crypthelper import *
import argparse


def validateInput(objArgumentsPassed) -> (str, str):
	bolKeyNotPresent = ("<class 'NoneType'>" == str(type(objArgumentsPassed.get_key)))
	if objArgumentsPassed.decrypt == objArgumentsPassed.encrypt:
		print("Error: using options -e / --encrypt and -d / --decrypt, pick one to use.")
		exit()
	elif bolKeyNotPresent and objArgumentsPassed.decrypt:
		print("Error: cannot decrypt without a key file.")
		exit()

	if objArgumentsPassed.decrypt:
		strAction = "decrypt"
	elif objArgumentsPassed.encrypt:
		strAction = "encrypt"
	else:
		print("Error: logic flow error, please revise the __main__")
		exit()

	if bolKeyNotPresent: 
		dtNow, strTimeNow = getTimeNow("mushed")
		strKeyFilepath = f"keychain_{strTimeNow}.txt"
		bolSuccess, strPotentialError = generateKeyChain(strKeyFilepath,3)
		if bolSuccess != True: 
			print(strPotentialError)
			exit()
	else: strKeyFilepath = str(objArgumentsPassed.get_key)

	return strAction, strKeyFilepath


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="crypthelper")
	parser.add_argument("file", help="File to apply multiple encrypts/decrypts")
	parser.add_argument("-k", "--key", dest="get_key", action="store",
						help="load in an existing key")
	parser.add_argument("-e", "--encrypt", action="store_true",
						help="to specify file to encrypt (if option -k is not used a new key will be generated)")
	parser.add_argument("-d", "--decrypt", action="store_true",
						help="to specify file to decrypt")
	objArguments = parser.parse_args()

	strAction, strKeyFilepath = validateInput(objArguments)
	strSubjectFilepath = str(objArguments.file)

	chainCryptor(strAction, strSubjectFilepath, strSubjectFilepath, strKeyFilepath)
	
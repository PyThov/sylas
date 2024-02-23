from cryptography.fernet import Fernet
import os

ENCRYPT = "1"
DECRYPT = "2"
PATH = os.environ.get("SYLAS_PATH")
KEYS = "%skeys\\" % PATH
ENCRYPTIONS = "%senc\\" % PATH


# Validates that a given file exists
def validateFile(filename):
    print("validating %s..." % filename)
    return os.path.exists(filename)


# Encrypts a .txt file and generates a key and encrypted .txt file
def encrypt(filename):
    txtFile = "%s.txt" % filename
    if not validateFile(txtFile):
        print("ERROR: %s does not exist" % txtFile)
        return

    print("Encrypting .%s.." % txtFile)
    
    # Generate a key
    key = Fernet.generate_key()
    with open('%s%s.key' % (KEYS, filename), 'wb') as filekey:
        filekey.write(key)

    # Read the .txt file you want to encrypt
    with open('%s' % txtFile, 'rb') as file:
        original = file.read()

    # Encrypt the file
    fernet = Fernet(key)
    encrypted = fernet.encrypt(original)

    # Write the encrypted file
    with open('%senc_%s' % (ENCRYPTIONS, txtFile), 'wb') as enc_file:
        enc_file.write(encrypted)

    print("Deleting %s..." % txtFile)
    os.remove('%s' % txtFile)


# Decrypts a .txt file given a .key
def decrypt(filename):
    txtFile = "%s.txt" % filename
    encFile = "%senc_%s" % (ENCRYPTIONS, txtFile)
    keyFile = "%s%s.key" % (KEYS, filename)

    if not validateFile(encFile):
        print("ERROR: enc_%s.txt does not exist" % filename)
        return
    
    if not validateFile(keyFile):
        print("ERROR: %s.key does not exist" % filename)
        return

    print("decrypting enc_%s.txt using %s.key..." % (filename, filename))

    # Load the key
    with open(keyFile, 'rb') as filekey:
        key = filekey.read()

    # Using the key, create a Fernet instance
    fernet = Fernet(key)

    # Read the encrypted file
    with open(encFile, 'rb') as enc_file:
        encrypted = enc_file.read()

    # Decrypt the file
    decrypted = fernet.decrypt(encrypted)

    # Write the decrypted data to a file
    print("decrypting to %s..." % txtFile)
    with open(txtFile, 'wb') as dec_file:
        dec_file.write(decrypted)


def getInput():

    action = input("(1)encrypt? or (2)decrypt?: ")
    if action not in ["1", "2"]:
        print("Please select option 1(encrypt) or 2(decrypt)")
        return getInput()

    filename = input("\nSylas: excellent... what is your filename?: ")
    
    return action, filename

def main():
    print("Sylas: Hello, can I break some chains today?\n")

    action, filename = getInput()
    print()

    if action == ENCRYPT:
        encrypt(filename)
    elif action == DECRYPT:
        decrypt(filename)
    else:
        print("\nSylas: Hmm... something went wrong...")

    print("\nSylas: The deed is done.")

main()

RSA Encryption (current: 2048 bits)

HOW IT WORKS
	RSA, used all around the internet, allows fully encrypted messages to be sent using a public key, so unlike other ciphers, there never has to be the interchanging of keys beforehand. If you want to send a message to me, I first have to have a private key that only I know. Then I use that private key to make a public key that everyone can see. Anyone can use that public key to encrypt a message, but only I can decrpyt that message, even though attackers will easily capture the encrypted message. If two different people do that, they can send secure messages.

HOW TO USE
	First, type "a" and Enter to create a public key. this will give you n, e (public key), and d (private key). Save these, but make sure only you know what d is.
	Second, send your n and e out to whoever you want. These represents your public key, and will be how people write you messages.
	To write you a message, create a text file that begins with n and e, separated by a space. Then on a new line create your message. The program should give you a long number as the output. This is the encrypted message, save it.
	Now, only someone with the private key d can decrypt. Create a new text file beginning with n and d, separated by a space. Then, on a new line, enter the encrypted message.
	After running, you should be left with your decrypted message. Yay!

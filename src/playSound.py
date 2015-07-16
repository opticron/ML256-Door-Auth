import subprocess

def PlaySound(textToSay):
  results = subprocess.check_output(['/home/pi/code/Text-to-Speech/speech.sh', textToSay])


